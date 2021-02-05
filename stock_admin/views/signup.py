from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views import generic
from stock_admin.forms import UserCreationForm


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('stock-list')
    template_name = 'signup.html'

    def form_valid(self, form):
        """After successful registration, login in the system.
        """
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)
        return response
