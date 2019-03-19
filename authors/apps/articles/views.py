from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
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
from authors.apps.articles.models import Article, ArticleLikesDislikes, Rating
from ..profiles.models import Profile
from django.core.mail import send_mail
import os


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


class RateArticleView(generics.GenericAPIView):
    serializer_class = serializers.RatingSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    renderer_classes = [ArticleJSONRenderer, ]

    def post(self, request, slug):

        user = request.user
        score_data = request.data.get("article", {})

        score = score_data.get("score", 0)
        article = get_object_or_404(Article, slug=slug)
        if score < 0 or score > 5:
            return Response(
                {"message": "Rating must be between 0 and 5"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.serializer_class(data=score_data)
        serializer.is_valid(raise_exception=True)

        if user.username == article.author.user.username:
            return Response(
                {"message": "You can not rate your own article"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            Rating.objects.get(
                rated_by_id=user.pk,
                article_id=article.pk,
                score=score
            )
            return Response(
                {"message": "You have already rated the article"},
                status=status.HTTP_200_OK)
        except Rating.DoesNotExist:
            serializer.save(rated_by=user, article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ArticleTagsApiView(generics.ListAPIView):

    def get(self, request):
        merged = []
        for tag in Article.get_all_tags():
            merged += tag
        return Response({"tags": set(merged)})


class FacebookShareView(APIView):
    """
    sharing an article on facebook
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, slug, **kwargs):

        try:
            Article.objects.get(slug=slug)
            # current_site = Site.objects.get_current().domain
            # print('\n\n\nThe domain is {}'.format(current_site))
            route = 'api/articles'
            url = "http://127.0.0.1:8000/{}/{}".format(route, slug)
            base_url = "https://www.facebook.com/sharer/sharer.php?u="
            url_link = base_url + url

            return Response(
                {
                    "message": "Authors Haven",
                    "link": url_link
                },
                status=status.HTTP_200_OK
            )
        except:
            return Response({
                "message": "Article not found."
            }, status=status.HTTP_404_NOT_FOUND
            )


class TwitterShareView(APIView):
    """
    sharing an article on twitter
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, slug, **kwargs):

        try:
            Article.objects.get(slug=slug)
            base_url = "https://twitter.com/home?status="
            # current_site = 'http://{}'.format(get_current_site(request))
            route = 'api/articles'
            url = "http://127.0.0.1:8000/{}/{}".format(route, slug)
            url_link = base_url + url

            return Response(
                {
                    "message": "Twitterlink",
                    "link": url_link
                },
                status=status.HTTP_200_OK
            )
        except:
            return Response({
                "message": "Article not found"
            },
                status=status.HTTP_404_NOT_FOUND
            )


class EmailShareView(APIView):
    """
    sharing an article via Email
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, slug):

        article = Article.objects.get(slug=slug)
        print(article)
        if not article:
            return Response({
                "message": "Article not found"
            },
                status=status.HTTP_404_NOT_FOUND
            )
        route = 'api/articles'
        url = "http://127.0.0.1:8000/{}/{}".format(route, slug)

        recipient = request.data.get('email')
        subject = "Authors Havenz"
        body = "Click here to read the article {}/".format(url)
        send_mail(
            subject, body, 'from_email', [recipient], fail_silently=False)

        return Response(
            {
                "message": "Email has been sent to {}".format(recipient),
                "link": url
            },
            status=status.HTTP_200_OK
        )
