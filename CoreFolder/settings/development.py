"""
Development-specific Django settings for BridgeLang.

Extends base settings with development-friendly defaults:
- SQLite database
- Console email backend
- Debug toolbar enabled
- Robots configured for development
"""

from CoreFolder.settings.base import *  # noqa: F401,F403

# Database — SQLite for local development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Debug Toolbar
INSTALLED_APPS += [  # noqa: F405
    'django_extensions',
    'debug_toolbar',
]

INTERNAL_IPS = [
    "127.0.0.1",
]

MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')  # noqa: F405

# Robots — enable in development for testing
ROBOTS_USE_HOST = True
ROBOTS_USE_SITEMAP = True

# Email — use console backend in development (prints to terminal)
EMAIL_BACKEND = config("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")  # noqa: F405
EMAIL_USE_TLS = False
EMAIL_HOST = config("EMAIL_HOST", default="localhost")  # noqa: F405
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")  # noqa: F405
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")  # noqa: F405
EMAIL_PORT = config("EMAIL_PORT", cast=int, default=25)  # noqa: F405
