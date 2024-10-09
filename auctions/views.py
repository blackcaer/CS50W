from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.handlers.wsgi import WSGIRequest

from .models import User, AuctionListing, Category, Bid
from .forms import AuctionListingCreateFrom, AuctionListing, CreateCommentForm, CreateBidForm
from .util import HiddenErrorList

from decimal import Decimal


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
    context = {'auction': auction, 'comments': comments}

    if not request.user.is_authenticated:
        return render(request, "auctions/auction_details.html", context)
    
    context['in_watchlist'] = auction in request.user.watchlist.all()

    if not auction.is_active:
        if auction.winning_bid is not None:
            context['winning_price'] = auction.winning_bid.price
            context['is_winner'] = request.user == auction.winning_bid.user

        return render(request, "auctions/auction_details.html", context)

    max_bid = auction.bids.order_by('-price').first()

    if max_bid is None:
        current_price = auction.start_bid
        min_price = auction.start_bid
    else:
        current_price = max_bid.price
        min_price = round(current_price + Decimal(0.01), 2)

    bid_form = CreateBidForm(initial={'price': min_price})
    
    bid_form.fields['price'].widget.attrs['min'] = min_price # Set minimum price in Bid form

    create_comment_form = CreateCommentForm()

    is_owner = (auction.owner == request.user)
    
    context.update({'user': request.user,
                    'create_comment_form': create_comment_form,
                    'create_bid_form': bid_form,
                    'is_owner': is_owner,
                    'current_price':current_price})
    
    watched_auctions = request.user.watchlist.all()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action in ('add_to_watchlist', 'remove_from_watchlist'):
            if auction not in watched_auctions:
                request.user.watchlist.add(auction)
            else:
                request.user.watchlist.remove(auction)
            return redirect('auction', auction_pk=auction_pk)
        
        elif action == 'add_comment':
            create_comment_form = CreateCommentForm(request.POST)
            if create_comment_form.is_valid():
                comment = create_comment_form.save(commit=False)
                comment.user = request.user
                comment.auction = auction
                comment.save()
                return redirect('auction', auction_pk=auction_pk)  
                 
        elif action == 'place_bid':
            bid_form = CreateBidForm(request.POST)
            bid_form.error_class = HiddenErrorList  # Hide default django errors

            if bid_form.is_valid():
                bid = bid_form.save(commit=False)
                if bid.price < min_price:
                    bid_form.add_error(
                        'price', f"Bid must be at least {min_price:.2f}")
                else:
                    bid.user = request.user
                    bid.auction = auction
                    bid.save()
                    return redirect('auction', auction_pk=auction_pk)
                
        elif action == 'close_auction' and is_owner:
            print("closing")
            auction.is_active=False
            if max_bid is not None:
                auction.winning_bid = max_bid
                
            auction.save()
            return redirect('auction', auction_pk=auction_pk)


    context.update({'create_comment_form': create_comment_form,
                    'create_bid_form': bid_form})

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
