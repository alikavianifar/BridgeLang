"""
Tests for the AppFolder application.

Covers models, views, forms, and URL routing for the homepage,
contact form, and newsletter subscription.
"""

from django.test import TestCase, Client
from django.urls import reverse

from AppFolder.models import Contact, NewsLetter
from AppFolder.forms import ContactForm, NewsLetterForm


class ContactModelTest(TestCase):
    """Tests for the Contact model."""

    def setUp(self) -> None:
        """Create a test contact instance."""
        self.contact = Contact.objects.create(
            name="John Doe",
            email="john@example.com",
            subject="Test Subject",
            message="Test message body",
        )

    def test_contact_creation(self) -> None:
        """Test that a Contact instance is created correctly."""
        self.assertEqual(self.contact.name, "John Doe")
        self.assertEqual(self.contact.email, "john@example.com")

    def test_contact_str(self) -> None:
        """Test the string representation of Contact."""
        self.assertEqual(str(self.contact), "John Doe")

    def test_contact_ordering(self) -> None:
        """Test that contacts are ordered by created_date."""
        contact2 = Contact.objects.create(
            name="Jane Doe",
            email="jane@example.com",
            subject="Another Subject",
            message="Another message",
        )
        contacts = list(Contact.objects.all())
        self.assertEqual(contacts[0], self.contact)
        self.assertEqual(contacts[1], contact2)


class NewsLetterModelTest(TestCase):
    """Tests for the NewsLetter model."""

    def test_newsletter_creation(self) -> None:
        """Test that a NewsLetter instance is created correctly."""
        newsletter = NewsLetter.objects.create(email="test@example.com")
        self.assertEqual(newsletter.email, "test@example.com")

    def test_newsletter_str(self) -> None:
        """Test the string representation of NewsLetter."""
        newsletter = NewsLetter.objects.create(email="test@example.com")
        self.assertEqual(str(newsletter), "test@example.com")


class ContactFormTest(TestCase):
    """Tests for the ContactForm."""

    def test_valid_contact_form(self) -> None:
        """Test that a valid form passes validation."""
        form = ContactForm(data={
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Test',
            'message': 'Hello world',
        })
        self.assertTrue(form.is_valid())

    def test_invalid_contact_form_missing_email(self) -> None:
        """Test that a form without email fails validation."""
        form = ContactForm(data={
            'name': 'John Doe',
            'email': '',
            'subject': 'Test',
            'message': 'Hello',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_invalid_contact_form_missing_name(self) -> None:
        """Test that a form without name fails validation."""
        form = ContactForm(data={
            'name': '',
            'email': 'john@example.com',
            'subject': 'Test',
            'message': 'Hello',
        })
        self.assertFalse(form.is_valid())


class NewsLetterFormTest(TestCase):
    """Tests for the NewsLetterForm."""

    def test_valid_newsletter_form(self) -> None:
        """Test that a valid email passes validation."""
        form = NewsLetterForm(data={'email': 'test@example.com'})
        self.assertTrue(form.is_valid())

    def test_invalid_newsletter_form(self) -> None:
        """Test that an invalid email fails validation."""
        form = NewsLetterForm(data={'email': 'not-an-email'})
        self.assertFalse(form.is_valid())


class IndexViewTest(TestCase):
    """Tests for the homepage view."""

    def test_index_page_status_code(self) -> None:
        """Test that the homepage returns HTTP 200."""
        response = self.client.get(reverse('AppFolder:index'))
        self.assertEqual(response.status_code, 200)

    def test_index_uses_correct_template(self) -> None:
        """Test that the homepage uses the correct template."""
        response = self.client.get(reverse('AppFolder:index'))
        self.assertTemplateUsed(response, 'main/index.html')


class ContactViewTest(TestCase):
    """Tests for the contact view."""

    def test_contact_page_get(self) -> None:
        """Test that GET request to contact page returns 200."""
        response = self.client.get(reverse('AppFolder:contact'))
        self.assertEqual(response.status_code, 200)


class NewsletterViewTest(TestCase):
    """Tests for the newsletter view."""

    def test_newsletter_post_valid(self) -> None:
        """Test that a valid newsletter submission redirects."""
        response = self.client.post(
            reverse('AppFolder:newsletter'),
            data={'email': 'test@example.com'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(NewsLetter.objects.count(), 1)

    def test_newsletter_post_invalid(self) -> None:
        """Test that an invalid newsletter submission redirects with error."""
        response = self.client.post(
            reverse('AppFolder:newsletter'),
            data={'email': 'invalid'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(NewsLetter.objects.count(), 0)


class URLRoutingTest(TestCase):
    """Tests for AppFolder URL routing."""

    def test_index_url_resolves(self) -> None:
        """Test that the index URL resolves correctly."""
        url = reverse('AppFolder:index')
        self.assertEqual(url, '/')

    def test_contact_url_resolves(self) -> None:
        """Test that the contact URL resolves correctly."""
        url = reverse('AppFolder:contact')
        self.assertEqual(url, '/contact')

    def test_newsletter_url_resolves(self) -> None:
        """Test that the newsletter URL resolves correctly."""
        url = reverse('AppFolder:newsletter')
        self.assertEqual(url, '/newsletter')
