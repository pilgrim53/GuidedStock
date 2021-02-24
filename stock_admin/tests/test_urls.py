from django.test import SimpleTestCase
from django.urls import resolve, reverse
from django.views.generic.base import TemplateView

from ..views.stock import StockCreate, StockDelete, StockUpdate
from ..views.stock_list import StockListView
from .. import views


class StockAdminUrlsTestCase(SimpleTestCase):

    def test_homepage_url_resolved(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func.view_class, TemplateView)

    def test_portfolio_list_url_resolved(self):
        url = reverse('portfolio')
        self.assertEqual(resolve(url).func.view_class, StockListView)

    def test_portfolio_create_url_resolved(self):
        url = reverse('create-stock')
        self.assertEqual(resolve(url).func.view_class, StockCreate)

    def test_portfolio_update_url_resolved(self):
        url = reverse('update-stock', args=(1,))
        self.assertEqual(resolve(url).func.view_class, StockUpdate)

    def test_portfolio_delete_url_resolved(self):
        url = reverse('delete-stock', args=(1,))
        self.assertEqual(resolve(url).func.view_class, StockDelete)

    def test_homepage_url_resolved(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func.view_class, TemplateView)

    def test_signup_url_resolved(self):
        url = reverse('signup')
        self.assertEqual(resolve(url).func.view_class, views.SignUp)

    def test_change_password_url_resolved(self):
        url = reverse('change_password')
        self.assertEqual(resolve(url).func.view_class,
                         views.ChangePasswordFormView)

    def test_terms_of_service_url_resolved(self):
        url = reverse('terms-of-service')
        self.assertEqual(resolve(url).func.view_class, TemplateView)

    def test_privacy_policy_url_resolved(self):
        url = reverse('privacy-policy')
        self.assertEqual(resolve(url).func.view_class, TemplateView)

    def test_cookie_policy_url_resolved(self):
        url = reverse('cookie-policy')
        self.assertEqual(resolve(url).func.view_class, TemplateView)

    def test_cookie_policy_url_resolved(self):
        url = reverse('cookie-policy')
        self.assertEqual(resolve(url).func.view_class, TemplateView)
