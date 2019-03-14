from rest_framework import serializers
from .models import Article, ArticleLikesDislikes, Rating

from ..profiles.serializers import ProfileSerializer


class ArticleSerializer (serializers.ModelSerializer):

    author = ProfileSerializer(read_only=True)
    user_rating = serializers.CharField(
        source="average_rating", required=False)
    read_time = serializers.CharField(source="read_time_calculator", required=False)

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
            "tagList",
            "image",
            "likes",
            "dislikes",
            "user_rating",
            "read_time",

        )
        read_only_fields = (
            'author',
            'slug',
            'created_at',
            'updated_at',
            'user_rating',
            "read_time",
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


class RatingSerializer(serializers.ModelSerializer):
    article = serializers.SerializerMethodField()
    rated_by = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    score = serializers.DecimalField(required=True, max_digits=5, decimal_places=2)

    class Meta:
        model = Rating
        fields = ('score', 'rated_by', 'article', 'author')

    def get_article(self, obj):
        return obj.article.title

    def get_author(self, obj):
        return obj.article.author.user.username

    def get_rated_by(self, obj):
        return obj.rated_by.username
