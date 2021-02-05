from django.urls import include, path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', views.stock_list.StockListView.as_view(), name='stock-list'),
    path('signup', views.SignUp.as_view(), name='signup'),
    path('terms-and-conditions', TemplateView.as_view(
        template_name='terms-and-conditions.html'), name='terms-and-conditions'),
]
