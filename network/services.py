"""App logic."""

from .models import User, Post, Like


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


def create_like(like_author, liked_post):
    """Create like.

    Args:
        like_author (string): Username who likes post.
        liked_post (int): Id of post, which is liked.

    Returns:
        Like: Return Like model object.
    """
    user = User.objects.get(username=like_author)
    post = Post.objects.get(pk=liked_post)

    return Like.objects.create(like_author=user, liked_post=post)
