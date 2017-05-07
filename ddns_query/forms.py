from registration.forms import RegistrationForm
from django.forms import ModelForm
from .models import Dyname
from django.contrib.auth import get_user_model


class CustomRegistrationForm(RegistrationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')


class AddDynameForm(ModelForm):
    class Meta:
        model = Dyname
        fields = [
            'prefix',
            'zone',
            'primary_dns_host',
            'primary_dns_ip',
        ]
