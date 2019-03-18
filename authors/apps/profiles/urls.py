from django.urls import path
from .views import (ProfileRetrieveAPIView, FollowsView, FollowersView,
                    ListAuthorsAPIView, ProfileUpdateAPIView, AuthorsAPIView)

urlpatterns = [
    path(
        'profiles/<username>',
        ProfileRetrieveAPIView.as_view(),
        name="get_profile"
    ),
    path(
        'profiles/<username>/edit',
        ProfileUpdateAPIView.as_view(),
        name="update_profile"
    ),
    path(
        'profiles/',
        ListAuthorsAPIView.as_view(),
        name="users_profiles"
    ),
    path(
        'authorslist/',
        AuthorsAPIView.as_view(),
        name="authors_list"
    ),
    path(
        'profiles/<username>/follows/',
        FollowsView.as_view(),
        name="follow_user"),
    path(
        'profiles/<username>/followers/',
        FollowersView.as_view(),
        name="get_followers")
]
