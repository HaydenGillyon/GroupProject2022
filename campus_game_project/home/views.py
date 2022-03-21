import email
from django.shortcuts import redirect, render
from welcome.models import User
from django.contrib import messages


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
    return redirect("/signin")


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
    return redirect("/signin")


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
    return redirect("/signin")


def profile(request):
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
            'points': user_det.points,
            'profile': user_det.profile,
        }
        return render(request, "home/profile.html", context)
    else:
        if 'logerror' in request.session:
            messages.error(request, 'Invalid credentials!')
            del request.session['logerror']
        elif 'blockerror' in request.session:
            messages.error(request, 'user blocked!')
            del request.session['blockerror']
    return redirect("/signin")


def logout(request):
    request.session.flush()
    return redirect("/")
