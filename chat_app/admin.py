from django.contrib import admin
from chat_app.models import ChatMessage

# Register your models here.
class ChatMessageAdmin(admin.ModelAdmin):
    list_editable = ['is_read']
    list_display = ['sender', 'reciever', 'message', 'is_read', 'date' ] 

admin.site.register(ChatMessage, ChatMessageAdmin)