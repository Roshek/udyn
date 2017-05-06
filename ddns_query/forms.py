from registration.forms import RegistrationForm
from .models import User


class CustomRegistrationForm(RegistrationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
