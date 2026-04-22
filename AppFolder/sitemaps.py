"""
Sitemap configuration for the AppFolder application.

Generates sitemap entries for the main static pages
(homepage and contact page).
"""

from django.contrib import sitemaps
from django.urls import reverse


class StaticViewSitemap(sitemaps.Sitemap):
    """Sitemap for static pages like the homepage and contact page."""

    priority = 0.5
    changefreq = "daily"

    def items(self) -> list[str]:
        """Return a list of named URL patterns to include in the sitemap."""
        return ["AppFolder:index", "AppFolder:contact"]

    def location(self, item: str) -> str:
        """Resolve the URL for each sitemap item."""
        return reverse(item)