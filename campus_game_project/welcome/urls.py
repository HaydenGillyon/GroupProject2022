from django.urls import path

from . import views

app_name = 'welcome'
urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('signin/', views.welcome, name='signin'),
    path('signup/', views.welcome, name='signup'),
]
