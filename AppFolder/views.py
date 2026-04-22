"""
Views for the AppFolder (main site pages).

Handles the homepage, contact form submission, and newsletter signup.
Email recipients and sender addresses are loaded from environment
variables for security.
"""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail
from decouple import config
from maintenance_mode.decorators import force_maintenance_mode_off

from AppFolder.forms import ContactForm, NewsLetterForm

# Email configuration from environment variables
CONTACT_FROM_EMAIL: str = config("CONTACT_FROM_EMAIL", default="noreply@example.com")
CONTACT_RECIPIENTS: list[str] = config(
    "CONTACT_RECIPIENTS",
    default="admin@example.com",
    cast=lambda v: [s.strip() for s in v.split(",")],
)
SITE_URL: str = config("SITE_URL", default="http://127.0.0.1:8000")


def index(request: HttpRequest) -> HttpResponse:
    """Render the main homepage."""
    return render(request, "main/index.html")


def contact(request: HttpRequest) -> HttpResponse:
    """
    Handle the contact form.

    On POST: validates the form, saves the contact message to the database,
    sends a notification email to admins, and redirects with a success message.
    On GET: displays an empty contact form with a CSRF token.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_obj = form.save()

            # Build notification email for admins
            name: str = form.cleaned_data['name']
            email: str = form.cleaned_data['email']
            title: str = form.cleaned_data['subject']
            message_body: str = form.cleaned_data['message']
            subject: str = 'New Contact Message'
            contact_edit_url: str = reverse(
                'admin:AppFolder_contact_change', args=[contact_obj.id]
            )
            email_message: str = (
                f'Name:\n{name}\n\n'
                f'Email:\n{email}\n\n'
                f'Subject:\n{title}\n\n'
                f'Message:\n{message_body}\n\n'
                f'Contact Edit Link:\n{SITE_URL}{contact_edit_url}'
            )
            send_mail(subject, email_message, CONTACT_FROM_EMAIL, CONTACT_RECIPIENTS)

            # Message alert
            messages.add_message(
                request, messages.SUCCESS,
                'Your message has been sent successfully.'
            )

            # Clear the token to allow new submissions
            request.session.pop('form_token', None)
            return redirect('AppFolder:contact')
        else:
            messages.add_message(
                request, messages.ERROR,
                'There was an error sending your message. Please try again.'
            )
    else:
        # Generate a new token for the form
        request.session['form_token'] = str(__import__('uuid').uuid4())

    form = ContactForm()
    return render(request, "main/index.html", {
        'form': form,
        'form_token': request.session.get('form_token', '')
    })


@force_maintenance_mode_off
def newsletter(request: HttpRequest) -> HttpResponse:
    """
    Handle newsletter email subscription.

    Saves the submitted email to the database and redirects
    to the homepage with a success or error message.
    """
    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Your email submitted successfully'
            )
            return redirect('/')
        else:
            messages.add_message(
                request, messages.ERROR,
                'Your email was not sent. Please try again.'
            )
            return redirect('/')