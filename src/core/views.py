from django.shortcuts import render
from posts.models import Post, Category
from users.models import Author

def index(request):
    posts = Post.objects.published().order_by("-published_at")[:10]
    categories = Category.objects.all()

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
        "index.html",
        {
            "posts": posts,
            "most_viewed": most_viewed,
            "trending_posts": trending_posts,
            "categories": categories,
        },
    )

def about(request):
    authors = Author.objects.all()
    categories = Category.objects.all()
    return render(
        request,
        "about.html",
        {
            "authors": authors,
            "categories": categories,
        },
    )
