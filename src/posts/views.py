from django.shortcuts import render
from .modles import Post

def post_list(request):
    posts = Post.PUBLISHED.all()
    #return render (request, 'home.html', {'posts' = posts }
    pass

def post_detail(request, slug):
    post = ge5_object_or_404(Post, slug=slug , status = Post.status.PUBLISHED)
    #return render(requst, 'post/detail.html', {'post' = post })
    pass
