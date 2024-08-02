from django.contrib.auth import get_user_model
from .models import *
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from django.db.models import Q



User = get_user_model()


# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         # Extract the username from the URL
#         print('==========================222222============', self.scope['user'].id)
#         sender_id = self.scope['url_route']['kwargs'].get('user_id', None)
#         category = self.scope['url_route']['kwargs'].get('category', None)
#         ad_id = self.scope['url_route']['kwargs'].get('ad_id', None)
        
#         if category == 'car':
#             ad = Car.objects.get(id =ad_id )
#             receiver_id = ad.user.id
            
        
#         if category == 'realestate':
#             ad = RealEstate.objects.get(id =ad_id )
#             receiver_id = ad.user.id
            

#         if category == 'other':
#             ad = OthersAds.objects.get(id =ad_id )
#             receiver_id = ad.user.id
            
       
        

        
#         self.room_name = f'room_{sender_id}_{receiver_id}_{category}_{ad_id}'
#         print(f'room_name:{self.room_name}')
#         self.room_group_name = f'chat_{sender_id}_{receiver_id}_{category}_{ad_id}'
#         print(f'room_group_name:{self.room_group_name} ')

        
#         self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         self.accept()

#     def disconnect(self, close_code):
#         # Leave the room group
#         self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         print('-----------------------', text_data_json)
#         text = text_data_json.get('message', '')
#         message_sender = text_data_json.get('sender', '')
#         message_sender = User.objects.get(username=text_data_json.get('sender', ''))
#         # print(ms,'!!!####')

#         sender_id = self.scope['url_route']['kwargs'].get('user_id', None)
#         sender = User.objects.get(id=sender_id)
        
#         # conversation.messa
#         print(text)
#         category = self.scope['url_route']['kwargs'].get('category', None)
#         ad_id = self.scope['url_route']['kwargs'].get('ad_id', None)
        
#         if category == 'car':
#             ad = Car.objects.get(id=ad_id)

#             conversation = CarConversation.objects.filter(car_ad=ad, starter=sender).first()
#             print(conversation)
#             if conversation is None:
#                 conversation = CarConversation.objects.create(car_ad=ad, starter=sender)
#             new_message = Message.objects.create( sender=message_sender,context=text)
#             conversation.messages.add(new_message)
        
#         if category == 'realestate':
#             ad = RealEstate.objects.get(id=ad_id)

#             conversation = RealEstateConversation.objects.filter(realestate_ad=ad, starter=sender).first()
#             print(conversation)
#             if conversation is None:
#                 conversation = RealEstateConversation.objects.create(realestate_ad=ad, starter=sender)
#             new_message = Message.objects.create(sender=message_sender, context=text)
#             conversation.messages.add(new_message)
        
#         if category == 'other':
#             ad = OthersAds.objects.get(id=ad_id)

#             conversation = OtherConversation.objects.filter(other_ad=ad, starter=sender).first()
#             print(conversation)
#             if conversation is None:
#                 conversation = OtherConversation.objects.create(other_ad=ad, starter=sender)
#             new_message = Message.objects.create(sender= message_sender,context=text)
#             conversation.messages.add(new_message)
       

#         # Send message to room group
#         self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': text,
#                 # 'username': self.username
#             }
#         )

#     def chat_message(self, event):
#         message = event['message']
#         username = event['username']
#         print('******************', event)

#         # Send message to WebSocket
#         self.send(text_data=json.dumps({
#             'message': message,
#             'username': username
#         }))




class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.starter_user_id = self.scope['url_route']['kwargs']['user_id']
        self.category = self.scope['url_route']['kwargs']['category']
        self.ad_id = self.scope['url_route']['kwargs']['ad_id']

        # Fetch user and advertisement from the database
        self.starter_user   =           await self.get_user(self.starter_user_id)
        self.ad             =           await self.get_ad(self.category, self.ad_id)

        self.room_name = f"chat_{self.starter_user_id}_{self.category}_{self.ad_id}"
        self.room_group_name = f"chat_{self.starter_user_id}_{self.category}_{self.ad_id}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        text = text_data_json.get('message', '')
        message_sender = text_data_json.get('sender', '')
        message_sender = await self.get_user(message_sender)
        print('--------------------',message_sender.id)
        conversation = await self.get_conversation(self.category, self.ad, self.starter_user)
        print('$$$$$$$$$$$$$$$$$$$$',conversation)
        if conversation is None:
            conversation = await self.create_conversation(self.category, self.ad, self.starter_user)

        new_message = await self.create_message(text, message_sender, conversation)
        await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': text,
                    'sender': message_sender.username
                }
            )



    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender  # Include sender in the response
        }))

    @database_sync_to_async
    def get_user(self, user):
        try:
            return User.objects.get(id=user)
        except:
            return User.objects.get(username=user)

    @database_sync_to_async
    def get_ad(self, category, ad_id):
        if category.lower() == 'car':
            return Car.objects.get(id=ad_id)
        if category.lower() == 'realestate':
            return RealEstate.objects.get(id=ad_id)
        if category.lower() == 'other':
            return OthersAds.objects.get(id=ad_id)
        
    @database_sync_to_async
    def get_conversation(self,category, ad, user):
        if category.lower() == 'car':
            return CarConversation.objects.filter(ad=ad, starter=user).first()
        if category.lower() == 'realestate':
            return RealEstateConversation.objects.filter(ad=ad, starter=user).first()
        if category.lower() == 'other':
            return OtherConversation.objects.filter(ad=ad, starter=user).first()
        
    @database_sync_to_async
    def create_conversation(self, category, ad, user):
        if category.lower() == 'car':
            return CarConversation.objects.create(ad=ad, starter=user)
        if category.lower() == 'realestate':
            return RealEstateConversation.objects.create(ad=ad, starter=user)
        if category.lower() == 'other':
            return OtherConversation.objects.create(ad=ad, starter=user)
        
    @database_sync_to_async
    def create_message(self, message, sender, conversation):
        new_message = Message.objects.create(sender= sender, context=message)
        conversation.messages.add(new_message)
        conversation.save()
        return new_message


        