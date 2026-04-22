"""
Views for the LessonsFolder application.

Provides views for browsing courses, viewing individual lessons,
and tracking user progress through lesson completion.
"""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from LessonsFolder.models import Course, Lesson, UserProgress


@login_required
def lessons_list(request: HttpRequest) -> HttpResponse:
    """
    Display all active courses with user progress.

    Shows a list of available courses. For authenticated users,
    calculates the completion percentage of each course.

    Args:
        request: The HTTP request object.

    Returns:
        Rendered lessons listing page.
    """
    courses = Course.objects.filter(is_active=True)

    # Calculate progress for each course
    courses_with_progress: list[dict] = []
    for course in courses:
        total_lessons: int = course.lessons.count()
        if total_lessons > 0:
            completed: int = UserProgress.objects.filter(
                user=request.user,
                lesson__course=course,
                completed=True,
            ).count()
            progress: int = int((completed / total_lessons) * 100)
        else:
            completed = 0
            progress = 0

        courses_with_progress.append({
            'course': course,
            'total_lessons': total_lessons,
            'completed_lessons': completed,
            'progress': progress,
        })

    context = {'courses_with_progress': courses_with_progress}
    return render(request, "lessons/lessons.html", context)


@login_required
def course_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Display course details with its lessons and user progress.

    Args:
        request: The HTTP request object.
        pk: The primary key of the course.

    Returns:
        Rendered course detail page with lesson list.
    """
    course = get_object_or_404(Course, pk=pk, is_active=True)
    lessons = course.lessons.all()

    # Get completed lesson IDs for the current user
    completed_lesson_ids: set[int] = set(
        UserProgress.objects.filter(
            user=request.user,
            lesson__course=course,
            completed=True,
        ).values_list('lesson_id', flat=True)
    )

    context = {
        'course': course,
        'lessons': lessons,
        'completed_lesson_ids': completed_lesson_ids,
    }
    return render(request, "lessons/course_detail.html", context)


@login_required
def lesson_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Display an individual lesson with its content.

    Args:
        request: The HTTP request object.
        pk: The primary key of the lesson.

    Returns:
        Rendered lesson detail page.
    """
    lesson = get_object_or_404(Lesson, pk=pk)

    # Check if user has completed this lesson
    progress, _ = UserProgress.objects.get_or_create(
        user=request.user, lesson=lesson
    )

    # Get previous and next lessons in the course
    previous_lesson = (
        Lesson.objects
        .filter(course=lesson.course, order__lt=lesson.order)
        .order_by('-order')
        .first()
    )
    next_lesson = (
        Lesson.objects
        .filter(course=lesson.course, order__gt=lesson.order)
        .order_by('order')
        .first()
    )

    context = {
        'lesson': lesson,
        'progress': progress,
        'previous_lesson': previous_lesson,
        'next_lesson': next_lesson,
    }
    return render(request, "lessons/lesson_detail.html", context)


@login_required
def mark_lesson_complete(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Mark a lesson as completed for the current user.

    Only accepts POST requests to prevent accidental completion.

    Args:
        request: The HTTP request object.
        pk: The primary key of the lesson.

    Returns:
        Redirect to the lesson detail page.
    """
    if request.method == 'POST':
        lesson = get_object_or_404(Lesson, pk=pk)
        progress, _ = UserProgress.objects.get_or_create(
            user=request.user, lesson=lesson
        )
        progress.completed = True
        progress.save()
        messages.add_message(
            request, messages.SUCCESS,
            f'Lesson "{lesson.title}" marked as complete!'
        )
    return redirect('Lessons:lesson_detail', pk=pk)