from django.urls import path

from actors import views

urlpatterns=[
    path('fetch-actors-in-movies/', views.fetch_actors_in_movies, name='fetch_actors_in_movies'),
    path('<int:movie_id>/', views.get_actors_by_movie, name='get_actors_by_movie'),
]