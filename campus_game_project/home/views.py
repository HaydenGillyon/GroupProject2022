from django.shortcuts import redirect, render
from welcome.models import User
from django.contrib import messages

''' main home page when user logs into the app '''
def home(request):
    if 'login' in request.session:
        if 'error' in request.session:
            messages.error(request, 'Invalid password!')
            del request.session['error']

        email = request.session['email']
        user_det = User.objects.get(email=email)
        context = {
            'user': user_det.name,
            'email': user_det.email,
            'id': user_det.id,
        }
        return render(request, 'home/landingPage.html', context)
    else:
        if 'logerror' in request.session:
            messages.error(request, 'Invalid credentials!')
            del request.session['logerror']
        elif 'blockerror' in request.session:
            messages.error(request, 'user blocked!')
            del request.session['blockerror']
    return redirect("../signin/")

''' displays the top 10 players of hide to survive '''
def leaderboard(request):
    if 'login' in request.session:
        if 'error' in request.session:
            messages.error(request, 'Invalid password!')
            del request.session['error']
        context = {
            'data': User.objects.all().order_by('-points')[:10]
        }
        return render(request, "home/leaderboard.html", context)
    else:
        if 'logerror' in request.session:
            messages.error(request, 'Invalid credentials!')
            del request.session['logerror']
        elif 'blockerror' in request.session:
            messages.error(request, 'user blocked!')
            del request.session['blockerror']
    return redirect("../../signin/")

''' shop for items with points won , 
    deprecated until further notice following 
    realization that we can raise serious money 
    switching to this into an nft marketplace '''
def shop(request):
    if 'login' in request.session:
        if 'error' in request.session:
            messages.error(request, 'Invalid password!')
            del request.session['error']
        email = request.session['email']
        user_det = User.objects.get(email=email)
        context = {
            'user': user_det.name,
            'email': user_det.email,
            'id': user_det.id,
        }
        return render(request, "home/shop.html", context)
    else:
        if 'logerror' in request.session:
            messages.error(request, 'Invalid credentials!')
            del request.session['logerror']
        elif 'blockerror' in request.session:
            messages.error(request, 'user blocked!')
            del request.session['blockerror']
    return redirect("../../signin/")

''' shows up the profile page that contains all the information of user '''
def profile(request):
    if 'login' in request.session:

        if 'error' in request.session:
            messages.error(request, 'Invalid password!')
            del request.session['error']
        email = request.session['email']
        user_det = User.objects.get(email=email)
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
    else:
        if 'logerror' in request.session:
            messages.error(request, 'Invalid credentials!')
            del request.session['logerror']
        elif 'blockerror' in request.session:
            messages.error(request, 'user blocked!')
            del request.session['blockerror']
    return redirect("../../signin/")

''' delete session data to log users out and then redirects to welcome page '''
def logout(request):
    request.session.flush()
    return redirect("/")
