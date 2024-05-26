<template>
  <v-container>
    <h2>당신을 위한 추천 영화</h2>
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6">
      </v-col>
      <RecommendMovie />
      <br>
      <br>
      <MovieList />
    </v-row>
  </v-container>
</template>

<script setup>
import MovieList from "@/components/MovieList.vue";
import RecommendMovie from "@/components/RecommendMovie.vue";
</script>

<style scoped>
</style>
