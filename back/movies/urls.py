from django.urls import path, include
from rest_framework.routers import DefaultRouter

from movies import views
from movies.views import MovieViewSet, RecommendMovieViewSet, get_similar_movies

router = DefaultRouter()
router.register('list', MovieViewSet)
router.register('recommend', RecommendMovieViewSet, basename='recommendmovie')

urlpatterns = [
    path('fetch-and-store-genre-id/', views.fetch_and_store_genre_id, name='fetch-and-store-genre-id'),
    path('fetch-and-store-movies/', views.fetch_and_store_movies, name='fetch-and-store-movies'),
    path('', include(router.urls)),
    path('<int:id>/', views.get_movie, name='get-movie'),
    path('similar/<int:id>/', get_similar_movies, name='similar_movies'),
]
