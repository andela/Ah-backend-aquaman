from django.urls import path
from .views import (ProfileRetrieveAPIView,
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
]
