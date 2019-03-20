from django.urls import path
from .views import (CommentCreateListView, CommentsAPIView,
                    CommentLikeView,
                    CommentEditHistoryAPIView
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
    path(
        '<slug>/comments/<int:pk>/history',
        CommentEditHistoryAPIView.as_view(),
        name='comment_history'),
    
]
