<template>
    <v-container class="background-container">
        <br>
        <h3>프로필 업데이트</h3>
        <h5>대표 프로필과 이메일 및 선호 장르를 수정 하실 수 있습니다.</h5>
        <br>
        <div class="update-container">

            <v-form @submit.prevent="handleSubmit" class="update-form">
                <v-row>
                    <v-col cols="12" sm="3">
                        <h3>프로필 수정</h3>
                    </v-col>
                    <v-col cols="12" sm="9">
                        <v-file-input
                                label="프로필 이미지"
                                accept="image/*"
                                @change="onFileSelected"
                                class="input-file"
                        ></v-file-input>
                    </v-col>
                </v-row>
                <v-row>
                    <v-col cols="12" sm="4">
                        <h3>이메일 수정</h3>
                    </v-col>
                    <v-col cols="12" sm="8">
                        <v-text-field
                                label="email"
                                v-model="profile.email"
                                class="input-field"
                        ></v-text-field>
                    </v-col>
                </v-row>

                <v-row>
                    <v-col cols="12" sm="3">
                        <h3>선호 장르 선택</h3>
                    </v-col>
                    <v-col cols="12" sm="9">
                        <div v-for="genre in genres" :key="genre.id" class="genre-checkbox">
                            <v-checkbox
                                    :label="genre.name"
                                    :value="genre.id"
                                    v-model="selectedGenres"
                            ></v-checkbox>
                        </div>
                    </v-col>
                </v-row>

                <div class="button-group">
                    <v-btn type="submit" @click="touch" color="rgb(255, 105, 180)" class="submit-btn">적용</v-btn>
                    <v-btn type="button" @click="touch" color="rgb(255, 105, 180)" class="cancel-btn">취소</v-btn>
                </div>
            </v-form>
        </div>
    </v-container>

</template>


<script setup>
import { ref } from "vue";
import { useAccountStore } from "@/store/user";
import { useRouter } from "vue-router";

const router = useRouter()
const touch = function () {
    router.go(-1)
}

const accountStore = useAccountStore();
const genres = [
    { name: "모험", id: 12 },
    { name: "판타지", id: 14 },
    { name: "애니메이션", id: 16 },
    { name: "드라마", id: 18 },
    { name: "공포", id: 27 },
    { name: "액션", id: 28 },
    { name: "코미디", id: 35 },
    { name: "역사", id: 36 },
    { name: "서부", id: 37 },
    { name: "스릴러", id: 53 },
    { name: "범죄", id: 80 },
    { name: "SF", id: 878 },
    { name: "미스터리", id: 9648 },
    { name: "음악", id: 10402 },
    { name: "로맨스", id: 10749 },
    { name: "가족", id: 10751 },
    { name: "전쟁", id: 10752 },
    { name: "TV 영화", id: 10770 },
]

const profile = ref({
    email: accountStore.email,
    profile_image: accountStore.profile_image,
});
const selectedGenres = ref(accountStore.like_genres || []);


const onFileSelected = (event) => {
    if (event.target.files && event.target.files[0]) {
        profile.value.profile_image = event.target.files[0];
        console.log("선택된 파일:", profile.value.profile_image);
        console.log(event.target.files[0])
    }
};

const handleSubmit = async () => {
    const formData = new FormData();
    if (profile.value.email !== accountStore.email) {
        formData.append('email', profile.value.email);
    }
    if (profile.value.profile_image !== accountStore.profile_image) {
        formData.append('profile_image', profile.value.profile_image);
    }
    if (selectedGenres.value.length > 0) {
        selectedGenres.value.forEach(genreId => {
            formData.append('like_genres', genreId);
        });
    } else if (accountStore.like_genres) {
        accountStore.like_genres.forEach(genreId => {
            formData.append('like_genres', genreId);
        });
    }

    try {
        const response = await accountStore.updateProfile(accountStore.username, formData);
        console.log('프로필 업데이트가 성공적으로 완료되었습니다.', response);
    } catch (err) {
        console.error('프로필 업데이트 중 오류가 발생했습니다:', err);
    }
};
</script>

<style scoped>
.background-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
    border-radius: 5px;
    margin-bottom: 20px;
}
.update-container {
    margin: 0 auto;
    padding: 20px;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
    border-radius: 5px;
}

.update-form {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.section {
    border: 1px solid #ddd;
    padding: 10px;
    margin-bottom: 20px;
}

h4 {
    font-size: 14px;
}

.input-file {
    width: 100%;
}

.genre-checkbox {
    display: inline-block;
    margin-right: 10px;
}

.input-field {
    margin-bottom: 20px;
}
.button-group {
    display: flex;
    justify-content: center;
    gap: 10px;
}

.submit-btn, .cancel-btn {
    align-self: center;
    padding: 10px 20px;
    font-size: 16px;
    color: #fff;
    background-color: rgb(255, 105, 180);
    border-radius: 5px;
    width: 50px;
}
</style>
