from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm

from .models import Stock, get_user_model


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['stock_name', 'ticker', 'purchase', 'sell_target',
                  'buy_target', 'shares', 'current', 'proximity', 'profit']


class UserCreationForm(BaseUserCreationForm):
    default_portfolio = forms.BooleanField(required=False)

    class Meta:
        model = get_user_model()
        fields = ('email', 'password1')
