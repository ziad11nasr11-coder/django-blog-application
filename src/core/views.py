from django.shortcuts import render
from posts.model import Post

def home(request):
    posts = Post.objects.published().order_by("-publish")[:10]

    most_viewed = (
        Post.objects.published()
        .order_by("-views")[:5]
    )

    trending_posts = (
        Post.objects.published()
        .order_by("-likes")[:5]
    )

    return render(
        request,
        "home.html",
        {
            "posts": posts,
            "most_viewed": most_viewed,
            "trending_posts": trending_posts,
        },
    )
