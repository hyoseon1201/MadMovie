<template>
  <v-app style="background-color: whitesmoke;">
    <v-app-bar class="transition-colors " :color="scrollPosition > 0 ? 'dark' : 'transparent'" :elevation="scrollPosition > 0 ? 1 : 0">
      <v-toolbar-title>
        <router-link :to="{ name: 'home' }" :class="scrollPosition > 0 ? 'main-page-black' : 'main-page-black'">
          <span style="white-space: nowrap; color: rgb(255, 105, 180)">MAD </span><span>MOVIE</span>
        </router-link>
      </v-toolbar-title>
      <v-text-field v-model="searchQuery" @keyup.enter="search" placeholder="Search..." outlined dense hide-details />
      <v-spacer></v-spacer>
      <v-btn v-if="!isLogin" @click="openDialog('login')">Login</v-btn>
      <v-btn v-else @click="goToProfile"  >Profile</v-btn>
      <v-btn v-if="!isLogin" @click="openDialog('signup')">Sign Up</v-btn>
      <v-btn v-else @click="handleLogout" >Logout</v-btn>
    </v-app-bar>
    <div v-if="$route.name === 'home'" class="image-container">
      <img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FUcNvb%2FbtrWwIo3y7C%2F5YjawDpV5oep6IYnfpvuZ0%2Fimg.jpg" class="fit-image">
    </div>
    <v-main>
      <a href="http://localhost:3000/detail/916224">
        <img style="width: 300px;
      text-decoration: none;
      position: absolute;
      right: 0px;
      top: 460px;
      " src="https://d3exygglbxwa7b.cloudfront.net/cat-chair-R-2.gif"></a>
      <router-view />
    </v-main>
    <v-dialog v-model="dialogOpen" max-width="400px">
      <login-view v-if="dialogType === 'login'" @close-dialog="closeDialog" />
      <sign-up-view v-else @close-dialog="closeDialog" />
    </v-dialog>
    <footer>
      <div style="background-color: rgb(16, 17, 19); color: white; text-align: center; padding: 17px;">
        <h4 style="font-weight: 540;">지금까지 <span style="color: rgb(255, 105, 180);">★842,759,218<strong>개의 평가가</strong></span> 쌓였어요.</h4>
      </div>
      <div style="background-color: rgb(28, 29, 31);
        color: rgb(165, 165, 167); font-weight: 500; padding-left: 15%; font-size: 12px;
      "><br>
        <p>서비스 이용약관 | 개인정보 처리방침 | 회사 안내</p><br>
        <div>
          <p>고객센터 | hs@madmovie.co.kr, ☎ 053-123-4567</p>
          <p>광고 문의 | hs@madmove.co.kr · 최신 광고 소개서 ◀ </p>
          <p>제휴 및 대외 협력 | https://google.co.kr/ · (주)구글코리아</p>
        </div><br>
        <div style="font-weight: 400; ">
          <p>주식회사 매드무비 | 공동 대표 곽효선, 안현성 | 서울특별시 강남구 강남대로 323 매드타운 3층</p>
          <p>사업자 등록 번호 237-72-64719</p>
          <p><strong><span style="color: rgb(255, 105, 180);">MAD</span> MOVIE </strong>ⓒ 2023 by MAD, Inc. All rights reserved.</p>
          <br><br>
        </div>
      </div>
    </footer>
  </v-app>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import { useAccountStore } from "@/store/user.js";
import axios from "axios";
import LoginView from '@/views/LoginView.vue'
import SignUpView from '@/views/SignUpView.vue'
import { useRouter } from 'vue-router'



const searchQuery = ref('')

const search = () => {
  router.push({ name: 'search', params: { query: searchQuery.value } })
  searchQuery.value = ''
}

const { isLogin } = useAccountStore();
const scrollPosition = ref(0)
const dialogOpen = ref(false)
const dialogType = ref('')
const router = useRouter()

const openDialog = (type) => {
  dialogType.value = type
  dialogOpen.value = true
}

const closeDialog = () => {
  dialogOpen.value = false
}

const updateScroll = () => {
  scrollPosition.value = window.pageYOffset || document.documentElement.scrollTop;
}

onMounted(() => {
  window.addEventListener('scroll', updateScroll);
});

onUnmounted(() => {
  window.removeEventListener('scroll', updateScroll);
});

const handleLogout = async () => {
  try {
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    await axios.post(`http://127.0.0.1:8000/accounts/logout/`)
    router.go()
  } catch (err) {
    console.log('로그아웃 요청 실패:', err)
  }
}

const goToProfile = function () {
  const username = localStorage.getItem('username')
  router.push(`/profile/${username}/`)
}

</script>

<style scoped>

.main-page-black {
  text-decoration: none;
  color: black;
  font-family: 'Roboto', sans-serif; /* 로고에 사용할 글꼴 */
  font-weight: 700; /* 굵은 글꼴 */
  font-size: 24px; /* 원하는 글꼴 크기로 조절 */
}
.transition-colors {
  transition: background-color 0.5s ease;
}
.image-container {
  height: 50vh;
  overflow: hidden;
}

.fit-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>
