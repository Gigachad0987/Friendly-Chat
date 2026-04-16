from typing import Any
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Chat, Message
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import login

class ChatListView(LoginRequiredMixin, ListView):
    model = Chat
    template_name = "chat/chat_list.html"
    context_object_name = "Chats"
    def get_queryset(self):
        chat_name = self.request.GET.get('chat_name')
        if chat_name:
            chat_name = chat_name.strip()
            chats = Chat.objects.filter(Q(user_1=self.request.user, user_2__username__icontains=chat_name ) | Q(user_2=self.request.user, user_1__username__icontains=chat_name))
            return chats
        chats = Chat.objects.filter(Q(user_1=self.request.user) | Q(user_2=self.request.user))
        return chats
    
    
class ChatDetailView(LoginRequiredMixin, DetailView):
    model = Chat
    template_name = "chat/chat_detail.html"
    context_object_name = "Chat_Info"
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        chat_name = self.request.GET.get('chat_name')
        if chat_name:
            chat_name = chat_name.strip()
            chats = Chat.objects.filter(Q(user_1=self.request.user, user_2__username__icontains=chat_name ) | Q(user_2=self.request.user, user_1__username__icontains=chat_name))
        else:
            chats = Chat.objects.filter(Q(user_1=self.request.user) | Q(user_2=self.request.user))
        context["chats"] = chats
        return context
    
class CreateMessageView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ["text"]
    def get_success_url(self) -> str:
        return reverse("ChatInfo", kwargs={"pk":self.kwargs["pk"]})
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.sender=self.request.user
        pk = self.kwargs["pk"]
        chat = Chat.objects.get(pk=pk)
        form.instance.chat=chat
        return super().form_valid(form)
    
class UserRegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('ChatList')
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)