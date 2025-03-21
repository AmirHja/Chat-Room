from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User

class Room(models.Model):
    admin = models.ForeignKey(verbose_name=_("admin"), to=User, blank=False, null=True, related_name="room",
                              on_delete=models.SET(User.objects.get(username="DeletedAccount").id))
    name = models.CharField(_("name"), max_length=64, blank=False, null=False)
    description = models.TextField(_("description"), blank=True, null=True, max_length=128)
    created_at = models.DateTimeField(_("created"), auto_now_add=True)

    def __str__(self):
        return self.name

class PublicMessage(models.Model):
    sender = models.ForeignKey(verbose_name=_("sender"), to=User,
                               blank=False, null=False, related_name="sent_public_messages",
                               on_delete=models.SET(User.objects.get(username="DeletedAccount").id))
    message = models.TextField(verbose_name=_("message"), blank=False, null=False)
    room = models.ForeignKey(verbose_name=_("room"), to=Room, blank=False, null=False, related_name="room",
                                  on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name=_("created time"), auto_now_add=True)

    def __str__(self):
        return f"{self.sender} in room {self.room}: {self.message}"

class PrivateMessage(models.Model):
    sender = models.ForeignKey(verbose_name=_("sender"), to=User,
                               blank=False, null=False, related_name="sent_private_messages",
                               on_delete=models.SET(User.objects.get(username="DeletedAccount").id))
    receiver = models.ForeignKey(verbose_name=_("receiver"), to=User,
                                 blank=False, null=False, related_name="received_private_messages",
                                 on_delete=models.SET(User.objects.get(username="DeletedAccount").id))
    message = models.TextField(verbose_name=_("message"), blank=False, null=False)
    created_at = models.DateTimeField(verbose_name=_("created time"), auto_now_add=True)

    def __str__(self):
        return f"{self.sender} to {self.receiver}: {self.message}"
