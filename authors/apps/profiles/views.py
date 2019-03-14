from rest_framework import generics, permissions, serializers, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from authors.apps.authentication.models import User
from authors.apps.authentication.renderers import UserJSONRenderer
from authors.apps.authentication.serializers import UserSerializer

from .models import Profile
from .permissions import IsOwnerOrReadOnly

from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer, ProfileUpdateSerializer


class ProfileRetrieveAPIView(generics.RetrieveAPIView):
    """
      Implements user's profile endpoint.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = ProfileSerializer

    def retrieve(self, request, username, *args, **kwargs):
        try:
            profile = Profile.objects.select_related('user').get(
                user__username=username)
        except Profile.DoesNotExist:
            raise serializers.ValidationError(
                "the user profile does not exist")

        serializer = self.serializer_class(profile)
        profile = {'profile': serializer.data}

        return Response(profile, status=status.HTTP_200_OK)


class ProfileUpdateAPIView(generics.UpdateAPIView):
    """ Allows the currently logged in user
    to edit their user profile
    """
    serializer_class = ProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self):
        username = self.kwargs.get("username")
        obj = get_object_or_404(Profile, user__username=username)
        return obj


class ListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, )


class ListAuthorsAPIView(ListView):
    """
    Implements listing of all users' profiles
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    renderer_classes = (ProfileJSONRenderer,)


class AuthorsAPIView(ListView):
    """
    Displays a list of existing authors with their profiles.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    renderer_classes = (UserJSONRenderer,)
