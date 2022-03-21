from html import escape
from django.shortcuts import redirect, render

from game.models import Game, Player
from welcome.models import User

from random import choice
from secrets import token_hex


# Renders html templates
def create(request):

    if 'login' in request.session:
        code = generate_code()
        return render(request, 'game/create.html', {
            "lobby_code": code,
        })
    return redirect('../../signin/')


def join(request):
    if 'login' in request.session:
        return render(request, 'game/join.html')
    return redirect('../../signin/')


# Code for enabling lobby functionality, the part of hide and seek before the game
def lobby(request, lobby_code):
    if 'login' not in request.session:
        return redirect('../../signin/')
    if request.POST['create'] == "True":

        status = create_game(request.POST, lobby_code)

        if not status[0]:
            return render(request, 'game/create.html', {
                'error_message': status[1],
                'lobby_code': lobby_code,
            })

    else:
        exists = False
        for x in Game.objects.all():
            if lobby_code == x.lobby_code:
                exists = True

                # Error page if lobby already in-game
                if x.running:
                    return render(request, 'game/join.html', {
                        'error_message': "This game has already started!",
                    })

        # Error page if lobby doesn't exist
        if not exists:
            return render(request, 'game/join.html', {
                'error_message': "This game doesn't exist!",
            })

    username = escape(request.POST['uname'])
    request.session['username'] = username

    game = Game.objects.get(lobby_code=lobby_code)

    if not check_rejoin(game, request.session['email']):
        # Add the player to the database
        if not create_player(game, username, request.session['email']):
            return render(request, 'game/join.html', {
                'error_message': 'That name already exists in the lobby!'
            })
    else:
        request.session['rejoin'] = 1

    return render(request, 'game/lobby.html', {
        'lobby_code': lobby_code,
        'username': username,
        'hiding_time': game.hiding_time,
        'seeking_time': game.seeking_time,
        'seeker_num': game.seeker_num,
        'lobby_longitude': game.lobby_longitude,
        'lobby_latitude': game.lobby_latitude,
    })


# Enables the player of a lobby to play the hide and seek game
# Represents the actual game functionality of hide and seek
def running(request, lobby_code):
    if 'login' not in request.session:
        return redirect('../../signin/')
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
        'start_time': game.game_start_time,
        'hiding_time': game.hiding_time,
        'seeking_time': game.seeking_time,
        'lobby_longitude': game.lobby_longitude,
        'lobby_latitude': game.lobby_latitude
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
    if 'login' not in request.session:
        return redirect('../../signin/')
    g = Game.objects.filter(lobby_code=lobby_code).first()
    username = request.session['username']
    player = Player.objects.filter(username=username, game=g).first()
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
        'seeker': player.seeker,
    })


# Shows an error page
def error(request):
    return render(request, 'game/error.html')


# Generates a unique code for a currently ongoing game
def generate_code():
    codes = []
    # Gets all the currently running lobbies
    for x in Game.objects.all():
        codes.append(x.lobby_code)

    return choice([i for i in range(1000, 10000) if i not in codes])


def validate_inputs(post):
    h_time = post['hiding_time']
    s_time = post['seeking_time']
    s_num = post['seeker_num']
    radius = post['radius']

    # Input not a number
    if not ((h_time.isdigit() or len(h_time) == 0) and (s_time.isdigit() or len(s_time) == 0)
            and (s_num.isdigit() or len(s_num) == 0) and (radius.isdigit() or len(radius) == 0)):
        return (False, "Settings must be digits!")

    if len(h_time) > 0:
        h_time = int(h_time)
        # Range for hiding time between 20 and 120 seconds
        if h_time < 20 or h_time > 120:
            return (False, "Hiding time must be between 20 and 120 seconds!")

    if len(s_time) > 0:
        s_time = int(s_time)
        # Range for seeking time between 120 and 1200 seconds
        if s_time < 120 or s_time > 1200:
            return (False, "Seeking time must be between 120 and 1200 seconds!")

    if len(s_num) > 0:
        s_num = int(s_num)
        # Range for number of seekers between 1 and 8
        if s_num < 1 or s_num > 8:
            return (False, "Seekers must be between 1 and 8!")

    if len(radius) > 0:
        radius = int(radius)
        # Range for radius between 50 and 1000 meters
        if radius < 50 or radius > 1000:
            return (False, "Radius must be between 50 and 1000 meters!")

    return [True]


def create_game(post, code):

    game = Game.objects.filter(lobby_code=code)

    if game:
        return True

    status = validate_inputs(post)
    if not status[0]:
        return status


    h_time = post['hiding_time']
    s_time = post['seeking_time']
    s_num = post['seeker_num']
    radius = post['radius']
    latit = post['lobby_latitude']
    longit = post['lobby_longitude']

    if len(h_time) == 0:
        h_time = 60
    else:
        h_time = int(h_time)

    if len(s_time) == 0:
        s_time = 600
    else:
        s_time = int(s_time)

    if len(s_num) == 0:
        s_num = 1
    else:
        s_num = int(s_num)

    if len(radius) == 0:
        radius = 100
    else:
        radius = int(radius)

    latit = float(latit)

    longit = float(longit)

    # Adds the game to the database
    Game(lobby_code=code, player_num=0, hiding_time=h_time, seeking_time=s_time, seeker_num=s_num,
         radius=radius, lobby_latitude=latit, lobby_longitude=longit).save()

    return [True]


def create_player(game, username, email):

    for x in Player.objects.filter(game=game):
        if x.username == username:
            return False

    user = User.objects.get(email=email)

    Player(username=username, game=game, seeker=False, ready=False, user=user).save()
    game.player_num += 1
    game.save()

    return True


def check_rejoin(game, email):
    for x in Player.objects.filter(game=game):
        if x.user.email == email:
            return True
    return False
