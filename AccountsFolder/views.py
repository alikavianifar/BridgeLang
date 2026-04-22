"""
Views for the AccountsFolder application.

Handles user authentication including login (with email or username),
logout, and registration with email verification.
"""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from decouple import config
import re

from AccountsFolder.forms import EmailUserCreationForm, EmailOrUsernameAuthenticationForm
from BlogFolder.models import Post

# Email configuration from environment variables
SIGNUP_FROM_EMAIL: str = config("SIGNUP_FROM_EMAIL", default="noreply@example.com")


def login_view(request: HttpRequest) -> HttpResponse:
    """
    Handle user login with username or email.

    Displays contextual messages when redirected from login-required pages.
    Supports 'next' parameter for post-login redirection.

    Args:
        request: The HTTP request object.

    Returns:
        Rendered login page or redirect on successful authentication.
    """
    next_url: str | None = request.GET.get('next')

    if next_url is not None:
        match = re.match(r'^/blog/post/(\d+)$', next_url)
        if match:
            try:
                post = Post.objects.get(id=match.group(1))
                messages.add_message(
                    request, messages.INFO,
                    f'Please login to read <strong>"{post.title}"</strong> post'
                )
            except Post.DoesNotExist:
                pass
        if next_url in ("/Lessons/", "/Lessons/practice"):
            messages.add_message(
                request, messages.INFO,
                'Please login to access course content'
            )

    if request.user.is_authenticated:
        messages.add_message(
            request, messages.ERROR,
            'You have already logged in'
        )
        return redirect('/')

    if request.method == 'POST':
        form = EmailOrUsernameAuthenticationForm(
            request=request, data=request.POST
        )
        if form.is_valid():
            username: str = form.cleaned_data.get('username')
            password: str = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                full_name: str = user.get_full_name() or user.username
                messages.add_message(
                    request, messages.SUCCESS,
                    f'Welcome {full_name}'
                )

                # Redirect to 'next' URL or default page
                next_url = request.POST.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('/Lessons/')
        else:
            messages.add_message(
                request, messages.ERROR,
                'Username or password is not valid'
            )
            return redirect('/Accounts/login/')

    form = EmailOrUsernameAuthenticationForm()
    context = {'form': form, 'next': request.GET.get('next', '')}
    return render(request, "accounts/login.html", context)


@login_required
def logout_view(request: HttpRequest) -> HttpResponse:
    """
    Log out the current user and redirect to the homepage.

    Args:
        request: The HTTP request object.

    Returns:
        Redirect to homepage with a success message.
    """
    logout(request)
    messages.add_message(
        request, messages.INFO,
        'Successful logout. We hope to see you again!'
    )
    return redirect('/')


def signup_view(request: HttpRequest) -> HttpResponse:
    """
    Handle new user registration.

    On POST: validates the registration form, creates the user account,
    sends a welcome email, and redirects to the login page.
    On GET: displays an empty registration form.

    Args:
        request: The HTTP request object.

    Returns:
        Rendered signup page or redirect on successful registration.
    """
    if request.user.is_authenticated:
        messages.add_message(
            request, messages.ERROR,
            'You are already signed up'
        )
        return redirect('/')

    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            # Send welcome email to the new user
            subject: str = "Welcome to BridgeLang"
            message: str = (
                "Thanks for joining us. "
                "We are excited to have you on board!"
            )
            recipient_list: list[str] = [form.cleaned_data.get('email')]
            send_mail(subject, message, SIGNUP_FROM_EMAIL, recipient_list)

            messages.add_message(
                request, messages.SUCCESS,
                'Your registration was successful'
            )
            return redirect('/Accounts/login/')
        else:
            messages.add_message(
                request, messages.ERROR,
                'Your registration was not successful'
            )
            return render(request, "accounts/signup.html", {'form': form})

    form = EmailUserCreationForm()
    context = {'form': form}
    return render(request, "accounts/signup.html", context)
