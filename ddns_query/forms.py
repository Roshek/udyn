from registration.forms import RegistrationForm

from django.contrib.auth import get_user_model


class CustomRegistrationForm(RegistrationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')
