from decimal import Decimal


from celery import shared_task
from yahoo_fin import stock_info

from .models import Stock

from .utils import get_current_users
from decimal import Decimal


@shared_task
def update_stock_prices():
    for ticker in Stock.objects.order_by().values_list("ticker", flat=True).distinct():
        Stock.objects.filter(ticker=ticker).update(
            current=round(Decimal(stock_info.get_live_price(ticker)), 2)
        )


@shared_task
def update_active_user_ticker():
    """For the only active users, Update the current, proximity, potential, profit based on the current live price."""
    stocks = Stock.objects.filter(user__in=get_current_users())
    tickers = set(list(stocks.values_list("ticker", flat=True)))

    # Get current price for unique tickers.
    tickers_price = {
        ticker: round(Decimal(stock_info.get_live_price(ticker)), 2)
        for ticker in tickers
    }

    objs = []

    for stock in stocks:
        if stock.ticker in tickers_price:
            live_price = tickers_price[stock.ticker]
            stock.profit, stock.potential, stock.proximity = stock.update_stock(
                live_price
            )
            stock.current = live_price
            objs.append(stock)

    Stock.objects.bulk_update(
        objs, ["current", "proximity", "potential", "profit"], batch_size=20000
    )  # Updates all columns by 100 sized chunks.
