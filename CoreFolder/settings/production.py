"""
Production-specific Django settings for BridgeLang.

Extends base settings with production-hardened defaults:
- PostgreSQL database
- SMTP email backend
- SSL/HSTS security headers
- Debug toolbar disabled
- Robots configured for production

Usage:
    DJANGO_SETTINGS_MODULE=CoreFolder.settings.production
"""

from CoreFolder.settings.base import *  # noqa: F401,F403

# Database — PostgreSQL for production
DATABASES = {
    "default": {
        "ENGINE": config("PGDB_ENGINE", default="django.db.backends.postgresql"),  # noqa: F405
        "NAME": config("PGDB_NAME", default="postgres"),  # noqa: F405
        "USER": config("PGDB_USER", default="postgres"),  # noqa: F405
        "PASSWORD": config("PGDB_PASS", default=""),  # noqa: F405
        "HOST": config("PGDB_HOST", default="localhost"),  # noqa: F405
        "PORT": config("PGDB_PORT", cast=int, default=5432),  # noqa: F405
    }
}

# Robots — disable in production (use custom robots.txt)
ROBOTS_USE_HOST = False
ROBOTS_USE_SITEMAP = False

# Email — SMTP backend for production
EMAIL_BACKEND = config("EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")  # noqa: F405
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")  # noqa: F405
EMAIL_PORT = config("EMAIL_PORT", cast=int, default=587)  # noqa: F405
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool, default=True)  # noqa: F405
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")  # noqa: F405
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")  # noqa: F405
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="")  # noqa: F405


# Security — SSL/HSTS configuration
if config("USE_SSL_CONFIG", cast=bool, default=False):  # noqa: F405
    # HTTPS settings
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True

    # HSTS settings
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    # Additional security headers
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = "SAMEORIGIN"
    SECURE_REFERRER_POLICY = "strict-origin"
    USE_X_FORWARDED_HOST = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
