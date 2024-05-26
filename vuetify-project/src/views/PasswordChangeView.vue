<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" sm="6">
        <v-card>
          <v-card-title>비밀번호 변경</v-card-title>
          <v-card-text>
            <v-form ref="form" v-model="valid">
              <v-text-field
                v-model="passwords.new_password1"
                :rules="passwordRules"
                label="새 비밀번호"
                type="password"
                required
              ></v-text-field>
              <v-text-field
                v-model="passwords.new_password2"
                :rules="passwordRules"
                label="새 비밀번호 확인"
                type="password"
                required
              ></v-text-field>
              <v-btn :disabled="!valid" @click="changePassword">변경하기</v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
import { useAccountStore } from "@/store/user";

const accountStore = useAccountStore();

const valid = ref(false);
const form = ref(null);
const passwords = ref({
  new_password1: '',
  new_password2: '',
});

const passwordRules = [
  v => !!v || '비밀번호를 입력해야 합니다.',
  v => (v && v.length >= 8) || '비밀번호는 8자 이상이어야 합니다.'
];

const changePassword = async () => {
  await accountStore.passwordChange(passwords.value);
};
</script>
