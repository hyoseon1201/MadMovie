<template>
  <v-container>
    <v-row v-if="movie" align="center" justify="center">
      <v-col cols="12" sm="6" md="4">
        <v-img :src="`https://image.tmdb.org/t/p/w500/${movie.poster_path}`" alt="Movie poster" class="mb-4"></v-img>
      </v-col>
      <v-col cols="12" sm="6" md="8">
        <v-card>
          <v-card-title class="headline">{{ movie.title }}</v-card-title>
          <p style="padding-left: 20px">{{ getGenreNamesForMovie(movie) }}</p>
          <br>
          <v-card-text>{{ movie.overview }}</v-card-text>
          <br>

          <!-- 여기서부터 예고편 영상 !! -->
          <div style="padding-left: 20px;">
            <h3>공식 예고편</h3>
            <br>
            <v-dialog v-model="showTrailer" max-width="560px">
              <v-card>
                <v-card-text>
                  <v-card-title style="font-weight: bold;">예고편</v-card-title>
                  <iframe v-if="showTrailer" width="100%" height="315"
                          :src="`https://www.youtube.com/embed/${youtubeTrailerId}`"
                          title="YouTube video player"
                          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                          allowfullscreen>
                  </iframe>
                </v-card-text>
              </v-card>
            </v-dialog>

            <v-btn @click="showTrailer = !showTrailer">
              <svg style="color: red" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                   class="bi bi-youtube" viewBox="0 0 16 16">
                <path
                    d="M8.051 1.999h.089c.822.003 4.987.033 6.11.335a2.01 2.01 0 0 1 1.415 1.42c.101.38.172.883.22 1.402l.01.104.022.26.008.104c.065.914.073 1.77.074 1.957v.075c-.001.194-.01 1.108-.082 2.06l-.008.105-.009.104c-.05.572-.124 1.14-.235 1.558a2.007 2.007 0 0 1-1.415 1.42c-1.16.312-5.569.334-6.18.335h-.142c-.309 0-1.587-.006-2.927-.052l-.17-.006-.087-.004-.171-.007-.171-.007c-1.11-.049-2.167-.128-2.654-.26a2.007 2.007 0 0 1-1.415-1.419c-.111-.417-.185-.986-.235-1.558L.09 9.82l-.008-.104A31.4 31.4 0 0 1 0 7.68v-.123c.002-.215.01-.958.064-1.778l.007-.103.003-.052.008-.104.022-.260.01-.104c.048-.519.119-1.023.22-1.402a2.007 2.007 0 0 1 1.415-1.42c.487-.13 1.544-.21 2.654-.26l.17-.007.172-.006.086-.003.171-.007A99.788 99.788 0 0 1 7.858 2h.193zM6.4 5.209v4.818l4.157-2.408L6.4 5.209z"
                    fill="red"></path>
              </svg>
            </v-btn>
            <br>
          </div>
          <!-- 여기서부터 등장인물 정보 -->
          <div style="padding: 20px">
            <div class="carousel" @mousedown="startDrag" @mousemove="onDrag" @mouseup="endDrag" @mouseleave="endDrag">
            <div class="carousel-item" v-for="(actor, index) in actors" :key="index">
              <img :src="`https://image.tmdb.org/t/p/w300/${actor.profile_path}`" :alt="actor.name"/>
              <div class="carousel-item-info">
                <p>{{ actor.name }}</p>
              </div>
            </div>
          </div>
          </div>
        </v-card>
      </v-col>
    </v-row>
    <hr>
    <br>

    <!-- 여기서부터 영화 리뷰작성 정보 -->

    <v-row class="my-4">
      <v-col cols="auto">
        <h2>영화 리뷰</h2>
      </v-col>
    </v-row>
    <v-form ref="form" v-model="valid" @submit.prevent="submitReview">
      <h4>별점을 선택해주세요.</h4>
      <v-rating
          v-model="rank"
          dense
          half-increments
          length="5"
          clearable
          active-color="rgb(255, 105, 180)"
      ></v-rating>
      <v-textarea label="감상평을 등록해주세요." v-model="content" :rules="contentRules" maxlength="50"></v-textarea>
      <v-btn color="rgb(255, 105, 180)" :disabled="!valid" type="submit" @click="createNewReview">작성하기</v-btn>
    </v-form>

    <!-- 여기서부터 댓글창 확인 -->

    <v-row class="mt-4">
      <v-col cols="6" md="3" v-for="(article, index) in articles" :key="index">
        <v-card class="mb-2" style="max-width: 350px;">
          <v-card-text
              style="min-height: 400px; display: flex; flex-direction: column; justify-content: space-between;">
            <header>
              <div style="display: flex;">
                <div class="image-cropper">
                  <RouterLink :to="{ name: 'profile', params: { username: article.author_username }}">
                    <img class="profile-pic" v-if="profile[index]" :src="'http://localhost:8000' + profile[index]"/>
                    <img class="profile-pic" v-else
                         src="https://static.vecteezy.com/system/resources/thumbnails/009/734/564/small/default-avatar-profile-icon-of-social-media-user-vector.jpg">
                  </RouterLink>
                </div>
                <RouterLink :to="{ name: 'profile', params: { username: article.author_username }}"
                            class="article-link">
                  <span style="font-size: 15px; white-space: nowrap; ">{{ article.author_username }}</span>
                </RouterLink>
              </div>
              <br>
              <hr style="border-top: 1px solid #eee;">
              <br>
              <RouterLink :to="{ name: 'article', params: {id: article.id} }" class="article-link">
                <p style="font-size: 15px;">{{ article.content }}</p>
              </RouterLink>
            </header>
            <div>
              <hr style="border-top: 1px solid #eee;">
              <p> {{ article.rank }}점 · {{
                  new Date(article.created_at).toLocaleDateString('ko-KR', {
                    year: 'numeric',
                    month: '2-digit',
                    day: '2-digit'
                  }) + ' ' + new Date(article.created_at).toLocaleTimeString('ko-KR', {
                    hour: '2-digit',
                    minute: '2-digit',
                    hour12: false
                  })
                }}</p>
              <v-btn class="deleteBtn" style="color: rgb(255, 105, 180); margin-right: 5px" v-if="article.author_username === username"
                     @click="deleteReview(article.id)">삭제
              </v-btn>
              <v-btn class="deleteBtn" style="color: rgb(255, 105, 180)" v-if="article.author_username === username" @click="editArticle(article)">
                수정
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-dialog v-model="editDialog" max-width="500px">
      <v-card>
        <v-card-title>리뷰 수정</v-card-title>
        <v-card-text>
          <v-textarea v-model="editContent" label="리뷰 내용"></v-textarea>
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="updateArticle">저장</v-btn>
          <v-btn @click="editDialog = false">취소</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <div class="pagination">
      <button
          v-for="pageNum in totalPages"
          :key="pageNum"
          :class="{'active': pageNum === currentPage}"
          @click="changePage(pageNum)"
      >
        {{ pageNum }}
      </button>
    </div>
  </v-container>
  <v-dialog v-model="dialogOpen" max-width="400px">
    <login-view v-if="dialogType === 'login'" @close-dialog="closeDialog"/>
    <sign-up-view v-else @close-dialog="closeDialog"/>
  </v-dialog>
