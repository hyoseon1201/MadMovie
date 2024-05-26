from django.urls import path
from .views import UserProfileView, UserFollowListView, manage_followings, check_following, delete_user

urlpatterns = [
    path('profile/<str:username>/', UserProfileView.as_view()),
    path('following/', manage_followings),
    path('is_following/<str:username>/', check_following),
    path('follow_list/', UserFollowListView.as_view(), name='user-follow-list'),
    path('delete/', delete_user, name='delete_user'),
]
