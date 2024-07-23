from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/chat/conversations/<str:username>/<int:ad_id>/", consumers.ChatConsumer.as_asgi()),
]