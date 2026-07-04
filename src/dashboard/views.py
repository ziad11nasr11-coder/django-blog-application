from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from posts.models import Post

@login_required
def dashboard_home(request):
    user_posts = Post.objects.filter(author=request.user)

    context = {
        'posts': user_posts,
        'posts_count': user_posts.count(),
    }
    return render(request, 'dashboard/dashboard.html', context)
