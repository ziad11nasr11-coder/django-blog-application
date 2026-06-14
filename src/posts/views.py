from django.shortcuts import render
from .modles import Post
from django.core.paginator import Paginator
from django.core.mail import send_mail
from .forms import EMAILPOSTFORM
from .forms import CommentForm
def post_list(request):
    posts = Post.PUBLISHED.all().order_by('-id')
    paginator = Paginator(post_list,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    
    #return render (request, 'home.html', {'posts' = posts, 'tag': tag }

def post_detail(request, year, month, day, slug):
    post = get_object_or_404(
        Post,
        slug=slug,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    comments = post.comments.filter(active=True)
    form = CommentForm()

    #return render(  request,"blog/post_detail.html",{"post": post},"comments": comments, "form": form )

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    sent = False

    if request.method == "POST":
        form = EmailPostForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )

            subject = (
                f"{cd['name']} recommends you read "
                f"{post.title}"
            )

            message = (
                f"Read '{post.title}' at {post_url}\n\n"
                f"{cd['name']}'s comments:\n"
                f"{cd['comments']}"
            )

            send_mail(
                subject,
                message,
                None,
                [cd["to"]]
            )

            sent = True

    else:
        form = EmailPostForm()

    return render(
        request,
        "blog/post/share.html",
        {
            "post": post,
            "form": form,
            "sent": sent,
        },
    )


def post_comment(request, post_id):
    post = get_object_or_404(
        Post.objects.published(),
        pk=post_id
    )

    comments = post.comments.filter(active=True)

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()

            return redirect(post.get_absolute_url())
    else:
        form = CommentForm()

    return render(
        request,
        "blog/post/detail.html",
        {
            "post": post,
            "comments": comments,
            "form": form,
        },
    )
