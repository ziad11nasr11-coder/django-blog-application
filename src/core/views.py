from django.shortcuts import render
from django.core.paginator import Paginator
from posts.models import Post, Category
from users.models import Author

def index(request):
    posts_qs = Post.objects.published().order_by("-published_at")
    categories = Category.objects.all()

    paginator = Paginator(posts_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

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
        "core/index.html",
        {
            "posts": page_obj,
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
        "core/about.html",
        {
            "authors": authors,
            "categories": categories,
        },
    )


def write_for_us(request):
    return render(request, "core/write_for_us.html")

def our_writers(request):
    return render(request, "core/our_writers.html")

def contact(request):
    return render(request, "core/contact.html")

def privacy(request):
    return render(request, "core/privacy.html")

def terms(request):
    return render(request, "core/terms.html")

def cookies(request):
    return render(request, "core/cookies.html")