from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import FormView
from stock_admin.forms import UserCreationForm
from stock_admin.models import StockManager, Subscribe
from stock_admin.utils import SendSubscribeMail

from ..models import Stock


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


class ChangePasswordFormView(FormView):
    template_name = "change_password.html"

    def get(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user)
        return render(request, self.template_name, {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
        return render(request, self.template_name, {
            'form': form
        })


def subscribe(request):
    if request.method == 'POST':
        email = request.POST['email_id']
        status = 200
        try:
            validate_email(email)
        except ValidationError:
            status = 422
            data = {'message': 'Email not valid!'}
            return JsonResponse(data, status=status)

        email_qs = Subscribe.objects.filter(email_id=email)
        if email_qs.exists():
            status = 422
            data = {'message': 'Email already exists!'}
            return JsonResponse(data, status=status)
        else:
            Subscribe.objects.create(email_id=email)
            # Send the Mail, Class available in utils.py
            SendSubscribeMail(email)
            data = {'message': 'Success! Please check your mail!'}
            return JsonResponse(data, status=status)

    return HttpResponse("/")
