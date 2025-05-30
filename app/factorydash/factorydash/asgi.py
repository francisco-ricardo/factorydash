"""
ASGI config for factorydash project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import monitoring.routing
from typing import Any


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'factorydash.settings')

#application = get_asgi_application()

application: Any = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(monitoring.routing.websocket_urlpatterns)
    ),
})