from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView,
    EmailVerifyAPIView)
urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view(), name='viewusers'),
    path('users/', RegistrationAPIView.as_view(), name='registration'),
    path('users/login/', LoginAPIView.as_view(), name='login'),
    path('users/verify/', EmailVerifyAPIView.as_view(), name='verify_email'),
]
