from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.views.generic import TemplateView
from django.conf.urls import url

from . import views



urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name="home.html"), name='home'),
    path('portfolio', login_required(views.StockListView.as_view()),
         name='portfolio'),
    path('portfolio/create-stock',
         login_required(views.StockCreate.as_view()), name='create-stock'),
    path('portfolio/update-stock/<int:pk>',
         login_required(views.StockUpdate.as_view()), name='update-stock'),
    path('portfolio/delete-stock/<int:pk>',
         login_required(views.StockDelete.as_view()), name='delete-stock'),
    path('signup', views.SignUp.as_view(), name='signup'),
    path('terms-and-conditions', TemplateView.as_view(
        template_name='terms-and-conditions.html'), name='terms-and-conditions'),
    url(r'^subscribe/', views.subscribe, name = "subscribe"),
]
