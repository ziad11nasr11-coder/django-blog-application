from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.db.models import Count

from .models import Post, Comment, Category
from .forms import EmailPostForm, CommentForm

try:
    from taggit.models import Tag
except ImportError:
    Tag = None


def post_list(request, tag_slug=None):
    posts = Post.objects.published().order_by('-published_at')
    tag = None
    category = None

    if tag_slug and Tag:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
   
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug, is_active=True)
        posts = posts.filter(category=category)

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/post/list.html', {
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

    comments = post.comments.filter(active=True)
    form = CommentForm()

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = (
        Post.published.filter(tags__in=post_tags_ids)
        .exclude(id=post.id)
        .annotate(same_tags=Count('tags'))
        .order_by('-same_tags', '-published_at')[:4]
    )

     if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect(post.get_absolute_url())
    return render(request, 'blog/post/detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'similar_posts': similar_posts,
    })


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

    return render(request, 'blog/post/share.html', {
        'post': post,
        'form': form,
        'sent': sent,
    })


def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
           return redirect(post.get_absolute_url())
    else:
        form = CommentForm()
    
    comments = post.comments.filter(active=True)
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = (
        Post.objects.published()
        .filter(tags__in=post_tags_ids)
        .exclude(id=post.id)
        .annotate(same_tags=Count('tags'))
        .order_by('-same_tags', '-published_at')[:4]
    )
    return render(request, 'blog/post/detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })

