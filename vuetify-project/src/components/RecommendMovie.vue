<template>
  <div class="carousel" ref="carouselRef" @mousedown="startDrag" @mousemove="onDrag" @mouseup="endDrag" @mouseleave="endDrag">
    <div class="carousel-item" v-for="(movie, index) in movies" :key="index">
      <router-link :to="{ name: 'detail', params: {id: movie.id}}">
        <img :src="`https://image.tmdb.org/t/p/w500/${movie.poster_path}`" :alt="movie.title" style="height: 500px"/>
      </router-link>
      <div class="carousel-item-info">
        <h2>{{ movie.title }}</h2>
        <p>{{ movie.release_date }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useMovieListStore } from "@/store/movielist";

const store = useMovieListStore();
const movies = ref([]);
const isDragging = ref(false);
const startPos = ref(0);
const currentScrollLeft = ref(0);

const carouselRef = ref(null);

onMounted(async () => {
  await store.recommendMovies();
  movies.value = store.movies.results;
});

const startDrag = (e) => {
  isDragging.value = true;
  startPos.value = e.pageX - carouselRef.value.offsetLeft;
  currentScrollLeft.value = carouselRef.value.scrollLeft;
};

let animationFrameId = null;

const onDrag = (e) => {
  if (!isDragging.value) return;
  e.preventDefault();

  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId); // 이전 애니메이션 프레임 취소
  }

  animationFrameId = requestAnimationFrame(() => {
    const x = e.pageX - carouselRef.value.offsetLeft;
    const walk = (x - startPos.value) * 3; // 스크롤 속도 조절
    carouselRef.value.scrollLeft = currentScrollLeft.value - walk;
  });
};
const endDrag = () => {
  isDragging.value = false;
};
</script>

<style scoped>
.carousel {
  display: flex;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scrollbar-width: thin; /* Firefox에서 스크롤 바 크기 조절 */
  scrollbar-color: gray transparent; /* Firefox에서 스크롤 바 색상 조절 */
  transition: transform 0.3s ease;
}

.carousel::-webkit-scrollbar {
  width: 10px; /* Chrome, Safari, Edge에서 스크롤 바 크기 조절 */
}

.carousel::-webkit-scrollbar-track {
  background: transparent; /* Chrome, Safari, Edge에서 스크롤 바 배경색 조절 */
}

.carousel::-webkit-scrollbar-thumb {
  background-color: gray; /* Chrome, Safari, Edge에서 스크롤 바 색상 조절 */
  border-radius: 20px;
  border: 3px solid transparent;
}

.carousel-item {
  flex: 0 0 auto;
  margin-right: 20px;
  width: 300px;
  scroll-snap-align: start;
}

.carousel-item img {
  width: 100%;
  height: auto;
}

.carousel-item-info {
  padding: 10px;
}

</style>
