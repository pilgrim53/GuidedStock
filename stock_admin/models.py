from decimal import Decimal

import yfinance as yf
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from yahoo_fin import stock_info


class Stock(models.Model):
    stock_name = models.CharField(blank=False, null=False, max_length=100)
    ticker = models.CharField(blank=False, null=False, max_length=40)
    purchase = models.DecimalField(
        default=0,
        blank=True, max_digits=10, decimal_places=2)
    sell_target = models.DecimalField(
        blank=True, max_digits=10, decimal_places=2, default=0)
    buy_target = models.DecimalField(
        blank=True, max_digits=10, decimal_places=2, default=0)
    shares = models.IntegerField(blank=True, default=0)
    current = models.DecimalField(
        blank=True, max_digits=10, decimal_places=2, default=0)
    proximity = models.DecimalField(
        blank=True, max_digits=10, decimal_places=2, default=0)
    profit = models.DecimalField(
        blank=True, max_digits=10, decimal_places=2, default=0)
    is_default = models.BooleanField(default=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    potential = models.DecimalField(
        blank=True, max_digits=10, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Stock'

    def __str__(self):
        return '%s (%s)' % (self.stock_name, self.ticker)

    def update_stock(self):
        self.current = round(
            Decimal(stock_info.get_live_price(self.ticker)), 2)
        if not self.purchase:
            self.purchase = 0
        if not self.shares:
            self.shares = 0
        if not self.buy_target:
            self.buy_target = 0
        if not self.sell_target:
            self.sell_target = 0
        self.potential = round(
            self.sell_target/self.current, 2) if self.sell_target else 0
        self.profit = round((self.current - self.purchase) * self.shares, 2)
        self.proximity = 0
        if self.sell_target and self.buy_target:
            goal = Decimal(self.sell_target - self.buy_target)
            if goal:
                self.proximity = (
                    round((self.current - self.buy_target) / goal, 2)) * 100
        elif self.sell_target and self.purchase:
            self.proximity = round(
                (self.current - self.purchase)/(self.sell_target - self.purchase), 2)*100

    def full_clean(self, exclude=None, validate_unique=True):
        """Validate the ticker before save.
        """
        self.ticker = str(self.ticker).upper()
        if self.shares and not self.purchase:
            raise ValidationError({
                'purchase': "If you own shares of %s then you should provide the purchase price." % self.ticker})
        if self.purchase and not self.shares:
            raise ValidationError({
                'shares': "If you have purchase price of %s then you should provide the shares." % self.ticker})

        if self.sell_target and self.buy_target:
            if self.sell_target < self.buy_target:
                raise ValidationError({
                    'sell_target': "Sell target must be higher than the buy target."})

        # Initialize the company name if it hasn't been already
        if not self.stock_name:
            self.stock_name = self.get_ticker_title()

    def get_ticker_title(self):
        result = yf.Ticker(self.ticker)
        if 'longName' in result.info:
            return result.info['longName']
        else:
            raise ValidationError(
                {'ticker': "Ticker not found!! Please enter valid ticker."})


class DefaultPortfolio(Stock):

    class Meta:
        proxy = True
        verbose_name = 'Stock'
        verbose_name_plural = 'Default Portfolio'


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
