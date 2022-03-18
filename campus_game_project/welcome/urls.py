from django.urls import path

from . import views

app_name = 'welcome'
urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
]
