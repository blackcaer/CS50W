from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create_page", views.create_page, name="create_page"),
    path("random_page", views.random_page, name="random_page"),
    path("<str:content_name>", views.content, name="content"),
    path("<str:content_name>/edit_page", views.edit_page, name="edit_page"),

]
