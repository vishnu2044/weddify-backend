from django.db import models
from django.contrib.auth.models import User
from user_accounts.models import UserProfile

# Create your models here.

class ChatMessage(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reciever')

    message = models.CharField(max_length=1000)
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    thread_name = models.CharField(null=True, blank=True, max_length=200)

    class Meta:
        ordering = ['date']

    def __str__(self) -> str:
        return f'{self.sender} - {self.reciever}'
    
    
class MessageRequest(models.Model):
    thread_name = models.CharField(null=True,blank=True, max_length=200)
    is_accepted = models.BooleanField(default=True)