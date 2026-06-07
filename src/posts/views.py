from django.shortcuts import render
from .modles import Post

def post_list(request):
    posts = Post.PUBLISHED.all()
    #return render (request, 'home.html', {'posts' = posts }

def post_detail(request, year, month, day, slug):
    post = get_object_or_404(
        Post,
        slug=slug,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    #return render(  request,"blog/post_detail.html",{"post": post}, )

