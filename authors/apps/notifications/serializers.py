from rest_framework import serializers
from .models import Notification, NotificationSettings
from ..authentication.serializers import UserSerializer


class NotifcationSettingsSerializers(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = NotificationSettings
        fields = ('user', 'email_notifications', 'in_app_notifications')

    def create(self, validated_data):
        return NotificationSettings.objects.create(**validated_data)


class NotifcationSerializers(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ('title', 'slug', 'notification', 'status', 'created_at')

        read_only_fields = (
            'author',
            'slug',
            'status',
            'created_at',
        )
