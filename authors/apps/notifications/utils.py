from django.core.mail import EmailMessage
from rest_framework import status, response
from .models import NotificationSettings, Notification
from ..authentication.models import User
from django.template.defaultfilters import slugify


class NotificationSettingsRenderer:
    @staticmethod
    def render_notification_settings(username):
        user = User.objects.filter(username=username).first()
        settings = NotificationSettings(
            user=user,
            email_notifications=True,
            in_app_notifications=True
        )
        settings.save()
        return response.Response(
            {"message": "notification settings created successfully"},
            status.HTTP_201_CREATED
        )


class NotificationRenderer:
    @staticmethod
    def send_notification(userlist, notificationdata):
        for userdata in userlist:
            NotificationRenderer.email_notifications(userdata, notificationdata)
            NotificationRenderer.in_app_notifications(userdata, notificationdata)
        return

    @staticmethod
    def email_notifications(userdata, notificationdata):
        user = User.objects.filter(email=userdata).first()
        setting = NotificationSettings.objects.filter(user_id=user.id).first()

        if setting.email_notifications:
            subject = f"[Authors Heaven] {notificationdata['title']}"
            body = f"Hello {user.username}, \n {notificationdata['body']}"
            EmailMessage(subject, body, to=[user.email]).send(fail_silently=False)
        return

    @staticmethod
    def in_app_notifications(userdata, notificationdata):
        user = User.objects.filter(email=userdata).first()
        setting = NotificationSettings.objects.filter(user_id=user.id).first()

        if setting.in_app_notifications:
            last = 0
            if len(Notification.objects.all()) > 0:
                last = Notification.objects.latest('id').id
            slug = slugify(str(last)+"-"+notificationdata['title'])

            notification = Notification(
                title=notificationdata['title'],
                notification=notificationdata['body'],
                status=False,
                user=user,
                slug=slug
            )
            notification.save()
        return


class NotificationCheck:
    @staticmethod
    def check_type(request):
        return NotificationSettings.objects.filter(
            user_id=request.user.id
        )
