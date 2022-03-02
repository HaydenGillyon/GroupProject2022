from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/game/(?P<lobby_code>\w+)/$', consumers.PlayerConsumer.as_asgi()),
    re_path(r'ws/game/running/(?P<lobby_code>\w+)/$', consumers.GameConsumer.as_asgi()),
]
