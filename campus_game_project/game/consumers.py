"""Contains all the logic for the Websockets to run. This enables the game to
be responsive for users and allows live updates depending on what happens, such
as a player being caught or someone joining the lobby.


Classes:

    PlayerConsumer
    GameConsumer


Functions:

    check_if_player_inbounds(int, float, float) -> bool
"""
import time
import re
import json
import math
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from game.models import Game, Player
from welcome.models import User
from random import randint


class PlayerConsumer(WebsocketConsumer):
    """Websocket class to handle all the events that can occur when the user is
    in the lobby waiting for the game.


    Attributes:

        scope : dict
            Dictionary containing all the data passed to the socket, including session.

        lobby_code : str
            The code of the lobby the socket is connected to.

        username : str
            The username of the player who has connected (not the user).

        channel_name : str
            The name of the channel the socket is using to communicate.

        channel_layer : RedisChannelLayer
            The channel layer object the socket is using to communicate.


    Methods:

        connect() -> None
            Defines behaviour for when the websocket connects.

        disconnect(int) -> None
            Defines behaviour for when the websocket connection ends.

        receive(str) -> None
            Defines behaviour for when the websocket receives any kind of message.

        lobby_event(dict) -> None
            For whenever a player joins or leaves the lobby.

        ready_event(dict) -> None
            For whenever a player readys or unreadys in the lobby.

        start_event(dict) -> None
            For when every player is ready and the game starts.
    """

    def connect(self):
        """Whenever a user connects to a lobby, through either joining or creating it,
        this function will run and complete the setup for the websocket. It adds the
        specific socket to the group allowing it to communicate with the others dynamically.
        """
        self.lobby_code = self.scope['url_route']['kwargs']['lobby_code']
        self.username = self.scope['session']['username']
        message = self.username + " has joined."

        # Adds the websocket to a group, named the lobby code
        async_to_sync(self.channel_layer.group_add)(
            self.lobby_code,
            self.channel_name
        )

        self.accept()
        players = []

        # Gets a list of all players currently in the game
        game = Game.objects.get(lobby_code=int(self.lobby_code))
        for player in Player.objects.filter(game=game):
            players.append({
                "username": player.username,
                "ready": player.ready
                })

        # Sends data to group
        async_to_sync(self.channel_layer.group_send)(
            self.lobby_code,
            {
                'type': 'lobby_event',
                'msg_type': 'join',
                'message': message,
                'username': self.scope['session']['username'],
                'players': players
            }
        )

    def disconnect(self, close_code):
        """Runs whenever a user leaves a specific lobby through any means. Removes the socket
        from the group and the user from the database the database if the user isn't refreshing.


        Parameters:

            close_code : int
                The type of disconnection.
        """
        if "playing" not in self.scope['session']:
            message = self.scope['session']['username'] + " has left."

            # Sends data to group
            async_to_sync(self.channel_layer.group_send)(
                self.lobby_code,
                {
                    'type': 'lobby_event',
                    'msg_type': 'leave',
                    'message': message,
                    'username': self.scope['session']['username'],
                    'players': None
                }
            )

            # Deletes the user from the database
            if 'rejoin' not in self.scope['session']:
                game = Game.objects.get(lobby_code=self.lobby_code)
                Player.objects.get(game=game, username=self.scope['session']['username']).delete()
                game.player_num -= 1
                game.save()
                if game.player_num == 0:
                    game.delete()
            else:
                del self.scope['session']['rejoin']

        # Leaves the group
        async_to_sync(self.channel_layer.group_discard)(
            self.lobby_code,
            self.channel_name
        )

    def receive(self, text_data):
        """Whenever the websocket receives a message of any kind from the channel layer,
        this functions runs and handles it depending on the type of message.


        Parameters:

            text_data : str
                A json containing all the data sent to the socket.
        """
        text_data_json = json.loads(text_data)

        if text_data_json['msg_type'] == "playing":
            self.scope['session']['playing'] = True

        # If a player has changed their ready state
        elif text_data_json['msg_type'] == "ready":
            ready = text_data_json['ready'].lower()
            username = text_data_json['username']
            message = username + " is " + ready + "."

            if ready == "unready":
                ready = False
            else:
                ready = True

            # Sets the player to ready
            game = Game.objects.get(lobby_code=self.lobby_code)
            player = Player.objects.get(game=game, username=username)
            player.ready = ready
            player.save()

            # If the game is ready to start
            if game.all_ready() and game.player_num > 1 and game.player_num > game.seeker_num:
                players = [p for p in Player.objects.filter(game=game)]

                # Sets the players as seekers
                for _ in range(game.seeker_num):
                    player = players[randint(0, len(players)-1)]
                    player.seeker = True
                    player.save()
                    players.remove(player)

                # Set game start time in seconds since epoch
                game.game_start_time = time.time()
                game.save()

                async_to_sync(self.channel_layer.group_send)(
                    self.lobby_code,
                    {
                        'type': 'start_game'
                    }
                )

            # Sends message to group
            async_to_sync(self.channel_layer.group_send)(
                self.lobby_code,
                {
                    'type': 'ready_event',
                    'message': message,
                    'username': self.scope['session']['username'],
                    'ready': ready
                }
            )

    def lobby_event(self, event):
        """Sends a message to all the websockets in the channel layer when
        a new player joins or a player leaves. Tells the webpage to remove the
        player from the player list display and updates the chat log.


        Parameters:

            event : dict
                Contains all the event information passed in.
        """
        msg_type = event['msg_type']
        message = event['message']
        username = event['username']
        players = event['players']

        self.send(text_data=json.dumps({
            'msg_type': msg_type,
            'message': message,
            'username': username,
            'players': players
        }))

    def ready_event(self, event):
        """Sends a message to all the websockets in the channel layer when
        a user changes their ready state. Tells the webpage to change the colour
        of the player in the player list and updates the chat log.


        Parameters:

            event : dict
                Contains all the event information passed in.
        """
        message = event['message']
        ready_user = event['username']
        username = self.username
        ready = event['ready']

        self.send(text_data=json.dumps({
            'msg_type': 'ready',
            'message': message,
            'username': username,
            'ready_user': ready_user,
            'ready': ready
        }))

    def start_game(self, event):
        """Sends a message to all websockets in the channel layer to tell them
        that the game is starting.


        Parameters:

            event : dict
                Contains all the event information passed in.
        """
        self.send(text_data=json.dumps({
            'msg_type': 'start'
        }))


