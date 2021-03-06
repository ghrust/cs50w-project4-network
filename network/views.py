import logging
import json

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.list import ListView
from django.core.paginator import Paginator

from .models import User, Post

from .forms import NewPostForm

from .services import get_following_posts, edit_post, toggle_like, count_likes


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S'
)


class AllPostsView(ListView):
    """Index page view."""

    template_name = 'network/index.html'
    context_object_name = 'posts'
    model = Post
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = NewPostForm()
        return context


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
    page_obj = Paginator(posts, 10)
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
        'page_obj': page_obj,
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

    if request.user.is_authenticated:
        f_posts = get_following_posts(request.user)

        context = {
            'f_posts': f_posts,
        }
        return render(request, 'network/following_posts.html', context)

    return redirect('index')


def edit_post_view(request):
    """Edit post view.

    Args:
        request (HttpRequest)

    Returns:
        HttpResponse
    """
    if request.method == 'POST':
        body: dict = json.loads(request.body)  # Convert from byte to dict
        post_id: int = body['post_id']
        edited_text: str = body['edited_text']

        edit_post(post_id=post_id, text=edited_text)
        return HttpResponse('Post edited.')

    return redirect('index')


def like_view(request):
    """Like view.

    Args:
        request (HttpRequest);
        data (json): Data from ajax request. Author of like, and liked post.
    """

    if request.method == 'POST':
        body = json.loads(request.body)  # Convert from byte to dict
        like_author = body['like_author']  # Author's username
        liked_post = body['liked_post']  # Post id

        toggle_like(like_author, liked_post)

        return HttpResponse(json.dumps(
            {'likes': count_likes(liked_post)}
        ))

    return redirect('index')
