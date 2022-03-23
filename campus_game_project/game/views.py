"""Handles the routing of HTTP requests for all urls contained in the game app. This is everything
to do with the running of the game, such as creating, joining or running lobbies. It also houses
all the helper functions necessary for the views to operate


Functions:

    create(ASGIRequest) -> HttpResponse, HttpResponseRedirect
    join(ASGIRequest) -> HttpResponse, HttpResponseRedirect
    lobby(ASGIRequest, int) -> HttpResponse, HttpResponseRedirect
    running(ASGIRequest, int) -> HttpResponse, HttpResponseRedirect
    end(ASGIRequest, int) -> HttpResponse, HttpResponseRedirect
    error(ASGIRequest) -> HttpResponse
    generate_code() -> int
    validate_inputs(QueryDict) -> tuple, list
    create_game(QueryDict, int) -> tuple, list
    create_player(Game, str, str) -> bool
    check_rejoin(Game, str) -> bool
"""
from html import escape
from django.shortcuts import redirect, render

from game.models import Game, Player
from welcome.models import User

from random import choice
from secrets import token_hex


def create(request):
    """Runs when a user goes to the page to create a lobby. Also generates a lobby code to pass in.


    Parameters:
    
        request : ASGIRequest
            The HTTP request.


    Returns:

        return : HttpResponse
            The template for the create page.

        return : HttpResponseRedirect
            Returns a redirect to the signin page if the user isn't logged in.
    """
    if 'login' in request.session:
        code = generate_code()
        return render(request, 'game/create.html', {
            "lobby_code": code,
        })
    return redirect('../../signin/')


def join(request):
    """Runs when a user goes to the page to join a lobby.


    Parameters:

        request : ASGIRequest
            The HTTP request.

    
    Returns:

        return : HttpResponse
            The template for the join page.

        return : HttpResponseRedirect
            Returns a redirect to the signin page if the user isn't logged in.
    """
    if 'login' in request.session:
        return render(request, 'game/join.html')
    return redirect('../../signin/')


def lobby(request, lobby_code):
    """Creates the Game in the database if the player is joining the lobby from 'create'.
    Creates the Player in the database with a reference to the Game that has the matching lobby code.
    After creating these, it returns the template for the lobby itself, or a potential error message.


    Parameters:

        request : ASGIRequest
            The HTTP request.

        lobby_code : int
            The code for the game you are trying to join.

        
    Returns:

        return : HttpResponse
            Either the lobby page or the page the user came from with an error if it is required.

        return : HttpResponseRedirect
            Returns a redirect to the signin page if the user isn't logged in.
    """
    if 'login' not in request.session:
        return redirect('../../signin/')

    # Creates the Game
    if request.POST['create'] == "True":

        status = create_game(request.POST, lobby_code)

        # Error in creating the game due to faulty inputs
        if not status[0]:
            return render(request, 'game/create.html', {
                'error_message': status[1],
                'lobby_code': lobby_code,
            })

    else:
        exists = False
        # Searches for the game
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

    # Add the player to the database if they aren't refreshing
    if not check_rejoin(game, request.session['email']):
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


def running(request, lobby_code):
    """Sends the player from the lobby to the main game page when everyone is ready.
    Collects all the necessary data for the running of the game and passes it to the template.
    

    Parameters:

        request : ASGIRequest
            The HTTP request.

        lobby_code : int
            The code for the game you are playing in.


    Returns:

        return : HttpResponse
            Either the lobby page.
        
        return : HttpResponseRedirect
            Returns a redirect to the signin page if the user isn't logged in or the homepage if there's an error.
    """
    if 'login' not in request.session:
        return redirect('../../../signin/')
    username = request.session['username']
    game = Game.objects.get(lobby_code=lobby_code)
    player = Player.objects.filter(username=username, game=game).first()

    # If the Player cannot be found, go to the home page
    if not player:
        return redirect('../../../home/')

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
        'lobby_latitude': game.lobby_latitude,
        'radius': game.radius,
        'profile_pic': player.user.profile_image_url,
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


def end(request, lobby_code):
    """
    The end screen showing the result of the game. Also provides a link to return to the lobby.
    The Game is deleted when all players have entered this view.


    Parameters:

        request : ASGIRequest
            The HTTP request.

        lobby_code : int
            The code of the game that has finished.


    Returns:

        return : HttpResponse
            The end screen template with all necessary data passed in.

        return : HttpResponseRedirect
            The signin page if the user is not logged in.
    """
    if 'login' not in request.session:
        return redirect('../../../signin/')

    g = Game.objects.filter(lobby_code=lobby_code).first()
    username = request.session['username']
    player = Player.objects.filter(username=username, game=g).first()

    # Keep for None safety as game could already be deleted
    if g:
        result = g.winner
        g.players_finished += 1
        g.save()

        # Player number is decremented upon leaving running stage
        if g.player_num < 1:
            g.delete()

    # If game has already been deleted
    else:   
        result = 'unknown'

    return render(request, 'game/end.html', {
        'lobby_code': lobby_code,
        'result': result,
        'seeker': player.seeker,
    })


