"""
Defines the required classes and functionality to setup the pre-game lobbies for hide and seek.

Classes:

    Player
    Game

Functions:

    create_lobby(object)
    join_lobby(object, int)

Imports:

    pickle

"""
from os import listdir

import pickle
from random import choice


class Player:
    """
    A class to represent a player of either type: seeker or hider.

    Attributes:
        username : str:
            The username of the player.
        ready_status : bool:
            Whether a player is ready to start or not.
        game : object:
            The game that the user is a part of.

    Methods:
        ready()
        unready()
    """

    def __init__(self, username):
        self.username = username
        self.ready_status = False
        self.game = None

    def ready(self):
        """
        Sets the player's ready_status to True.
        """
        self.ready_status = True

    def unready(self):
        """
        Sets the player's ready_status to False.
        """
        self.ready_status = False


class Game:
    """
    A class representing a game that's either currently running or in the process of setting up.

    Attributes:
        host : object:
            The player who created the lobby.
        players : list:
            A list of all players currently in the lobby.
        code : int:
            The code to join the lobby.

    Methods:
        create_code()
        print_players()
        update()
        player_join(object)
    """

    def __init__(self, host):
        self.host = host
        self.players = [host]

        self.create_code()

    def create_code(self):
        """
        Creates a unique code for the lobby.
        """
        files = listdir("active_games")
        codes = [int(x[:4]) for x in files]

        self.code = choice([i for i in range(1000, 10000) if i not in codes])

    def print_players(self):
        """
        Prints to console all players currently in the lobby.
        """
        for player_num in range(len(self.players)):
            print("Player " + str(player_num+1) + ": " + self.players[player_num].username)

    def update(self):
        """
        Pickles the game object and writes it to a pkl file.
        """
        with open("active_games/" + str(self.code) + ".pkl", 'wb') as out:
            pickle.dump(self, out, pickle.HIGHEST_PROTOCOL)

    def player_join(self, player):
        """
        Joins a player to the lobby.

        Parameters:
            player : object:
                The player who's joining the lobby.
        """
        self.players.append(player)


def create_lobby(request):
    """
    Allows the host of the lobby to create a game object.

        Parameters:
            request : object:
                The http request containing the session data.

        Returns:
            False: error occurred
            True: run as normal
    """

    # Checks request and username
    try:
        if type(request.session['username']) is not str:
            # Error
            return False
    except (AttributeError, TypeError, KeyError):
        # Error
        return False

    host = Player(request.session['username'])
    game = Game(host)
    host.game = game

    game.update()
    return True


def join_lobby(request, code):
    """
    Allows a user to join a specific lobby after entering a code.

        Parameters:
            request : object:
                The http request containing the session data.
            code : int:
                The 6 digit code for the lobby.

        Returns:
            False: error occurred
            True: run as normal
    """
    try:
        with open("active_games/" + str(code) + ".pkl", 'rb') as inp:
            game = pickle.load(inp)
    except FileNotFoundError:
        # Lobby doesn't exist
        return False

    # Checks request and username
    try:
        if request.session['username'] is None:
            # Error
            return False
    except (AttributeError, TypeError, KeyError):
        # Error
        return False

    player = Player(request.session['username'])
    game.player_join(player)
    player.game = game

    game.update()
    return True
