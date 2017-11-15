from registration.forms import RegistrationForm
from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.conf import settings
from .models import Dyname

class CustomRegistrationForm(RegistrationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')


class AddDynameForm(ModelForm):
    custom_zone = forms.BooleanField(required=False)

    class Meta:
        model = Dyname
        fields = [
            'custom_zone',
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
            for bzone in settings.BLACK_LIST:
                if bzone in czone:
                    raise ValidationError(
                        _("Invalid zone: " + czone + ". Use of this zone in custom mode is not permitted."),
                        code='invalid_zone',
                        params={'value': 'invalid_zone'},
                    )
        else:
            cleaned_data['zone'] = settings.SETTINGS_DICT['DEFAULT_ZONE']
            cleaned_data['primary_dns_host'] = settings.SETTINGS_DICT['DEFAULT_NS_HOST']
            cleaned_data['primary_dns_ip'] = settings.SETTINGS_DICT['DEFAULT_NS_IP']

        return cleaned_data
