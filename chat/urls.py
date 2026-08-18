from django.urls import path
from chat import views

urlpatterns = [
    path('chat/', views.chat_list_view, name='chat_list'),
    path('chat/<int:receiver_id>/', views.chat_room_view, name='chat_room'),
    path('chat/<int:receiver_id>/get/', views.get_messages, name='get_messages'),
    path('chat/<int:receiver_id>/send/', views.send_message, name='send_message'),
]