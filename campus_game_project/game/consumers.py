import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from game.models import Game, Player


class PlayerConsumer(WebsocketConsumer):

    # Behaviour when the user connects
    def connect(self):
        self.lobby_code = self.scope['url_route']['kwargs']['lobby_code']
        message = self.scope['session']['username'] + " has joined."

        # Adds the websocket to a group, named the lobby code
        async_to_sync(self.channel_layer.group_add)(
            self.lobby_code,
            self.channel_name
        )

        self.accept()

        players = []

        g = Game.objects.get(lobby_code=int(self.lobby_code))

        for y in Player.objects.filter(game=g):
            players.append({
                "username": y.username,
                "ready": y.ready
                })

        # Sends message to group
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
        message = self.scope['session']['username'] + " has left."

        # Sends message to group
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

        g = Game.objects.get(lobby_code=self.lobby_code)
        Player.objects.get(game=g, username=self.scope['session']['username']).delete()

        # Leaves the group
        async_to_sync(self.channel_layer.group_discard)(
            self.lobby_code,
            self.channel_name
        )

    # Behaviour when the websocket receives a message
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        ready = text_data_json['ready'].lower()
        username = text_data_json['username']
        message = username + " is " + ready + "."

        if ready == "unready":
            ready = False
        else:
            ready = True

        g = Game.objects.get(lobby_code=self.lobby_code)
        p = Player.objects.get(game=g, username=username)
        p.ready = ready
        p.save()

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
        message = event['message']
        username = event['username']
        ready = event['ready']

        self.send(text_data=json.dumps({
            'msg_type': 'ready',
            'message': message,
            'username': username,
            'ready': ready
        }))
