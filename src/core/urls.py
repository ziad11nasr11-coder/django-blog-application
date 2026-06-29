from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("write_for_us/", views.write_for_us, name="write_for_us"),
    path("our_writers/", views.our_writers, name="our_writers"),
    path("privacy/", views.privacy, name="privacy"),
    path("terms/", views.terms, name="terms"),
    path("cookies", views.cookies, name="cookies"),
]
