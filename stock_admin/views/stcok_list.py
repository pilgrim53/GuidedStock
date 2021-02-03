from decimal import Decimal

import yfinance as yf
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
from stock_admin.forms import StockForm
from stock_admin.models import Stock

from .models import Stock


class StockListView(ListView):
    model = Stock
    template_name = 'stock-list.html'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return None
        queryset = Stock.objects.filter(user=self.request.user)
        show_list = []
        for stock in queryset:
            if stock.showinform:
                # Use Yahoo Finance to get the current price of the stock
                cur_info = yf.Ticker(stock.ticker).info

                # Initialize the company name if it hasn't been already
                if stock.stock_name == stock.ticker:
                    stock.stock_name = cur_info.get(
                        'longBusinessSummary')[0:25]

                # Pull out the latest bid price
                price = cur_info.get('bid')
                if (price is None):
                    price = 1
                else:
                    if isinstance(price, float):
                        stock.current = Decimal(price)
                    else:
                        if isinstance(price, dict):
                            bid = str(price.get('fmt'))
                            if bid > 0:
                                stock.current = Decimal(bid)
                        else:
                            if price > 0:
                                stock.current = Decimal(price)

                if stock.current == 0:
                    stock.current = Decimal(0.01)

                stock.current = round(stock.current, 2)
                stock.potential = round(stock.sell_target/stock.current, 2)

                # Calculate Profit and Proximity differently if we own shares
                if stock.shares > 0 and stock.purchase:
                    stock.profit = round(
                        (stock.current - stock.purchase) * stock.shares)
                    stock.proximity = round(
                        (1-((stock.sell_target-stock.current)/(stock.sell_target-stock.purchase)))*100)

                    # stock.potential = round(((stock.shares*(stock.sell_target-stock.current ))/(stock.shares*stock.current)),2)
                else:
                    goal = stock.sell_target - stock.buy_target
                    if goal != 0:
                        factor = (stock.current - stock.buy_target) / goal
                        stock.proximity = round(
                            ((1 + abs(stock.current-stock.sell_target)/goal) * factor)*100)
                    else:
                        stock.proximity = 0

                stock.save()
                show_list.append(stock)
        print(show_list)
        return sorted(show_list, key=lambda x: x.potential)
