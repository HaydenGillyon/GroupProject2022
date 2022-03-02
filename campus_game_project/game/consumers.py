from django.utils import timezone
import pytz
from datetime import datetime
import re
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from game.models import Game, Player
from random import randint


class PlayerConsumer(WebsocketConsumer):

    # Behaviour when the user connects
    def connect(self):
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
        g = Game.objects.get(lobby_code=int(self.lobby_code))
        for y in Player.objects.filter(game=g):
            players.append({
                "username": y.username,
                "ready": y.ready
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

    # Behaviour when the user disconnects
    def disconnect(self, close_code):

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
            g = Game.objects.get(lobby_code=self.lobby_code)
            Player.objects.get(game=g, username=self.scope['session']['username']).delete()
            g.player_num -= 1
            g.save()

        # Leaves the group
        async_to_sync(self.channel_layer.group_discard)(
            self.lobby_code,
            self.channel_name
        )

    # Behaviour when the websocket receives a message
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json['msg_type'] == "playing":
            self.scope['session']['playing'] = True
        elif text_data_json['msg_type'] == "ready":
            ready = text_data_json['ready'].lower()
            username = text_data_json['username']
            message = username + " is " + ready + "."

            if ready == "unready":
                ready = False
            else:
                ready = True

            # Sets the player to ready
            g = Game.objects.get(lobby_code=self.lobby_code)
            p = Player.objects.get(game=g, username=username)
            p.ready = ready
            p.save()

            if g.all_ready() and g.player_num > 1:
                players = Player.objects.filter(game=g)
                p = players[randint(0, len(players)-1)]
                p.seeker = True
                p.save()

                g.game_start_time = timezone.now()

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

    # A user joins or leaves
    def lobby_event(self, event):
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

    # A user readys or unreadys
    def ready_event(self, event):
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
        self.send(text_data=json.dumps({
            'msg_type': 'start'
        }))


class GameConsumer(WebsocketConsumer):

    # Behaviour when the user connects
    def connect(self):
        self.lobby_code = self.scope['url_route']['kwargs']['lobby_code']
        self.username = self.scope['session']['username']

        # Adds the websocket to a group, named the lobby code
        async_to_sync(self.channel_layer.group_add)(
            self.lobby_code,
            self.channel_name
        )

        self.accept()

    # Behaviour when the user disconnects
    def disconnect(self, close_code):
        # Leaves the group
        async_to_sync(self.channel_layer.group_discard)(
            self.lobby_code,
            self.channel_name
        )
        # Deletes the user from the database
        g = Game.objects.get(lobby_code=self.lobby_code)
        Player.objects.get(game=g, username=self.scope['session']['username']).delete()
        g.player_num -= 1
        g.save()

    # Behaviour when the websocket receives a message
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json['msg_type'] == 'hider_code_attempt':
            result = self.check_code(text_data_json['attempt_code'])
            self.send(text_data=json.dumps({
                'msg_type': 'code_result',
                'result': result,
            }))
        elif text_data_json['msg_type'] == 'seeking_over':
            # Hiders won
            # Sends message to group to call game_finish
            event = {
                    'type': 'game_finish',
                    'who_won': 'hiders'
                }
            async_to_sync(self.channel_layer.group_send)(
                self.lobby_code,
                event
            )

    # Final method that will be called upon the game finishing
    def game_finish(self, event):
        # IMPLEMENT POST-GAME PAGE SWITCH FROM HERE
        print("FINISH")
        pass

    def check_code(self, attempt_code):
        game = Game.objects.filter(lobby_code=self.lobby_code).first()
        # Check that time isn't up or in hiding phase
        hiding_duration = 60000
        seeking_duration = 600000
        total_duration = hiding_duration + seeking_duration
        current_time = timezone.now()
        epoch = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
        time_ms = int((current_time - epoch).total_seconds() * 1000.0)
        game_start_time_ms = int((game.game_start_time - epoch).total_seconds() * 1000.0)
        elapsed = time_ms - game_start_time_ms

        if elapsed > total_duration:
            # Time is up
            return "Time is up!"
        elif elapsed < hiding_duration:
            # Hiding phase is still on
            return "Stay still! The hiding phase is still active!"

        # Check if valid 4 digit hex code
        if not re.match('^[A-Fa-f0-9]+$', attempt_code) or len(attempt_code) != 4:
            return "Not a valid code! Please try again."

        # Check if player code exists and if it is already found
        matching_players = Player.objects.filter(game=game, hider_code=attempt_code)
        if matching_players:    # Keep for None safety
            matched = matching_players.first()
            if matched.found:
                return "Player already found!"
            else:
                matched.found = True
                matched.save()
                self.check_found_hiders()
                return "You found " + matched.username

    def check_found_hiders(self):
        game = Game.objects.filter(lobby_code=self.lobby_code).first()
        hiders = Player.objects.filter(game=game, seeker=False, found=False)
        if len(hiders):
            return
        # All found so seeker wins
        # Sends message to group to call game_finish
        event = {
                'type': 'game_finish',
                'who_won': 'seeker'
            }
        async_to_sync(self.channel_layer.group_send)(
            self.lobby_code,
            event
        )
