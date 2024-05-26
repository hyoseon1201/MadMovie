<template>
  <br>
  <br>
  <br>
  <br>
  <v-container>
    <v-row v-if="store.movies.results && store.movies.results.length > 0">
      <v-col cols="12" sm="3" v-for="movie in store.movies.results" :key="movie.id">
        <MovieCard :movie="movie"/>
      </v-col>
    </v-row>
    <v-row v-else>
      <v-col cols="12">
        <h2 ref="noResults">검색 결과가 없습니다.</h2>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import MovieCard from "@/components/MovieCard.vue";
import {useMovieListStore} from "@/store/movielist";
import {onMounted, watchEffect} from "vue";

const store = useMovieListStore()

const props = defineProps({
  query: String
})

onMounted(async () => {
  if (props.query) {
    await store.searchMovies(String(props.query))
  }
})

watchEffect(async () => {
  if (props.query) {
    await store.searchMovies(String(props.query))
  }
});

</script>

<style scoped>
</style>
