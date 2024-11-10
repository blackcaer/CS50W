
from django.urls import path

from . import views

urlpatterns = [
    path("", views.show_posts, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.show_posts, name="following"),

    path("profile/<int:id>", views.show_profile, name="show_profile"),

    # API routes
    path("add_post", views.add_post, name="add_post"),
    path("get_posts", views.get_posts, name="get_posts"),   

    path("profile/<int:id>/is_followed", views.is_followed, name="is_followed"),
    path("profile/<int:id>/toggle_follow",
         views.toggle_follow, name="toggle_follow"),

]
