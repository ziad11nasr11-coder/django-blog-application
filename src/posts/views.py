from django.shortcuts import render
from .modles import Post
from django.core.paginator import Paginator
from django.core.mail import send_mail
from .forms import EMAILPOSTFORM
def post_list(request):
    posts = Post.PUBLISHED.all().order_by('-id')
    paginator = Paginator(post_list,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
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

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = EmailPostForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
    else:
        form = EmailPostForm()

    #return render(request,"blog/post/share.html",{"post": post,"form": form},)
