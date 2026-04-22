"""
Models for the AccountsFolder application.

This module is intentionally minimal as the application uses
Django's built-in User model (django.contrib.auth.models.User).
Custom user functionality is handled via the authentication
backend in backends.py.
"""

from django.db import models

# This app uses Django's built-in User model.
# See AccountsFolder.backends for custom authentication logic.
