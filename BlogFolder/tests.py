"""
Tests for the BlogFolder application.

Covers models, views, forms, and URL routing for blog posts,
categories, comments, and search functionality.
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

from BlogFolder.models import Post, Category, Comment
from BlogFolder.forms import CommentForm


class CategoryModelTest(TestCase):
    """Tests for the Category model."""

    def test_category_creation(self) -> None:
        """Test that a Category is created with the correct name."""
        category = Category.objects.create(name="Python")
        self.assertEqual(str(category), "Python")


class PostModelTest(TestCase):
    """Tests for the Post model."""

    def setUp(self) -> None:
        """Create test user, category, and post."""
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )
        self.category = Category.objects.create(name="Django")
        self.post = Post.objects.create(
            author=self.user,
            title="Test Post",
            content="This is test content for the blog post.",
            published_date=timezone.now(),
            status=True,
        )
        self.post.category.add(self.category)

    def test_post_creation(self) -> None:
        """Test that a Post instance is created correctly."""
        self.assertEqual(self.post.title, "Test Post")
        self.assertTrue(self.post.status)

    def test_post_str(self) -> None:
        """Test the string representation of Post."""
        self.assertIn("Test Post", str(self.post))

    def test_post_absolute_url(self) -> None:
        """Test get_absolute_url returns the correct URL."""
        expected_url = reverse('BlogFolder:detail', kwargs={'id': self.post.id})
        self.assertEqual(self.post.get_absolute_url(), expected_url)

    def test_author_full_name_with_names(self) -> None:
        """Test author_full_name when first/last name are set."""
        self.user.first_name = "John"
        self.user.last_name = "Doe"
        self.user.save()
        self.assertEqual(self.post.author_full_name(), "John Doe")

    def test_author_full_name_without_names(self) -> None:
        """Test author_full_name falls back to username."""
        self.assertEqual(self.post.author_full_name(), "testuser")

    def test_author_full_name_no_author(self) -> None:
        """Test author_full_name when author is None."""
        self.post.author = None
        self.post.save()
        self.assertEqual(self.post.author_full_name(), "Unknown Author")

    def test_post_ordering(self) -> None:
        """Test that posts are ordered by published_date descending."""
        post2 = Post.objects.create(
            author=self.user,
            title="Newer Post",
            content="Newer content",
            published_date=timezone.now(),
            status=True,
        )
        posts = list(Post.objects.all())
        self.assertEqual(posts[0], post2)  # Newer first


class CommentModelTest(TestCase):
    """Tests for the Comment model."""

    def setUp(self) -> None:
        """Create test user and post for comments."""
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )
        self.post = Post.objects.create(
            author=self.user,
            title="Test Post",
            content="Content",
            published_date=timezone.now(),
            status=True,
        )

    def test_comment_creation(self) -> None:
        """Test that a Comment is created correctly."""
        comment = Comment.objects.create(
            post=self.post,
            name="Commenter",
            email="commenter@example.com",
            message="Great post!",
        )
        self.assertEqual(str(comment), "Commenter")
        self.assertFalse(comment.approved)  # Default is False


class CommentFormTest(TestCase):
    """Tests for the CommentForm."""

    def test_valid_comment_form(self) -> None:
        """Test that a valid comment form passes validation."""
        form = CommentForm(data={
            'name': 'John',
            'email': 'john@example.com',
            'subject': 'Great!',
            'message': 'Wonderful post.',
        })
        self.assertTrue(form.is_valid())

    def test_comment_form_excludes_post_field(self) -> None:
        """Test that the 'post' field is NOT in the form (security)."""
        form = CommentForm()
        self.assertNotIn('post', form.fields)

    def test_invalid_comment_form_missing_message(self) -> None:
        """Test that a form without message fails validation."""
        form = CommentForm(data={
            'name': 'John',
            'email': 'john@example.com',
            'message': '',
        })
        self.assertFalse(form.is_valid())


class BlogViewTest(TestCase):
    """Tests for blog views."""

    def setUp(self) -> None:
        """Create test data for view tests."""
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )
        self.category = Category.objects.create(name="Tutorial")
        self.post = Post.objects.create(
            author=self.user,
            title="Published Post",
            content="This is a published blog post.",
            published_date=timezone.now(),
            status=True,
        )
        self.post.category.add(self.category)

    def test_blog_list_page(self) -> None:
        """Test that the blog listing page returns HTTP 200."""
        response = self.client.get(reverse('BlogFolder:blog'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Published Post")

    def test_blog_detail_page(self) -> None:
        """Test that the blog detail page returns HTTP 200."""
        response = self.client.get(
            reverse('BlogFolder:detail', kwargs={'id': self.post.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_blog_detail_increments_view_count(self) -> None:
        """Test that viewing a post increments the view counter."""
        initial_count = self.post.view_count
        self.client.get(
            reverse('BlogFolder:detail', kwargs={'id': self.post.id})
        )
        self.post.refresh_from_db()
        self.assertEqual(self.post.view_count, initial_count + 1)

    def test_blog_detail_login_required_redirect(self) -> None:
        """Test that login-required posts redirect unauthenticated users."""
        self.post.login_required = True
        self.post.save()
        response = self.client.get(
            reverse('BlogFolder:detail', kwargs={'id': self.post.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn('/Accounts/login/', response.url)

    def test_blog_filter_by_category(self) -> None:
        """Test filtering blog posts by category name."""
        response = self.client.get(
            reverse('BlogFolder:category', kwargs={'category_name': 'Tutorial'})
        )
        self.assertEqual(response.status_code, 200)

    def test_blog_search(self) -> None:
        """Test blog search functionality."""
        response = self.client.get(
            reverse('BlogFolder:search'), {'s': 'published'}
        )
        self.assertEqual(response.status_code, 200)

    def test_blog_search_empty_query(self) -> None:
        """Test blog search with empty query returns all posts."""
        response = self.client.get(
            reverse('BlogFolder:search'), {'s': ''}
        )
        self.assertEqual(response.status_code, 200)

    def test_draft_post_not_visible(self) -> None:
        """Test that draft posts are not shown in the blog listing."""
        Post.objects.create(
            author=self.user,
            title="Draft Post",
            content="Draft content",
            published_date=timezone.now(),
            status=False,
        )
        response = self.client.get(reverse('BlogFolder:blog'))
        self.assertNotContains(response, "Draft Post")


class BlogURLTest(TestCase):
    """Tests for BlogFolder URL routing."""

    def test_blog_list_url(self) -> None:
        """Test that the blog list URL resolves correctly."""
        self.assertEqual(reverse('BlogFolder:blog'), '/blog/')

    def test_blog_search_url(self) -> None:
        """Test that the search URL resolves correctly."""
        self.assertEqual(reverse('BlogFolder:search'), '/blog/search')
