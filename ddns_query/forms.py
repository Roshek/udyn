from registration.forms import RegistrationForm
from django import forms
from django.forms import ModelForm
from .models import Dyname
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class CustomRegistrationForm(RegistrationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')


class AddDynameForm(ModelForm):
    custom_zone = forms.BooleanField(required=False)

    class Meta:
        model = Dyname
        fields = [
            'prefix',
            'zone',
            'primary_dns_host',
            'primary_dns_ip',
        ]

    def clean(self):
        cleaned_data = super(AddDynameForm, self).clean()
        custom = cleaned_data['custom_zone']
        czone = cleaned_data.get('zone')
        if custom:
            if 'aszabados' in czone:
                raise ValidationError(
                    _("Invalid zone: use zone outside of aszabados.eu domain"),
                    code='invalid_zone',
                    params={'value': "asd"},
                )
        else:
            cleaned_data['zone'] = Dyname._meta.get_field('zone').default
            cleaned_data['primary_dns_host'] = Dyname._meta.get_field(
                'primary_dns_host').default
            cleaned_data['primary_dns_ip'] = Dyname._meta.get_field(
                'primary_dns_ip').default

        return cleaned_data
