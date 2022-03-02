from django.urls import path

from . import views

app_name = 'home'
urlpatterns = [
    path('', views.home, name='home'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('shop/', views.shop, name='shop'),
    path('profile/', views.profile, name='profile'),
]
