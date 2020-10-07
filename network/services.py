"""App logic."""

from django.db.utils import IntegrityError
from .models import User, Post, Like
from typing import Optional


def get_following_posts(user):
    """Return posts of users that the current user is subscribed to."""

    f_users = User.objects.filter(followers__follower=user)
    f_posts = Post.objects.filter(author__in=f_users)

    return f_posts


def edit_post(post_id: int, text: str) -> None:
    """Edit post in database.

    Args:
        post_id (int): Database post id;
        text (string): New text
    """
    post: Post = Post.objects.get(pk=post_id)
    post.content = text
    post.save()


def count_likes(post_id: int) -> int:
    """Return the number of likes for this post.

    Args:
        post_id (int): post id.

    Returns:
        int: Number of likes.
    """
    post = Post.objects.get(pk=post_id)
    return post.likes.all().count()


def toggle_like(like_author: str, liked_post: int) -> Optional[Like]:
    """Create like. If post is liked, delete like.

    Args:
        like_author (string): Username who likes post.
        liked_post (int): Id of post, which is liked.

    Returns:
        Like: Return Like model object.
    """
    user = User.objects.get(username=like_author)
    post = Post.objects.get(pk=liked_post)

    try:
        return Like.objects.create(like_author=user, liked_post=post)
    except IntegrityError:
        # If like is exists, unlike.
        Like.objects.get(like_author=user, liked_post=post).delete()
