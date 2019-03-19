from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, serializers, status
from rest_framework.permissions import IsAuthenticated
from ..notifications.utils import NotificationRenderer

from authors.apps.articles.models import Article
from ..profiles.models import Profile
from .utils import CommentsUtilities
from .models import Comment, CommentLike
from .serializers import CommentSerializer, CommentLikeSerializer


class CommentCreateListView(generics.ListCreateAPIView):
    """
    create comments and retrieve comments
    """
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, )
    queryset = Comment.objects.all()
    lookup_field = 'article'

    def post(self, request, slug):
        """
        This method allows user to
        comment on an article
        This method posts a comment to an article
        """
        article = get_object_or_404(Article, slug=slug)
        data = request.data
        author = Profile.objects.get(user=request.user)

        check = CommentsUtilities.check_for_highlited_range(
            request.data,
            article.body, data
        )

        if isinstance(check, dict):
            data = check
        else:
            return check

        serializer = self.serializer_class(data=data, context={'article': article})
        serializer.is_valid(raise_exception=True)
        serializer.save(commented_by=author, article=article)

        if "first_highlited" in request.data and "last_highlited" in request.data:
            comment = serializer.data
        else:
            comment = {
                "created_at": serializer.data['created_at'],
                "updated_at": serializer.data['updated_at'],
                "commented_by": serializer.data['commented_by'],
                "body": serializer.data['body'],
                "article": serializer.data['article'],
                "id": serializer.data['id']
            }
            notification = {
                "title": "Article comments",
                "body": "{} commented on an article {}".format(author.user.username, article.title) + \
                    "\n" + serializer.data['body'],
            }
            NotificationRenderer.send_notification(
                article.favorites.values_list('user__email', flat=True),
                notification
            )
        return Response({"comment": comment}, status=status.HTTP_201_CREATED)

    def get(self, request, slug):

        article = get_object_or_404(Article, slug=slug)
        comment = Comment.objects.filter(article=article)
        serializer = self.serializer_class(comment, many=True, context={"request":request})
        return Response({"comments": serializer.data}, status=status.HTTP_200_OK)


class CommentsAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, )
    lookup_fields = 'pk', 'slug'
    queryset = Comment.objects.all()

    def destroy(self, request, pk, slug):
        comment = get_object_or_404(Comment, pk=pk)
        user = Profile.objects.get(user=request.user)

        if comment.commented_by != user:
            return Response({
                "message": "You can only delete a comment you created"
            }, status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response({
            "message": "Comment successfully deleted"
        }, status=status.HTTP_200_OK)

    def get(self, request, pk, slug):
        comment = get_object_or_404(Comment, pk=pk)
        serialized_data = self.serializer_class(comment)
        return Response({
            "comment": serialized_data.data
        }, status=status.HTTP_200_OK)

    def update(self, request, pk, slug):
        """
        This function updates a given comment
        for an article with given id and slag
        """
        comment = get_object_or_404(Comment, pk=pk)
        article = get_object_or_404(Article, pk=comment.article.pk)
        user = Profile.objects.get(user=request.user)
        data = request.data

        if comment.commented_by != user:
            return Response({
                "message": "You can only edit a comment you created"
            }, status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(
            comment,
            data,
            partial=True, context={"article": article})
        serializer.is_valid(raise_exception=True)
        if comment.body == data["body"]:
            return Response({
                "message": "Please ensure the comment body has changed"
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class CommentLikeView(generics.GenericAPIView):
    serializer_class = CommentLikeSerializer
    permission_classes = (IsAuthenticated,)

    def put(self, *args, **kwargs):
        """
        function for liking a comment on a given article
        """
        comment = get_object_or_404(Comment, pk=kwargs.get("pk"))
        user = get_object_or_404(Profile, user=self.request.user)
        try:
            CommentLike.objects.get(liked_by=user)
        except CommentLike.DoesNotExist:
            serializer = self.serializer_class(data={})
            serializer.is_valid(raise_exception=True)
            serializer.save(liked_by=user,
                            comment=comment, like_status=True)
            return Response({
                "message": "comment liked successfully"
            }, status=status.HTTP_200_OK)

        return Response({
            "message": "you already liked this comment"
        }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, *args, **kwargs):
        """
        Function to retrieve all likes on a comment
        """
        comment = get_object_or_404(Comment, pk=kwargs.get("pk"))
        likes = CommentLike.objects.filter(
            like_status=True).filter(comment=comment)
        serializer = self.serializer_class(likes, many=True)
        return Response({
            "likes": serializer.data,
            "likesCount": likes.count()
        }, status=status.HTTP_200_OK)

    def delete(self, *args, **kwargs):
        """
        Function to remove a like from a comment you
        had already liked
        """
        try:
            user = get_object_or_404(
                Profile, user=self.request.user)
            CommentLike.objects.get(liked_by=user)
        except CommentLike.DoesNotExist:
            return Response({
                'message': 'you have not yet liked this comment'
            }, status=status.HTTP_400_BAD_REQUEST)
        CommentLike.objects.get(liked_by=user).delete()
        return Response({
            "message": "unliked comment successfully"
            }, status=status.HTTP_200_OK)

class CommentEditHistoryAPIView(generics.GenericAPIView):
    """This class handles returning edit history for a comment
    that a user created on a particular article
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, slug, pk):
        comment = get_object_or_404(Comment, id=pk)
        comment_history = comment.comment_history.all()
        edit_history = []
        for edit in list(comment_history):
            
            comment_edit_history = {
                "date": edit.history_date,
                "id": edit.history_id,
                "comment_body": edit.body
            }
            edit_history.append(comment_edit_history)
        comment = Comment.objects.get(pk=pk)
        if comment.commented_by.user != request.user:
            return Response({
                'message': 
                "You didn't create this comment Access Denied"
            }, status=status.HTTP_403_FORBIDDEN)
        return Response({
            "history": edit_history,
            "number_of_edits": len(edit_history) - 1
        }, status=status.HTTP_200_OK)
