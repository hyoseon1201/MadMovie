<template>
  <hr style="border-top: 1px solid #eee;">
  <v-container>
    <v-row>
      <v-col cols="12">
        <div style="display: flex; align-items: center;">
          <div v-if="authorUsername" class="image-cropper">
            <RouterLink :to="{ name: 'profile', params: { username: authorUsername }}">
              <img class="profile-pic" v-if="profileImage" :src="'http://localhost:8000' + profileImage"/>
              <img class="profile-pic" v-else
                   src="https://static.vecteezy.com/system/resources/thumbnails/009/734/564/small/default-avatar-profile-icon-of-social-media-user-vector.jpg">
            </RouterLink>
          </div>
          <div v-if="authorUsername">
            <span>
              <RouterLink :to="{ name: 'profile', params: { username: authorUsername }}" class="user-link">
                <strong>{{ authorUsername }}</strong>
              </RouterLink>
                | <span style="font-size: 12px;">{{ createdDate }}</span></span>
          </div>
        </div>
      </v-col>
    </v-row>
    <br>
    <p style="font-size: 14px; font-weight: bold;">{{ articleContent }}</p> <br>
    <p style="color: 787878; font-size: 12px;">댓글 {{ commentList.length }}</p>
    <v-divider></v-divider>
    <div>
      <br>
      <h3 style="color: rgb(255, 105, 180);">댓글 목록</h3><br>
      <v-form @submit.prevent="commentCreate">
        <v-text-field v-model="newComment" label="댓글 작성" outlined></v-text-field>
        <v-btn type="submit" color="rgb(255, 105, 180)">댓글쓰기</v-btn>
        <p><br></p>
      </v-form>
      <v-list>

        <v-list-item v-for="comment in commentList" :key="comment.id">
          <v-list-item-content>
            <p style="font-size: 12px;"><span style="font-size: 12px;">
            {{ comment.author_username }} <strong>·</strong> <span style="font-size: 10px;">
            {{
                new Date(comment.created_at).toLocaleString('ko-KR', {
                  year: '2-digit',
                  month: '2-digit',
                  day: '2-digit',
                  hour: '2-digit',
                  minute: '2-digit'
                })
              }}
            </span>
            </span>
            </p><br>
            <v-list-item-subtitle>{{ comment.content }}</v-list-item-subtitle>

          </v-list-item-content>
          <v-btn style="color: hotpink; top: 13px; right: 80px; position: absolute; width: 30px; height: 30px;" icon
          @click="editComment(comment)">
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
          <v-btn style="color: hotpink; top: 13px; right: 20px; position: absolute; width: 30px; height: 30px;" icon
                 @click="commentDelete(comment.id)">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
          <hr style="border-top: 1px solid #eee;">
        </v-list-item>
      </v-list>
      <v-dialog v-model="editDialog" max-width="500px">
        <v-card>
          <v-card-title>댓글 수정</v-card-title>
          <v-card-text>
            <v-textarea v-model="editContent" label="댓글 내용"></v-textarea>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="updateComment">저장</v-btn>
            <v-btn @click="editDialog = false">취소</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
  </v-container>
</template>

<script setup>
import {onMounted, ref} from 'vue';
import {useMovieListStore} from "@/store/movielist";
import {useRoute} from "vue-router";

const store = useMovieListStore();
const route = useRoute();
const commentList = ref([]);
const articleContent = ref("");
const newComment = ref("");

// 프로필 설정을 위해 추가된 부분
const profileImage = ref("");
const authorUsername = ref("");
const createdDate = ref("");

const editDialog = ref(false);
const editContent = ref('');
const editingCommentId = ref(null);

function editComment(comment) {
  editingCommentId.value = comment.id;
  editContent.value = comment.content;
  editDialog.value = true;
}

async function updateComment() {
  try {
    await store.commentUpdate(editingCommentId.value, { content: editContent.value });
    editDialog.value = false;
    await store.commentList(route.params.id); // 댓글 목록 새로고침
    commentList.value = store.comments; // 업데이트된 댓글 목록 반영
  } catch (error) {
    console.error('Error updating comment:', error);
  }
}

onMounted(async () => {
  try {
    await store.articleDetail(route.params.id);
    articleContent.value = store.article.content;
    profileImage.value = store.article.author_profile_image;
    authorUsername.value = store.article.author_username;
    createdDate.value = new Date(store.article.created_at).toLocaleString('ko-KR', {
      year: '2-digit',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
    console.log(authorUsername.value)
    await store.commentList(route.params.id);
    commentList.value = store.comments;
  } catch (error) {
    console.error("Error loading article or comments", error);
    // 적절한 에러 처리 로직 추가
  }
});


const commentDelete = async (commentId) => {
  await store.commentDelete(commentId);
  commentList.value = commentList.value.filter(comment => comment.id !== commentId);
};

const commentCreate = async () => {
  await store.commentCreate(route.params.id, {content: newComment.value});
  newComment.value = ''; // 입력 필드 초기화
  await store.commentList(route.params.id); // 댓글 목록 새로고침
  commentList.value = store.comments; // 업데이트된 댓글 목록 반영
};
</script>

<style scoped>
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

.user-link {
  text-decoration: none; /* 링크 밑줄 제거 */
  color: inherit; /* 기본 글자 색상 유지 */
}

</style>
