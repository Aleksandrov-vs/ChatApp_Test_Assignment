from django.db import models
from django.utils import timezone


class Token(models.Model):
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    access_expired_date = models.DateTimeField(default=timezone.now)
    refresh_expired_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "access_token obj"
