<template>
  <v-container>
    <v-row>
      <!-- 좌측 패널 -->
      <v-col cols="12" md="4">
        <v-card class="pa-4">
          <!-- 썸네일 이미지 변경 -->
          <v-file-input
            v-model="thumbnail"
            label="썸네일 이미지 변경"
            accept="image/*"
            outlined
            dense
            clearable
            @update:modelValue="handleImageUpload"
          />

          <div v-if="previewImage" class="relative-container mt-2">
            <v-img :src="previewImage" class="thumbnail-preview" />
            <v-btn
              icon
              small
              color="red"
              class="delete-button"
              @click="removeImage"
            >
              <v-icon small>mdi-close</v-icon>
            </v-btn>
          </div>

          <!-- 날짜 및 시간 선택 -->
          <v-card class="mt-3 pa-2">
            <v-card-title class="text-subtitle1">모임 날짜 및 시간</v-card-title>
            <Datepicker
              v-model="datetime"
              locale="ko"
              :enable-time-picker="true"
              format="yyyy-MM-dd HH:mm"
              auto-apply
              :min-date="new Date()"
              class="mt-2"
            />
          </v-card>

          <!-- 맛집 선택 -->
          <v-autocomplete
            v-model="selectedRestaurant"
            :items="restaurantList"
            item-text="name"
            item-value="id"
            label="맛집 장소 검색"
            outlined dense clearable hide-details
            :loading="loadingRestaurants"
            @update:search-input="onSearchRestaurant"
            class="mt-4"
          />
        </v-card>
      </v-col>

      <!-- 우측 패널 -->
      <v-col cols="12" md="8">
        <v-card class="pa-4">
          <v-text-field v-model="title" label="모임 제목" outlined dense class="mb-4" />
          <v-textarea v-model="content" label="모임 소개" outlined dense rows="6" />

          <v-btn color="primary" block class="mt-4" @click="submitBoard">수정 완료</v-btn>
          <v-btn color="grey" block class="mt-2" @click="router.push('/board/all')">취소</v-btn>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import Datepicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css';
import * as axiosUtility from '~/utility/axiosInstance';

const route = useRoute();
const router = useRouter();
const boardId = route.params.id;

const title = ref('');
const content = ref('');
const datetime = ref<Date | null>(null);
const thumbnail = ref<File | null>(null);
const previewImage = ref('');
const selectedRestaurant = ref<number | null>(null);
const restaurantList = ref([]);
const loadingRestaurants = ref(false);

onMounted(() => {
  const token = localStorage.getItem("userToken");
  if (!token) {
    alert("로그인 후 이용해주세요");
    router.push("/account/login");
    return;
  }
  loadBoardDetail(token);
});

const loadBoardDetail = async (token: string) => {
  try {
    const { djangoAxiosInstance } = axiosUtility.createAxiosInstances();
    const res = await djangoAxiosInstance.get(`/board/${boardId}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    const board = res.data;

    title.value = board.title;
    content.value = board.content;

    const parsed = board.end_time?.includes('T')
      ? new Date(board.end_time)
      : new Date(board.end_time.replace(' ', 'T'));

    datetime.value = !isNaN(parsed.getTime()) ? parsed : new Date();
    previewImage.value = board.image_url || '';
    selectedRestaurant.value = board.restaurant_id || null;
  } catch (error) {
    console.error('❌ 게시글 상세 불러오기 실패:', error);
    alert('게시글 정보를 불러오는 데 실패했습니다.');
  }
};

const handleImageUpload = (file: File | File[] | null) => {
  const selectedFile = Array.isArray(file) ? file[0] : file;
  if (!(selectedFile instanceof File)) {
    removeImage();
    return;
  }

  thumbnail.value = selectedFile;
  const reader = new FileReader();
  reader.onload = (e) => {
    previewImage.value = e.target?.result as string;
  };
  reader.readAsDataURL(selectedFile);
};

const removeImage = () => {
  thumbnail.value = null;
  previewImage.value = '';
};

const onSearchRestaurant = async (searchText: string) => {
  if (!searchText) return;
  loadingRestaurants.value = true;
  try {
    const { djangoAxiosInstance } = axiosUtility.createAxiosInstances();
    const res = await djangoAxiosInstance.get('/restaurants/search/', {
      params: { keyword: searchText },
    });
    restaurantList.value = res.data.results || [];
  } catch (error) {
    console.error('❌ 맛집 검색 실패:', error);
  } finally {
    loadingRestaurants.value = false;
  }
};

const submitBoard = async () => {
  const token = localStorage.getItem("userToken");
  if (!token) return alert("로그인 후 이용해주세요");

  try {
    const formData = new FormData();
    formData.append("title", title.value);
    formData.append("content", content.value);
    formData.append("end_time", datetime.value?.toISOString() || '');
    if (selectedRestaurant.value) {
      formData.append("restaurant", selectedRestaurant.value.toString());
    }

    // 이미지 처리
    if (thumbnail.value instanceof File) {
      formData.append("image", thumbnail.value);
    } else if (thumbnail.value === null) {
      formData.append("image", "");  // 이미지 제거 요청
    }

    const { djangoAxiosInstance } = axiosUtility.createAxiosInstances();
    const res = await djangoAxiosInstance.patch(`/board/update/${boardId}/`, formData, {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": undefined,  // axios가 자동으로 multipart 설정
      },
    });

    console.log("✅ 게시글 수정 성공:", res.data);
    router.push(`/board/${boardId}`);
  } catch (error) {
    console.error("❌ 게시글 수정 실패:", error);
    alert("게시글 수정 중 오류가 발생했습니다.");
  }
};
</script>

<style scoped>
.thumbnail-preview {
  width: 100%;
  height: 150px;
  object-fit: cover;
  border-radius: 8px;
}
.relative-container {
  position: relative;
}
.delete-button {
  position: absolute;
  top: 5px;
  right: 5px;
  z-index: 1;
}
</style>
