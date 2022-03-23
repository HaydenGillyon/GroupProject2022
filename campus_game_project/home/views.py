"""Handles the routing of HTTP requests for all urls contained in the home app. This is
everything related to the home page, such as the profile and leaderboards.


Functions:

    home(ASGIRequest) -> HttpResponse, HttpResponseRedirect
    leaderboard(ASGIRequest) -> HttpResponse, HttpResponseRedirect
    profile(ASGIRequest) -> HttpResponse, HttpResponseRedirect
    logout(ASGIRequest) -> HttpResponseRedirect
"""
from django.shortcuts import redirect, render
from welcome.models import User


def home(request):
    """Runs when a user goes to the home page, the main page of the app.
    Allows the user to go to the create or join pages.


    Parameters:

        request : ASGIRequest
            The HTTP request.


    Returns:

        return : HttpResponse
            The template for the home page.

        return : HttpResponseRedirect
            Returns a redirect to the signin page if the user isn't logged in.
    """
    if 'login' in request.session:

        email = request.session['email']
        user_det = User.objects.get(email=email)

        context = {
            'user': user_det.name,
            'email': user_det.email,
            'id': user_det.id,
        }
        return render(request, 'home/landingPage.html', context)

    return redirect("../signin/")


def leaderboard(request):
    """Runs when a user goes to the leaderboard page. Displays the top players
    in order based on their points gained from playing games.


    Parameters:

        request : ASGIRequest
            The HTTP request.


    Returns:

        return : HttpResponse
            The template for the leaderboard page.

        return : HttpResponseRedirect
            Returns a redirect to the signin page if the user isn't logged in.
    """
    if 'login' in request.session:

        context = {
            'data': User.objects.all().order_by('-points')[:10]
        }
        return render(request, "home/leaderboard.html", context)

    return redirect("../../signin/")


def profile(request):
    """Runs when a user goes to the profile page. Displays all necessary information about the user,
    including profile picture, email, username, points. Also allows the user to change their profile
    picture depending on the number of points they've obtained.


    Parameters:

        request : ASGIRequest
            The HTTP request.


    Returns:

        return : HttpResponse
            The template for the profile page.

        return : HttpResponseRedirect
            Returns a redirect to the signin page if the user isn't logged in.
    """
    if 'login' in request.session:

        email = request.session['email']
        user_det = User.objects.get(email=email)

        # If the user selects a new pfp, it refreshes the page with the pfp passed via post.
        if request.POST:
            user_det.profile_image_url = request.POST['profile_pic']
            user_det.save()

        context = {
            'user': user_det.name,
            'email': user_det.email,
            'id': user_det.id,
            'points': user_det.points,
            'profile': user_det.profile_image_url,
        }
        return render(request, "home/profile.html", context)

    return redirect("../../signin/")


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
