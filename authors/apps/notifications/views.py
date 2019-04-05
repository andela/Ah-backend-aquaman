from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
from rest_framework import (
    generics,
    permissions,
    response,
    status,
)
from ..authentication.models import User
from .serializers import NotifcationSerializers, NotifcationSettingsSerializers
from .models import NotificationSettings, Notification
from .utils import NotificationCheck


class NotificationsRetriveAPIView(generics.GenericAPIView):
    serializer_class = NotifcationSerializers
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        user = User.objects.filter(email=request.user.email).first()
        notifications = Notification.objects.filter(user_id=user.id)
        serializer = NotifcationSerializers(notifications, many=True)
        result = {
            "notificationCount": len(notifications),
            "notifications": serializer.data
        }
        return response.Response(result, status.HTTP_200_OK)


class NotificationsDetailsAPIView(generics.GenericAPIView):
    serializer_class = NotifcationSerializers
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, slug):
        user = User.objects.filter(email=request.user.email).first()
        notification = Notification.objects.filter(user_id=user.id, slug=slug)

        if not notification:
            return response.Response(
                {"error": "notification not found."},
                status.HTTP_404_NOT_FOUND
            )
        notification.update(status=True)
        serializer = NotifcationSerializers(notification, many=True)
        return response.Response({"notification": serializer.data}, status.HTTP_200_OK)


class NotificationsUnreadAPIView(generics.GenericAPIView):
    serializer_class = NotifcationSerializers
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        user = User.objects.filter(email=request.user.email).first()
        notifications = Notification.objects.filter(user_id=user.id, status=False)
        serializer = NotifcationSerializers(notifications, many=True)
        result = {
            "notificationCount": len(notifications),
            "notifications": serializer.data
        }
        return response.Response(result, status.HTTP_200_OK)


class NotificationSettingsAPIView(generics.GenericAPIView):
    serializer_class = NotifcationSettingsSerializers

    def create(self, request):
        serializer = self.serializer_class(
            data={
                "email_notifications": True,
                "in_app_notifications": True,
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=User.objects.filter(email=request).first())
        return


class NotificationsOptoutApiView(generics.GenericAPIView):
    serializer_class = NotifcationSettingsSerializers
    permission_classes = [permissions.IsAuthenticated, ]

    def put(self, request, type):
        if type == "email":
            NotificationCheck.check_type(request).update(
                email_notifications=request.data['settings']
            )
        elif type == "app":
            NotificationCheck.check_type(request).update(
                in_app_notifications=request.data['settings']
            )
        else:
            return response.Response(
                {
                    "error": "The settings type should be email or app."
                },
                status.HTTP_400_BAD_REQUEST
            )

        return response.Response(
            {
                "message": "Your settings have been configured successfully."
            },
            status.HTTP_200_OK
        )
