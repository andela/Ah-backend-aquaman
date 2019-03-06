from rest_framework import serializers
from .models import Article

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
        )
        read_only_fields = (
            'author',
            'slug',
            'created_at',
            'updated_at',
        )
