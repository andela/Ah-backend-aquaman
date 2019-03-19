from django.urls import path

from .views import (
    ArticlesApiView, ArticleDetailApiView, TwitterShareView,
    ArticleTagsApiView, FacebookShareView, EmailShareView,
    ArticleLikeApiView, RateArticleView, ArticleLikeApiView,
)

urlpatterns = [
    path('articles/', ArticlesApiView.as_view(), name='articles'),
    path(
        'articles/<slug>/',
        ArticleDetailApiView.as_view(),
        name='article-detail'
    ),
    path(
        'articles/<slug>/like/',
        ArticleLikeApiView.as_view(),
        name='article-like'
    ),
    path("articles/<slug>/rate/", RateArticleView.as_view(), name="rating"),
    path(
        'tags/',
        ArticleTagsApiView.as_view(),
        name='article-tags'
    ),
    path('articles/<slug>/facebook/', FacebookShareView.as_view()),
    path('articles/<slug>/twitter/', TwitterShareView.as_view()),
    path('articles/<slug>/email/', EmailShareView.as_view()),
]
