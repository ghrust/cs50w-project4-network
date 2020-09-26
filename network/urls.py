
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('new_post', views.new_post, name='new_post'),
    path('profile/<str:username>', views.profile_page, name='profile_page'),
    path('follow/<str:target_name>', views.follow_view, name='follow_view'),
    path('unfollow/<str:target_name>', views.unfollow_view, name='unfollow_view'),
    path('following_posts', views.following_posts_view, name='following_posts'),
    path('edit_post', views.edit_post_view, name='edit_post'),
]
