import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatMessage
from django.contrib.auth.models import User


class PersonalChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        current_user_id = int(self.scope['query_string'])
        other_user_id = self.scope['url_route']['kwargs']['id']

        self.room_name = (
            f"{current_user_id}_{other_user_id}"
            if int(current_user_id) > int(other_user_id)
            else f"{other_user_id}_{current_user_id}"
        )
        print("::::::::::::::::::::consumer id", current_user_id)
        self.room_group_name = f'chat_{self.room_name}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await super().disconnect(close_code)

    async def receive(self, text_data=None, bytes_data = None):
        data = json.loads(text_data)
        print("^^^^^^^^^^^^^^^^^^^^^^",data, '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        message = data['message']
        print(message)
        sender_username =  data['senderUsername']
        reciever_username = data['receiver_username']
        print('receiver name >>>>>>>>>', reciever_username)
        print('sender name >>>>>>>>>', sender_username)
        

        await self.save_message(
            sender_username = sender_username, 
            reciever_username = reciever_username, 
            message = message,
            thread_name = self.room_group_name
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type' : 'chat_message',
                'message' : message,
                'senderUsername' : sender_username
            }
        )
    
    async def chat_message(self, event):
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(">>>>>>>>>>>>> chat message function working")
        message = event['message']
        username = event['senderUsername']

        await self.send(
            text_data= json.dumps(
                {
                    'message' : message,
                    'senderUsername': username,
                    'messages' : message
                }
            )
        )


        
    @database_sync_to_async
    def get_messages(self):
        messages = []
        for instance in ChatMessage.objects.filter(thread_name = self.room_group_name):
            messages = ChatMessage(instance).data 
        return messages
    
    @database_sync_to_async
    def save_message(self, sender_username, reciever_username, message, thread_name):
        sender_instance = User.objects.get(username = sender_username)
        receiver_instance = User.objects.get(username = reciever_username)
        print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print(sender_username, 'sender_username>>>>>>>>>>>>>>>>>>>>')
        print(reciever_username, 'receiver_username>>>>>>>>>>>>>>>>')
        print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        ChatMessage.objects.create(sender = sender_instance, reciever = receiver_instance, message=message, thread_name = thread_name)

    
