import concurrent.futures
from decimal import Decimal

from celery import shared_task
from yahoo_fin import stock_info
from yahoo_fin import stock_info as si

from .models import Stock


def ticker_live_price_(ticker):
    return {'ticker_name': ticker, 'ticker_price': si.get_live_price(ticker)}


# @shared_task
def update_stock_prices():
    # for ticker in Stock.objects.order_by().values_list('ticker', flat=True).distinct():
    #     live_price = round(Decimal(stock_info.get_live_price(ticker)), 2)
    #     Stock.objects.filter(ticker=ticker).update(
    #         current=live_price)
    
    list_of_ticker = list(Stock.objects.order_by(
    ).values_list('ticker', flat=True).distinct())

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(list_of_ticker)) as excutor:
        results = excutor.map(ticker_live_price_, list_of_ticker)
        obj = [result for result in results]

    for ticker in list_of_ticker:
        live_price = [i['ticker_price']
                      for i in obj if i['ticker_name'] == ticker]

        live_price = round(Decimal(live_price[0]), 2)

        Stock.objects.filter(ticker=ticker).update(
            current=live_price)
