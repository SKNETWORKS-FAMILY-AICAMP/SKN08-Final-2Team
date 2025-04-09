<template>
  <v-container>
    <v-row>
      <!-- 왼쪽 패널: 이미지와 기본 정보 표시 -->
      <v-col cols="12" md="4">
        <v-card class="pa-4">
          <v-img :src="boardDetails.image" class="thumbnail-preview" />

          <v-list>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title class="headline">모임 제목</v-list-item-title>
                <v-list-item-subtitle>{{ boardDetails.title }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>모임 날짜</v-list-item-title>
                <v-list-item-subtitle>{{ formattedDate }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>맛집 장소</v-list-item-title>
                <v-list-item-subtitle>{{ boardDetails.restaurant }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>

      <!-- 오른쪽 패널: 모임 소개 -->
      <v-col cols="12" md="8">
        <v-card class="pa-4">
          <v-card-title class="text-h5">모임 소개</v-card-title>
          <v-card-text>{{ boardDetails.description }}</v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useBoardDetailStore } from '~/board/stores/detail/BoardDetailStore';

const route = useRoute();
const boardStore = useBoardDetailStore();
const boardDetails = ref({
  title: '',
  image: '',
  date: '',
  restaurant: '',
  description: ''
});

onMounted(async () => {
  const boardId = route.params.id;
  await boardStore.requestDetailBoard(boardId);
  const { title, image, date, restaurant, description } = boardStore.board;
  boardDetails.value = { title, image, date, restaurant, description };
});

const formattedDate = computed(() => {
  return new Date(boardDetails.value.date).toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
});
</script>

<style scoped>
.thumbnail-preview {
  width: 100%;
  height: 200px;
  object-fit: cover;
}
</style>
