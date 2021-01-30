from django.urls import include, path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', views.stock_list_view, name='stock-list'),
]
