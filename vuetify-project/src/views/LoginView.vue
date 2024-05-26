<template>
  <v-card>
    <div style="text-align: center;">
      <v-card-title>
        <span style="white-space: nowrap; color: rgb(255, 105, 180)">MAD </span>
        <span>MOVIE</span>
      </v-card-title>
      <v-card-title style="font-weight: bold;">로그인</v-card-title>
    </div>
    <v-card-text>
      <v-form @submit.prevent="handleLogin">
        <v-text-field v-model="username" label="ID" required></v-text-field>
        <v-text-field v-model="password" label="Password" type="password" required></v-text-field>
        <v-btn type="submit" color="rgb(255, 105, 180)" style="width: 100%;">로그인</v-btn>
      </v-form>
    </v-card-text>
  </v-card>
  <v-snackbar v-model="snackbar" color="error">
    아이디 또는 비밀번호를 잘못 입력했습니다.
  </v-snackbar>
</template>

<script setup>
import {ref} from 'vue'
import {useAccountStore} from '@/store/user.js'
import {useRouter} from 'vue-router'

const username = ref('')
const password = ref('')
const {login} = useAccountStore()
const router = useRouter()
const snackbar = ref(false)

const handleLogin = async () => {
  try {
    await login({username: username.value, password: password.value})
    // 로그인 성공 시 홈 페이지로 이동
    router.go()
    console.log('로그인 성공')
  } catch (error) {
    // 실패 시 에러 처리 로직을 추가할 수 있습니다.
    snackbar.value = true
  }
}
</script>
