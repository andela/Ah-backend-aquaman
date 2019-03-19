from rest_framework import serializers
from .models import Article, ArticleLikesDislikes, Rating
from authors.apps.comments.models import Comment

from ..profiles.serializers import ProfileSerializer


class ArticleSerializer (serializers.ModelSerializer):

    author = ProfileSerializer(read_only=True)
    user_rating = serializers.CharField(
        source="average_rating", required=False,read_only=True)
    read_time = serializers.CharField(max_length=100, read_only=True)
    favorites = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

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
            "favorited",
            "favorites",
            "favoritesCount",
            "comments",
        )
        read_only_fields = (
            'author',
            'slug',
            'created_at',
            'updated_at',
            "favorited",
            "favorites",
            'user_rating',
            "favoritesCount",
            "likes",
            "dislikes",
            "read_time",
            "comments",

        )

    def get_favorites(self, obj):
        user_profile = obj.favorites.all()
        user_favorites = []
        for profile in user_profile:
            user_favorites.append(profile.user.username)
        return user_favorites
    def get_comments(self,obj):
        comments = Comment.objects.filter(article=obj)
        comment_data = []
        for comment in comments:
            comment_data.append(comment.body)
        return comment_data


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
    score = serializers.DecimalField(
        required=True, max_digits=5, decimal_places=2)

    class Meta:
        model = Rating
        fields = ('score', 'rated_by', 'article', 'author')

    def get_article(self, obj):
        return obj.article.title

    def get_author(self, obj):
        return obj.article.author.user.username

    def get_rated_by(self, obj):
        return obj.rated_by.username
