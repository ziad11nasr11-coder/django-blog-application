from django.test import TestCase
from django.urls import reverse

from posts.models import Category, Post
from users.models import Author


class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Technology",
            slug="technology",
            description="Technology articles",
        )

    def test_category_str(self):
        self.assertEqual(
            str(self.category),
            "Technology",
        )

    def test_category_absolute_url(self):
        self.assertEqual(
            self.category.get_absolute_url(),
            reverse(
                "post_list_by_category",
                args=["technology"],
            ),
        )

    def test_category_is_active_by_default(self):
        self.assertTrue(self.category.is_active)


class PostModelTest(TestCase):

    def setUp(self):
        self.author = Author.objects.create(
            username="testauthor",
        )

        self.category = Category.objects.create(
            name="Technology",
            slug="technology",
        )

        self.post = Post.objects.create(
            title="Django Testing",
            slug="django-testing",
            content="Learning Django testing.",
            author=self.author,
            category=self.category,
        )

    def test_post_str(self):
        self.assertEqual(
            str(self.post),
            "Django Testing",
        )

    def test_post_absolute_url(self):
        self.assertEqual(
            self.post.get_absolute_url(),
            reverse(
                "post_detail",
                args=[
                    self.post.published_at.year,
                    self.post.published_at.month,
                    self.post.published_at.day,
                    self.post.slug,
                ],
            ),
        )

    def test_post_default_status_is_draft(self):
        self.assertEqual(
            self.post.status,
            Post.Status.DRAFT,
        )

    def test_post_default_views(self):
        self.assertEqual(
            self.post.views,
            0,
        )

    def test_post_default_likes(self):
        self.assertEqual(
            self.post.likes,
            0,
        )

    def test_post_default_reading_time(self):
        self.assertEqual(
            self.post.reading_time,
            0,
        )


class PostQuerySetTest(TestCase):

    def setUp(self):
        self.author = Author.objects.create(
            username="testauthor",
        )

        self.draft = Post.objects.create(
            title="Draft Post",
            slug="draft-post",
            content="Draft content",
            author=self.author,
            status=Post.Status.DRAFT,
        )

        self.published = Post.objects.create(
            title="Published Post",
            slug="published-post",
            content="Published content",
            author=self.author,
            status=Post.Status.PUBLISHED,
        )

        self.archived = Post.objects.create(
            title="Archived Post",
            slug="archived-post",
            content="Archived content",
            author=self.author,
            status=Post.Status.ARCHIVED,
        )

    def test_published_queryset(self):
        posts = Post.objects.published()

        self.assertIn(
            self.published,
            posts,
        )

        self.assertNotIn(
            self.draft,
            posts,
        )

        self.assertNotIn(
            self.archived,
            posts,
        )

    def test_drafts_queryset(self):
        posts = Post.objects.drafts()

        self.assertIn(
            self.draft,
            posts,
        )

        self.assertNotIn(
            self.published,
            posts,
        )

        self.assertNotIn(
            self.archived,
            posts,
        )

    def test_archived_queryset(self):
        posts = Post.objects.archived()

        self.assertIn(
            self.archived,
            posts,
        )

        self.assertNotIn(
            self.draft,
            posts,
        )

        self.assertNotIn(
            self.published,
            posts,
        )