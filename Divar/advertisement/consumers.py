from django.contrib.auth import get_user_model

from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json


User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # user = self.scope['username']
        # print(user,'__________%%%%%%%%%%%')
        # current_user = await self.get_user(username = self.request.user )
        # print(current_user,'__________%%%%%%%%%%%')
        other_user = self.scope['url_route']['kwargs']['username']
        ad_id = self.scope['url_route']['kwargs']['ad_id']
        print(other_user,'__________%%%%%%%%%%%')
        print(ad_id,'__________%%%%%%%%%%%')

        self.room_group_name = f"{other_user}-{ad_id}"
        print(self.room_group_name,'__________%%%%%%%%%%%')

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name)
        
        await self.accept()



        # print(f"User: {self.scope['user']}")

        # self.username = self.scope['user']
        # current_user = await self.get_user(username = self.username )
        # print(current_user,'@@@@@@@@@@@@@@@@@@')
        


    # async def disconnect(self, close_code):
    #     await self.channel_layer.group_discard(
    #         self.room_group_name,
    #         self.channel_name
    #     )



    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(f"Received message: {message}")

        # self.send(text_data=json.dumps({
        #     'message': message
        # }))

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'message': message
            })
        
        # print(f"Received message: {message}")


    @database_sync_to_async
    def get_user(self, username):
        return User.objects.filter(username=username).first()
