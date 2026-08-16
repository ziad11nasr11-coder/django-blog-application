from django.core.cache import cache
from django.db.models import Count

from posts.models import Post
from posts.models import Category


SIDEBAR_CACHE_TIMEOUT = 60 * 5


def sidebar_data(request):
    trending_posts = cache.get("sidebar_trending_posts")

    if trending_posts is None:
        trending_posts = list(
            Post.objects.published()
            .select_related("author", "category")
            .order_by("-likes")[:5]
        )

        cache.set(
            "sidebar_trending_posts",
            trending_posts,
            SIDEBAR_CACHE_TIMEOUT,
        )

    categories = cache.get("sidebar_categories")

    if categories is None:
        categories = list(
            Category.objects.filter(is_active=True)
            .annotate(posts_count=Count("posts"))
            .order_by("name")
        )

        cache.set(
            "sidebar_categories",
            categories,
            SIDEBAR_CACHE_TIMEOUT,
        )

    return {
        "trending_posts": trending_posts,
        "categories": categories,
    }