"""App logic."""

from .models import User, Post


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
