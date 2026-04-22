"""
Custom authentication backend for the AccountsFolder application.

Provides an authentication backend that allows users to log in
using either their username or email address.
"""

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.http import HttpRequest


class EmailOrUsernameModelBackend(ModelBackend):
    """
    Custom authentication backend supporting login via email or username.

    Attempts to find the user by username first, then falls back
    to email lookup. Password verification and active status checks
    are performed before granting access.
    """

    def authenticate(
        self,
        request: HttpRequest,
        username: str = None,
        password: str = None,
        **kwargs,
    ):
        """
        Authenticate a user by username or email.

        Args:
            request: The HTTP request object.
            username: The username or email provided by the user.
            password: The password provided by the user.

        Returns:
            The authenticated User object, or None if authentication fails.
        """
        UserModel = get_user_model()

        # Try username first
        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            # Fall back to email lookup
            try:
                user = UserModel.objects.get(email=username)
            except UserModel.DoesNotExist:
                return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
