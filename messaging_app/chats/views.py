from rest_framework import generics
from .models import Chat
from .serializers import ChatSerializer

class ChatListCreateAPIView(generics.ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer