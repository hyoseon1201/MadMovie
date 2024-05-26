import requests
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from movies.filters import MovieFilter, CustomSearchFilter
from movies.models import Genre, Movie
from movies.serializers import MovieSerializer, GenreSerializer

from fuzzywuzzy import fuzz

def calculate_similarity(title1, title2):
    return fuzz.ratio(title1, title2)


@api_view(['GET'])
def fetch_and_store_genre_id(request):
    try:
        url = "https://api.themoviedb.org/3/genre/movie/list?language=ko"
        api_key = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlYjZiZmZkYWQ1MjAyMmJiZjRmNTkyZTA4MTRiZmVkMyIsInN1YiI6IjY0ODY3MGYyZTI3MjYwMDBhZmMzMzk2OCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.-GcQmFZSpxrYGxBAjJwRH5AhE0abtu1H-dC96fzm9JM"

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        genres_data = response.json().get('genres', [])

        for genre_data in genres_data:
            serializer = GenreSerializer(data=genre_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()

        return Response({'message': 'Genres fetched and stored successfully.'}, status=status.HTTP_201_CREATED)
    except requests.RequestException as e:
        return Response({'error': f"Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def fetch_and_store_movies(request):
    try:
        api_key = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlYjZiZmZkYWQ1MjAyMmJiZjRmNTkyZTA4MTRiZmVkMyIsInN1YiI6IjY0ODY3MGYyZTI3MjYwMDBhZmMzMzk2OCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.-GcQmFZSpxrYGxBAjJwRH5AhE0abtu1H-dC96fzm9JM"

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

        movie_fields = ['id', 'adult', 'title', 'original_title', 'overview', 'genres', 'runtime', 'release_date',
                        'poster_path', 'status', 'vote_average', 'vote_count']

        for page in range(1, 201):
            url = f"https://api.themoviedb.org/3/movie/top_rated?language=ko&page={page}"

            response = requests.get(url, headers=headers)
            response.raise_for_status()

            movies_data = response.json().get('results', [])

            for movie_data in movies_data:
                genre_ids = movie_data.pop('genre_ids', [])
                filtered_movie_data = {k: v for k, v in movie_data.items() if k in movie_fields}
                movie, created = Movie.objects.get_or_create(
                    id=filtered_movie_data['id'], defaults=filtered_movie_data)

                if created:
                    for genre_id in genre_ids:
                        genre = Genre.objects.get(id=genre_id)
                        movie.genres.add(genre)

                movie.save()

        return Response({'message': 'Top rated movies fetched and stored successfully.'},
                        status=status.HTTP_201_CREATED)
    except requests.RequestException as e:
        return Response({'error': f"Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend, CustomSearchFilter]
    filterset_class = MovieFilter
    search_fields = ['title']


class RecommendMovieViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MovieSerializer
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            like_genres = user.like_genres.all()
            if user.like_genres.count() == 0:
                return Movie.objects.all().order_by('-views').distinct()
            return Movie.objects.filter(genres__in=like_genres).order_by('-views').distinct()
        else:
            return Movie.objects.all().order_by('-views').distinct()


@api_view(['GET'])
def get_movie(request, id):
    try:
        movie = Movie.objects.get(pk=id)
        movie.views += 1
        movie.save(update_fields=['views'])
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    except Movie.DoesNotExist:
        return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_similar_movies(request, id):
    try:
        target_movie = Movie.objects.get(pk=id)
        target_title = target_movie.title

        all_movies = Movie.objects.exclude(pk=id)
        similarities = []

        for movie in all_movies:
            similarity = calculate_similarity(target_title, movie.title)
            similarities.append((movie.id, similarity))

        top_similar_movies = sorted(similarities, key=lambda x: x[1], reverse=True)[:4]
        top_similar_ids = [movie_id for movie_id, _ in top_similar_movies]

        return Response({'similar_movie_ids': top_similar_ids})
    except Movie.DoesNotExist:
        return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)