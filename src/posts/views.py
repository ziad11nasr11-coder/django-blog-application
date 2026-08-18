from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from comments.forms import CommentForm

from .forms import EmailPostForm
from .models import Category, Post

try:
    from taggit.models import Tag
except ImportError:
    Tag = None


def post_list(request, tag_slug=None, category_slug=None):
    posts = (Post.objects.published().select_related("author", "category").order_by("-published_at"))
    tag = None
    category = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug, is_active=True)
        posts = posts.filter(category=category)

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'post/list.html', {
        'posts': page_obj,
        'tag': tag,
        'category': category,
    })


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(
        Post,
        slug=slug,
        status=Post.Status.PUBLISHED,
        published_at__year=year,
        published_at__month=month,
        published_at__day=day,
    )

    comments_list = post.comments.approved()

    paginator = Paginator(comments_list, 10)
    page_number = request.GET.get("comments_page")
    comments = paginator.get_page(page_number)

    post_tags_ids = post.tags.values_list("id", flat=True)

    similar_posts = (
        Post.objects.published()
        .filter(tags__in=post_tags_ids)
        .exclude(id=post.id)
        .annotate(same_tags=Count("tags"))
        .order_by("-same_tags", "-published_at")[:4]
    )

    form = CommentForm(user=request.user)

    return render(
        request,
        "post/detail.html",
        {
            "post": post,
            "comments": comments,
            "form": form,
            "similar_posts": similar_posts,
        },
    )

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())

            subject = f"{cd['name']} recommends you read {post.title}"
            message = (
                f"Read '{post.title}' at {post_url}\n\n"
                f"{cd['name']}'s comments:\n"
                f"{cd['comments']}"
            )

            send_mail(subject, message, None, [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'post/share.html', {
        'post': post,
        'form': form,
        'sent': sent,
    })


def category_posts(request, slug=None, category_slug=None):
    category_slug_val = slug or category_slug

    category = get_object_or_404(
        Category,
        slug=category_slug_val,
        is_active=True,
    )

    posts_qs = (
        Post.objects
        .published()
        .filter(category=category)
        .order_by("-published_at")
    )

    total_count = posts_qs.count()

    paginator = Paginator(posts_qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    trending_posts = (
        Post.objects
        .published()
        .order_by("-likes")[:5]
    )

    categories = Category.objects.all()

    return render(
        request,
        "post/category_posts.html",
        {
            "category": category,
            "posts": page_obj,
            "total_count": total_count,
            "trending_posts": trending_posts,
            "categories": categories,
        },
    )
def search_posts(request):
    query = request.GET.get("q", "").strip()

    posts = (
        Post.objects.published()
        .select_related(
            "author",
            "category",
        )
    )

    if query:
        posts = (
            posts.filter(
                Q(title__icontains=query)
                | Q(content__icontains=query)
                | Q(tags__name__icontains=query)
            )
            .distinct()
        )

    paginator = Paginator(posts, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "post/search.html",
        {
            "query": query,
            "posts": page_obj,
            "results_count": paginator.count,
        },
    )