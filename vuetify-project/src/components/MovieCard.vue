<template>
  <v-hover v-slot="{ hover }" open-delay="200">
    <v-card :elevation="hover ? 16 : 2" :class="{ 'on-hover': hover }">
      <router-link :to="{ name: 'detail', params: {id: movie.id}}">
        <v-img :src="posterPath" alt="" class="fixed-height"></v-img>
      </router-link>
      <v-card-title class="subtitle-2">{{ movie.title }}</v-card-title>
      <v-card-text>
        <v-row align="center" class="mx-0">
          <div class="grey--text">
            {{ movie.release_date }}
          </div>
        </v-row>
      </v-card-text>
    </v-card>
  </v-hover>
</template>

<script setup>
import {computed} from "vue";

const props = defineProps(['movie']);

const posterPath = computed(() => `https://image.tmdb.org/t/p/w500/${props.movie.poster_path}`);
</script>

<style scoped>
.fixed-height {
  width: 100%;
  height: 30%;
  object-fit: cover;
}
</style>
