from django.db import models
from ..authentication.models import User

# Create your models here.


class NotificationSettings(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_notificationsettings"
    )
    email_notifications = models.BooleanField(default=True)
    in_app_notifications = models.BooleanField(default=True)


class Notification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_notifications"
    )
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    notification = models.TextField()
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
