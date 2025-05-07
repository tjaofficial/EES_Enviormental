from django.urls import re_path # type: ignore
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/notifications/$', consumers.NotifConsumer.as_asgi())
]