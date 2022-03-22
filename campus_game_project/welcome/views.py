# from traceback import print_tb
from django.shortcuts import redirect, render
from .models import User
from hashlib import sha256
from html import escape

''' Main page for website '''
def welcome(request):
    if 'login' in request.session:
        return redirect('../home/')
    return render(request, 'welcome/welcome.html')

''' creates an entry in the database for user and logs the user in when successful '''
def signup(request):
    if 'login' in request.session:
        return redirect('home/')
    else:
        if request.POST:
            uname = escape(request.POST['uname'])
            email = escape(request.POST['email'])
            passw = request.POST['pass']
            hashpass = sha256(passw.encode()).hexdigest()

            user = User.objects.filter(name=uname)
            if user:
                return render(request, 'welcome/signup.html', {
                    'error_message': "Username already taken!",
                })

            user = User.objects.filter(email=email)
            if user:
                return render(request, 'welcome/signup.html', {
                    'error_message': "Email already taken!",
                })

            user = User(name=uname, email=email, password=hashpass)
            user.save()
            request.session['login'] = 1
            request.session['user'] = uname
            request.session['email'] = email
            return redirect('/signin')
        else:
            return render(request, 'welcome/signup.html')

''' signs user in to the app and redirects to home page if sucessful '''
def signin(request):
    if 'login' in request.session:
        return redirect("/home/")
    else:
        if request.POST:
            email = escape(request.POST['email'])
            passw = request.POST['pass']
            hashpass = sha256(passw.encode()).hexdigest()
            user = User.objects.filter(email=email, password=hashpass)
            # List not empty
            if user:
                user = User.objects.get(email=email)
                if user.status == 1:
                    request.session['login'] = 1
                    request.session['email'] = email
                    return redirect("/home/")
                else:
                    request.session['blockerror'] = 1
                    return render(request, 'welcome/error.html')
            else:
                return render(request, 'welcome/signin.html', {
                    'error_message': "Username or Password is incorrect!",
                })
        else:
            return render(request, 'welcome/signin.html')

''' delete session data to log users out and then redirects to welcome page '''
def logout(request):
    request.session.flush()
    return redirect("/")

''' displays legal page, also redirects from both welcome and signup '''
def legal(request):
    if not request.POST:
        return render(request, 'welcome/legal.html')
    elif request.POST:
        return render(request, 'welcome/legal.html', {
            "origin": request.POST["origin"]
        })
