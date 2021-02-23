from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.views.generic import TemplateView

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
    path('password', login_required(
        views.ChangePasswordFormView.as_view()), name='change_password'),
    path('change-password-done', login_required(TemplateView.as_view(template_name="registration/password_change_done.html")),
         name='change-password-done'),
    path('terms-of-service', TemplateView.as_view(template_name="terms_of_service.html"),
         name='terms-of-service'),
    path('privacy-policy', TemplateView.as_view(template_name="privacy_policy.html"),
         name='privacy-policy'),
    path('cookie-policy', TemplateView.as_view(template_name="cookie_policy.html"),
         name='cookie-policy'),
    path('subscribe/', views.subscribe, name="subscribe"),
]
