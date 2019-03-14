from django.urls import path

from .views import (
        ArticlesApiView, ArticleDetailApiView,
        ArticleLikeApiView,
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
]
