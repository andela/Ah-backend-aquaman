from django.urls import path

from authors.apps.social_auth.views import (
    FacebookSocialAuthView, GoogleSocialAuthView, TwitterSocialAuthView
)

urlpatterns = [
    path('auth/google/', GoogleSocialAuthView.as_view()),
    path('auth/facebook/', FacebookSocialAuthView.as_view()),
    path('auth/twitter/', TwitterSocialAuthView.as_view()),
]