</template>

<script setup>
import {ref, onMounted} from 'vue'
import {useMovieListStore} from '@/store/movielist.js'
import {useAccountStore} from "@/store/user"
import LoginView from "@/views/LoginView.vue"
import SignUpView from "@/views/SignUpView.vue"

const props = defineProps(['id'])
const movie = ref(null)
const actors = ref([])
const movieListStore = useMovieListStore()
const articles = ref([])
const username = localStorage.getItem('username')
const profile = ref([]);

const dialogOpen = ref(false)
const dialogType = ref('')

const showTrailer = ref(false)
const form = ref(null)
const valid = ref(false)
const rank = ref(0)
const content = ref('')
const contentRules = [v => !!v || '내용은 필수입니다']
const store = useMovieListStore()

const youtubeTrailerId = ref(null)
const currentPage = ref(1)
const totalPages = ref(10)

const editDialog = ref(false);
const editContent = ref('');
const editingArticleId = ref(null);

function editArticle(article) {
  editingArticleId.value = article.id;
  editContent.value = article.content;
  editDialog.value = true;
}

async function updateArticle() {
  try {
    await movieListStore.articleUpdate(editingArticleId.value, { content: editContent.value });
    editDialog.value = false;
  } catch (error) {
    console.error('Error updating article:', error);
  }
}

const genres = [
  {name: "모험", id: 12},
  {name: "판타지", id: 14},
  {name: "애니메이션", id: 16},
  {name: "드라마", id: 18},
  {name: "공포", id: 27},
  {name: "액션", id: 28},
  {name: "코미디", id: 35},
  {name: "역사", id: 36},
  {name: "서부", id: 37},
  {name: "스릴러", id: 53},
  {name: "범죄", id: 80},
  {name: "SF", id: 878},
  {name: "미스터리", id: 9648},
  {name: "음악", id: 10402},
  {name: "로맨스", id: 10749},
  {name: "가족", id: 10751},
  {name: "전쟁", id: 10752},
  {name: "TV 영화", id: 10770},
]

