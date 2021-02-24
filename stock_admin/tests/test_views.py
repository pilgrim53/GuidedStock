from django.test import TestCase, Client
from django.urls import reverse, resolve
from ..models import Stock, get_user_model


class TextView(TestCase):

    def setUp(self):
        self.client = Client()
        self.create_stock_url = reverse('create-stock')

        self.user = get_user_model().objects.create_user(
            username='javed', email='javed@javed.com', password='my_secret')

        self.stock = Stock(ticker="fb", purchase=1000,
                           sell_target=100, buy_target=20, current=50, user=self.user)
        self.stock.save()
        return super().setUp()

    def test_should_takes_ticker_and__purchase_and_buy_target_and_sell_target_based_on_proximity_count(self):
        stock = Stock(ticker='PLTR',purchase=28.96,buy_target=27,sell_target=35,shares=10)
        stock.full_clean()