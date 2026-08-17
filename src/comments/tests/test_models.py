from django.contrib.auth import get_user_model
from django.test import TestCase

from posts.models import Category, Post

from ..models import Comment


User = get_user_model()


class CommentModelTest(TestCase):

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

    def test_comment_str(self):
        comment = Comment.objects.create(
            post=self.post,
            name="Ahmed",
            email="ahmed@example.com",
            content="Great article!",
        )

        self.assertEqual(
            str(comment),
            f"Comment by Ahmed on {self.post}",
        )

    def test_comment_default_status_is_pending(self):
        comment = Comment.objects.create(
            post=self.post,
            name="Ahmed",
            email="ahmed@example.com",
            content="Great article!",
        )

        self.assertEqual(
            comment.status,
            Comment.Status.PENDING,
        )

    def test_approved_queryset(self):
        approved = Comment.objects.create(
            post=self.post,
            name="Ahmed",
            email="ahmed@example.com",
            content="Approved comment",
            status=Comment.Status.APPROVED,
        )

        pending = Comment.objects.create(
            post=self.post,
            name="Ali",
            email="ali@example.com",
            content="Pending comment",
            status=Comment.Status.PENDING,
        )

        comments = Comment.objects.approved()

        self.assertIn(approved, comments)
        self.assertNotIn(pending, comments)

    def test_pending_queryset(self):
        pending = Comment.objects.create(
            post=self.post,
            name="Ali",
            email="ali@example.com",
            content="Pending comment",
            status=Comment.Status.PENDING,
        )

        approved = Comment.objects.create(
            post=self.post,
            name="Ahmed",
            email="ahmed@example.com",
            content="Approved comment",
            status=Comment.Status.APPROVED,
        )

        comments = Comment.objects.pending()

        self.assertIn(pending, comments)
        self.assertNotIn(approved, comments)

    def test_comment_can_belong_to_authenticated_author(self):
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            name="Ahmed",
            email="ahmed@example.com",
            content="Great article!",
        )

        self.assertEqual(
            comment.author,
            self.user,
        )

    def test_comment_can_exist_without_author(self):
        comment = Comment.objects.create(
            post=self.post,
            name="Guest",
            email="guest@example.com",
            content="Guest comment",
        )

        self.assertIsNone(comment.author)