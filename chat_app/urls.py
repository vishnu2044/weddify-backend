from django.urls import path
from . import views


urlpatterns = [
    path('chat-list/<int:user_id>/', views.ChatListView.as_view()),
    path('get-userdetails/<int:user_id>/', views.GetUserDetails.as_view(), name='user_details'),
    path('user-previous-chats/<int:user1>/<int:user2>/', views.PrevieousMessagesView.as_view()),

]
