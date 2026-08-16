from django.db.models import Count

from posts.models import Post
from posts.models import Category


def sidebar_data(request):
    trending_posts = (
        Post.objects.published()
        .select_related("author", "category")
        .order_by("-likes")[:5]
    )

    categories = (
        Category.objects.filter(is_active=True)
        .annotate(posts_count=Count("posts"))
        .order_by("name")
    )

    return {
        "trending_posts": trending_posts,
        "categories": categories,
    }