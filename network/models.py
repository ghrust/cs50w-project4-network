from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    def follow(self, target_user):
        """Follow to another user. Add entry to UserFollowing table."""
        UserFollowing.objects.create(follower=self, following=target_user)

    def unfollow(self, target_user):
        """Unfollow from another user. Delete entry from UserFollowing table."""
        UserFollowing.objects.get(follower=self, following=target_user).delete()


class Post(models.Model):
    content = models.CharField(max_length=500)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.content


class UserFollowing(models.Model):
    """Model for following user to another user."""

    follower = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE
    )

    following = models.ForeignKey(
        User,
        related_name='followers',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f'{self.follower} follows {self.following}'


class Like(models.Model):
    """Model for likes.
    like_author (User): Who likes post;
    liked_post (Post): Post which user likes
    """

    like_author = models.ForeignKey(
        User,
        related_name='likes',
        on_delete=models.CASCADE,
    )

    liked_post = models.ForeignKey(
        Post,
        related_name='likes',
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ('like_author', 'liked_post')

    def __str__(self):
        return f'{self.like_author} likes {self.liked_post}.'
