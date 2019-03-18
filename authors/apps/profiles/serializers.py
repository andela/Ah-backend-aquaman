from rest_framework import serializers

from .models import Profile, Follow


class ProfileSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    bio = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Profile
        fields = ('username', 'email', 'bio', 'image')
        read_only_fields = ('username', )


class ProfileUpdateSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(source="User")

    class Meta:
        extra_kwargs = {
            'username': {
                'read_only': True
            }
        }
        model = Profile
        fields = [
            'username',
            'bio',
            'image',
        ]

    def get_username(self, obj):
        return f"{obj.user.username}"

    def to_representation(self, instance):
        """
         customizing the data seen by user
        """
        return {
            "profile": {
                "username": instance.user.username,
                "bio": instance.bio,
                "image": instance.image or None,  # put null if no image image url was set
            }
        }


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('follower', 'followed', 'followed_at')
