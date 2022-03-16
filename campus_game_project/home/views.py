from django.shortcuts import redirect, render
from django.http import HttpResponse
from welcome.models import User
from django.contrib import messages
from django.db.models import Q


def home(request):
    if request.session.has_key('login'):
        if request.session.has_key('error'):
            messages.error(request, 'Invalid password!')
            del request.session['error']    
        user = request.session['user']
        user_det = User.objects.get(email=user)
        context = {
            'user': user_det.name,
            'email': user_det.email,
            'id': user_det.id,   
        }   
        return render(request,'home/landingPage.html',context)
    else:   
        if request.session.has_key('logerror'):
            messages.error(request, 'Invalid credentials!')
            del request.session['logerror'] 
        elif request.session.has_key('blockerror'):  
            messages.error(request, 'user blocked!')
            del request.session['blockerror'] 
    return redirect("/signin")

def leaderboard(request):
    if request.session.has_key('login'):
        if request.session.has_key('error'):
            messages.error(request, 'Invalid password!')
            del request.session['error']    
        user = request.session['user']
        user_det = User.objects.get(email=user)
        context = {
            'user': user_det.name,
            'email': user_det.email,
            'id': user_det.id,   
        }   
        return render(request,"home/leaderboard.html",context)
    else:   
        if request.session.has_key('logerror'):
            messages.error(request, 'Invalid credentials!')
            del request.session['logerror'] 
        elif request.session.has_key('blockerror'):  
            messages.error(request, 'user blocked!')
            del request.session['blockerror']     
    return redirect("/signin")


def shop(request):
    if request.session.has_key('login'):
        if request.session.has_key('error'):
            messages.error(request, 'Invalid password!')
            del request.session['error']    
        user = request.session['user']
        user_det = User.objects.get(email=user)
        context = {
            'user': user_det.name,
            'email': user_det.email,
            'id': user_det.id,   
        }   
        return render(request,"home/shop.html",context)
    else:   
        if request.session.has_key('logerror'):
            messages.error(request, 'Invalid credentials!')
            del request.session['logerror'] 
        elif request.session.has_key('blockerror'):  
            messages.error(request, 'user blocked!')
            del request.session['blockerror']     
    return redirect("/signin")

def  profile(request):
    if request.session.has_key('login'):
        if request.session.has_key('error'):
            messages.error(request, 'Invalid password!')
            del request.session['error']    
        user = request.session['user']
        user_det = User.objects.get(email=user)
        context = {
            'user': user_det.name,
            'email': user_det.email,
            'id': user_det.id,   
        }   
        return render(request,"home/profile.html",context)
    else:   
        if request.session.has_key('logerror'):
            messages.error(request, 'Invalid credentials!')
            del request.session['logerror'] 
        elif request.session.has_key('blockerror'):  
            messages.error(request, 'user blocked!')
            del request.session['blockerror']     
    return redirect("/signin")


def logout(request):
    request.session.flush()
    return redirect("/")