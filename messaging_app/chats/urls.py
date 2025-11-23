from django.urls import path
from . import views

urlpatterns = [
    path('', views.ChatListCreateAPIView.as_view(), name='chat-list-create'),
]