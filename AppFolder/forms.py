"""
Forms for the AppFolder application.

Provides ModelForms for the Contact and NewsLetter models,
used on the main site pages.
"""

from django import forms

from AppFolder.models import Contact, NewsLetter


class ContactForm(forms.ModelForm):
    """Form for submitting a contact message."""

    class Meta:
        model = Contact
        fields = ('name', 'email', 'subject', 'message')


class NewsLetterForm(forms.ModelForm):
    """Form for subscribing to the newsletter."""

    class Meta:
        model = NewsLetter
        fields = ('email',)