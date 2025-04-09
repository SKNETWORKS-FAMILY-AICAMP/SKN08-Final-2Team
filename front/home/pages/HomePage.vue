<script setup lang="ts">
import TypingEffect from "@/home/pages/TypingEffect.vue";
import SearchLLM from "@/home/pages/SearchLLM.vue";
import EarthEffect from "@/home/pages/EarthEffect.vue"; // ✅ 지구본 컴포넌트 추가
</script>

<template>
  <v-container fluid class="home-container">
    <!-- ✅ 지구본 효과 추가 -->
    <v-row justify="center">
      <EarthEffect />
    </v-row>

    <!-- ✅ 타이핑 효과 -->
    <v-row justify="center" class="typing-effect">
      <TypingEffect />
    </v-row>

    <!-- ✅ 검색창 -->
    <v-row justify="center" class="search-box">
      <SearchLLM />
    </v-row>
  </v-container>

  <v-container>
    <v-row>
      <v-col cols="12" class="text-center">
        <v-divider></v-divider>
        <p>&copy; 2025 SNACK. All rights reserved.</p>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
/* ✅ 전체 화면 정렬 */
.home-container {
  height: 100vh;
}

/* ✅ 타이핑 효과 위쪽에 지구본 배치 */
.typing-effect {
  margin-top: 300px;
}

/* ✅ 검색창 위치 조정 */
.search-box {
  margin-top: 30px;
}
</style>
