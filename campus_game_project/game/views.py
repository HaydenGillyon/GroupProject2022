from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError

from game.models import Game, Player

from random import choice
from secrets import token_hex


# Renders html templates
def create(request):
    return render(request, 'game/create.html')


def join(request):
    return render(request, 'game/join.html')


# Code for enabling lobby functionality, the part of hide and seek before the game
@csrf_exempt
def lobby(request, lobby_code):
    try:
        # If the lobby is being created, enters with a default code of 0
        if request.POST['create'] == "True":
            h_time = int(request.POST['hiding_time'])
            s_time = int(request.POST['seeking_time'])
            s_num = int(request.POST['seeker_num'])
            radius = int(request.POST['radius'])

            code = generate_code()

            # Adds the game to the database
            Game(lobby_code=code, player_num=0, hiding_time=h_time, seeking_time=s_time, seeker_num=s_num, radius=radius).save()

            request.session['username'] = request.POST['uname']

            # Redirects to url with correct code
            return redirect('/game/' + str(code) + '/', request=request)

        else:
            exists = False
            for x in Game.objects.all():
                if lobby_code == x.lobby_code:
                    exists = True

                    # Error page if lobby already in-game
                    if x.running:
                        return render(request, 'game/error.html')

            # Error page if lobby doesn't exist
            if not exists:
                return render(request, 'game/error.html')

            username = request.POST['uname']
            request.session['username'] = username

            # Add the player to the database
            game = Game.objects.get(lobby_code=lobby_code)
            if len(Player.objects.filter(game=game)):
                for x in Player.objects.filter(game=game):
                    if x.username == username:
                        return render(request, 'game/error.html')
            Player(username=username, game=game, seeker=False, ready=False).save()
            game.player_num += 1
            game.save()

            return render(request, 'game/lobby.html', {
                'lobby_code': lobby_code,
                'username': username,
            })
    # This error is thrown if there has been a redirect when creating the lobby
    except MultiValueDictKeyError:
        username = request.session['username']

        # Adds the player to the database
        game = Game.objects.get(lobby_code=lobby_code)
        if len(Player.objects.filter(game=game)):
            for x in Player.objects.filter(game=game):
                if x.username == username:
                    return render(request, 'game/error.html')
        Player(username=username, game=game, seeker=False, ready=False).save()
        game.player_num += 1
        game.save()

        return render(request, 'game/lobby.html', {
            'lobby_code': lobby_code,
            'username': username,
        })


# Enables the player of a lobby to play the hide and seek game
# Represents the actual game functionality of hide and seek
def running(request, lobby_code):
    username = request.session['username']
    game = Game.objects.get(lobby_code=lobby_code)
    player = Player.objects.filter(username=username, game=game).first()

    # Error thrown if the player matching lobby_code and username can't be found
    if not player:
        return render(request, 'game/error.html')

    game.running = True
    game.save()

    # player.seeker is True if the player was selected as the seeker
    data_dict = {
        'lobby_code': lobby_code,
        'username': username,
        'seeker': player.seeker,
        'start_time': game.game_start_time
    }
    if (not player.seeker) and (player.hider_code is None):
        # 4 character secret hex code
        hider_code = token_hex(2)
        player.hider_code = hider_code
        player.save()
        data_dict['hider_code'] = hider_code
    elif (not player.seeker):
        data_dict['hider_code'] = player.hider_code

    return render(request, 'game/running.html', data_dict)


# Ends the lobby of the game being played
def end(request, lobby_code):
    g = Game.objects.filter(lobby_code=lobby_code).first()
    if g:   # Keep for None safety as game could already be deleted
        result = g.winner

        g.players_finished += 1
        g.save()

        if g.player_num < 1:    # Player number is decremented upon leaving running stage
            g.delete()
    else:   # If game has already been deleted
        result = 'unknown'
    return render(request, 'game/end.html', {
        'lobby_code': lobby_code,
        'result': result,
    })


# Generates a unique code for a currently ongoing game
def generate_code():
    codes = []
    # Gets all the currently running lobbies
    for x in Game.objects.all():
        codes.append(x.lobby_code)

    return choice([i for i in range(1000, 10000) if i not in codes])
