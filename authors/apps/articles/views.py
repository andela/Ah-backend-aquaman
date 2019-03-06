from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, permissions
from . import (
    serializers,
    permissions as app_permissions
)
from .renderers import ArticleJSONRenderer
from .utils import Utils
from authors.apps.articles.models import Article
from ..profiles.models import Profile


class ArticlesApiView (generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.ArticleSerializer

    def get(self, request, format=None):
        articles = Article.objects.all()
        serializer = serializers.ArticleSerializer(articles, many=True)

        article_dict = {
            "articles":  serializer.data,
            "articleCount": len(list(serializer.data))
        }
        return Response(article_dict)

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
