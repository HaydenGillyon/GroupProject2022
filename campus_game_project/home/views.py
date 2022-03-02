# from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.


def home(request):
    return render(request,'home/landingPage.html')


def leaderboard(request):
    return render(request,"home/leaderboard.html")


def shop(request):
    print(request)
    return render(request,"home/shop.html")

def  profile(request):
        print(request)
        return render(request,"home/profile.html")
