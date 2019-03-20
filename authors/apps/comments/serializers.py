from rest_framework import serializers
from .models import Comment
from ..profiles.serializers import ProfileSerializer


class CommentSerializer(serializers.ModelSerializer):

    author = ProfileSerializer(read_only=True)
    commented_by = ProfileSerializer(read_only=True)

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
            "highlighted_text"
        )
        read_only_fields = (
            "article",
            "author",
            "created_at",
            "updated_at",
            "id"
        )
