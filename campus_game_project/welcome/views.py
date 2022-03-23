"""Handles the routing of HTTP requests for all urls contained in the welcome app. This is
everything related to the signing in, such as the signin, signup and legal pages.


Functions:

    welcome(ASGIRequest) -> HttpResponse, HttpResponseRedirect
    signup(ASGIRequest) -> HttpResponse, HttpResponseRedirect
    signin(ASGIRequest) -> HttpResponse, HttpResponseRedirect
    logout(ASGIRequest) -> HttpResponseRedirect
    legal(ASGIRequest) -> HttpResponse
"""
from django.shortcuts import redirect, render
from welcome.models import User
from hashlib import sha256
from html import escape


def welcome(request):
    """Runs when a user goes to the welcome page, the front page of the app.


    Parameters:

        request : ASGIRequest
            The HTTP request.


    Returns:

        return : HttpResponse
            The template for the welcome page.

        return : HttpResponseRedirect
            Returns a redirect to the home page if the user is logged in.
    """
    if 'login' in request.session:
        return redirect('../home/')
    return render(request, 'welcome/welcome.html')


def signup(request):
    """Runs when a user goes to the signup page. Allows them to create an account.
    The email and password must follow a specific format and the user must have accepted
    the terms and conditions.


    Parameters:

        request : ASGIRequest
            The HTTP request.


    Returns:

        return : HttpResponse
            The template for signup page.

        return : HttpResponseRedirect
            Returns a redirect to the home page if the user is logged in.
    """
    if 'login' in request.session:
        return redirect('home/')
    else:
        if request.POST:
            uname = escape(request.POST['uname'])
            email = escape(request.POST['email'])
            passw = request.POST['pass']
            hashpass = sha256(passw.encode()).hexdigest()

            # Checks if username is taken
            user = User.objects.filter(name=uname)
            if user:
                return render(request, 'welcome/signup.html', {
                    'error_message': "Username already taken!",
                })

            # Checks if email is taken
            user = User.objects.filter(email=email)
            if user:
                return render(request, 'welcome/signup.html', {
                    'error_message': "Email already taken!",
                })

            # Creates the user and takes them to signin
            user = User(name=uname, email=email, password=hashpass)
            user.save()
            request.session['login'] = 1
            request.session['user'] = uname
            request.session['email'] = email
            return redirect('/signin')
        else:
            return render(request, 'welcome/signup.html')


def signin(request):
    """Runs when a user goes to the signin page. Allows the user to login using
    the details specified in the signup.


    Parameters:

        request : ASGIRequest
            The HTTP request.


    Returns:

        return : HttpResponse
            The template for the signin page or an error page if something goes wrong.

        return : HttpResponseRedirect
            Returns a redirect to the home page if the user is logged in.
    """
    if 'login' in request.session:
        return redirect("/home/")
    else:
        if request.POST:
            email = escape(request.POST['email'])
            passw = request.POST['pass']
            hashpass = sha256(passw.encode()).hexdigest()
            user = User.objects.filter(email=email, password=hashpass)

            # Checks if inputs exist in the database
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


def logout(request):
    """Runs when a user logs out. Empties all the session data and sends them to the welcome page.


    Parameters:

        request : ASGIRequest
            The HTTP request.


    Returns:

        return : HttpResponseRedirect
            Returns a redirect to the welcome page after logout.
    """
    request.session.flush()
    return redirect("/")


def legal(request):
    """Returns the template for the legal page, containing terms and conditions. The function
    checks for post requests as the buttons to enter the legal page send a post request to let
    the legal page know what page it came from. This is to dynamically change the functionality
    of the return button present on the page.


    Parameters:

        request : ASGIRequest
            The HTTP request.


    Returns:

        return : HttpResponse
            The legal page template.
    """
    if not request.POST:
        return render(request, 'welcome/legal.html')
    elif request.POST:
        return render(request, 'welcome/legal.html', {
            "origin": request.POST["origin"]
        })
