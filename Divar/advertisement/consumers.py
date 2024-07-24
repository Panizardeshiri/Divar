from django.contrib.auth import get_user_model
from .models import *
from channels.generic.websocket import WebsocketConsumer

import json
from django.db.models import Q



User = get_user_model()


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # Extract the username from the URL
        username = self.scope['url_route']['kwargs'].get('username', None)
        category = self.scope['url_route']['kwargs'].get('category', None)
        ad_id = self.scope['url_route']['kwargs'].get('ad_id', None)
        # print(ad_id)
        # ad = Car.objects.get(id=ad_id)
        # print(ad)
        other_username = User.objects.get(username='moji')
        

        


    
        self.username = username
        self.room_name = f'room_{username}_{other_username.username}'
        self.room_group_name = f'chat_{username}_{other_username.username}'

            # Join the room group
        self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave the room group
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print('-----------------------', text_data_json)
        text = text_data_json.get('message', '')
        sender = User.objects.get(username='moji')
        print(text)
        category = self.scope['url_route']['kwargs'].get('category', None)
        ad_id = self.scope['url_route']['kwargs'].get('ad_id', None)
        print(ad_id)
        ad = Car.objects.get(id=ad_id)
        print(ad)
        if category == 'car':
            ad = Car.objects.get(id=ad_id)

            conversation = CarConversation.objects.filter(car_ad=ad, starter=sender).first()
            print(conversation)
            if conversation is None:
                conversation = CarConversation.objects.create(car_ad=ad, starter=sender)
            new_message = Message.objects.create(sender=sender, context=text)
            conversation.messages.add(new_message)
        
        if category == 'realestate':
            ad = RealEstate.objects.get(id=ad_id)

            conversation = RealEstateConversation.objects.filter(realestate_ad=ad, starter=sender).first()
            print(conversation)
            if conversation is None:
                conversation = RealEstateConversation.objects.create(realestate_ad=ad, starter=sender)
            new_message = Message.objects.create(sender=sender, context=text)
            conversation.messages.add(new_message)
        
        if category == 'other':
            ad = OthersAds.objects.get(id=ad_id)

            conversation = OtherConversation.objects.filter(other_ad=ad, starter=sender).first()
            print(conversation)
            if conversation is None:
                conversation = OtherConversation.objects.create(other_ad=ad, starter=sender)
            new_message = Message.objects.create(sender=sender, context=text)
            conversation.messages.add(new_message)
       

        # Send message to room group
        self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': text,
                'username': self.username
            }
        )

    def chat_message(self, event):
        message = event['message']
        username = event['username']
        print('******************', event)

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))