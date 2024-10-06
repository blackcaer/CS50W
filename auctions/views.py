from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.handlers.wsgi import WSGIRequest

from .models import User, AuctionListing
from .forms import AuctionListingCreateFrom, AuctionListing


def index(request: WSGIRequest):
    auctions = AuctionListing.objects.filter(is_active=True)

    return render(request, "auctions/index.html", {'auctions': auctions})


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


def show_auction(request, auction_pk):
    auction = AuctionListing.objects.get(pk=auction_pk)
    print(auction)
    return render(request, "auctions/auction_details.html", {'auction': auction})

