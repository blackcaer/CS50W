
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    #path("create_post", views.create_post, name="create_post"),
    path("profile/<int:id>", views.show_profile, name="show_profile"),#del?

     # API routes
    path("get_posts", views.get_new_posts, name="get_posts"),
    path("get_posts/user/<int:id>", views.get_user_posts, name="get_user_posts"),
    
]
