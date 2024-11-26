from django.urls import path
from .views import RoomChatHistory, SendMessage, ChatHistory

urlpatterns = [
    path('send/', SendMessage.as_view(), name='send_message'), # Đường dẫn của API, đến view(API) tương ứng
    path('history/', ChatHistory.as_view(), name='chat_history'),
    path('room/<str:room_name>/history/', RoomChatHistory.as_view(), name='room_chat_history'),
]
