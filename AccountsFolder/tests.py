"""
Tests for the AccountsFolder application.

Covers authentication views (login, logout, signup), custom
authentication backend, and registration form validation.
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from AccountsFolder.forms import EmailUserCreationForm
from AccountsFolder.backends import EmailOrUsernameModelBackend


class EmailOrUsernameBackendTest(TestCase):
    """Tests for the custom EmailOrUsername authentication backend."""

    def setUp(self) -> None:
        """Create a test user."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='securepass123',
        )
        self.backend = EmailOrUsernameModelBackend()

    def test_authenticate_with_username(self) -> None:
        """Test authentication with a valid username."""
        user = self.backend.authenticate(
            request=None, username='testuser', password='securepass123'
        )
        self.assertEqual(user, self.user)

    def test_authenticate_with_email(self) -> None:
        """Test authentication with a valid email address."""
        user = self.backend.authenticate(
            request=None, username='test@example.com', password='securepass123'
        )
        self.assertEqual(user, self.user)

    def test_authenticate_wrong_password(self) -> None:
        """Test that wrong password returns None."""
        user = self.backend.authenticate(
            request=None, username='testuser', password='wrongpassword'
        )
        self.assertIsNone(user)

    def test_authenticate_nonexistent_user(self) -> None:
        """Test that nonexistent user returns None."""
        user = self.backend.authenticate(
            request=None, username='nouser', password='pass'
        )
        self.assertIsNone(user)


class LoginViewTest(TestCase):
    """Tests for the login view."""

    def setUp(self) -> None:
        """Create a test user for login tests."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='securepass123',
        )

    def test_login_page_get(self) -> None:
        """Test that the login page renders correctly."""
        response = self.client.get(reverse('Accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_redirect_if_authenticated(self) -> None:
        """Test that authenticated users are redirected from login page."""
        self.client.login(username='testuser', password='securepass123')
        response = self.client.get(reverse('Accounts:login'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')


class LogoutViewTest(TestCase):
    """Tests for the logout view."""

    def setUp(self) -> None:
        """Create and login a test user."""
        self.user = User.objects.create_user(
            username='testuser', password='securepass123'
        )
        self.client.login(username='testuser', password='securepass123')

    def test_logout_redirects(self) -> None:
        """Test that logout redirects to homepage."""
        response = self.client.get(reverse('Accounts:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_logout_requires_login(self) -> None:
        """Test that unauthenticated users are redirected to login."""
        self.client.logout()
        response = self.client.get(reverse('Accounts:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/Accounts/login/', response.url)


class SignupViewTest(TestCase):
    """Tests for the signup view."""

    def test_signup_page_get(self) -> None:
        """Test that the signup page renders correctly."""
        response = self.client.get(reverse('Accounts:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')

    def test_signup_redirect_if_authenticated(self) -> None:
        """Test that authenticated users are redirected from signup."""
        User.objects.create_user(
            username='testuser', password='securepass123'
        )
        self.client.login(username='testuser', password='securepass123')
        response = self.client.get(reverse('Accounts:signup'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')


class EmailUserCreationFormTest(TestCase):
    """Tests for the custom user creation form."""

    def test_duplicate_email_rejected(self) -> None:
        """Test that duplicate emails are rejected during registration."""
        User.objects.create_user(
            username='existing',
            email='taken@example.com',
            password='pass123',
        )
        form = EmailUserCreationForm(data={
            'username': 'newuser',
            'email': 'taken@example.com',
            'password1': 'complexPass123!',
            'password2': 'complexPass123!',
            'captcha_0': 'test',
            'captcha_1': 'PASSED',
        })
        # Even without captcha validation, the email check should fail
        self.assertFalse(form.is_valid())


class AccountsURLTest(TestCase):
    """Tests for AccountsFolder URL routing."""

    def test_login_url(self) -> None:
        """Test that the login URL resolves correctly."""
        self.assertEqual(reverse('Accounts:login'), '/Accounts/login/')

    def test_signup_url(self) -> None:
        """Test that the signup URL resolves correctly."""
        self.assertEqual(reverse('Accounts:signup'), '/Accounts/signup/')

    def test_logout_url(self) -> None:
        """Test that the logout URL resolves correctly."""
        self.assertEqual(reverse('Accounts:logout'), '/Accounts/logout/')
