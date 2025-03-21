from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User

class Room(models.Model):
    admin = models.ForeignKey(verbose_name=_("admin"), to=User, blank=False, null=True,
                              on_delete=models.SET("Deleted Account"))
    name = models.CharField(_("name"), max_length=64, blank=False, null=False)
    description = models.TextField(_("description"), blank=True, null=True, max_length=128)
    created_at = models.DateTimeField(_("created"), auto_now_add=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(verbose_name=_("user"), to=User, blank=False, null=False,
                             on_delete=models.SET("Deleted Account"))
    message = models.TextField(verbose_name=_("message"), blank=False, null=False)
    room = models.ForeignKey(verbose_name=_("room"), to=Room, blank=False, null=False,
                                  on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name=_("created time"), auto_now_add=True)

    def __str__(self):
        return f"{self.user}: {self.message}"