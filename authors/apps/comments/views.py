from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, serializers, status
from rest_framework.permissions import IsAuthenticated

from authors.apps.articles.models import Article
from ..profiles.models import Profile

from .models import Comment
from .serializers import CommentSerializer


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
        """
        article = get_object_or_404(Article, slug=slug)
        data = request.data.get('comment')
        author = Profile.objects.get(user=request.user)

        serializer = self.serializer_class(data=data, context={'article': article})
        serializer.is_valid(raise_exception=True)
        serializer.save(commented_by=author, article=article)
        return Response({"comment":serializer.data},
            status=status.HTTP_201_CREATED)

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
        This function allows the user
        to update a comment he has made
        """
        comment = get_object_or_404(Comment, pk=pk)
        article = get_object_or_404(Article, pk=comment.article.pk)
        user = Profile.objects.get(user=request.user)
        data = request.data.get("comment")

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
