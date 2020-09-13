"""App logic."""

from .models import User, Post


def get_following_posts(user):
    """Return posts of users that the current user is subscribed to."""

    f_users = User.objects.filter(followers__follower=user)
    f_posts = Post.objects.filter(author__in=f_users)

    return f_posts
