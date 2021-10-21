from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm

from .models import Stock, get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['stock_name', 'ticker', 'purchase', 'sell_target',
                  'buy_target', 'shares', 'current', 'proximity', 'profit']


class UserCreationForm(BaseUserCreationForm):
    error_messages = {
        'password_mismatch': "Your passwords must match",
    }
    first_name = forms.CharField(
        error_messages={'required': 'Your First Name is required.'})
    last_name = forms.CharField(
        error_messages={'required': 'Your Last Name is required.'})
    password1 = forms.CharField(error_messages={
                                'required': 'A password is required.'}, widget=forms.PasswordInput)
    password2 = forms.CharField(error_messages={
        'required': 'Confirm password is required.'}, widget=forms.PasswordInput)
    default_portfolio = forms.BooleanField(required=False)
    terms_condition = forms.BooleanField(initial=False, required=False)

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name','email', 'password1')
        error_messages = {
            'email': {
                'required': _("Your email address is required."),
                'unique': _("This email is already registered"),
            },
        }

    def clean_terms_condition(self):
        terms_condition = self.cleaned_data['terms_condition']
        if not terms_condition:
            raise ValidationError(
                "You must agree to the Terms and Conditions to use GuidedStock")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return terms_condition
