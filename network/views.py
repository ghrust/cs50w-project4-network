import logging

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .services import get_following_posts

from .models import User, Post

from .forms import NewPostForm

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S'
)


def index(request):
    """Main page."""

    form = NewPostForm()

    # get posts from database, send to index page.
    posts = Post.objects.all()

    context = {'form': form, 'posts': posts}

    return render(request, "network/index.html", context)


def login_view(request):
    """Login page."""

    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        logging.info(f'Username: {user}.')

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
    """Logout."""

    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    """Register page."""

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


def new_post(request):
    """Create new post."""

    if request.method == 'POST':
        post = request.POST['post']

        # Save post to database.
        p = Post(content=post, author=request.user)
        p.save()

        logging.info(f'User {request.user} adds post.')

    return redirect('index')


def profile_page(request, username):
    """User profile page."""

    user = User.objects.get(username=username)
    posts = Post.objects.filter(author=user)
    followings = user.following.all()
    followers = user.followers.all()

    # Сheck if the user is a follower of the user whose profile was loaded.
    is_follower = False
    for item in followers:
        if request.user.username == item.follower.username:
            is_follower = True

    context = {
        'username': username,
        'posts': posts,
        'followings': followings,
        'followers': followers,
        'is_follower': is_follower,
    }

    return render(request, "network/profile.html", context)


def follow_view(request, target_name):
    """Follow view. User may follow to another user."""

    target_user = User.objects.get(username=target_name)

    request.user.follow(target_user)

    return redirect('index')


def unfollow_view(request, target_name):
    """Unfollow from another user."""

    target_user = User.objects.get(username=target_name)

    request.user.unfollow(target_user)

    return redirect('index')


def following_posts_view(request):
    """Page with posts of users that the current user is subscribed to."""

    f_posts = get_following_posts(request.user)

    context = {
        'f_posts': f_posts,
    }
    return render(request, 'network/following_posts.html', context)
