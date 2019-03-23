from rest_framework import serializers
from .models import Comment, CommentLike
from ..profiles.serializers import ProfileSerializer


class CommentSerializer(serializers.ModelSerializer):

    author = ProfileSerializer(read_only=True)
    commented_by = ProfileSerializer(read_only=True)
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            "created_at",
            "updated_at",
            "commented_by",
            "body",
            "author",
            "article",
            "id",
            "first_highlited",
            "last_highlited",
            "highlighted_text",
            "like_count"
        )
        read_only_fields = (
            "article",
            "author",
            "created_at",
            "updated_at",
            "id",
            "like_count"
        )
    def get_like_count(self,obj):
        return CommentLike.objects.filter(comment=obj).count()

class CommentLikeSerializer(serializers.ModelSerializer):
    liked_by = ProfileSerializer(read_only=True)
    class Meta:
        model = CommentLike
        fields = ('liked_by',)
        read_only_fields = ('like_status', 'liked_by')