def error(request):
    """Error debug page.


    Parameters:

        request : ASGIRequest
            The HTTP request.

    
    Returns:
    
        return : HttpResponse
            The rendered error html page.
    """
    return render(request, 'game/error.html')


def generate_code():
    """Generates a unique 4 digits code between 1000 and 9999 to serve as the game lobby code.
    Gets a list of all currently running game codes and selects a random number not in that list.


    Returns:

        return : int
            The 4 digit code that has been randomly selected.
    """
    codes = []
    # Gets all the currently running lobbies
    for x in Game.objects.all():
        codes.append(x.lobby_code)

    return choice([i for i in range(1000, 10000) if i not in codes])


def validate_inputs(post):
    """Determines whether the input settings for the game lobby are valid. If they are invalid it gives
    the reason why.


    Parameters:

        post : QueryDict
            The POST request containing the settings.


    Returns:
    
        return : tuple
            If it is invalid, returns a tuple containing the value FALSE and the error message.

        return : list
            If it is valid, returns a list of length 1 containing TRUE. This is to prevent the checking
            from outside the function failing.
    """
    h_time = post['hiding_time']
    s_time = post['seeking_time']
    s_num = post['seeker_num']
    radius = post['radius']

    # Input not a number
    if not ((h_time.isdigit() or len(h_time) == 0) and (s_time.isdigit() or len(s_time) == 0)
            and (s_num.isdigit() or len(s_num) == 0) and (radius.isdigit() or len(radius) == 0)):
        return (False, "Settings must be digits!")

    # Range for hiding time between 20 and 120 seconds
    if len(h_time) > 0:
        h_time = int(h_time)
        if h_time < 20 or h_time > 120:
            return (False, "Hiding time must be between 20 and 120 seconds!")

    # Range for seeking time between 120 and 1200 seconds
    if len(s_time) > 0:
        s_time = int(s_time)
        if s_time < 120 or s_time > 1200:
            return (False, "Seeking time must be between 120 and 1200 seconds!")

    # Range for number of seekers between 1 and 8
    if len(s_num) > 0:
        s_num = int(s_num)
        if s_num < 1 or s_num > 8:
            return (False, "Seekers must be between 1 and 8!")

    # Range for radius between 50 and 1000 meters
    if len(radius) > 0:
        radius = int(radius)
        if radius < 50 or radius > 1000:
            return (False, "Radius must be between 50 and 1000 meters!")

    return [True]


def create_game(post, code):
    """Creates the game using the input settings values and writes it to the database.
    If the input settings are empty, it sets a default value.


    Parameters:

        post : QueryDict
            The POST request containing the settings.

        code : int
            The lobby code of the game being created.


    Returns:

        return : tuple
            If the settings are invalid, return the tuple containing FALSE and the error message.

        return : list
            If creating the game succeeds, return a list containing only TRUE for the error checking
            outside the function.
    """
    game = Game.objects.filter(lobby_code=code)

    if game:
        return [True]

    status = validate_inputs(post)
    if not status[0]:
        return status

    # Settings variables
    h_time = post['hiding_time']
    s_time = post['seeking_time']
    s_num = post['seeker_num']
    radius = post['radius']
    latit = post['lobby_latitude']
    longit = post['lobby_longitude']

    # Default hiding time is 60 seconds
    if len(h_time) == 0:
        h_time = 60
    else:
        h_time = int(h_time)

    # Default seeking time is 10 minutes
    if len(s_time) == 0:
        s_time = 600
    else:
        s_time = int(s_time)

    # Default seekers is 1
    if len(s_num) == 0:
        s_num = 1
    else:
        s_num = int(s_num)

    # Default radius is 100 meters
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
    """Adds a Player to the database with a reference to the current game they're playing,
    as well as a reference to the User that created them.


    Parameters:
    
        game : Game
            The game that the user is participating in.

        username : str
            The name that the player wants to be called by in this game.

        email : str
            The email address of the user creating the player.


    Returns:

        return : bool
            False if the username is already in the lobby, True if successful.
    """
    for x in Player.objects.filter(game=game):
        if x.username == username:
            return False

    user = User.objects.get(email=email)

    # Creating the Player
    Player(username=username, game=game, seeker=False, ready=False, user=user).save()
    game.player_num += 1
    game.save()

    return True


def check_rejoin(game, email):
    """Checks if the user has refreshed the lobby page. If they have then it doesn't need to
    remove the Player from the database later.


    Parameters:

        game : Game
            The game lobby that the user refreshed.

        email : str
            The email of the user who refreshed.


    Returns:

        return : bool
            True if the user refreshed, False if they didn't.
    """
    # If the User is already bound to a Player, the user has refreshed the page
    for x in Player.objects.filter(game=game):
        if x.user.email == email:
            return True
    return False
