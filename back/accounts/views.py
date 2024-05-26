from rest_framework.views import APIView
from .serializers import UserSerializer, UserFollowSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import User

class UserProfileView(APIView):
    def get(self, request, username=None, format=None):
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request, username=None, format=None):
        user = request.user
        if username and username != user.username:
            return Response({"detail": "Cannot modify another user's profile."}, status=status.HTTP_403_FORBIDDEN)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def manage_followings(request):
    user = request.user
    username_to_follow = request.data.get('follow')
    username_to_unfollow = request.data.get('unfollow')

    if username_to_follow:
        user_to_follow = get_object_or_404(User, username=username_to_follow)
        user.followings.add(user_to_follow)

    if username_to_unfollow:
        user_to_unfollow = get_object_or_404(User, username=username_to_unfollow)
        user.followings.remove(user_to_unfollow)

    serializer = UserFollowSerializer(user, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_following(request, username):
    target_user = get_object_or_404(User, username=username)
    is_following = request.user.is_following(target_user)
    return Response({'is_following': is_following}, status=status.HTTP_200_OK)


class UserFollowListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        followings = user.followings.all()
        followers = user.followers.all()

        followings_serializer = UserFollowSerializer(followings, many=True)
        followers_serializer = UserFollowSerializer(followers, many=True)

        return Response({
            'followings': followings_serializer.data,
            'followers': followers_serializer.data
        })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    request.user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)