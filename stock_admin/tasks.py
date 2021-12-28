from decimal import Decimal

from django.db.models.expressions import F


from celery import shared_task
from yahoo_fin import stock_info
from yahoo_fin import stock_info as si

from .models import Stock

from .utils import get_current_users
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)
# @shared_task
def update_stock_prices():
    for ticker in Stock.objects.order_by().values_list("ticker", flat=True).distinct():
        Stock.objects.filter(ticker=ticker).update(
            current=round(Decimal(stock_info.get_live_price(ticker)), 2)
        )


@shared_task
def update_active_user_ticker():
    try:
        """For the only active users, Update the current price, proximity, potential, profit based on the current live price."""
        stocks = Stock.objects.filter(user__in=get_current_users())
        if stocks:
            tickers = stocks.values_list("ticker", flat=True).distinct()
        else:
            logger.info("Active users are not available")
            return

        logger.info(f"Tickers:- {tickers}")

        if not tickers:
            logger.info("For the active user, Tickers are not available")
        else:
            tickers_price = {}
            for ticker in tickers:
                try:
                    price = round(Decimal(stock_info.get_live_price(ticker)), 2)
                    tickers_price[ticker] = price
                except Exception as e:
                    logger.error(
                        f"Exception on {ticker} ticker and Exception is:- {str(e)}"
                    )

            objs = []
            for stock in stocks:
                try:
                    if stock.ticker in tickers_price:
                        live_price = tickers_price[stock.ticker]
                        (
                            stock.profit,
                            stock.potential,
                            stock.proximity,
                        ) = stock.update_stock(live_price)
                        stock.current = live_price
                        objs.append(stock)
                except Exception as e:
                    logger.error(
                        f"Error on updating the values for this {stock.ticker} stock and exception is:- {str(e)}"
                    )
                    pass

            Stock.objects.bulk_update(
                objs, ["current", "proximity", "potential", "profit"], batch_size=20000
            )  # Updates all columns by 20000 sized chunks.
            return True
    except:
        return False
