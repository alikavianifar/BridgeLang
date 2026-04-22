"""
Custom template tags for the BlogFolder application.

Provides reusable template tags for displaying blog statistics,
popular posts, categories with post counts, and recent posts.
"""

from django import template
from django.utils import timezone
from django.db.models import QuerySet

from BlogFolder.models import Post, Category, Comment
from django.contrib.auth.models import User

register = template.Library()


@register.simple_tag
def views_count() -> int:
    """Return the total view count across all published posts."""
    posts: QuerySet[Post] = Post.objects.filter(
        status=True, published_date__lte=timezone.now()
    )
    return sum(post.view_count for post in posts)


@register.simple_tag
def posts_count() -> int:
    """Return the number of published blog posts."""
    return Post.objects.filter(
        status=True, published_date__lte=timezone.now()
    ).count()


@register.simple_tag
def authors_count() -> int:
    """Return the total number of registered users."""
    return User.objects.all().count()


@register.simple_tag
def all_comments_count() -> int:
    """Return the number of approved comments."""
    return Comment.objects.filter(approved=True).count()


@register.inclusion_tag('blog/blog-popular-posts.html')
def popular_posts() -> dict:
    """Render the top 3 most-viewed published posts."""
    posts: QuerySet[Post] = (
        Post.objects
        .filter(status=True, published_date__lte=timezone.now())
        .order_by('-view_count')[:3]
    )
    return {'posts': posts}


@register.inclusion_tag('blog/blog-categories.html')
def categories() -> dict:
    """Render all categories with their published post counts."""
    posts: QuerySet[Post] = Post.objects.filter(
        status=True, published_date__lte=timezone.now()
    )
    all_categories: QuerySet[Category] = Category.objects.all()
    categories_dictionary: dict[Category, int] = {
        cat: posts.filter(category=cat).count()
        for cat in all_categories
    }
    return {'categories': categories_dictionary}


@register.inclusion_tag('main/recent-blog-posts.html')
def recent_blog_posts() -> dict:
    """Render the 3 most recently published blog posts."""
    posts: QuerySet[Post] = (
        Post.objects
        .filter(status=True, published_date__lte=timezone.now())
        .order_by('-published_date')[:3]
    )
    return {'posts': posts}