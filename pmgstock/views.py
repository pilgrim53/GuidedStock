from django.shortcuts    import render
from django.http         import HttpResponse
from decimal             import Decimal
from .models             import Stock
from .forms              import RawStockForm
import yfinance as yf
# import html5lib 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Create your views here.
# Called by Main Page
def LoginView(request):
  return render(request, "login.html")

# Called by Main Page
def stock_list_view(request):
  my_form = RawStockForm()
  if request.user.is_authenticated:
    # user = authenticate(username='MartinP', password='vmVTQdaCS7E99%S')
    # if username is not None:
    # A backend authenticated the credentials


     object_list=Stock.objects.all()
     show_list=[]
     
     for stock in object_list:
       if stock.username == request.user.username:
         if stock.showinform == True:
           #Use Yahoo Finance to get the current price of the stock   
           cur_info=yf.Ticker(stock.ticker).info
  
           #Initialize the company name if it hasn't been already
           if stock.stock_name == stock.ticker:
              stock.stock_name=cur_info.get('longBusinessSummary')[0:25]
           
           # Pull out the latest bid price
           price=cur_info.get('bid')
           if (price is None):
              a=1
           else:
              if isinstance(price, float):
                 stock.current=Decimal(price)
              else: 
                 if isinstance(price, dict):
                    bid = str(price.get('fmt'))
                    stock.current = Decimal(bid)
                 else:
                    stock.current=Decimal(price)
           
           if stock.current == 0:
              stock.current=Decimal(0.01) 
                   
           stock.current=round(stock.current, 2)
           stock.potential = round(stock.sell_target/stock.current,2) 
        
           # Calculate Profit and Proximity differently if we own shares
           if stock.shares > 0 : 
              stock.profit = round((stock.current - stock.purchase) * stock.shares)
              stock.proximity = round((1-((stock.sell_target-stock.current)/(stock.sell_target-stock.purchase)))*100)
  
              # stock.potential = round(((stock.shares*(stock.sell_target-stock.current ))/(stock.shares*stock.current)),2)
           else:
              goal = stock.sell_target - stock.buy_target
              if goal != 0:
                 factor  = (stock.current - stock.buy_target) / goal
                 stock.proximity = round(((1 + abs(stock.current-stock.sell_target)/goal) * factor)*100)
              else:
                 stock.proximity = 0
                 
           stock.save()
           show_list.append(stock)    
  
     # context  = { "form": my_form, "show_list": sorted(show_list, key=lambda x: x.proximity , reverse=True) } 
 
     # else:
     #    show_list=[ "not authenticated" ]
     
  context  = { "form": my_form, "show_list": sorted(show_list, key=lambda x: x.potential) }  
   
  return render(request, "StockView.html", context)


