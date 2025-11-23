from rest_framework import serializers
from .models import User, Conversation, Message

# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'role']


# Message serializer
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)  # nested user info

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']


# Conversation serializer
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)  # nested users
    messages = MessageSerializer(many=True, read_only=True)   # nested messages in conversation

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']
