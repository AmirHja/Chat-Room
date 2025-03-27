from django.shortcuts import render, get_object_or_404
from .models import PublicMessage, Room, PrivateMessage



def public_message(request):
    room_name = "Test-room"
    if request.user.is_authenticated:
        room = get_object_or_404(Room, name=room_name)
        messages = PublicMessage.objects.filter(room=room).order_by("created_at")

        return render(request, "chats/public_message.html", {
            "room_name": room.name,
            "messages": messages
        })
    else:
        return render(request, 'chats/forbidden.html')

def private_message(request):
    if request.user.is_authenticated:
        messages = PrivateMessage.objects.filter(receiver=request.user).order_by("created_at")
        return render(request, "chats/private_message.html", {"messages": messages})
    else:
        return render(request, 'chats/forbidden.html')