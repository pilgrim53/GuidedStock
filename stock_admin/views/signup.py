from django.contrib.auth import authenticate, login
from stock_admin.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from stock_admin.models import StockManager


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('portfolio')
    template_name = 'signup.html'

    def form_valid(self, form):
        """After successful registration, login in the system.
        """
        response = super().form_valid(form)
        email = form.cleaned_data.get('email')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(email=email, password=raw_password)
        login(self.request, user)
        if form.cleaned_data.get('default_portfolio'):
            StockManager().create_default_portfolio(user)
        return response
