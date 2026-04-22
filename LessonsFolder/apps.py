"""
Django app configuration for the LessonsFolder application.
"""

from django.apps import AppConfig


class LessonsfolderConfig(AppConfig):
    """Configuration for the Lessons application."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'LessonsFolder'
    verbose_name = 'Lessons'
