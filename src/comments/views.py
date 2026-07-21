from django.shortcuts import render
from .utils import get_client_ip
from posts.models import Post
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from comments.forms import CommentForm
from django.db.models import Count

def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.ip_address = get_client_ip(request)
            comment.save()
        return redirect(post.get_absolute_url())
    else:
        form = CommentForm()
    
    comments = post.comments.approved()
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = (
        Post.objects.published()
        .filter(tags__in=post_tags_ids)
        .exclude(id=post.id)
        .annotate(same_tags=Count('tags'))
        .order_by('-same_tags', '-published_at')[:4]
    )
    return render(request, 'post/detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'similar_posts': similar_posts,     
    })
