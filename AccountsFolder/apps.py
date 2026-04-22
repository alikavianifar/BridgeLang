"""
Django app configuration for the AccountsFolder application.
"""

from django.apps import AppConfig


class AccountsfolderConfig(AppConfig):
    """Configuration for the Accounts application."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AccountsFolder'
    verbose_name = 'Accounts'
