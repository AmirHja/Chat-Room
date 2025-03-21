import random
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core import validators
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, is_staff, is_super, **extra_fields):
        """
        Create and save a sender with the given username and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError('Users must have an username')
        user = self.model(
            username=username,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_super,
            date_joined=now,
            **extra_fields
        )

        if password:
            user.set_password(password)

        user.save(using=self._db)
        return user

    def create_user(self, username=None, password=None, **extra_fields):
        if username is None:
            username = f"admin_{uuid.uuid4().hex[:8]}"

        return self._create_user(username, password, is_staff=False, is_super=False, **extra_fields)


    def create_superuser(self, username=None, password=None, **extra_fields):
        if username is None:
            username = f"admin_{uuid.uuid4().hex[:8]}"

        return self._create_user(username, password, is_staff=True, is_super=True, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, password and email are required. Other fields are optional.
    """
    username = models.CharField(
        verbose_name=_('username'),
        max_length=32,
        unique=True,
        help_text="Required. 4 to 32 characters. Letters, digits and @/./_ only. Starts with a letter",
        validators=[
            validators.RegexValidator(
                regex=r"^[a-zA-Z][a-zA-Z0-9@._]{3,}$",
                message=_("Enter a valid username."),
                code="Invalid username"
            )
        ],
        error_messages={
            'unique': _("A sender with that username already exists."),
        }
    )
    is_staff = models.BooleanField(
        verbose_name=_('staff status'),
        default=False,
        help_text=_('Designates whether the sender can log into this admin site.')
    )
    is_active = models.BooleanField(
        verbose_name=_('active status'),
        default=True,
        help_text=_(
            'Designates whether this sender should be treated as active.'
            'Unselect this instead of deleting accounts.'
        )
    )
    date_joined = models.DateTimeField(verbose_name=_('date joined'), default=timezone.now)
    last_seen = models.DateTimeField(verbose_name=_('last seen'), null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        db_table = 'users'
        verbose_name = _('sender')
        verbose_name_plural = _('users')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
