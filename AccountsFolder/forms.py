"""
Forms for the AccountsFolder application.

Provides custom registration and authentication forms with
email validation, CAPTCHA protection, and email-or-username
login support.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField


class EmailUserCreationForm(UserCreationForm):
    """
    User registration form with required email and CAPTCHA.

    Extends Django's UserCreationForm to require a unique email
    address and includes CAPTCHA to prevent automated signups.
    """

    captcha = CaptchaField()
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self) -> str:
        """Validate that the email address is not already registered."""
        email: str = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email


class EmailOrUsernameAuthenticationForm(AuthenticationForm):
    """
    Login form accepting either username or email with CAPTCHA.

    Extends Django's AuthenticationForm to allow users to log in
    with their email address in addition to their username.
    """

    captcha = CaptchaField()
    username = forms.CharField(label="Username or Email", max_length=254)