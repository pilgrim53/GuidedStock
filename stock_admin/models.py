from django.contrib.auth.models import User
from django.db import models


class Stock(models.Model):
    stock_name = models.CharField(blank=False, null=False, max_length=40)
    ticker = models.CharField(blank=False, null=False, max_length=10)
    purchase = models.DecimalField(
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
    showinform = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    potential = models.DecimalField(
        blank=True, null=True, max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Stock'
