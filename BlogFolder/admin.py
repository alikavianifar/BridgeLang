"""
Admin configuration for the BlogFolder application.

Customizes the admin interface for Post, Category, and Comment models
with Summernote editor integration, permission controls, and
optimized list views.
"""

from django.contrib import admin
from django.contrib.auth.models import User
from django.http import HttpRequest
from django_summernote.admin import SummernoteModelAdmin

from BlogFolder.models import Post, Category, Comment


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    """
    Admin configuration for blog posts.

    Features:
        - Summernote rich text editor for content
        - Author auto-assignment for non-superusers
        - Edit/delete permissions scoped to post author
        - View count is read-only for non-superusers
    """

    date_hierarchy = 'created_date'
    empty_value_display = '-empty-'
    list_display = (
        'title', 'author_full_name', 'view_count',
        'status', 'login_required', 'published_date',
    )
    list_filter = ('status', 'published_date')
    search_fields = ('title', 'content')
    summernote_fields = ('content',)

    def formfield_for_foreignkey(self, db_field, request: HttpRequest, **kwargs):
        """Restrict author choices: superusers see all, others see only themselves."""
        if db_field.name == "author":
            if request.user.is_superuser:
                kwargs['queryset'] = User.objects.all()
            else:
                kwargs['queryset'] = User.objects.filter(pk=request.user.pk)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request: HttpRequest, obj: Post, form, change: bool) -> None:
        """Auto-assign the current user as author for non-superusers."""
        if not request.user.is_superuser:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def has_delete_permission(self, request: HttpRequest, obj: Post = None) -> bool:
        """Only allow deletion by the post author or superusers."""
        if obj is not None:
            return obj.author == request.user or request.user.is_superuser
        return super().has_delete_permission(request, obj)

    def has_change_permission(self, request: HttpRequest, obj: Post = None) -> bool:
        """Only allow editing by the post author or superusers."""
        if obj is not None:
            return obj.author == request.user or request.user.is_superuser
        return super().has_change_permission(request, obj)

    def formfield_for_dbfield(self, db_field, request: HttpRequest, **kwargs):
        """Make view_count read-only for non-superusers."""
        if db_field.name == "view_count":
            if not request.user.is_superuser:
                kwargs['disabled'] = True
        return super().formfield_for_dbfield(db_field, request, **kwargs)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for blog categories."""

    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin configuration for blog comments with approval workflow."""

    date_hierarchy = 'created_date'
    empty_value_display = '-empty-'
    list_display = ('name', 'post', 'approved', 'created_date')
    list_filter = ('post', 'approved')
    search_fields = ('name', 'message')
