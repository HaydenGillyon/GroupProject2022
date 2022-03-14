from django.urls import path

from . import views

app_name = 'game'
urlpatterns = [
    path('create/', views.create, name='create'),
    path('join/', views.join, name='join'),
    path('<int:lobby_code>/', views.lobby, name='lobby'),
    path('running/<int:lobby_code>/', views.running, name='running'),
    path('end/<int:lobby_code>/', views.end, name='end'),
    path('error/', views.error, name='error')
]
