from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserListCreateAPIView.as_view(), name='user-list-create'),
    path('conversations/', views.ConversationListCreateAPIView.as_view(), name='conversation-list-create'),
    path('messages/', views.MessageListCreateAPIView.as_view(), name='message-list-create'),
]