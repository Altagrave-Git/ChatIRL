from django.urls import re_path
from . import consumers


websocket_urlpatterns = [
    re_path(r'ws/room/(?P<room_name>.*)/$', consumers.ChatRoomConsumer.as_asgi()),
    re_path(r'ws/private/(?P<username>.*)/$', consumers.PrivateChatConsumer.as_asgi()),
]