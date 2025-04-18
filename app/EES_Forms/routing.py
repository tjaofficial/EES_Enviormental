from django.urls import re_path # type: ignore
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/notifications/(?P<facility>\w+)/$", consumers.NotifConsumer.as_asgi())
]