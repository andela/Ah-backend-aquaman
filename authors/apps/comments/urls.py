from django.urls import path
from .views import (CommentCreateListView, CommentsAPIView,
                    CommentLikeView
                )

urlpatterns = [
    path(
        '<slug>/comments/',
        CommentCreateListView.as_view(),
        name='post_comment'),
    path(
        '<slug>/comments/<int:pk>',
        CommentsAPIView.as_view(),
        name='single_comment'),
    path(
        '<slug>/comments/<int:pk>/like/',
         CommentLikeView.as_view(),
         name='comment-like'),
]
