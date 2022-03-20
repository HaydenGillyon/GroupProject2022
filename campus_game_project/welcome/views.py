from django.shortcuts import redirect, render
from .models import User
from hashlib import sha256
from django.contrib import messages


def welcome(request):
    return render(request, 'welcome/welcome.html')


def signup(request):
    if 'login' in request.session:
        return redirect('home/')
    else:
        if request.POST:
            uname = request.POST['uname']
            email = request.POST['email']
            passw = request.POST['pass']
            hashpass = sha256(passw.encode()).hexdigest()
            user = User.objects.filter(name=uname)
            if user:
                messages.error(request, 'username already exists!')
                return render(request, 'welcome/signup.html')
            else:
                user = User.objects.filter(email=email)
                if user:
                    messages.error(request, 'email already exists!')
                    return render(request, 'welcome/signup.html')
                else:
                    '''obj = User(name=uname,email=email,password=hashpass)
                    obj.name = uname
                    obj.password = hashpass
                    obj.email = email'''
                    user = User(name=uname, email=email, password=hashpass)
                    user.save()
                    request.session['login'] = 1
                    request.session['user'] = uname
                    request.session['email'] = email
                    return redirect('/signin')
        else:
            return render(request, 'welcome/signup.html')


def signin(request):
    if 'login' in request.session:
        return redirect("/home/")
    else:
        if request.POST:
            email = request.POST['email']
            passw = request.POST['pass']
            hashpass = sha256(passw.encode()).hexdigest()
            user = User.objects.filter(email=email, password=hashpass)
            # List not empty
            if user:
                user = User.objects.get(email=email)
                if user.status == 1:
                    request.session['login'] = 1
                    request.session['email'] = email
                    return redirect("/home")
                else:
                    request.session['blockerror'] = 1
                    return redirect("/")
            else:
                request.session['logerror'] = 1
                return redirect("/")
        else:
            return render(request, 'welcome/signin.html')


def logout(request):
    request.session.flush()
    return redirect("/")


def legal(request):
    if not request.POST:
        return render(request, 'welcome/legal.html')
    elif request.POST:
        return redirect("/")
