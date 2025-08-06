from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.home, name='home'),
    path('chat/', views.chat, name='chat'),
    path('history/', views.get_chat_history, name='history'),
] 