function getGenreNames(genreIds) {
  return genreIds.map(id => genres.find(genre => genre.id === id)?.name || "Unknown Genre").filter(name => name !== "Unknown Genre");
}

const getGenreNamesForMovie = (movie) => {
  if (!movie || !movie.genres) {
    return '';
  }
  return getGenreNames(movie.genres).join(", ");
}

const changePage = async (pageNum) => {
  console.log('페이지 변경 시도:', pageNum);
  currentPage.value = pageNum;
  await movieListStore.articleList(props.id, pageNum);
  console.log('새로운 데이터:', movieListStore.articles);
  articles.value = movieListStore.articles;
};


const fetchYoutubeTrailer = async () => {
  try {
    const query = encodeURIComponent(`${movie.value.title} 예고편`);
    const response = await fetch(`https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q=${query} 예고편&type=video&key=AIzaSyApvjQRlJvP3CbLR6y71t2ktHEnw_rbW7c`);
    const data = await response.json();
    return data.items[0].id.videoId;
  } catch (error) {
    return null;
  }
}

const openDialog = (type) => {
  dialogType.value = type
  dialogOpen.value = true

}
const closeDialog = () => {
  dialogOpen.value = false

}
onMounted(async () => {

  await movieListStore.detailMovie(props.id)

  movie.value = movieListStore.movies
  await movieListStore.actorList(props.id)

  actors.value = movieListStore.actors
  await movieListStore.articleList(props.id, currentPage.value)
  totalPages.value = movieListStore.total_pages
  console.log('데이터:', movieListStore.articles)

  articles.value = movieListStore.articles

  if (movie.value && movie.value.title) {
    youtubeTrailerId.value = await fetchYoutubeTrailer();

  }
  for (const article of articles.value) {
    const profileData = await useAccountStore().getProfile(article.author_username);
    profile.value.push(profileData.profile_image)
  }

  console.log(movie.value.genres)
})

function createNewReview() {
  const isLoggedIn = useAccountStore().isLogin
  if (!isLoggedIn) {
    openDialog('login')
  }
}

async function submitReview() {
  if (form.value.validate() && useAccountStore().isLogin) {
    const reviewData = {
      rank: rank.value,
      content: content.value,
      movie: props.id
    }
    const newArticle = await store.articleCreate(reviewData);
    console.log('새로운 게시글:', newArticle);
    articles.value.push(newArticle); // 새로운 게시글을 articles 배열에 추가
  }

  content.value = ''; // content 초기화
  rank.value = 0;     // rank 초기화
}


async function deleteReview(id) {
  try {
    // Delete the comment on the server
    await store.articleDelete(id);

    // Remove the deleted comment from the articles array
    const index = articles.value.findIndex(article => article.id === id);
    if (index !== -1) {
      articles.value.splice(index, 1);
    }
  } catch (error) {
    console.error('Error deleting comment:', error);
  }
}

const isDragging = ref(false);
const startPos = ref(0);
const currentScrollLeft = ref(0);
const carouselRef = ref(null);

const startDrag = (e) => {
  isDragging.value = true;
  startPos.value = e.pageX - carouselRef.value.offsetLeft;
  currentScrollLeft.value = carouselRef.value.scrollLeft;
};

const onDrag = (e) => {
  if (!isDragging.value) return;
  e.preventDefault();
  const x = e.pageX - carouselRef.value.offsetLeft;
  const walk = (x - startPos.value) * 3; // 스크롤 속도 조절
  carouselRef.value.scrollLeft = currentScrollLeft.value - walk;
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
  width: 300px;
  scroll-snap-align: start;
}

.carousel-item img {
  width: 200px; /* 이미지 너비를 조절합니다. */
  height: auto; /* 이미지 높이를 자동으로 설정하여 비율을 유지합니다. */
}

.carousel-item-info {
  padding: 10px;
}

.headline {
  font-size: 32px;
  font-weight: bold;
}

.pagination {
  display: flex;
  justify-content: center;
  padding: 10px;
  list-style: none;
}

.pagination button {
  margin: 0 5px;
  padding: 5px 10px;
  border: 1px solid #ddd;
  background-color: white;
  cursor: pointer;
  transition: background-color 0.3s;
}

.pagination button:hover {
  background-color: #eee;
}

.pagination button.active {
  background-color: rgb(255, 105, 180);
  color: white;
  border-color: white;
}

.article-link {
  text-decoration: none; /* 링크 밑줄 제거 */
  color: inherit; /* 기본 글자 색상 유지 */
}

.image-cropper {
  width: 30px;
  height: 30px;
  position: relative;
  overflow: hidden;
  border-radius: 50%;
}

.profile-pic {
  display: inline;
  height: 100%;
  width: 100%;
  object-fit: cover;
}
</style>
