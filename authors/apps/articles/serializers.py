from rest_framework import serializers
from .models import Article, ArticleLikesDislikes

from ..profiles.serializers import ProfileSerializer


class ArticleSerializer (serializers.ModelSerializer):

    author = ProfileSerializer(read_only=True)

    class Meta:
        model = Article
        fields = (
            "slug",
            "title",
            'body',
            "description",
            "created_at",
            "updated_at",
            "body",
            "author",
            "image",
            "likes",
            "dislikes",
        )
        read_only_fields = (
            'author',
            'slug',
            'created_at',
            'updated_at',
        )


class ArticleLikeDislikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArticleLikesDislikes

        fields = (
            'user',
            'article',
            'likes',
            'created_at'
        )

        extra_kwargs = {
            'user': {'write_only': True},
            'article': {'write_only': True},
        }
