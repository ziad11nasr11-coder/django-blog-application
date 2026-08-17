from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from comments.models import Comment
from posts.models import Category, Post

from unittest.mock import patch

User = get_user_model()


class PostCommentViewTest(TestCase):
    
    def setUp(self):
        self.captcha_patcher = patch(
            "comments.forms.ReCaptchaField.validate",
            return_value=None,
        )
        self.captcha_patcher.start()
        self.addCleanup(self.captcha_patcher.stop)

        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
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
            status=Post.Status.PUBLISHED,
        )

        self.url = reverse(
            "post_comment",
            args=[self.post.id],
        )

    def test_get_request_displays_post_page(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["post"],
            self.post,
        )

    def test_unpublished_post_returns_404(self):
        self.post.status = Post.Status.DRAFT
        self.post.save()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    def test_authenticated_user_can_submit_comment(self):
        self.client.login(
            username="testuser",
            password="StrongPassword123!",
        )

        response = self.client.post(
            self.url,
            {
                "content": "Great article!",
            },
        )

        self.assertEqual(response.status_code, 302)

        comment = Comment.objects.get(
            post=self.post,
        )

        self.assertEqual(
            comment.author,
            self.user,
        )

        self.assertEqual(
            comment.name,
            self.user.username,
        )

        self.assertEqual(
            comment.email,
            self.user.email,
        )

        self.assertEqual(
            comment.content,
            "Great article!",
        )

        self.assertEqual(
            comment.status,
            Comment.Status.PENDING,
        )

    def test_anonymous_user_can_submit_comment(self):
        response = self.client.post(
            self.url,
            {
                "name": "Guest",
                "email": "guest@example.com",
                "content": "Nice article!",
            },
        )

        self.assertEqual(response.status_code, 302)

        comment = Comment.objects.get(
            post=self.post,
        )

        self.assertIsNone(comment.author)
        self.assertEqual(comment.name, "Guest")
        self.assertEqual(
            comment.email,
            "guest@example.com",
        )

    def test_invalid_comment_is_not_created(self):
        self.client.login(
            username="testuser",
            password="StrongPassword123!",
        )

        response = self.client.post(
            self.url,
            {
                "content": "   ",
                "captcha": "",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            Comment.objects.count(),
            0,
        )

    def test_comment_ip_address_is_saved(self):
        self.client.login(
            username="testuser",
            password="StrongPassword123!",
        )

        self.client.post(
            self.url,
            {
                "content": "Testing IP address.",
                "captcha": "",
            },
        )

        comment = Comment.objects.get(
            post=self.post,
        )

        self.assertIsNotNone(
            comment.ip_address,
        )

    def test_comment_rate_limit(self):
        self.client.login(
            username="testuser",
            password="StrongPassword123!",
        )

        old_time = timezone.now() - timedelta(
            minutes=5
        )

        for index in range(5):
            Comment.objects.create(
                post=self.post,
                author=self.user,
                name=self.user.username,
                email=self.user.email,
                content=f"Existing comment {index}",
                ip_address="127.0.0.1",
                created_at=old_time,
            )

        response = self.client.post(
            self.url,
            {
                "content": "Sixth comment",
                "captcha": "",
            },
            REMOTE_ADDR="127.0.0.1",
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertEqual(
            Comment.objects.count(),
            5,
        )