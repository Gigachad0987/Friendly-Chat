from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    user_1 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='Chats_1')
    user_2 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='Chats_2')
    created_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints=[models.UniqueConstraint(fields=['user_1', 'user_2'],name='unique_chat_user_1_user_2')]
        ordering=['-created_time']
    def save(self, *args, **kwargs):
        if self.user_1 == self.user_2:
            raise ValueError('Chat cannot be with yourself.')
        if self.user_1.id > self.user_2.id:
            self.user_1, self.user_2 = self.user_2, self.user_1
        super().save(*args, **kwargs)
    
class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='Messages')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='Messages')
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    class Meta():
        ordering = ['created_time']