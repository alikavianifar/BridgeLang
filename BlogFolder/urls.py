"""
URL configuration for the BlogFolder application.

Maps URL paths for blog listing, detail, author/category/tag
filtering, and search.
"""

from django.urls import path

from BlogFolder.views import blog, blog_detail, blog_search

app_name = 'BlogFolder'

urlpatterns = [
    path('', blog, name='blog'),
    path('post/<int:id>', blog_detail, name='detail'),
    path('author/<int:author_id>', blog, name='author'),
    path('category/<str:category_name>', blog, name='category'),
    path('tag/<str:tag_name>', blog, name='tag'),
    path('search', blog_search, name='search'),
]
