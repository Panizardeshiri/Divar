import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from advertisement.routing import websocket_urlpatterns
from channels.auth import AuthMiddlewareStack
# from channels.sessions import SessionMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Divar.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
   { 
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack((URLRouter(websocket_urlpatterns)))
        
    }
)