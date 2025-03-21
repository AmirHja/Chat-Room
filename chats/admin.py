from django.contrib import admin

from .models import *

@admin.register(PublicMessage)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["sender", "room", "created_at", "message"]
    raw_id_fields = ["sender", "room"]
    list_display_links = ["sender"]
    list_filter = ["created_at"]
    search_fields = ["sender", "message"]
    date_hierarchy = "created_at"

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "admin"]
    raw_id_fields = ["admin"]
    list_display_links = ["name"]
    list_filter = ["created_at"]
    search_fields = ["name", "admin"]
    date_hierarchy = "created_at"

@admin.register(PrivateMessage)
class PVAdmin(admin.ModelAdmin):
    list_display = ["sender", "receiver", "created_at", "message"]
    raw_id_fields = ["sender", "receiver"]
    list_display_links = ["sender"]
    list_filter = ["created_at"]
    search_fields = ["sender", "receiver", "message"]
    date_hierarchy = "created_at"