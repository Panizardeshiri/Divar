from django.contrib.auth import get_user_model
from .models import *
from channels.generic.websocket import WebsocketConsumer

import json
from django.db.models import Q



User = get_user_model()


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # Extract the username from the URL
        print('==========================222222============', self.scope['user'].id)
        sender_id = self.scope['url_route']['kwargs'].get('user_id', None)
        category = self.scope['url_route']['kwargs'].get('category', None)
        ad_id = self.scope['url_route']['kwargs'].get('ad_id', None)
        
        if category == 'car':
            ad = Car.objects.get(id =ad_id )
            receiver_id = ad.user.id
            
        
        if category == 'realestate':
            ad = RealEstate.objects.get(id =ad_id )
            receiver_id = ad.user.id
            

        if category == 'other':
            ad = OthersAds.objects.get(id =ad_id )
            receiver_id = ad.user.id
            
       
        

        
        self.room_name = f'room_{sender_id}_{receiver_id}_{category}_{ad_id}'
        print(f'room_name:{self.room_name}')
        self.room_group_name = f'chat_{sender_id}_{receiver_id}_{category}_{ad_id}'
        print(f'room_group_name:{self.room_group_name} ')

        
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
        message_sender = text_data_json.get('sender', '')
        message_sender = User.objects.get(username=text_data_json.get('sender', ''))
        # print(ms,'!!!####')

        sender_id = self.scope['url_route']['kwargs'].get('user_id', None)
        sender = User.objects.get(id=sender_id)
        
        # conversation.messa
        print(text)
        category = self.scope['url_route']['kwargs'].get('category', None)
        ad_id = self.scope['url_route']['kwargs'].get('ad_id', None)
        
        if category == 'car':
            ad = Car.objects.get(id=ad_id)

            conversation = CarConversation.objects.filter(car_ad=ad, starter=sender).first()
            print(conversation)
            if conversation is None:
                conversation = CarConversation.objects.create(car_ad=ad, starter=sender)
            new_message = Message.objects.create( sender=message_sender,context=text)
            conversation.messages.add(new_message)
        
        if category == 'realestate':
            ad = RealEstate.objects.get(id=ad_id)

            conversation = RealEstateConversation.objects.filter(realestate_ad=ad, starter=sender).first()
            print(conversation)
            if conversation is None:
                conversation = RealEstateConversation.objects.create(realestate_ad=ad, starter=sender)
            new_message = Message.objects.create(sender=message_sender, context=text)
            conversation.messages.add(new_message)
        
        if category == 'other':
            ad = OthersAds.objects.get(id=ad_id)

            conversation = OtherConversation.objects.filter(other_ad=ad, starter=sender).first()
            print(conversation)
            if conversation is None:
                conversation = OtherConversation.objects.create(other_ad=ad, starter=sender)
            new_message = Message.objects.create(sender= message_sender,context=text)
            conversation.messages.add(new_message)
       

        # Send message to room group
        self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': text,
                # 'username': self.username
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