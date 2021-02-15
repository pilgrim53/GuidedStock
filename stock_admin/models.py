from decimal import Decimal
from urllib.request import urlopen

from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from yahoo_fin import stock_info


class Stock(models.Model):
    stock_name = models.CharField(blank=False, null=False, max_length=100)
    ticker = models.CharField(blank=False, null=False, max_length=40)
    purchase = models.DecimalField(
        default=0,
        blank=True, null=True, max_digits=10, decimal_places=2)
    sell_target = models.DecimalField(
        blank=True, null=True, max_digits=10, decimal_places=2, default=0)
    buy_target = models.DecimalField(
        blank=True, null=True, max_digits=10, decimal_places=2, default=0)
    shares = models.IntegerField(blank=True, null=True, default=0)
    current = models.DecimalField(
        blank=True, null=True, max_digits=10, decimal_places=2)
    proximity = models.DecimalField(
        blank=True, null=True, max_digits=10, decimal_places=2)
    profit = models.DecimalField(
        blank=True, null=True, max_digits=10, decimal_places=2)
    is_default = models.BooleanField(default=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    potential = models.DecimalField(
        blank=True, null=True, max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Stock'

    def update_stock(self):
        self.potential = round(
            self.sell_target/self.current, 2) if self.sell_target else 0
        # Calculate Profit and Proximity differently if we own shares
        if self.shares > 0 and self.purchase:
            self.profit = round(
                (self.current - self.purchase) * self.shares)
            goal = self.sell_target - self.purchase
            self.proximity = round((self.current - self.purchase)/goal, 2)*100
        else:
            self.profit = 0
            goal = Decimal(self.sell_target - self.buy_target)
            if goal != 0:
                self.proximity = (
                    round((self.current - self.buy_target) / goal, 2)) * 100
            else:
                self.proximity = 0

    def full_clean(self, exclude=None, validate_unique=True):
        """Validate the ticker before save.
        """
        if self.shares and not self.purchase:
            print("if in in full clean stock")
            raise ValidationError({
                'purchase': "If you own shares of %s then you should provide the purchase price." % self.ticker})
        try:
            self.current = round(
                Decimal(stock_info.get_live_price(self.ticker)), 2)
            # Initialize the company name if it hasn't been already
            if not self.stock_name:
                self.stock_name = self.get_ticker_title()
        except:
            raise ValidationError(
                {'ticker': "Ticker not found!! Please enter valid ticker."})

    def get_ticker_title(self):
        html = urlopen('https://finance.yahoo.com/quote/%s/' % self.ticker)
        bsh = BeautifulSoup(html.read(), 'html.parser')
        return bsh.h1.string.replace('(%s)' % self.ticker, '')


class StockManager():
    def create_default_portfolio(self, user):
        stocks = Stock.objects.filter(
            is_default=True, user__in=get_user_model().objects.filter(is_superuser=True))
        for stock in stocks:
            Stock(is_default=False, stock_name=stock.stock_name, buy_target=stock.buy_target, sell_target=stock.sell_target,
                  current=stock.current, user=user, ticker=stock.ticker).save()


@receiver(pre_save, sender=Stock, dispatch_uid="update_stock")
def update_stock(sender, instance, **kwargs):
    instance.update_stock()


class Subscribe(models.Model):
    email_id = models.EmailField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email_id
