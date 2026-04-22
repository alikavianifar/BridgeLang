"""
URL configuration for the AppFolder application.

Maps URL paths to views for the homepage, contact form,
and newsletter subscription.
"""

from django.urls import path

from AppFolder.views import index, contact, newsletter

app_name = 'AppFolder'

urlpatterns = [
    path('', index, name='index'),
    path('contact', contact, name='contact'),
    path('newsletter', newsletter, name='newsletter'),
]
