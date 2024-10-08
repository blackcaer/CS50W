from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_auction", views.create_auction, name="create_auction"),
    path("auctions/<int:auction_pk>", views.show_auction, name="auction"),
    path("watchlist", views.show_watchlist, name="watchlist"),
    path("categories", views.show_categories, name="categories"),
    path("categories/<str:category_name>", views.show_category_listings, name="category_listings"),

]
