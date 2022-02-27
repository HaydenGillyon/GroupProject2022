from aiohttp import WebSocketError
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/game/(?P<lobby_code>\w+)/$', consumers.PlayerConsumer.as_asgi()),
]