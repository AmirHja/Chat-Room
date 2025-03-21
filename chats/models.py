from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User


class Message(models.Model):
    user = models.ForeignKey(verbose_name=_('user'), to=User, blank=False, null=False,
                             on_delete=models.SET("Deleted Account"))
    message = models.TextField(verbose_name=_("message"), blank=False, null=False)
    created_at = models.DateTimeField(verbose_name=_("created time"), auto_now_add=True)

    def __str__(self):
        return f"{self.user}: {self.message}"