"""
Models for the LessonsFolder application.

Defines database models for language courses, individual lessons,
and tracking user progress through lesson completion.
"""

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Course(models.Model):
    """
    A language learning course containing multiple lessons.

    Fields:
        title: The course name (e.g., "English for Beginners").
        description: A detailed description of the course content.
        level: Difficulty level (beginner, intermediate, advanced).
        image: Optional cover image for the course.
        is_active: Whether the course is currently available.
        created_date: Auto-set when the course is created.
        updated_date: Auto-set on every save.
    """

    LEVEL_CHOICES: list[tuple[str, str]] = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    title: str = models.CharField(max_length=255)
    description: str = models.TextField()
    level: str = models.CharField(
        max_length=20, choices=LEVEL_CHOICES, default='beginner'
    )
    image = models.ImageField(
        upload_to='lessons/courses/', blank=True, null=True
    )
    is_active: bool = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_date']
        verbose_name_plural = 'courses'

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        """Return the canonical URL for this course."""
        return reverse('Lessons:course_detail', kwargs={'pk': self.pk})

    def lesson_count(self) -> int:
        """Return the number of lessons in this course."""
        return self.lessons.count()


class Lesson(models.Model):
    """
    An individual lesson within a course.

    Fields:
        course: The parent course this lesson belongs to.
        title: The lesson title.
        content: Full lesson content (HTML supported).
        order: Display order within the course.
        duration_minutes: Estimated time to complete in minutes.
        is_free: Whether this lesson is accessible without login.
        created_date: Auto-set when the lesson is created.
        updated_date: Auto-set on every save.
    """

    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='lessons'
    )
    title: str = models.CharField(max_length=255)
    content: str = models.TextField()
    order: int = models.PositiveIntegerField(default=0)
    duration_minutes: int = models.PositiveIntegerField(default=10)
    is_free: bool = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self) -> str:
        return f"{self.course.title} — {self.title}"

    def get_absolute_url(self) -> str:
        """Return the canonical URL for this lesson."""
        return reverse('Lessons:lesson_detail', kwargs={'pk': self.pk})


class UserProgress(models.Model):
    """
    Tracks a user's completion status for individual lessons.

    Fields:
        user: The user whose progress is being tracked.
        lesson: The lesson that was completed.
        completed: Whether the user has finished the lesson.
        completed_date: When the lesson was marked as completed.
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='lesson_progress'
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name='user_progress'
    )
    completed: bool = models.BooleanField(default=False)
    completed_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'lesson')
        verbose_name_plural = 'user progress'

    def __str__(self) -> str:
        status = "✓" if self.completed else "✗"
        return f"{self.user.username} — {self.lesson.title} [{status}]"
