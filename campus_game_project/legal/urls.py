from django.urls import path

from . import views

app_name = 'legal'
urlpatterns = [
    path('', views.legal, name='legal'),
]
