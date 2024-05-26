<template>
  <div class="mx-3">
    <h2 class="mt-2 grey--text">장르별 추천영화</h2>
    <div>
      <v-btn v-for="genre in genres" :key="genre.id" @click="fetchMoviesByGenre(genre.id)">
        {{ genre.name }}
      </v-btn>
    </div>
    <v-container fluid>
      <v-row>
        <v-col cols="12" sm="3" v-for="movie in store.movies.results" :key="movie.id">
          <MovieCard :movie="movie"/>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useMovieListStore } from "@/store/movielist";
import MovieCard from "@/components/MovieCard.vue";

const store = useMovieListStore();
const genres = [
  { id: 12, name: '모험' },
  { id: 14, name: '판타지' },
  { id: 16, name: '애니메이션' },
  { id: 18, name: '드라마' },
  { id: 27, name: '공포' },
  { id: 28, name: '액션' },
  { id: 35, name: '코미디' },
  { id: 36, name: '역사' },
  { id: 37, name: '서부' },
  { id: 53, name: '스릴러' },
  { id: 80, name: '범죄' },
  // { id: 99, name: '다큐멘터리' },
  { id: 878, name: 'SF' },
  { id: 9648, name: '미스터리' },
  { id: 10402, name: '음악' },
  { id: 10749, name: '로맨스' },
  { id: 10751, name: '가족' },
  { id: 10752, name: '전쟁' },
  { id: 10770, name: 'TV 영화' }
];

onMounted(async () => {
  await store.genresMovies(String(12))
})

const fetchMoviesByGenre = async (genreId) => {
  await store.genresMovies(String(genreId))
}
</script>

<style>

</style>
