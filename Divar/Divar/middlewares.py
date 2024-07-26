# middlewares.py

from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
import jwt

User = get_user_model()

class JWTAuthMiddleware(BaseMiddleware):
    """
    Custom middleware to authenticate users using JWT token in the WebSocket scope.
    """

    @database_sync_to_async
    def get_user(self, validated_token):
        try:
            user_id = validated_token.get('user_id')
            user = User.objects.get(id=user_id)
            return user
        except User.DoesNotExist:
            return AnonymousUser()

    async def __call__(self, scope, receive, send):
        # Get the token from the headers
        headers = dict(scope['headers'])
        if b'authorization' in headers:
            try:
                token_name, token_key = headers[b'authorization'].decode().split()
                if token_name == 'Bearer':
                    # Decode the token and fetch the user
                    validated_token = UntypedToken(token_key)
                    scope['user'] = await self.get_user(validated_token)
            except (InvalidToken, TokenError, ValueError):
                scope['user'] = AnonymousUser()
        else:
            scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)
