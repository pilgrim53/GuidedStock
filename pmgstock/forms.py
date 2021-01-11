from django import forms
from .models import Stock
import yfinance as yf

class StockForm(forms.ModelForm):
   class Meta:
      model       = Stock
      fields      = [ 'stock_name', 'ticker', 'purchase', 'sell_target', 'buy_target', 'shares', 'current', 'proximity', 'profit' ]
   
class RawStockForm(forms.Form):
   stock_name      = forms.CharField()
   ticker          = forms.CharField()
   purchase        = forms.DecimalField()
   sell_target     = forms.DecimalField()
   buy_target      = forms.DecimalField()
   shares          = forms.IntegerField()
   current         = forms.DecimalField()
   proximity       = forms.DecimalField()   
   profit          = forms.DecimalField()
   
 
    
