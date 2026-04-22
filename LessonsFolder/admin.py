"""
Admin configuration for the LessonsFolder application.

Registers Course, Lesson, and UserProgress models with customized
admin list views for efficient content management.
"""

from django.contrib import admin

from LessonsFolder.models import Course, Lesson, UserProgress


class LessonInline(admin.TabularInline):
    """Inline editor for lessons within the course admin page."""

    model = Lesson
    extra = 1
    fields = ('title', 'order', 'duration_minutes', 'is_free')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Admin configuration for Course model with inline lessons."""

    list_display = ('title', 'level', 'lesson_count', 'is_active', 'created_date')
    list_filter = ('level', 'is_active')
    search_fields = ('title', 'description')
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Admin configuration for individual Lesson model."""

    list_display = ('title', 'course', 'order', 'duration_minutes', 'is_free')
    list_filter = ('course', 'is_free')
    search_fields = ('title', 'content')


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    """Admin configuration for tracking user lesson completion."""

    list_display = ('user', 'lesson', 'completed', 'completed_date')
    list_filter = ('completed',)
    search_fields = ('user__username', 'lesson__title')
