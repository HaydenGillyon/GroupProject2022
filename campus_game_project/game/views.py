from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError

from game.models import Game, Player

from random import choice


def create(request):
    return render(request, 'game/create.html')


def join(request):
    return render(request, 'game/join.html')


@csrf_exempt
def lobby(request, lobby_code):
    try:
        if request.POST['create'] == "True":
            code = generate_code()
            Game(lobby_code=code, player_num=0).save()
            print(request.POST)
            request.session['username'] = request.POST['uname']
            return redirect('/game/' + str(code) + '/', request=request)

        else:
            exists = False
            for x in Game.objects.all():
                if lobby_code == x.lobby_code:
                    exists = True
            # Error page if lobby doesn't exist
            if not exists:
                return render(request, 'game/error.html')

            username = request.POST['uname']

            request.session['username'] = username

            game = Game.objects.filter(lobby_code=lobby_code)[0]

            Player(username=username, game=game, seeker=False, ready=False).save()

            game.player_num += 1
            game.save()

            return render(request, 'game/lobby.html', {
                'lobby_code': lobby_code,
                'username': username,
            })

    except MultiValueDictKeyError:
        username = request.session['username']

        game = Game.objects.filter(lobby_code=lobby_code)[0]

        Player(username=username, game=game, seeker=False, ready=False).save()

        game.player_num += 1
        game.save()

        return render(request, 'game/lobby.html', {
            'lobby_code': lobby_code,
            'username': username,
        })


def generate_code():
    codes = []
    for x in Game.objects.all():
        codes.append(x.lobby_code)

    return choice([i for i in range(1000, 10000) if i not in codes])
