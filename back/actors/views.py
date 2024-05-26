import requests
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from actors.models import Actor
from movies.models import Movie


@api_view(['GET'])
def fetch_actors_in_movies(request):
    for movie in Movie.objects.all():  # 모든 Movie 객체에 대해
        # TMDB API 호출
        url = f"https://api.themoviedb.org/3/movie/{movie.id}/credits?language=ko"
        api_key = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlYjZiZmZkYWQ1MjAyMmJiZjRmNTkyZTA4MTRiZmVkMyIsInN1YiI6IjY0ODY3MGYyZTI3MjYwMDBhZmMzMzk2OCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.-GcQmFZSpxrYGxBAjJwRH5AhE0abtu1H-dC96fzm9JM"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # 응답 데이터 가져오기
        credits_data = response.json().get('cast', [])

        # 필요한 필드만 선택
        actor_fields = ['id', 'name', 'profile_path', 'known_for_department']  # 필요한 필드를 리스트로 작성

        # 데이터베이스에 저장
        for actor_data in credits_data:
            filtered_actor_data = {k: v for k, v in actor_data.items() if k in actor_fields}
            if 'profile_path' in filtered_actor_data and filtered_actor_data['profile_path'] and filtered_actor_data['known_for_department'] == 'Acting':  # profile_path가 있는지 확인
                actor, created = Actor.objects.get_or_create(
                    id=filtered_actor_data['id'], defaults=filtered_actor_data)

                if created:
                    actor.movies.add(movie)  # Actor 객체와 Movie 객체를 연결

                actor.save()  # Actor 객체를 저장
    return Response({'message': 'Actors fetched and stored successfully.'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_actors_by_movie(request, movie_id):
    try:
        # 해당 영화에 출연한 배우들의 ID를 가져옵니다.
        actor_ids = Actor.objects.filter(movies__id=movie_id).values_list('id', flat=True)

        # 가져온 배우 ID를 사용하여 배우의 정보를 조회합니다.
        actors_data = []
        for actor_id in actor_ids:
            actor = Actor.objects.get(id=actor_id)
            actors_data.append({
                'name': actor.name,
                'profile_path': actor.profile_path
            })

        return Response(actors_data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)