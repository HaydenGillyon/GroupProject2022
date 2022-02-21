# from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    print(request)
    return HttpResponse("<h1>HOME</h1>")


def leaderboard(request):
    print(request)
    return HttpResponse("<h1>LEADERBOARD</h1>")


def shop(request):
    print(request)
    return HttpResponse("<h1>SHOP</h1>")
