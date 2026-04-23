from django.urls import path
from . import views

urlpatterns=[
    path("", views.ChatListView.as_view(), name="ChatList"),
    path("chat/<int:pk>", views.ChatDetailView.as_view(), name="ChatInfo"),
    path("chat/<int:pk>/message", views.CreateMessageView.as_view(), name="MessageCreate"),
    path("register/", views.UserRegisterView.as_view(), name='Register'),
    path("user_search/", views.UserSearchView.as_view(), name='UserSearch'),
]