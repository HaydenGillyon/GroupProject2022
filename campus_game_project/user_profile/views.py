# from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def profile(request):
    print(request)
    return HttpResponse("<h1>PROFILE</h1>")
