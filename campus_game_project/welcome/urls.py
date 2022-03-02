from django.urls import path

from . import views

app_name = 'welcome'
urlpatterns = [
    path('', views.welcome, name='welcome'),
    #path('signin', views.sign_in, name='signin'),
    #path('signout', views.sign_out, name='signout'),
    #path('callback', views.callback, name='callback'),
]
