from django.urls import path
from .views import (
    NotificationsRetriveAPIView,
    NotificationsUnreadAPIView,
    NotificationsOptoutApiView,
    NotificationsDetailsAPIView,
)

urlpatterns = [
    path(
        'notifications/',
        NotificationsRetriveAPIView.as_view(),
        name='viewnotifications'
    ),
    path(
        'notifications/single/<slug>/',
        NotificationsDetailsAPIView.as_view(),
        name='singlenotification'
    ),
    path(
        'notifications/unread/',
        NotificationsUnreadAPIView.as_view(),
        name='unreadnotifications'
    ),
    path(
        'notification/<type>/',
        NotificationsOptoutApiView.as_view(),
        name='optoutnotifications'
    )
]
