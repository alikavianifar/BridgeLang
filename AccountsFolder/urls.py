"""
URL configuration for the AccountsFolder application.

Maps URL paths for user authentication: login, logout, and signup.
"""

from django.urls import path

from AccountsFolder import views

app_name = 'Accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
]
