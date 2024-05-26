<template>
  <v-container>
    <br><br><br><br>
    <v-row v-if="isLoading" justify="center">
      <v-progress-circular indeterminate></v-progress-circular>
    </v-row>
    <v-row v-else-if="profile" justify="center">
      <div class="image-cropper mb-4">
        <img
            :src="profile.profile_image ? 'http://localhost:8000' + profile.profile_image : 'https://static.vecteezy.com/system/resources/thumbnails/009/734/564/small/default-avatar-profile-icon-of-social-media-user-vector.jpg'"
            class="profile-pic"
        /></div>
      <v-col cols="12" sm="8" md="6">
        <h2>{{ profile.username }}</h2>
        <div>
          <p>Email: {{ profile.email }}</p>
          <p>좋아하는 장르: {{ getGenreNames(profile.like_genres).join(', ') }}</p>
          <p>팔로잉: {{ profile.followings.length }}</p>
          <p>팔로워: {{ profile.followers.length }}</p>
        </div>
        <v-btn v-if="currentUserUsername === profile.username" color="rgb(255, 105, 180)" @click="editProfile" style="margin-right: 10px">프로필
          수정하기
        </v-btn>
        <v-btn v-if="currentUserUsername === profile.username" color="rgb(255, 105, 180)" @click="handleDeleteAccount" style="margin-right: 10px">
          회원탈퇴
        </v-btn>
        <v-btn v-if="currentUserUsername === profile.username" color="rgb(255, 105, 180)" @click="changePassword">
          비밀번호 변경
        </v-btn>

        <!-- 팔로우/언팔로우 버튼 추가 -->
        <v-btn
            v-else-if="!profile.is_following"
            color="rgb(255, 105, 180)"
            @click="handleFollowUnfollow(profile.username, 'follow')"
        >팔로우
        </v-btn>
        <v-btn
            v-else
            style="color: rgb(255, 105, 180)"
            @click="handleFollowUnfollow(profile.username, 'unfollow')"
        >언팔로우
        </v-btn>
      </v-col>
    </v-row>
    <v-row v-else justify="center">
      <v-col cols="12" sm="8" md="6">
        <p>프로필 정보를 불러올 수 없습니다.</p>
      </v-col>
    </v-row>
    <br>
    <br>
    <br>
    <!-- 팔로잉 목록 (현재 로그인한 사용자일 때만 보여줌) -->
    <v-row v-if="currentUserUsername === profile.username" justify="center">
      <v-col cols="12" sm="8" md="6">
        <h3>팔로잉</h3>
        <v-list dense>
          <v-list-item
              v-for="following in followings"
              :key="following.username"
          >
            <v-list-item-content>
              <v-list-item-title>
                <RouterLink :to="{ name: 'profile', params: { username: following.username } }" class="name-link">
                  {{ following.username }}
                </RouterLink>
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-col>
    </v-row>

    <!-- 팔로워 목록 (현재 로그인한 사용자일 때만 보여줌) -->
    <v-row v-if="currentUserUsername === profile.username" justify="center">
      <v-col cols="12" sm="8" md="6">
        <h3>팔로워</h3>
        <v-list dense>
          <v-list-item
              v-for="follower in followers"
              :key="follower.username"
          >
            <v-list-item-content>
              <v-list-item-title>
                <RouterLink :to="{ name: 'profile', params: { username: follower.username} }" class="name-link">
                  {{ follower.username }}
                </RouterLink>
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-col>
    </v-row>
  </v-container>
  <v-dialog v-model="dialogOpen" max-width="400px">
    <login-view v-if="dialogType === 'login'" @close-dialog="closeDialog"/>
    <sign-up-view v-else @close-dialog="closeDialog"/>
  </v-dialog>
</template>

<script setup>
import {onMounted, ref, watch} from 'vue'
import {useRoute} from 'vue-router'
import {useAccountStore} from '@/store/user.js'
import SignUpView from "@/views/SignUpView.vue"
import LoginView from "@/views/LoginView.vue"
import router from "@/router"
import axios from "axios";

const route = useRoute()
const profile = ref({
  followings: [],
  followers: [],
})
const isLoading = ref(true)

const dialogOpen = ref(false)
const dialogType = ref('')

const currentUserUsername = localStorage.getItem('username')

const accountStore = useAccountStore()

const followings = ref([]);
const followers = ref([]);

const openDialog = (type) => {
  dialogType.value = type
  dialogOpen.value = true
}


const closeDialog = () => {
  dialogOpen.value = false
}

const loadProfileData = async (username) => {
  try {
    const profileData = await accountStore.getProfile(username);
    profile.value = profileData;

    // isFollowing 함수 호출
    const followingData = await accountStore.isFollowing(username);
    profile.value.is_following = followingData.is_following;

    const followListData = await accountStore.getFollowList();
    followings.value = followListData.followings;
    followers.value = followListData.followers;
  } catch (error) {
    // ... 오류 처리 ...
  } finally {
    isLoading.value = false;
  }
};

onMounted(async () => {
  try {
    loadProfileData(route.params.username);
    const username = route.params.username;
    const profileData = await accountStore.getProfile(username);
    profile.value = profileData;

    // isFollowing 함수 호출
    const followingData = await accountStore.isFollowing(username);
    profile.value.is_following = followingData.is_following;

    const followListData = await accountStore.getFollowList();
    followings.value = followListData.followings;
    followers.value = followListData.followers;

  } catch (error) {
    if (error.response && error.response.status === 401) {
      openDialog('login');
    } else {
      console.error('프로필 정보를 불러오는 데 실패했습니다.', error);
    }
  } finally {
    isLoading.value = false;
  }
});

watch(() => route.params.username, (newUsername) => {
  isLoading.value = true;
  loadProfileData(newUsername);
});

watch(() => profile.value, (newProfile) => {
  console.log('프로필 정보가 변경되었습니다:', newProfile);
});

const editProfile = () => {
  if (profile.value) {
    router.push({
      name: 'profileUpdate',
      params: {username: profile.value.username},
      props: {existingProfile: profile.value}
    });
  }
}

const handleDeleteAccount = async () => {
  await accountStore.deleteAccount();
  try {
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    await axios.post(`http://127.0.0.1:8000/accounts/logout/`)
    router.go()
  } catch (err) {
    console.log('로그아웃 요청 실패:', err)
  }
  router.push('/')
};

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

const getGenreNames = (item) => {
  return item.map(id => {
    const genre = genres.find(genre => genre.id === id)
    return genre ? genre.name : ''
  })
}

const handleFollowUnfollow = async (username, action) => {
  try {
    await accountStore.manageFollowing(username, action)
    profile.value.is_following = action === 'follow'; // 프로필 상태 업데이트
    console.log(`${action === 'follow' ? '팔로우' : '언팔로우'}가 성공적으로 완료되었습니다.`)
  } catch (err) {
    console.error(`${action === 'follow' ? '팔로우' : '언팔로우'} 중 오류가 발생했습니다:`, err)
  }
}

const changePassword = async () => {
  router.push({name: 'passwordChange'})
};

</script>

<style scoped>
.image-cropper {
  width: 300px;
  height: 300px;
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

.name-link {
  text-decoration: none; /* 링크 밑줄 제거 */
  color: inherit; /* 기본 글자 색상 유지 */
}

</style>
