from django.urls import path
from .views import public_message, private_message

urlpatterns = [

    path("Test-room/", public_message, name="chat_room"),
    path("dm/", private_message, name="direct_messages")
]