"""
Models for the BlogFolder application.

Defines database models for blog posts, categories, and comments.
Posts support tagging, categorization, view counting, and
login-required access control.
"""

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class Category(models.Model):
    """
    Blog post category for organizing content.

    Fields:
        name: The category display name.
    """

    name: str = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    """
    A blog post with rich content, tagging, and access control.

    Fields:
        author: The user who wrote the post (nullable on deletion).
        title: The post headline.
        content: The full post body (supports HTML via Summernote).
        category: Many-to-many relationship with Category.
        tag: Tags managed by django-taggit.
        image: Featured image for the post.
        created_date: Auto-set when the post is first created.
        updated_date: Auto-set on every save.
        published_date: When the post was published (nullable).
        login_required: Whether authentication is needed to view.
        status: Whether the post is published (True) or draft (False).
        view_count: Number of times the post has been viewed.
    """

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title: str = models.CharField(max_length=255)
    content: str = models.TextField()
    category = models.ManyToManyField(Category)
    tag = TaggableManager()
    image = models.ImageField(upload_to='blog/', default='blog/default.png')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(null=True)
    login_required: bool = models.BooleanField(default=False)
    status: bool = models.BooleanField(default=False)
    view_count: int = models.IntegerField(default=0)

    class Meta:
        ordering = ['-published_date']

    def get_absolute_url(self) -> str:
        """Return the canonical URL for this post."""
        return reverse('BlogFolder:detail', kwargs={'id': self.id})

    def __str__(self) -> str:
        return f" {self.id} - {self.title} "

    def author_full_name(self) -> str:
        """
        Return the author's full name, falling back to username.

        Used in the admin panel to display a human-readable author name.
        """
        if self.author:
            if self.author.first_name or self.author.last_name:
                return f"{self.author.first_name} {self.author.last_name}".strip()
            return self.author.username
        return "Unknown Author"

    author_full_name.short_description = 'AUTHOR'
    author_full_name.admin_order_field = 'author__username'


class Comment(models.Model):
    """
    A comment on a blog post, subject to admin approval.

    Fields:
        post: The blog post this comment belongs to.
        name: The commenter's display name.
        email: The commenter's email address.
        subject: Optional subject line.
        message: The comment body text.
        created_date: Auto-set when the comment is created.
        updated_date: Auto-set on every save.
        approved: Whether an admin has approved the comment for display.
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name: str = models.CharField(max_length=255)
    email: str = models.EmailField()
    subject: str = models.CharField(max_length=255, blank=True, null=True)
    message: str = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    approved: bool = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name