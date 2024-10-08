from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.handlers.wsgi import WSGIRequest

from .models import User, AuctionListing, Category
from .forms import AuctionListingCreateFrom, AuctionListing, CreateCommentForm


def index(request: WSGIRequest):
    auctions = AuctionListing.objects.filter(is_active=True)

    return render(request, "auctions/show_auctions.html", {'auctions': auctions, 'header': 'Active Listings'})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_auction(request):
    form = AuctionListingCreateFrom()

    if request.method == 'POST':
        form = AuctionListingCreateFrom(request.POST)

        if form.is_valid():
            auction: AuctionListing = form.save(commit=False)
            auction.owner = request.user
            auction.save()
            return HttpResponseRedirect(reverse(f'auction', args=[auction.pk]))
        else:
            pass

    return render(request, 'auctions/create_auction.html', {'form': form})


def show_auction(request: WSGIRequest, auction_pk):
    auction = AuctionListing.objects.get(pk=auction_pk)
    comments = auction.comments.all()
    context = {'auction': auction,'comments':comments}

    if not request.user.is_authenticated:
        return render(request, "auctions/auction_details.html", context)
    
    watched_auctions = request.user.watchlist.all()

    if request.method == 'POST':
        action = request.POST.get('action')
        if action in ('add_to_watchlist','remove_from_watchlist'):
            if auction not in watched_auctions:
                request.user.watchlist.add(auction)
            else:
                request.user.watchlist.remove(auction)
        elif action == 'add_comment':
            form = CreateCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.auction = auction
                comment.save()
        return redirect('auction',auction_pk=auction_pk)

    create_comment_form = CreateCommentForm()
    in_watchlist = auction in request.user.watchlist.all()
    
    context.update({'user': request.user,
                    'in_watchlist': in_watchlist,
                    'create_comment_form':create_comment_form})

    return render(request, "auctions/auction_details.html", context)


def show_watchlist(request):
    watched_auctions = request.user.watchlist.all()
    return render(request, 'auctions/show_auctions.html', {'auctions': watched_auctions, 'header': 'Watched listings'})


def show_categories(request):
    categories = Category.objects.all()
    return render(request, 'auctions/show_categories.html', {'categories': categories})


def show_category_listings(request, category_name):
    category_listings = Category.objects.get(name=category_name).auctions.all()
    return render(request, 'auctions/show_auctions.html', {'auctions': category_listings, 'header': f'Category: {category_name}'})
