from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import User,Admin
from hashlib import sha256
from django.contrib import messages
from django.db.models import Q

def welcome(request):
    return render(request, 'welcome/welcome.html')

def signup(request):
    if request.session.has_key('login'):
        print("this")
        return redirect(welcome)
    else:    
        if request.POST:
            uname = request.POST['uname']
            email = request.POST['email']
            passw = request.POST['pass']
            hashpass = sha256(passw.encode()).hexdigest()
            user = User.objects.filter(name=uname)
            if user:
                messages.error(request, 'username already exists!')
                return render(request, 'welcome/registration.html')
            else:  
                user = User.objects.filter(email=email)
                if user:
                    messages.error(request, 'email already exists!')
                    return render(request, 'welcome/registration.html')
                else:
                    obj = User()
                    obj.name = uname
                    obj.password = hashpass
                    obj.email = email
                    obj.save()
                    request.session['login'] = 1
                    request.session['user'] = uname
                    return redirect(welcome)
        else:
            return render(request, 'welcome/signup.html')

def signin(request):
    if request.session.has_key('login'):
        return redirect("/home")
    else:    
        if request.POST:
            uname = request.POST['uname']
            passw = request.POST['pass']
            hashpass = sha256(passw.encode()).hexdigest()
            user = User.objects.filter(name=uname,password=hashpass)
            if user:
                user = User.objects.get(name=uname)
                if user.status == 1:
                    request.session['login'] = 1
                    request.session['user'] = uname
                    return redirect("/home")
                else:
                    request.session['blockerror'] = 1   
                    return redirect(welcome)   
            else:
                request.session['logerror'] = 1
                return redirect(welcome)
        else:
            return render(request,'welcome/signin.html')


def logout(request):
    request.session.flush()
    return redirect(welcome)
