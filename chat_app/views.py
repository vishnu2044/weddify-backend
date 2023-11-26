from rest_framework import generics, status
from .serializer import MessageSerializer ,ChatListSerializer, ProfileSerializer
from .models import ChatMessage
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response


class PrevieousMessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        user1 = int(self.kwargs['user1'])
        user2 = int(self.kwargs['user2'])

        thread_suffix = f"{user1}_{user2}" if user1 > user2 else f"{user2}_{user1}"
        thread_name = 'chat_'+thread_suffix
        queryset = ChatMessage.objects.filter(
            thread_name=thread_name
        )

        return queryset
    

class GetUserDetails(APIView):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        serializer = ProfileSerializer(user)
        return Response(serializer.data)

class ChatListView(generics.ListAPIView):
    serializer_class = ChatListSerializer
    user_id = None

    def get_queryset(self):
        user_id = int(self.kwargs['user_id'])
        distinct_senders = ChatMessage.objects.filter(reciever__id = user_id).values('sender__username').distinct()
        distinct_receivers = ChatMessage.objects.filter(sender__id = user_id).values('reciever__username').distinct()

        distinct_usernames = set()
        for entry in distinct_senders:
            distinct_usernames.add(entry['sender__username'])

        for entry in distinct_receivers:
            distinct_usernames.add(entry['reciever__username'])

        return distinct_usernames
        
    def get_serializer_context(self):
        context = super(ChatListView, self).get_serializer_context()
        user_id = int(self.kwargs['user_id'])
        context.update({'user_id': user_id})
        return context




class UpdateMessageStatus(APIView):
    def post(self, reqeust):
        try:
            user_id = reqeust.data.get('user_id') 
            sender_id  =reqeust.data.get('sender_id')

            t = ChatMessage.objects.filter(sender = sender_id, reciever = user_id, is_read = False)
            t.update(is_read = True)
            print("messages updated successfully !!!!!!!!!!!!!!!!!!!!!")
            return Response(data={'message': 'success'}, status= status.HTTP_200_OK)
        
        except :
            return Response(status= status.HTTP_400_BAD_REQUEST)