from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render

from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Chat, Message
from django.db.models import Q

class ChatListView(LoginRequiredMixin, ListView):
    model = Chat
    template_name = "chat/chat_list.html"
    context_object_name = "Chats"
    def get_queryset(self):
        chats = Chat.objects.filter(Q(user_1=self.request.user) | Q(user_2=self.request.user))
        return chats
    
class ChatDetailView(LoginRequiredMixin, DetailView):
    model = Chat
    template_name = "chat/chat_detail.html"
    context_object_name = "Chat_Info"