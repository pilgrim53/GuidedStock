from django.urls import include, path

from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', views.stock_list_view, name='stock-list'),
    path('signup', views.SignUp.as_view(), name='signup'),
    path('terms-and-conditions', TemplateView.as_view(template_name='terms-and-conditions.html'), name='terms-and-conditions'),
]
