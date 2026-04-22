"""
Django app configuration for the AppFolder application.
"""

from django.apps import AppConfig


class AppfolderConfig(AppConfig):
    """Configuration for the main App (homepage, contact, newsletter)."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AppFolder'
    verbose_name = 'Main Site'
