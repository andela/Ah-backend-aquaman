from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView)
urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view(), name='viewusers'),
    path('users/', RegistrationAPIView.as_view(), name='registration'),
    path('users/login/', LoginAPIView.as_view(), name='login'),
]
