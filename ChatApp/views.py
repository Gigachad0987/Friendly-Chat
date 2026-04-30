from typing import Any
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Chat, Message
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User



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
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        messages.error(self.request, "The message can't be empty")
        pk = self.kwargs["pk"]
        return redirect("ChatInfo", pk=pk)
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
    
class UserSearchView(ListView):
    model = User
    template_name = "chat/user_search.html"
    context_object_name = "Users"
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["chats"] = Chat.objects.filter(Q(user_1=self.request.user) | Q(user_2=self.request.user))
        return context
    def get_queryset(self) -> QuerySet[Any]:
        user_name = self.request.GET.get("UserName", "").strip()
        users = User.objects.exclude(pk = self.request.user.pk)
        if user_name:
            users = users.filter(username__contains= user_name)
        else:
            users = users.none()
        return users
    
class CreateChatView(View):
    def get(self, request, pk):
        other_user = User.objects.get(pk=pk)
        if request.user.id < other_user.id:
            user_1, user_2 = request.user, other_user
        else:
            user_1, user_2 = other_user, request.user
            
        new_chat, _ = Chat.objects.get_or_create(user_1 = user_1, user_2 = user_2)
        return redirect("ChatInfo", pk=new_chat.pk)
    
class DeleteChatView(View):
    def post(self, request, pk):
        chat = Chat.objects.get(pk=pk)
        chat.delete()
        return redirect("ChatList")
        