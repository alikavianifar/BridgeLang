"""
Tests for the LessonsFolder application.

Covers models, views, and URL routing for courses, lessons,
and user progress tracking.
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from LessonsFolder.models import Course, Lesson, UserProgress


class CourseModelTest(TestCase):
    """Tests for the Course model."""

    def setUp(self) -> None:
        """Create a test course."""
        self.course = Course.objects.create(
            title="English Basics",
            description="Learn the fundamentals of English.",
            level="beginner",
        )

    def test_course_creation(self) -> None:
        """Test that a Course is created correctly."""
        self.assertEqual(self.course.title, "English Basics")
        self.assertEqual(self.course.level, "beginner")
        self.assertTrue(self.course.is_active)

    def test_course_str(self) -> None:
        """Test the string representation of Course."""
        self.assertEqual(str(self.course), "English Basics")

    def test_course_lesson_count(self) -> None:
        """Test the lesson_count method."""
        Lesson.objects.create(
            course=self.course, title="Lesson 1",
            content="Content", order=1,
        )
        Lesson.objects.create(
            course=self.course, title="Lesson 2",
            content="Content", order=2,
        )
        self.assertEqual(self.course.lesson_count(), 2)

    def test_course_absolute_url(self) -> None:
        """Test get_absolute_url returns correct URL."""
        expected = reverse('Lessons:course_detail', kwargs={'pk': self.course.pk})
        self.assertEqual(self.course.get_absolute_url(), expected)


class LessonModelTest(TestCase):
    """Tests for the Lesson model."""

    def setUp(self) -> None:
        """Create test course and lesson."""
        self.course = Course.objects.create(
            title="Test Course", description="Desc", level="beginner",
        )
        self.lesson = Lesson.objects.create(
            course=self.course,
            title="First Lesson",
            content="Lesson content here.",
            order=1,
            duration_minutes=15,
        )

    def test_lesson_creation(self) -> None:
        """Test that a Lesson is created correctly."""
        self.assertEqual(self.lesson.title, "First Lesson")
        self.assertEqual(self.lesson.duration_minutes, 15)

    def test_lesson_str(self) -> None:
        """Test the string representation of Lesson."""
        self.assertIn("First Lesson", str(self.lesson))
        self.assertIn("Test Course", str(self.lesson))

    def test_lesson_ordering(self) -> None:
        """Test that lessons are ordered by the 'order' field."""
        lesson2 = Lesson.objects.create(
            course=self.course, title="Second Lesson",
            content="Content", order=2,
        )
        lessons = list(self.course.lessons.all())
        self.assertEqual(lessons[0], self.lesson)
        self.assertEqual(lessons[1], lesson2)


class UserProgressModelTest(TestCase):
    """Tests for the UserProgress model."""

    def setUp(self) -> None:
        """Create test user, course, and lesson."""
        self.user = User.objects.create_user(
            username='student', password='pass123'
        )
        self.course = Course.objects.create(
            title="Course", description="Desc", level="beginner",
        )
        self.lesson = Lesson.objects.create(
            course=self.course, title="Lesson",
            content="Content", order=1,
        )

    def test_progress_creation(self) -> None:
        """Test that UserProgress is created correctly."""
        progress = UserProgress.objects.create(
            user=self.user, lesson=self.lesson,
        )
        self.assertFalse(progress.completed)

    def test_progress_unique_together(self) -> None:
        """Test that duplicate user-lesson progress is prevented."""
        UserProgress.objects.create(user=self.user, lesson=self.lesson)
        with self.assertRaises(Exception):
            UserProgress.objects.create(user=self.user, lesson=self.lesson)

    def test_progress_str(self) -> None:
        """Test the string representation of UserProgress."""
        progress = UserProgress.objects.create(
            user=self.user, lesson=self.lesson, completed=True,
        )
        self.assertIn("✓", str(progress))


class LessonsViewTest(TestCase):
    """Tests for Lessons views."""

    def setUp(self) -> None:
        """Create test user and course data."""
        self.user = User.objects.create_user(
            username='student', password='pass123'
        )
        self.course = Course.objects.create(
            title="English 101",
            description="Basic English course.",
            level="beginner",
        )
        self.lesson = Lesson.objects.create(
            course=self.course, title="Greetings",
            content="Learn basic greetings.", order=1,
        )
        self.client.login(username='student', password='pass123')

    def test_lessons_list_requires_login(self) -> None:
        """Test that lessons list requires authentication."""
        self.client.logout()
        response = self.client.get(reverse('Lessons:lessons'))
        self.assertEqual(response.status_code, 302)

    def test_lessons_list_authenticated(self) -> None:
        """Test that authenticated users can access the lessons list."""
        response = self.client.get(reverse('Lessons:lessons'))
        self.assertEqual(response.status_code, 200)

    def test_course_detail_page(self) -> None:
        """Test the course detail page."""
        response = self.client.get(
            reverse('Lessons:course_detail', kwargs={'pk': self.course.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "English 101")

    def test_lesson_detail_page(self) -> None:
        """Test the lesson detail page."""
        response = self.client.get(
            reverse('Lessons:lesson_detail', kwargs={'pk': self.lesson.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Greetings")

    def test_mark_lesson_complete(self) -> None:
        """Test marking a lesson as complete."""
        response = self.client.post(
            reverse('Lessons:mark_complete', kwargs={'pk': self.lesson.pk})
        )
        self.assertEqual(response.status_code, 302)
        progress = UserProgress.objects.get(
            user=self.user, lesson=self.lesson
        )
        self.assertTrue(progress.completed)

    def test_mark_complete_get_not_allowed(self) -> None:
        """Test that GET requests to mark_complete redirect without action."""
        response = self.client.get(
            reverse('Lessons:mark_complete', kwargs={'pk': self.lesson.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            UserProgress.objects.filter(
                user=self.user, lesson=self.lesson, completed=True
            ).exists()
        )


class LessonsURLTest(TestCase):
    """Tests for LessonsFolder URL routing."""

    def test_lessons_list_url(self) -> None:
        """Test that the lessons list URL resolves correctly."""
        self.assertEqual(reverse('Lessons:lessons'), '/Lessons/')

    def test_course_detail_url(self) -> None:
        """Test that the course detail URL resolves correctly."""
        url = reverse('Lessons:course_detail', kwargs={'pk': 1})
        self.assertEqual(url, '/Lessons/course/1/')
