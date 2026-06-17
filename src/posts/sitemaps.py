from django.contrib.sitemaps import Sitemap
from blog.models import Post

class PostSitemap(Sitemap):
    changefreq = "weekly"

    def items(self):
        return Post.objects.filter(status="published")

    def lastmod(self, obj):
        return obj.updated_at or obj.created_at

    def location(self, obj):
        return obj.get_absolute_url()

    def priority(self, obj):
        return 1.0 if getattr(obj, "featured", False) else 0.7

    def changefreq(self, obj):
        return "daily" if getattr(obj, "featured", False) else "weekly"
