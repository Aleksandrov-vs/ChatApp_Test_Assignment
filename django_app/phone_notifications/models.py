import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Mailing(UUIDMixin, TimeStampedMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(
        _('notification message'),
        null=False
    )

    def __str__(self):
        return self.message


class SendStatus(models.TextChoices):
    NEW = 'new', _('New')
    SENT = 'sent', _('Sent')
    DELIVERED = 'delivered', _('Delivered')
    READ = 'read', _('Read')
    ERR = 'err', _('Error')


class PhoneNotification(UUIDMixin, TimeStampedMixin):
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name='phone_notification'
    )
    number = PhoneNumberField(_('phone number'), blank=False)
    send_status = models.TextField(
        _('send status'),
        choices=SendStatus.choices,
        default=SendStatus.NEW,
        null=False
    )
    err_text = models.TextField(default='')

    def __str__(self):
        return self.number
