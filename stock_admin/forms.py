from django import forms

from .models import Stock


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['stock_name', 'ticker', 'purchase', 'sell_target',
                  'buy_target', 'shares', 'current', 'proximity', 'profit']
