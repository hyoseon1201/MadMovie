from rest_framework import serializers

from movies.models import Movie, Genre


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'adult', 'title', 'original_title', 'overview', 'genres', 'release_date',
                  'poster_path', 'vote_average', 'vote_count', 'views']

    def create(self, validated_data):
        genres_data = validated_data.pop('genres')
        movie = Movie.objects.create(**validated_data)
        for genre_data in genres_data:
            genre, created = Genre.objects.get_or_create(name=genre_data['name'])
            movie.genres.add(genre)
        return movie


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']