from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from authors.apps.social_auth.register import UserJSONRenderer
from authors.apps.social_auth.serializers import\
    FacebookSocialAuthViewSerializer,\
    GoogleSocialAuthViewSerializer,\
    TwitterAuthViewSerializer


class SocialAuthView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)

    @staticmethod
    def post_data(request, serializer_class):
        user = request.data.get('user', {})
        serializer = serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)


class GoogleSocialAuthView(SocialAuthView):
    serializer_class = GoogleSocialAuthViewSerializer

    def post(self, request):
        return SocialAuthView.post_data(request, self.serializer_class)


class FacebookSocialAuthView(SocialAuthView):
    serializer_class = FacebookSocialAuthViewSerializer

    def post(self, request):
        return SocialAuthView.post_data(request, self.serializer_class)


class TwitterSocialAuthView(SocialAuthView):
    serializer_class = TwitterAuthViewSerializer

    def post(self, request):
        return SocialAuthView.post_data(request, self.serializer_class)
