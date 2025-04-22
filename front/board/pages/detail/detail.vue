<template>
  <v-container>
    <v-row>
      <!-- 왼쪽: 썸네일 -->
      <v-col cols="12" md="4">
        <v-card class="pa-4">
          <v-img
            :src="boardStore.board?.image_url || '/default-thumbnail.jpg'"
            class="thumbnail-preview"
          />
          <v-list>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title class="text-subtitle-1 font-weight-bold">✨ 모임 제목</v-list-item-title>
                <v-list-item-subtitle class="text-h6 orange--text">{{ boardStore.board?.title }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title class="text-subtitle-1 font-weight-bold">📅 모임 날짜</v-list-item-title>
                <v-list-item-subtitle>{{ formattedDate }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title class="text-subtitle-1 font-weight-bold">📍 맛집 장소</v-list-item-title>
                <v-list-item-subtitle>{{ boardStore.board?.restaurant }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-list>
          <v-btn v-if="boardStore.board?.is_author" color="primary" class="mt-4" @click="goToModify">✏️ 수정</v-btn>
          <v-btn class="mt-2" color="grey" @click="router.back()">⬅️ 이전 페이지</v-btn>
        </v-card>
      </v-col>

      <!-- 가운데: 소개 -->
      <v-col cols="12" md="4">
        <v-card class="pa-4">
          <v-card-title class="text-h5 font-weight-bold">모임 소개</v-card-title>
          <v-card-text>{{ boardStore.board?.content }}</v-card-text>
        </v-card>
      </v-col>

      <!-- 오른쪽: 댓글 -->
      <v-col cols="12" md="4">
        <v-card class="pa-4 comment-box">
          <v-card-title class="text-h6 font-weight-bold">💬 댓글</v-card-title>

          <v-textarea
            v-model="newComment"
            label="댓글을 입력해주세요"
            outlined
            dense
            rows="2"
            class="text-sm"
          />
          <div class="d-flex justify-end">
            <v-btn color="orange" size="x-small" variant="text" @click="submitComment">등록</v-btn>
          </div>

          <v-divider class="my-3" />

          <v-list v-if="groupedComments.length">
            <Comment
              v-for="comment in groupedComments"
              :key="comment.comment_id"
              :comment="comment"
              :level="0"
              @delete="deleteComment"
              @like="toggleLike"
              @reply="submitReply"
            />
          </v-list>

          <p v-else class="grey--text">댓글이 없습니다.</p>

          <v-pagination
            v-model="commentPage"
            :length="totalPages"
            @update:modelValue="onPageChange"
            color="orange"
            class="mt-4"
          />
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useBoardDetailStore } from '~/board/stores/detail/BoardDetailStore';
import { useCommentStore } from '~/comment/stores/CommentStore';
import Comment from '~/comment/pages/Comment.vue';

const route = useRoute();
const router = useRouter();
const boardStore = useBoardDetailStore();
const commentStore = useCommentStore();
const boardId = Number(route.params.id);


const newComment = ref('');
const commentPage = ref(1);
const totalPages = computed(() => Math.ceil(commentStore.total / 10));
const groupedComments = computed(() => commentStore.comments || []);

const formattedDate = computed(() => {
  const dateStr = boardStore.board?.end_time;
  if (!dateStr) return '';
  return new Date(dateStr).toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
});

const goToModify = () => router.push(`/board/modify/${boardId}`);

const loadPage = async (page = 1) => {
  await commentStore.loadComments(boardId, page);
};

onMounted(async () => {
  await boardStore.requestDetailBoard(boardId);
  console.log("📸 이미지 URL:", boardStore.board?.image_url); 
  await loadPage(commentPage.value);
});

const submitComment = async () => {
  const accountId = Number(localStorage.getItem('account_id'));
  const token = localStorage.getItem('userToken');
  if (!newComment.value.trim() || !token || !accountId) return;

  await commentStore.addComment({ board_id: boardId, content: newComment.value });
  newComment.value = '';
  await loadPage(1); // 최신 댓글 보기 위해 1페이지 리셋
};

const submitReply = async ({ parentId, content }) => {
  const accountId = Number(localStorage.getItem('account_id'));
  const token = localStorage.getItem('userToken');
  if (!content.trim() || !token || !accountId) return;

  await commentStore.addReply({ board_id: boardId, content, parent_id: parentId });
  await loadPage(commentPage.value); // 현재 페이지 유지
};

const deleteComment = async (commentId) => {
  const accountId = Number(localStorage.getItem('account_id'));
  const token = localStorage.getItem('userToken');
  if (!confirm('정말로 삭제하시겠습니까?')) return;

  await commentStore.removeComment(commentId);
  await loadPage(commentPage.value); // 현재 페이지 유지
};

const toggleLike = async (commentId) => {
  console.log("좋아요 토글:", commentId);
  // 서버 연동 시 POST/DELETE 처리
  await loadPage(commentPage.value); // 상태 동기화
};
const onPageChange = async (page) => {
  commentPage.value = page;
  await commentStore.loadComments(boardId, page);
};

</script>

<style scoped>
.thumbnail-preview {
  width: 100%;
  height: 200px;
  object-fit: cover;
}
.comment-box {
  max-height: 100vh;
  overflow-y: auto;
  border-radius: 8px;
}
.text-sm {
  font-size: 0.85rem;
}
</style>
