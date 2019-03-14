from django.urls import path

from .views import (
        ArticlesApiView, ArticleDetailApiView,
        ArticleLikeApiView, RateArticleView,
    FavoriteHandlerView, ArticleTagsApiView, ReportArticleView
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

    path("articles/<slug>/report/", ReportArticleView.as_view(),
         name="report-article"),

    path(
        'tags/',
        ArticleTagsApiView.as_view(),
        name='article-tags'
    ),
    path('articles/<slug>/favorite', FavoriteHandlerView.as_view(),
    name='article-favorite'),
]
