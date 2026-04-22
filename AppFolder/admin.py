"""
Admin configuration for the AppFolder application.

Registers Contact and NewsLetter models with customized
admin list views for efficient management.
"""

from django.contrib import admin

from AppFolder.models import Contact, NewsLetter


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Admin configuration for Contact model with date hierarchy and search."""

    date_hierarchy = 'created_date'
    empty_value_display = '-empty-'
    list_display = ('name', 'email', 'subject', 'created_date')
    list_filter = ('created_date',)
    search_fields = ('subject', 'message')


@admin.register(NewsLetter)
class NewsLetterAdmin(admin.ModelAdmin):
    """Admin configuration for NewsLetter model."""

    list_display = ('email',)
    search_fields = ('email',)