from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json

from .models import User, Post

POSTS_PER_PAGE = 10


def show_posts(request):
    if request.path == '/following' and not request.user.is_authenticated:
        return redirect('index')
    return render(request, "network/show_posts.html")


def add_post(request):
    if request.method == 'POST' and request.user.is_authenticated:
        data = json.loads(request.body)
        new_post = Post(author=request.user, content=data['content'])
        print("POOOST", new_post)
        new_post.save()

        return JsonResponse(new_post.serialize())

    return JsonResponse({'error': 'Invalid request'}, status=400)


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def create_post(request):
    if request.method == 'POST':
        new_post = Post(author=request.user,
                        content=request.POST['content'])
        new_post.save()
        return redirect('index')
    else:
        return render(request, 'network/create_post.html')


def show_profile(request, id):
    profile = User.objects.get(id=id)
    return render(request, 'network/profile.html', {'profile': profile})


def get_posts(request):
    user_id = request.GET.get('user_id')
    followed = request.GET.get('followed')
    page_num = request.GET.get('page') or 1

    if followed == 'true' and request.user.is_authenticated:
        followed_users = request.user.following.all()
        posts = Post.objects.filter(
            author__in=followed_users).order_by('-date_created')
    elif user_id:
        posts = User.objects.get(
            id=user_id).posts.all().order_by('-date_created')
    else:
        posts = Post.objects.all().order_by('-date_created')

    paginator = Paginator(posts, POSTS_PER_PAGE)
    posts = paginator.get_page(page_num)
    return JsonResponse({'posts':[post.serialize() for post in posts],'page_count':paginator.num_pages})


@login_required
def is_followed(request, id):
    """Check if the logged-in user follows the user with the given ID."""
    is_followed = request.user.following.filter(id=id).exists()
    return JsonResponse({"is_followed": is_followed})


@login_required
def toggle_follow(request, id):
    """Toggle follow/unfollow for the user with the given ID."""

    if request.method == 'PUT':
        profile_user = User.objects.get(id=id)
        if profile_user.followers.filter(id=request.user.id).exists():
            # Unfollow if already following
            profile_user.followers.remove(request.user)
            is_followed = False
        else:
            # Follow if not following
            profile_user.followers.add(request.user)
            is_followed = True
        return JsonResponse({"is_followed": is_followed})
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)
    
