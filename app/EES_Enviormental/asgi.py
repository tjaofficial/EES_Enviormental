"""
ASGI config for EES_Enviormental project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import EES_Forms.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EES_Enviormental.settings')

from . import urls

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    # 'websocket': URLRouter(urls.websocket_urlpatterns)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            EES_Forms.routing.websocket_urlpatterns
        )
    )
})
