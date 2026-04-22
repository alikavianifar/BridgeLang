"""
Sitemap configuration for the BlogFolder application.

Generates sitemap entries for all published blog posts to
improve search engine discoverability.
"""

from datetime import datetime

from django.contrib.sitemaps import Sitemap

from BlogFolder.models import Post


class BlogSitemap(Sitemap):
    """Sitemap for published blog posts."""

    changefreq = "daily"
    priority = 0.5

    def items(self):
        """Return all published blog posts."""
        return Post.objects.filter(status=True)

    def lastmod(self, obj: Post) -> datetime:
        """Return the publication date as the last modification date."""
        return obj.published_date