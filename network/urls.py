
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('new_post', views.new_post, name='new_post'),
    path('profile/<str:username>', views.profile_page, name='profile_page'),
    path('follow/<str:following_username>', views.following_view, name='following_view')
]
