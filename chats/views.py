from django.http.response  import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message, Room



def chat_room(request, room_name):
    if request.user.is_authenticated:
        room = get_object_or_404(Room, name=room_name)
        messages = Message.objects.filter(room=room).order_by("created_at")

        return render(request, "chats/chat_room.html", {
            "room_name": room.name,
            "messages": messages
        })
    else:
        return render(request, 'chats/forbidden.html')
