"""
Django app configuration for the BlogFolder application.
"""

from django.apps import AppConfig


class BlogfolderConfig(AppConfig):
    """Configuration for the Blog application."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'BlogFolder'
    verbose_name = 'Blog'
