from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass


class Post(models.Model):
    content = models.CharField(max_length=500)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
