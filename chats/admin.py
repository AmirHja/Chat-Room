from django.contrib import admin

from .models import *

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'message']
    raw_id_fields = ['user']
    list_display_links = ['user']
    list_filter = ['created_at']
    search_fields = ['user', 'message']
    date_hierarchy = 'created_at'
