"""
Models for the AppFolder application.

Defines database models for the Contact form submissions
and Newsletter email subscriptions.
"""

from django.db import models


class Contact(models.Model):
    """
    Stores a contact form submission.

    Fields:
        name: The sender's full name.
        email: The sender's email address.
        subject: The subject line of the message.
        message: The body text of the message.
        created_date: Timestamp when the message was created.
        updated_date: Timestamp when the message was last updated.
    """

    name: str = models.CharField(max_length=255)
    email: str = models.EmailField()
    subject: str = models.CharField(max_length=255)
    message: str = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_date']

    def __str__(self) -> str:
        return self.name


class NewsLetter(models.Model):
    """
    Stores a newsletter subscriber's email address.

    Fields:
        email: The subscriber's email address.
    """

    email: str = models.EmailField()

    def __str__(self) -> str:
        return self.email