from decimal import Decimal
from urllib.request import urlopen

from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
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
    is_default = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    potential = models.DecimalField(
        blank=True, null=True, max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Stock'

    def full_clean(self, exclude=None, validate_unique=True):
        """Validate the ticker before save.
        """
        if self.shares and not self.purchase:
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

    def save_stock_info(self):
        """Fetch the stock info from  yfinance and Update the stock info.
        """
        self.potential = round(self.sell_target/self.current, 2)

        # Calculate Profit and Proximity differently if we own shares
        if self.shares > 0 and self.purchase:
            self.profit = round(
                (self.current - self.purchase) * self.shares)
            self.proximity = round(
                (1-((self.sell_target-self.current)/(self.sell_target-self.purchase)))*100)

            # self.potential = round(((self.shares*(self.sell_target-self.current ))/(self.shares*self.current)),2)
        else:
            goal = self.sell_target - self.buy_target
            if goal != 0:
                factor = (self.current - self.buy_target) / goal
                self.proximity = round(
                    ((1 + abs(self.current-self.sell_target)/goal) * factor)*100)
            else:
                self.proximity = 0

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.save_stock_info()
        return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


class StockManager():

    def create_default_portfolio(self, user):
        stocks = Stock.objects.filter(
            is_default=True, user__in=User.objects.filter(is_superuser=True))
        for stock in stocks:
            Stock(is_default=False, stock_name=stock.stock_name,
                  current=stock.current, user=user, ticker=stock.ticker).save()
