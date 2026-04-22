"""
Settings package for BridgeLang.

Automatically selects the correct settings module based on the
DJANGO_SETTINGS_MODULE environment variable. Defaults to the
development settings for backward compatibility.

Usage:
    Development: DJANGO_SETTINGS_MODULE=CoreFolder.settings.development
    Production:  DJANGO_SETTINGS_MODULE=CoreFolder.settings.production

If DJANGO_SETTINGS_MODULE is set to 'CoreFolder.settings' (the old
single-file path), this __init__ imports development settings.
"""

import os

env = os.environ.get('DJANGO_SETTINGS_MODULE', '')

# If someone sets DJANGO_SETTINGS_MODULE=CoreFolder.settings (old style),
# default to development settings for backward compatibility
if env == 'CoreFolder.settings' or not env:
    from CoreFolder.settings.development import *  # noqa: F401,F403
