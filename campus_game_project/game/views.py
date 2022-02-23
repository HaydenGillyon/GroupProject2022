from django.http import HttpResponse
# from django.shortcuts import render

# Create your views here.


def create(request):
    print(request)
    return HttpResponse("<h1>CREATE LOBBY</h1>")


def join(request):
    print(request)
    return HttpResponse("<h1>JOIN LOBBY</h1>")


def in_lobby(request, lobby_id):
    print(request)
    return HttpResponse("<h1>LOBBY " + str(lobby_id) + "</h1>")
