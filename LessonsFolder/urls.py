"""
URL configuration for the LessonsFolder application.

Maps URL paths for course listing, course detail, lesson detail,
and lesson completion tracking.
"""

from django.urls import path

from LessonsFolder.views import (
    lessons_list,
    course_detail,
    lesson_detail,
    mark_lesson_complete,
)

app_name = 'Lessons'

urlpatterns = [
    path('', lessons_list, name='lessons'),
    path('course/<int:pk>/', course_detail, name='course_detail'),
    path('lesson/<int:pk>/', lesson_detail, name='lesson_detail'),
    path('lesson/<int:pk>/complete/', mark_lesson_complete, name='mark_complete'),
]
