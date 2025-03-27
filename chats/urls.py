from django.urls import path
from .views import public_message, private_message, load_message, send_message

urlpatterns = [

    path("Test-room/", public_message, name="chat_room"),
    path("dm/", private_message, name="direct_messages"),
    path("load_messages/<str:username>/", load_message, name="load_message"),
    path('send_message/', send_message, name='send_message'),
]