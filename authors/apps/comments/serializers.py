from rest_framework import serializers
from .models import Comment
from ..profiles.serializers import ProfileSerializer


class CommentSerializer(serializers.ModelSerializer):
   
    author = ProfileSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            "created_at",
            "updated_at",
            "body",
            "author",
            "article",
            "id"
        )
        read_only_fields = (
            "article",
            "author",
            "created_at",
            "updated_at",
            "id"
        )
