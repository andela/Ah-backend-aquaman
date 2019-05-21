from itertools import chain
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework import generics, permissions

from authors.apps.articles.serializers import ReadingStatsSerializer
from . import (serializers, permissions as app_permissions)
from .pagination import ArticlesLimitOffsetPagination
from .renderers import ArticleJSONRenderer
from .utils import Utils
from authors.apps.articles.models import Article, ArticleLikesDislikes, Rating, Bookmark, ReadingStats
from ..profiles.models import Profile
from authors.apps.core.utils import Utilities


class ArticlesApiView (generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.ArticleSerializer
    pagination_class = ArticlesLimitOffsetPagination
    queryset = Article.objects.all()
    search_fields = (
        'title',
        'body',
        'description',
        'tagList',
        'author__username',
        'favorited_articles')

    def get_queryset(self):
        queryset = self.queryset
        tag = self.request.query_params.get('tag', None)
        keyword = self.request.query_params.get('keyword', None)
        favorite = self.request.query_params.get('favorite', None)
        author = self.request.query_params.get('author', None)

        queryset_keyword, queryset_tag, queryset_default, \
            queryset_favorite, queryset_author = [], [], [], [], []

        if keyword:
            result = (
                Q(title__icontains=keyword) |
                Q(body__icontains=keyword) |
                Q(description__icontains=keyword)
            )
            queryset_keyword = queryset.filter(result)

        elif tag:
            queryset_tag = queryset.filter(tagList__icontains=tag)
        elif favorite:
            queryset_favorite = \
                queryset.filter(favorites__user__username__icontains=favorite)
        elif author:
            queryset_author = \
                queryset.filter(author__user__username__icontains=author)
        else:
            queryset_default = queryset.all()

        queryset = list(chain(
            queryset_keyword,
            queryset_tag,
            queryset_favorite,
            queryset_author,
            queryset_default
        ))
        return queryset

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save(author=Profile.objects.filter(user=request.user).first(),
                        slug=Utils.create_slug(request.data['title']))

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ArticleDetailApiView (generics.GenericAPIView):
    permission_classes = (app_permissions.IsAuthorOrReadOnly, permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.ArticleSerializer

    def get(self, request, slug):
        article = self.get_object(slug)
        context = {"request": request}
        if not article:
            return Response({'errors': 'that article was not found'}, status=status.HTTP_404_NOT_FOUND)
        user = request.user

        serialized_data = self.serializer_class(article, context=context)

        if request.auth and (user.id != article.author.pk):

            ReadingStats.objects.create(article=article, user=user)

        return Response(serialized_data.data, status=status.HTTP_200_OK)

    def patch(self, request, slug):
        data = request.data
        article_data = data
        article = self.get_object(slug)
        context = {"request": request}
        if article:
            self.check_object_permissions(request, article)
            serializer_data = self.serializer_class(article, article_data, partial=True, context=context)
            serializer_data.is_valid(raise_exception=True)
            serializer_data.save()
            return Response(serializer_data.data,status=status.HTTP_200_OK)

        return Response({'errors': 'that article was not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, slug):
        article = self.get_object(slug)
        if article:
            self.check_object_permissions(request, article)
            article.delete()
            return Response({'article': 'Article has been deleted'}, status=status.HTTP_200_OK)
        return Response({'errors': 'that article was not found'}, status=status.HTTP_404_NOT_FOUND)

    def get_object(self, slug):
        return Article.objects.filter(slug=slug).first()


class ArticleLikeApiView(generics.GenericAPIView):

    serializer_class = serializers.ArticleLikeDislikeSerializer

    def post(self, request, slug):
        """This function enables a user to like or dislike an article."""
        article = Article.objects.filter(slug=slug).first()
        liked_article = ArticleLikesDislikes.objects.filter(article_id=article.id, user_id=request.user.id)

        if len(liked_article) <= 0:
            # when a user likes the article for the first time
            # the article is liked.
            serializer_data = self.serializer_class(data={"user": request.user.id, "article": article.id,
                                                          "likes": True})
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
        likes = ArticleLikesDislikes.objects.filter(article_id=article.id, likes=True)
        dislikes = ArticleLikesDislikes.objects.filter(article_id=article.id, likes=False)
        Article.objects.filter(slug=slug).update(likes=(len(likes)), dislikes=(len(dislikes)), )

        return Response(data, status=status.HTTP_200_OK)


class RateArticleView(generics.GenericAPIView):
    serializer_class = serializers.RatingSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    renderer_classes = [ArticleJSONRenderer, ]

    def post(self, request, slug):

        user = request.user
        score_data = request.data

        score = score_data.get("score", 0)
        article = get_object_or_404(Article, slug=slug)
        if score < 0 or score > 5:
            return Response({"message": "Rating must be between 0 and 5"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=score_data)
        serializer.is_valid(raise_exception=True)

        if user.username == article.author.user.username:
            return Response({"message": "You can not rate your own article"}, status=status.HTTP_403_FORBIDDEN)

        try:
            Rating.objects.get(rated_by_id=user.pk, article_id=article.pk, score=score)
            return Response({"message": "You have already rated the article"}, status=status.HTTP_200_OK)

        except Rating.DoesNotExist:
            serializer.save(rated_by=user, article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ArticleTagsApiView(generics.ListAPIView):

    def get(self, request):
        merged = []
        for tag in Article.get_all_tags():
            merged += tag
        return Response({"tags": set(merged)})


class FavoriteHandlerView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    renderer_classes = [ArticleJSONRenderer, ]
    serializer_class = serializers.ArticleSerializer

    def post(self, request, slug):
        user = request.user
        article = get_object_or_404(Article, slug=slug)

        if article.author.user.username == user.username:
            return Response({"message": "Please favourite another author's article", },
                            status=status.HTTP_403_FORBIDDEN)

        if article in user.profile.favorited_articles.all():
            return Response({"error": "This article is in your favorites"},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            return Article.objects.handle_favorite_an_article(user_obj=user, slug=article.slug)

    def delete(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        if article in request.user.profile.favorited_articles.all():
            return Article.objects.unfavorite_an_article(
                request_user=request.user, slug=article.slug)
        else:
            return Response({"error": "Article does not exist in your favorites"},
                            status=status.HTTP_400_BAD_REQUEST)


class ReportArticleView(generics.GenericAPIView):
    serializer_class = serializers.ReportedArticleSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, slug):
        reporter = Profile.objects.get(user=request.user)
        article = Article.objects.filter(slug=slug).first()
        data = {"reporter": reporter,
                "article": article,
                "reason": request.data['reason'] if 'reason' in request.data
                else ''}
        if reporter == article.author:
            return Response({"message": "You cannot report your own article"},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(reporter=reporter, article=article)
        data = {"subject": "[Article Reported]", "to":
                serializer.data['article']['author']['email'],
                "body": f"Your article was reported,These are the details:\n{data['reason']}"}
        Utilities.send_email(data,None,'article_reports')

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BookmarksApiView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    renderer_classes = [ArticleJSONRenderer, ]
    serializer_class = serializers.BookmarkSerializer

    def post(self, request, slug=None):
        """This method creates a bookmark"""
        user = request.user
        article = get_object_or_404(Article, slug=slug)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        is_bookmarked = Bookmark.objects.filter(user_id=user.id, article_id=article.id).exists()

        if not (user.email == article.author.user.email):

            if not is_bookmarked:

                Bookmark.objects.create(article=article, user=user)

                return Response({'message': 'Article has been bookmarked'}, status=status.HTTP_201_CREATED)

            return Response({'error': 'You have already bookmarked this article'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': 'You can not bookmark your own article'},
                        status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, slug=None):
        user = request.user
        article = get_object_or_404(Article, slug=slug)
        bookmark = Bookmark.objects.filter(user_id=user.id, article_id=article.id)

        if bookmark:
            bookmark.delete()
            return Response({'message': 'Article has been unbookmarked'}, status=status.HTTP_200_OK)
        return Response({'error': 'Article does not exist in your bookmarks list'}, status=status.HTTP_400_BAD_REQUEST)


class BookmarksListView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = serializers.BookmarkSerializer

    def get(self, request):
        bookmarks = Bookmark.objects.filter(user=request.user).all()
        if len(bookmarks) < 1:
            return Response({'message': 'You have not bookmarked any articles yet'})
        serializer = self.serializer_class(bookmarks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReadingStatsApiView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ReadingStatsSerializer

    def get(self, request, slug):
        user = request.user.id
        read_stats = ReadingStats.objects.filter(user=user).all()
        article = get_object_or_404(Article, slug=slug)
        context = {"request": request}

        count = read_stats.count()
        serializer = self.serializer_class(article, context=context)
        return Response({'numberOfArticlesRead': count, 'article': serializer.data},
                        status=status.HTTP_200_OK)
