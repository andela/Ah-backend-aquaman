from rest_framework import generics, permissions, serializers, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from authors.apps.authentication.models import User
from authors.apps.authentication.renderers import UserJSONRenderer
from authors.apps.authentication.serializers import UserSerializer
from .models import Profile, Follow
from .permissions import IsOwnerOrReadOnly
from .renderers import ProfileJSONRenderer
from .serializers import \
    ProfileSerializer, ProfileUpdateSerializer, FollowSerializer
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
    """
    Allows the currently logged in user
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


class FollowsView(generics.CreateAPIView, generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = FollowSerializer

    def post(self, request, username):
        """
        User follows an Author
        """
        follower = User.objects.get(username=request.user.username)
        followed = get_object_or_404(User, username=username)
        check = self.check_follow_status(follower, followed)
        if isinstance(check, Response):
            return check
        follow_data = {
            'follower': follower.id,
            'followed': followed.profile.id}
        serializer = self.serializer_class(data=follow_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "Successfuly followed {}".format(followed.username)
        }, status=status.HTTP_201_CREATED)

    def check_follow_status(self, follower, followed):
        if follower.id == followed.id:
            return Response({
                'error': 'You cannot follow your own profile.'
            }, status=status.HTTP_400_BAD_REQUEST)
        query_result = Follow.objects.filter(
            follower_id=follower.id, followed_id=followed.profile.id).first()
        if query_result:
            return Response({
                "error": "You are already following {}.".format(followed.username)
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username):
        """
        User unfollows an Author
        """
        follower = User.objects.get(username=request.user.username)
        followed = get_object_or_404(User, username=username)
        follow = Follow.objects.filter(
            follower_id=follower.id, followed_id=followed.profile.id).first()
        if not follow:
            return Response({
                'error': 'You cannot unfollow a user you are not following.'
            }, status=status.HTTP_400_BAD_REQUEST)
        follow.delete()
        return Response(
            {'message': 'You have successfully unfollowed {}.'.format(
                username)},
            status=status.HTTP_200_OK)

    def get(self, request, username):
        """
        Get all Authors a user is following
        """
        user = get_object_or_404(User, username=username)
        follows = Follow.objects.filter(follower_id=user.id)
        serializer = self.serializer_class(follows, many=True)
        following_list = list()
        for follow in serializer.data:
            profile = Profile.objects.get(id=follow['followed'])
            following_list.append({
                "username": profile.user.username,
                "bio": profile.bio,
                "image": profile.image,
                "followed_at": follow['followed_at']
            })
        if len(following_list) == 0:
            response = {'message': '{} has no following'.format(username)}
        response = {'following_count': len(
            following_list), 'following': following_list}
        return Response(response, status=status.HTTP_200_OK)


class FollowersView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = FollowSerializer

    def get(self, request, username):
        """
        Get all Users following an Author
        """
        user = get_object_or_404(User, username=username)
        followers = Follow.objects.filter(followed_id=user.id)
        serializer = self.serializer_class(followers, many=True)
        followers_list = list()
        for follow in serializer.data:
            profile = Profile.objects.get(id=follow['followed'])
            user = User.objects.get(id=follow['follower'])
            followers_list.append({
                "username": user.username,
                "bio": profile.bio,
                "image": profile.image,
                "followed_at": follow['followed_at']
            })
        if not followers_list:
            response = {
                'message': '{} has no followers'.format(username)}
        else:
            response = {
                'follower_count': len(followers_list), 'followers': followers_list}
        return Response(response, status=status.HTTP_200_OK)
