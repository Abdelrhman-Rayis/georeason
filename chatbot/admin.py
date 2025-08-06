from django.contrib import admin
from .models import ChatSession, ChatMessage

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'user', 'model_choice', 'created_at', 'updated_at')
    list_filter = ('model_choice', 'created_at')
    search_fields = ('session_id', 'user__username')
    readonly_fields = ('session_id', 'created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('session', 'message_preview', 'response_preview', 'is_user_message', 'timestamp')
    list_filter = ('is_user_message', 'timestamp', 'session__model_choice')
    search_fields = ('message', 'response', 'session__session_id')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message'
    
    def response_preview(self, obj):
        return obj.response[:50] + '...' if len(obj.response) > 50 else obj.response
    response_preview.short_description = 'Response'
