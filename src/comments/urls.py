from django.urls import path
from . import views

urlpatterns = [
path(
        "<int:post_id>/comment/",
        views.post_comment,
        name="post_comment",
    ),
]