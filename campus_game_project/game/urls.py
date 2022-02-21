from django.urls import path

from . import views

app_name = 'game'
urlpatterns = [
    path('create/', views.create, name='create'),
    path('join/', views.join, name='join'),
    path('<int:lobby_id>/', views.in_lobby, name='lobby'),
]