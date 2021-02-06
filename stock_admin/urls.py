from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name="home.html"), name='home'),
    path('portfolio', login_required(views.stock_list.StockListView.as_view()),
         name='portfolio'),
    path('signup', views.SignUp.as_view(), name='signup'),
    path('terms-and-conditions', TemplateView.as_view(
        template_name='terms-and-conditions.html'), name='terms-and-conditions'),
]
