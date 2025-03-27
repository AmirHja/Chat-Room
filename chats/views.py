from django.shortcuts import render, get_object_or_404
from django.template.context_processors import request
from django.http import JsonResponse

from .models import PublicMessage, Room, PrivateMessage
from users.models import User



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
        user = request.user
        chat_partners = User.objects.filter(
            id__in=PrivateMessage.objects.filter(receiver=user).values_list('sender', flat=True)
        ) | User.objects.filter(
            id__in=PrivateMessage.objects.filter(sender=user).values_list('receiver', flat=True)
        )
        return render(request, "chats/private_message.html", {"chat_partners": chat_partners})
    else:
        return render(request, 'chats/forbidden.html')

def load_message(request, username):
    if request.user.is_authenticated:
        user = request.user
        partner = get_object_or_404(User, username=username)

        messages = PrivateMessage.objects.filter(
            sender__in=[user, partner],
            receiver__in=[user, partner]
        ).order_by("created_at")

        messages_data = [
            {"sender": msg.sender.username, "message": msg.message,
             "timestamp": msg.created_at.strftime("%Y-%m-%d %H:%M")}
            for msg in messages
        ]
        return JsonResponse({"messages": messages_data})
    else:
        return render(request, 'chats/forbidden.html')

def send_message(request):
    if request.method == "POST":
        sender = request.user
        receiver_username = request.POST.get("receiver")
        message_content = request.POST.get("message", "").strip()

        if not message_content or not receiver_username:
            return JsonResponse({"error": "message is not valid"}, status=400)

        try:
            receiver = User.objects.get(username=receiver_username)
        except User.DoesNotExist:
            return JsonResponse({"error": "user is not found!"}, status=404)

        message = PrivateMessage.objects.create(sender=sender, receiver=receiver, message=message_content)

        return JsonResponse({
            "sender": sender.username,
            "message": message.message,
            "timestamp": message.created_at.strftime("%Y-%m-%d %H:%M")
        })
