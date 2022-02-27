import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class PlayerConsumer(WebsocketConsumer):

    def connect(self):
        self.lobby_code = self.scope['url_route']['kwargs']['lobby_code']
        message = self.scope['session']['username'] + " has joined."

        async_to_sync(self.channel_layer.group_add)(
            self.lobby_code,
            self.channel_name
        )

        self.accept()

        async_to_sync(self.channel_layer.group_send)(
            self.lobby_code,
            {
                'type': 'lobby_event',
                'message': message
            }
        )

    def disconnect(self, close_code):
        message = self.scope['session']['username'] + " has left."

        async_to_sync(self.channel_layer.group_send)(
            self.lobby_code,
            {
                'type': 'lobby_event',
                'message': message
            }
        )

        async_to_sync(self.channel_layer.group_discard)(
            self.lobby_code,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        ready = text_data_json['ready']
        username = text_data_json['username']
        message = username + " is " + ready + "."

        async_to_sync(self.channel_layer.group_send)(
            self.lobby_code,
            {
                'type': 'lobby_event',
                'message': message
            }
        )

    def lobby_event(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'message': message
        }))
