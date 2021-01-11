from django.shortcuts    import render
from django.http         import HttpResponse
from decimal             import Decimal
from .models             import Stock
from .forms              import RawStockForm
import yfinance as yf


# Create your views here.

# Called by Main Page
def stock_list_view(request):
   my_form = RawStockForm()
   object_list=Stock.objects.all()
   
   for stock in object_list:
#      if stock.hide == False:
         cur_info=yf.Ticker(stock.ticker).info
         price=cur_info.get('bid')


         if price is None:
            price=0
         else:
            if isinstance(price, float):
               stock.current=Decimal(price)
            else: 
               if isinstance(price, dict):
                  bid = str(price.get('raw'))
                  stock.current = Decimal(bid)
               else:
                  stock.current=Decimal(price)
            
         stock.current=round(stock.current, 2) 
      
         if stock.stock_name == stock.ticker:
            stock.stock_name=cur_info.get('longBusinessSummary')[0:25]
 
         stock.profit = round((stock.current - stock.purchase) * stock.shares)
      
         if stock.shares > 0 : 
            stock.proximity = round((1-((stock.sell_target-stock.current)/(stock.sell_target-stock.purchase)))*100)
         else:
            if stock.current > 0 : 
               goal = stock.sell_target - stock.buy_target
               factor  = (stock.current - stock.buy_target) / goal
               stock.proximity = round(((1 + abs(stock.current-stock.sell_target)/goal) * factor)*100)


   context  = { "form": my_form, "object_list": sorted(object_list, key=lambda x: x.proximity , reverse=True) }   
   return render(request, "StockView.html", context)


