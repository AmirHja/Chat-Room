import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

import chats.routing

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'computerNetworkProject.settings')
#
# application = get_asgi_application()


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "computerNetworkProject.settings")


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chats.routing.websocket_urlpatterns
        )
    ),
})