from django.conf.urls import url
from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView, EmailVerification
)

urlpatterns = [
    url(r'^user/?$', UserRetrieveUpdateAPIView.as_view(), name='viewusers'),
    url(r'^users/?$', RegistrationAPIView.as_view(), name='registration'),
    url(r'^users/login/?$', LoginAPIView.as_view(), name='login'),
    url(r'^auth/verify/', EmailVerification.as_view(), name='verifyemail'),
]
