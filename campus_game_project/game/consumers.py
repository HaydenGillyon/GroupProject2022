import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


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

        # Sends message to group
        async_to_sync(self.channel_layer.group_send)(
            self.lobby_code,
            {
                'type': 'lobby_event',
                'message': message
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
                'message': message
            }
        )

        # Leaves the group
        async_to_sync(self.channel_layer.group_discard)(
            self.lobby_code,
            self.channel_name
        )

    # Behaviour when the websocket receives a message
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        ready = text_data_json['ready']
        username = text_data_json['username']
        message = username + " is " + ready + "."

        # Sends message to group
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
