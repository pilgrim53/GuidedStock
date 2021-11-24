from decimal import Decimal

from celery import shared_task
from yahoo_fin import stock_info

from .models import Stock


@shared_task
def update_stock_prices():
    for ticker in Stock.objects.order_by().values_list('ticker', flat=True).distinct():
        live_price = round(Decimal(stock_info.get_live_price(ticker)), 2)
        Stock.objects.filter(ticker=ticker).update(
            current=live_price)
