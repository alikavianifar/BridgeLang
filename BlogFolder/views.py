"""
Views for the BlogFolder application.

Handles blog listing (with filtering by author, category, and tag),
blog detail pages, comment submission, and blog search functionality.
"""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from decouple import config
import uuid

from BlogFolder.models import Post, Category, Comment
from BlogFolder.forms import CommentForm

# Email configuration from environment variables
BLOG_FROM_EMAIL: str = config("BLOG_FROM_EMAIL", default="noreply@example.com")
BLOG_RECIPIENTS: list[str] = config(
    "BLOG_RECIPIENTS",
    default="admin@example.com",
    cast=lambda v: [s.strip() for s in v.split(",")],
)
SITE_URL: str = config("SITE_URL", default="http://127.0.0.1:8000")

# Number of posts per page
POSTS_PER_PAGE: int = 4


def blog(request: HttpRequest, **kwargs) -> HttpResponse:
    """
    Display a paginated list of published blog posts.

    Supports filtering by:
        - author_id: Filter posts by author
        - category_name: Filter posts by category
        - tag_name: Filter posts by tag

    Args:
        request: The HTTP request object.
        **kwargs: Optional filter parameters (author_id, category_name, tag_name).

    Returns:
        Rendered blog listing page with paginated posts.
    """
    posts = (
        Post.objects
        .filter(status=True, published_date__lte=timezone.now())
        .order_by('-published_date')
    )

    if kwargs.get('author_id'):
        posts = posts.filter(author__id=kwargs['author_id'])

    if kwargs.get('category_name'):
        posts = posts.filter(category__name=kwargs['category_name'])

    if kwargs.get('tag_name'):
        posts = posts.filter(tag__name__in=[kwargs['tag_name']])

    # All categories for sidebar
    category = Category.objects.all()

    # Pagination
    paginator = Paginator(posts, POSTS_PER_PAGE)
    try:
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)
    except PageNotAnInteger:
        posts = paginator.get_page(1)
    except EmptyPage:
        posts = paginator.get_page(1)

    context = {'posts': posts, 'category': category}
    return render(request, "blog/blog.html", context)


def blog_detail(request: HttpRequest, id: int) -> HttpResponse:
    """
    Display a single blog post with its comments and comment form.

    On POST: validates and saves a new comment, sends email notification
    to admins, and redirects back to the post.
    On GET: displays the post, approved comments, and navigation to
    previous/next posts.

    If the post requires login and the user is not authenticated,
    redirects to the login page with a 'next' parameter.

    Args:
        request: The HTTP request object.
        id: The primary key of the blog post.

    Returns:
        Rendered blog detail page or redirect to login.
    """
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # Save comment with the correct post (set in the view, not from user input)
            comment = form.save(commit=False)
            post_obj = get_object_or_404(
                Post.objects.filter(status=True, published_date__lte=timezone.now()),
                id=id
            )
            comment.post = post_obj
            comment.save()

            # Build notification email for admins
            name: str = form.cleaned_data['name']
            email: str = form.cleaned_data['email']
            title: str = form.cleaned_data.get('subject', '')
            message_body: str = form.cleaned_data['message']
            subject: str = 'New Blog Comment'
            comment_edit_url: str = reverse(
                'admin:BlogFolder_comment_change', args=[comment.id]
            )
            email_message: str = (
                f'Name:\n{name}\n\n'
                f'Email:\n{email}\n\n'
                f'Subject:\n{title}\n\n'
                f'Message:\n{message_body}\n\n'
                f'Comment Edit Link:\n{SITE_URL}{comment_edit_url}'
            )
            send_mail(subject, email_message, BLOG_FROM_EMAIL, BLOG_RECIPIENTS)

            messages.add_message(
                request, messages.SUCCESS,
                'Your comment has been sent successfully.'
            )
            # Clear the token to allow new submissions
            request.session.pop('form_token', None)
            return redirect('BlogFolder:detail', id=id)

        else:
            messages.add_message(
                request, messages.ERROR,
                'There was an error sending your comment. Please try again.'
            )

    # Generate a new token for the form
    request.session['form_token'] = str(uuid.uuid4())
    post = get_object_or_404(
        Post.objects.filter(status=True, published_date__lte=timezone.now()),
        id=id
    )

    if not post.login_required or request.user.is_authenticated:
        post.view_count += 1
        post.save()

        # All categories for sidebar
        category = Category.objects.all()

        comments = Comment.objects.filter(
            post=post.id, approved=True
        ).order_by('-created_date')

        previous_post = (
            Post.objects
            .filter(
                status=True,
                published_date__lte=timezone.now(),
                published_date__lt=post.published_date,
            )
            .order_by('-published_date')
            .first()
        )

        next_post = (
            Post.objects
            .filter(
                status=True,
                published_date__lte=timezone.now(),
                published_date__gt=post.published_date,
            )
            .order_by('published_date')
            .first()
        )

        form = CommentForm()
        context = {
            'post': post,
            'category': category,
            'comments': comments,
            'previous_post': previous_post,
            'next_post': next_post,
            'form': form,
            'form_token': request.session.get('form_token', ''),
        }
        return render(request, "blog/blog-details.html", context)

    else:
        next_url: str = request.get_full_path()
        return redirect(f'/Accounts/login/?next={next_url}')


def blog_search(request: HttpRequest) -> HttpResponse:
    """
    Search published blog posts by content.

    Filters posts whose content contains the search query parameter 's'.

    Args:
        request: The HTTP request object with GET parameter 's'.

    Returns:
        Rendered blog listing page with filtered results.
    """
    posts = Post.objects.filter(
        status=True, published_date__lte=timezone.now()
    )
    if request.method == 'GET':
        search_query = request.GET.get('s', '')
        if search_query:
            posts = posts.filter(content__icontains=search_query)
    context = {'posts': posts}
    return render(request, "blog/blog.html", context)