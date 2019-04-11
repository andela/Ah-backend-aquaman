from django.db import models
from django.db.models.signals import post_save
from authors.apps.authentication.models import User
from datetime import datetime


class Profile(models.Model):
    """
      Creates the profile model that will hold user profiles
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=120, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    image = models.URLField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    @property
    def owner(self):
        return self.user


def user_post_save_receiver(instance, created, *args, **kwargs):
    """
    Handle creating the profile when a user finishes
    the signup process
    """
    if created:
        Profile.objects.get_or_create(
            user=instance,
        )


post_save.connect(user_post_save_receiver, sender=User)


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE)
    followed = models.ForeignKey(Profile, on_delete=models.CASCADE)
    followed_at = models.DateTimeField(default=datetime.now, blank=True)
