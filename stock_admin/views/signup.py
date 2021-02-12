from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views import generic
from stock_admin.forms import UserCreationForm
from stock_admin.models import StockManager, Subscribe
from stock_admin.utils import SendSubscribeMail


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
