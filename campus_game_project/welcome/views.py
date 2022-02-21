# from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def welcome(request):
    print(request)
    return HttpResponse("<h1>WELCOME</h1>")
