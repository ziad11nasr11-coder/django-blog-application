from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse

from .models import Post


class LatestPostsFeed(Feed):
    title = "My Blog"
    description = "Latest published posts from the blog"

    def link(self):
        return reverse("blog:post_list")

    def items(self):
        return (
            Post.objects.published()
            .select_related("author")
            .order_by("-publish")[:10]
        )

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords_html(item.body, 40)

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.publish

    def item_author_name(self, item):
        return item.author.get_full_name() or item.author.username

    def item_guid(self, item):
        return str(item.id)
