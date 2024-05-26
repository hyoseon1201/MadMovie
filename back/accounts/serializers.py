from allauth.account.adapter import get_adapter
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from accounts.models import User


class CustomRegisterSerializer(RegisterSerializer):
    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'email': self.validated_data.get('email', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        return user

class UserSerializer(serializers.ModelSerializer):

    profile_image = serializers.ImageField(use_url=True, required=False)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'like_genres', 'followings', 'followers', 'profile_image']
        extra_kwargs = {
            'followings': {'required': False},
            'like_genres': {'required': False},
        }

    def update(self, instance, validated_data):
        like_genres = validated_data.pop('like_genres', None)
        followings = validated_data.pop('followings', None)

        instance = super().update(instance, validated_data)

        if like_genres is not None:
            instance.like_genres.set(like_genres)

        if followings is not None:
            instance.followings.set(followings)

        return instance


class UserFollowSerializer(serializers.ModelSerializer):
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'is_following']

    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return request.user.is_following(obj)
        return False