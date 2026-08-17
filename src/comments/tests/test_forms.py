from django.contrib.auth import get_user_model
from django.test import TestCase

from posts.models import Category, Post

from ..forms import CommentForm


User = get_user_model()


class CommentFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="StrongPassword123!",
        )

        self.category = Category.objects.create(
            name="Technology",
            slug="technology",
        )

        self.post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            content="Test post content.",
            author=self.user,
            category=self.category,
        )

    def test_anonymous_user_sees_name_and_email_fields(self):
        form = CommentForm()

        self.assertIn("name", form.fields)
        self.assertIn("email", form.fields)
        self.assertIn("content", form.fields)

    def test_authenticated_user_does_not_see_name_and_email_fields(self):
        form = CommentForm(user=self.user)

        self.assertNotIn("name", form.fields)
        self.assertNotIn("email", form.fields)
        self.assertIn("content", form.fields)

    def test_empty_content_is_invalid(self):
        form = CommentForm(
            data={
                "name": "Ahmed",
                "email": "ahmed@example.com",
                "content": "   ",
            }
        )

        form.fields.pop("captcha")

        self.assertFalse(form.is_valid())
        self.assertIn("content", form.errors)

    def test_valid_content_is_cleaned(self):
        form = CommentForm(
            data={
                "name": "Ahmed",
                "email": "ahmed@example.com",
                "content": "  Great article!  ",
            }
        )

        form.fields.pop("captcha")

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["content"],
            "Great article!",
        )

    def test_invalid_email_is_rejected(self):
        form = CommentForm(
            data={
                "name": "Ahmed",
                "email": "invalid-email",
                "content": "Great article!",
            }
        )

        form.fields.pop("captcha")

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)