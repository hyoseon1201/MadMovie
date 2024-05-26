<template>
  <v-card>
    <div style="text-align: center;">
      <v-card-title>
        <span style="white-space: nowrap; color: rgb(255, 105, 180)">MAD </span>
        <span>MOVIE</span>
      </v-card-title>
      <v-card-title style="font-weight: bold;">
        회원가입
      </v-card-title>
    </div>
    <v-card-text>
      <v-form @submit.prevent="signUp">
        <v-text-field v-model="username" label="ID" required></v-text-field>
        <v-text-field v-model="email" label="Email" required></v-text-field>
        <v-text-field v-model="password1" label="Password" type="password" required></v-text-field>
        <v-text-field v-model="password2" label="Password Confirmation" type="password" required></v-text-field>
        <v-btn type="submit" color="rgb(255, 105, 180)" style="width: 100%;">회원가입</v-btn>
      </v-form>
    </v-card-text>
  </v-card>
  <v-snackbar v-model="snackbar" color="error">
    다시 시도해주세요.
  </v-snackbar>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useAccountStore } from '@/store/user.js'

const store = useAccountStore()
const username = ref(null)
const email = ref(null)
const password1 = ref(null)
const password2 = ref(null)
const snackbar = ref(false)

const signUp = async () => {
  const payload = {
    username: username.value,
    email: email.value,
    password1: password1.value,
    password2: password2.value,
  }
  store.signUp(payload)
}

watch(() => store.error, (newError) => {
  if (newError) {
    snackbar.value = true
  }
})

</script>

<style scoped>
</style>
