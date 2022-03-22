from http.client import ImproperConnectionState
from django.urls import path

from . import views

app_name = 'home'
urlpatterns = [
    path('', views.home, name='home'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    # path('shop/', views.shop, name='shop'), shop under progresss , relaunching to sell nfts
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
]
