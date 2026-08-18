from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from taggit.models import Tag

from posts.models import Category, Post


User = get_user_model()


class PostListViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testauthor",
            password="StrongPassword123!",
        )

        self.technology = Category.objects.create(
            name="Technology",
            slug="technology",
            is_active=True,
        )

        self.science = Category.objects.create(
            name="Science",
            slug="science",
            is_active=True,
        )

        self.published_post = Post.objects.create(
            title="Published Post",
            slug="published-post",
            content="Published content",
            author=self.user,
            category=self.technology,
            status=Post.Status.PUBLISHED,
        )

        self.draft_post = Post.objects.create(
            title="Draft Post",
            slug="draft-post",
            content="Draft content",
            author=self.user,
            category=self.technology,
            status=Post.Status.DRAFT,
        )

    def test_post_list_returns_200(self):
        response = self.client.get(
            reverse("home")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_post_list_contains_only_published_posts(self):
        response = self.client.get(
            reverse("home")
        )

        posts = response.context["posts"]

        self.assertIn(
            self.published_post,
            posts,
        )

        self.assertNotIn(
            self.draft_post,
            posts,
        )

    def test_category_filter_returns_matching_posts(self):
        response = self.client.get(
            reverse(
                "post_list_by_category",
                args=["technology"],
            )
        )

        posts = response.context["posts"]

        self.assertIn(
            self.published_post,
            posts,
        )

    def test_inactive_category_returns_404(self):
        self.technology.is_active = False
        self.technology.save()

        response = self.client.get(
            reverse(
                "post_list_by_category",
                args=["technology"],
            )
        )

        self.assertEqual(
            response.status_code,
            404,
        )

    def test_tag_filter_returns_matching_posts(self):
        tag = Tag.objects.create(
            name="Django",
            slug="django",
        )

        self.published_post.tags.add(tag)

        response = self.client.get(
            reverse(
                "post_list_by_tag",
                args=["django"],
            )
        )

        posts = response.context["posts"]

        self.assertIn(
            self.published_post,
            posts,
        )

    def test_nonexistent_tag_returns_404(self):
        response = self.client.get(
            reverse(
                "post_list_by_tag",
                args=["does-not-exist"],
            )
        )

        self.assertEqual(
            response.status_code,
            404,
        )

    def test_pagination_returns_ten_posts_per_page(self):
        for index in range(11):
            Post.objects.create(
                title=f"Post {index}",
                slug=f"post-{index}",
                content="Test content",
                author=self.user,
                category=self.technology,
                status=Post.Status.PUBLISHED,
            )

        response = self.client.get(
            reverse("home")
        )

        posts = response.context["posts"]

        self.assertEqual(
            len(posts.object_list),
            10,
        )