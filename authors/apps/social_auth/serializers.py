from rest_framework import serializers
from authors.apps.social_auth import facebook, google, twitter
from authors.apps.social_auth.register import\
    register_social_user


class SocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()


class FacebookSocialAuthViewSerializer(SocialAuthSerializer):
    """Handles serialization of facebook related data"""

    def validate_auth_token(self, auth_token):

        user_data = facebook.Facebook.validate(auth_token)
        try:
            user_id = user_data['id']
            email = user_data['email']
            name = user_data['name']
            provider = 'facebook'
            return register_social_user(
                provider=provider,
                user_id=user_id,
                email=email,
                name=name
            )
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )


class GoogleSocialAuthViewSerializer(SocialAuthSerializer):
    """Handles serialization of google related data"""

    def validate_auth_token(self, auth_token):

        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )
        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name)


class TwitterAuthViewSerializer(SocialAuthSerializer):
    """Handles serialization of twitter related data"""

    def validate_auth_token(self, auth_token):

        user_info = twitter.TwitterAuthTokenVerification.\
            validate_twitter_auth_tokens(auth_token)
        try:
            user_id = user_info['id_str']
            email = user_info['email']
            name = user_info['name']
            provider = 'twitter'
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name)
