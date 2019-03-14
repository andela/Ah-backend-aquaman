from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, permissions
from . import (
    serializers,
    permissions as app_permissions
)
from .pagination import ArticlesLimitOffsetPagination
from .renderers import ArticleJSONRenderer
from .utils import Utils
from authors.apps.articles.models import Article, ArticleLikesDislikes
from ..profiles.models import Profile


class ArticlesApiView (generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.ArticleSerializer
    queryset = Article.objects.all()
    pagination_class = ArticlesLimitOffsetPagination

    def post(self, request):
        data = request.data.get('article')
        serializer = self.serializer_class(
            data=data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(
            author=Profile.objects.filter(user=request.user).first(),
            slug=Utils.create_slug(data['title'])
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ArticleDetailApiView (generics.GenericAPIView):
    permission_classes = (app_permissions.IsAuthorOrReadOnly,
                          permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.ArticleSerializer
    renderer_classes = (ArticleJSONRenderer,)

    def get(self, request, slug):
        article = self.get_object(slug)
        context = {"request": request}
        if not article:
            return Response({
                'errors': 'that article was not found'
            }, status=status.HTTP_404_NOT_FOUND)
        serialized_data = self.serializer_class(article,
                                                context=context)

        return Response(serialized_data.data, status=status.HTTP_200_OK)

    def patch(self, request, slug):
        data = request.data
        article_data = data.get('article') if "article" in data else data
        article = self.get_object(slug)
        context = {"request": request}
        if article:
            self.check_object_permissions(request, article)
            serializer_data = self.serializer_class(article,
                                                    article_data,
                                                    partial=True,
                                                    context=context)
            serializer_data.is_valid(raise_exception=True)
            serializer_data.save()
            return Response(serializer_data.data,
                            status=status.HTTP_200_OK)
        return Response({
            'errors': 'that article was not found'
        }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, slug):
        article = self.get_object(slug)
        if article:
            self.check_object_permissions(request, article)
            article.delete()
            return Response({
                'article': 'Article has been deleted'},
                status=status.HTTP_200_OK
            )
        return Response({
            'errors': 'that article was not found'
        }, status=status.HTTP_404_NOT_FOUND)

    def get_object(self, slug):
        return Article.objects.filter(slug=slug).first()


class ArticleLikeApiView(generics.GenericAPIView):

    serializer_class = serializers.ArticleLikeDislikeSerializer

    def post(self, request, slug):
        """This function enables a user to like or dislike an article."""
        article = Article.objects.filter(slug=slug).first()
        liked_article = ArticleLikesDislikes.objects.filter(
            article_id=article.id,
            user_id=request.user.id
        )

        if len(liked_article) <= 0:
            # when a user likes the article for the first time
            # the article is liked.
            serializer_data = self.serializer_class(data={
                "user": request.user.id,
                "article": article.id,
                "likes": True
            })
            serializer_data.is_valid(raise_exception=True)
            serializer_data.save()
            data = {
                "article": article.title,
                "username": request.user.username,
                "details": serializer_data.data
            }
        else:
            # this section is triggered when a user clicks the endpoint the
            # the second time, and it is toggled
            value = not ((liked_article.first()).likes)
            liked_article.update(likes=value)
            data = {
                "article": article.title,
                "username": request.user.username,
                "details": {
                    "likes": liked_article.first().likes,
                    "created_at": liked_article.first().created_at
                }
            }
        # updates the number of likes and dislikes of a given article
        likes = ArticleLikesDislikes.objects.filter(
            article_id=article.id, likes=True)
        dislikes = ArticleLikesDislikes.objects.filter(
            article_id=article.id, likes=False)
        Article.objects.filter(slug=slug).update(
            likes=(len(likes)),
            dislikes=(len(dislikes)),
        )

        return Response(data, status=status.HTTP_200_OK)