class GameConsumer(WebsocketConsumer):
    """Websocket class to handle all the events that can occur when the user is
    in the running game, such as players being caught.


    Attributes:

        scope : dict
            Dictionary containing all the data passed to the socket, including session.

        lobby_code : str
            The code of the lobby the socket is connected to.

        username : str
            The username of the player who has connected (not the user).

        channel_name : str
            The name of the channel the socket is using to communicate.

        channel_layer : RedisChannelLayer
            The channel layer object the socket is using to communicate.


    Methods:

        connect() -> None
            Defines behaviour for when the websocket connects.

        disconnect(int) -> None
            Defines behaviour for when the websocket connection ends.

        receive(str) -> None
            Defines behaviour for when the websocket receives any kind of message.

        game_finish(dict) -> None
            The final method that runs when a win condition has been met.

        check_code(str) -> None
            Checks if a hider code is valid.

        check_found_hiders() -> None
            Checks if all hiders have been found.
    """

    def connect(self):
        """Whenever a user connects to a running game, this function will run and complete
        the setup for the websocket. It adds the specific socket to the group allowing it to
        communicate with the others dynamically.
        """
        self.lobby_code = self.scope['url_route']['kwargs']['lobby_code']
        self.username = self.scope['session']['username']

        # Adds the websocket to a group, named the lobby code
        async_to_sync(self.channel_layer.group_add)(
            self.lobby_code,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        """Runs whenever a user leaves a game through any means. Removes the socket from the group
        and removes the user from the database.


        Parameters:

            close_code : int
                The type of disconnection.
        """
        # Leaves the group
        async_to_sync(self.channel_layer.group_discard)(
            self.lobby_code,
            self.channel_name
        )

        # Deletes the user from the database
        try:
            g = Game.objects.get(lobby_code=self.lobby_code)
            Player.objects.get(game=g, username=self.scope['session']['username']).delete()
            g.player_num -= 1
            g.save()
            if g.player_num == 0:
                    g.delete()
        except Game.DoesNotExist:
            pass

    def receive(self, text_data):
        """Whenever the websocket receives a message of any kind from the channel layer,
        this functions runs and handles it depending on the type of message.


        Parameters:

            text_data : str
                A json containing all the data sent to the socket.
        """
        text_data_json = json.loads(text_data)

        # If the seeker is entering a hider code
        if text_data_json['msg_type'] == 'hider_code_attempt':
            result = self.check_code(text_data_json['attempt_code'])
            self.send(text_data=json.dumps({
                'msg_type': 'code_result',
                'result': result,
            }))

        # Hiders win
        elif text_data_json['msg_type'] == 'seeking_over':
            event = {
                    'type': 'game_finish',
                    'who_won': 'hiders'
                }
            async_to_sync(self.channel_layer.group_send)(
                self.lobby_code,
                event
            )

        # Regular position check
        elif text_data_json['msg_type'] == 'position_update':
            latit = text_data_json['player_latitude']
            longit = text_data_json['player_longitude']

            if not check_if_player_inbounds(self.lobby_code, latit, longit):
                self.send(text_data=json.dumps({
                    'msg_type': 'outbounds_alert'
                }))
            else:
                self.send(text_data=json.dumps({
                    'msg_type': 'position_update',
                    'latitude': latit,
                    'longitude': longit,
                }))

        # Check if player is still out of bounds after the countdown
        elif text_data_json['msg_type'] == 'outbounds_update':
            latit = text_data_json['player_latitude']
            longit = text_data_json['player_longitude']
            timestamp = text_data_json['timestamp']
            outbounds_timestamp = text_data_json['outbounds_timestamp']

            if not check_if_player_inbounds(self.lobby_code, latit, longit):
                if (timestamp - outbounds_timestamp) > 20000:
                    self.send(text_data=json.dumps({
                        'msg_type': 'outbounds_kick'
                    }))
                    # To end game if last hider is kicked
                    self.check_found_hiders()
            else:
                self.send(text_data=json.dumps({
                    'msg_type': 'inbounds_alert',
                }))

    def game_finish(self, event):
        """Updates the database depending on which team wins, doing things such as
        assigning points. Sends a message to the front end to divert to the end screen.


        Parameters:

            event : dict
                Contains all the event information passed in.
        """
        result = event['who_won']
        g = Game.objects.get(lobby_code=self.lobby_code)
        g.winner = result

        # Checks if player has won or lost and sends points to player
        user = User.objects.get(email=self.scope['session']['email'])
        player = Player.objects.get(game=g, user=user)
        if player.seeker:
            team = "seeker"
        else:
            team = "hider"

        if result == team:
            user.points += 100
            user.save()
        else:
            user.points += 20
            user.save()
        g.save()

        self.send(text_data=json.dumps({
                'msg_type': 'end',
                'lobby_code': self.lobby_code
        }))

    # Checks if a current game should be aborted due to time limit
    def check_code(self, attempt_code):
        """Checks the hider code that the seeker inputs to see if it is valid.
        If it is then they have found the hider.


        Parameters:

            attempt_code : str
                The code to be validated.


        Returns:

            return : str
                The corresponding message to be displayed to the user.
        """

        game = Game.objects.filter(lobby_code=self.lobby_code).first()

        # Check that time isn't up or in hiding phase
        hiding_duration = game.hiding_time
        seeking_duration = game.seeking_time
        total_duration = hiding_duration + seeking_duration
        current_time = time.time()
        elapsed = current_time - game.game_start_time

        # Time is up
        if elapsed > total_duration:
            return "Time is up!"
        # Hiding phase is still on
        elif elapsed < hiding_duration:
            return "Stay still! The hiding phase is still active!"

        # Check if valid 4 digit hex code
        if (not re.match('^[A-Fa-f0-9]+$', attempt_code)) or len(attempt_code) != 4:
            return "Not a valid code! Please try again."

        # Check if player code exists and if it is already found
        matching_players = Player.objects.filter(game=game, hider_code=attempt_code)

        # Keep for None safety
        if matching_players:
            matched = matching_players.first()
            if matched.found:
                return "Player already found!"
            else:
                matched.found = True
                matched.save()
                self.check_found_hiders()
                return "You found " + matched.username

    def check_found_hiders(self):
        """Checks if there are any unfound hiders. If all hiders have been found,
        the game ends.
        """
        # Gets all hiders in the game with found = False
        game = Game.objects.filter(lobby_code=self.lobby_code).first()
        hiders = Player.objects.filter(game=game, seeker=False, found=False)

        if len(hiders):
            return

        # All hiders found so calls game_finish
        event = {
                'type': 'game_finish',
                'who_won': 'seeker'
            }

        async_to_sync(self.channel_layer.group_send)(
            self.lobby_code,
            event
        )


def check_if_player_inbounds(lobby_code, player_latitude, player_longitude):
    """Checks if a player is in bounds of the game or not. This is calculated using the
    latitude and longitude of the center of the game, as well as the radius of the game.


    Parameters:

        lobby_code : int
            The lobby code of the game to check.

        player_latitude : float
            The player's current latitude.

        player_longitude : float
            The player's current longitude.


    Returns:

        return : bool
            True or False depending on the result of the calculation.
    """
    game = Game.objects.get(lobby_code=lobby_code)

    # Get game radius and coordinates of game
    game_radius = game.radius
    lobby_latitude = game.lobby_latitude
    lobby_longitude = game.lobby_longitude

    # calculate player distance from centre of game
    dlon = player_longitude - lobby_longitude
    dlat = player_latitude - lobby_latitude
    a = math.sin(dlat/2)**2 + math.cos(lobby_latitude)*math.cos(player_latitude)*math.sin(dlon/2)**2
    c = 2*math.asin(math.sqrt(a))
    player_distance = 6371000*c

    # Compare player_distance to radius
    return player_distance < game_radius
