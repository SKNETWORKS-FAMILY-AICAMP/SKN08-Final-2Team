<template>
    <v-app-bar app color="white" elevation="0" class="nav-bar">
      <!-- ✅ 로고 -->
      <v-btn @click="goToHome" plain class="logo-container">
        <img src="/assets/images/logo/logo_pont_web.png" alt="로고" class="logo">
      </v-btn>
  
      <!-- ✅ 네비게이션 메뉴 -->
      <div class="nav-center">
        <v-btn v-for="(menu, index) in menus" :key="index"
               class="nav-btn"
               :class="{ active: activeMenu === menu.label }"
               @click="navigateTo(menu.route)">
          {{ menu.label }}
        </v-btn>
        <v-btn class="nav-btn download-btn" @click="showAppDownloadModal = true">앱 다운로드</v-btn>
      </div>
  
      <v-spacer></v-spacer>
  
      <!-- ✅ 사람 아이콘 (로그인 상태에 따라 UserModal 띄우기) -->
      <v-btn icon class="auth-btn" @click="isAuthenticated ? showUserModal = true : signIn()">
        <v-icon :style="{ color: '#FF6F00' }">
          {{ isAuthenticated ? 'mdi-account-circle' : 'mdi-account-circle-outline' }}
        </v-icon>
      </v-btn>
  
      <!-- ✅ 앱 다운로드 모달 -->
      <AppDownloadModal :show="showAppDownloadModal" @update:show="showAppDownloadModal = $event" />
      <UserModal
        :show="showUserModal"
        @update:show="showUserModal = $event"
        @logout="confirmLogout" 
      />
    </v-app-bar>
  </template>
  
  <script setup lang="ts">
  import { ref, computed } from "vue";
  import { useRouter } from "vue-router";
  import { useAuthenticationStore } from "~/account/login/stores/authenticationStore";
  import AppDownloadModal from "~/appdown/pages/AppDownloadModal.vue";
  import UserModal from "~/account/userModal/pages/userModal.vue"

  
  const router = useRouter();
  const authenticationStore = useAuthenticationStore();
  
  const showAppDownloadModal = ref(false);
  const showUserModal = ref(false); // ✅ 유저 모달 상태
  
  const menus = ref([
    { label: "맛집 찾기", route: "/restaurant/all" },
    { label: "밥 친구 찾기", route: "/board/all" },
  ]);
  
  const activeMenu = ref("맛집 찾기");
  const isAuthenticated = computed(() => authenticationStore.isAuthenticated);
  

  const navigateTo = (path: string) => {
    activeMenu.value = menus.value.find(menu => menu.route === path)?.label || "맛집 찾기";
    router.push(path);
  };
  
  const goToHome = () => {
    router.push("/");
  };
  
  const signIn = () => {
    router.push("/account/login");
  };
  
// ✅ 로그아웃 확인 후 실행
const confirmLogout = () => {
  if (confirm("로그아웃하시겠습니까?")) {
    authenticationStore.isAuthenticated = false;
    localStorage.removeItem("userToken");
    showUserModal.value = false;
    router.push("/"); // ✅ 로그아웃 후 홈으로 이동
  }
};
  </script>
  
  <style scoped>
  /* ✅ 네비게이션 바 스타일 */
  .nav-bar {
    display: flex;
    align-items: center;
    height: 64px;
    padding: 0 16px;
    position: relative;
  }
  
  /* ✅ 로고 컨테이너 */
  .logo-container {
    display: flex;
    align-items: center;
    width: 120px;
  }
  
  .logo {
    max-width: 120px;
    height: auto;
  }
  
  /* ✅ 네비게이션 메뉴 중앙 정렬 */
  .nav-center {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 30px;
  }
  
  /* ✅ 네비게이션 버튼 */
  .nav-btn {
    font-size: 16px;
    color: #757575;
    font-weight: 500;
    background-color: transparent;
    text-transform: none;
    padding: 10px 16px;
  }
  
  /* ✅ 활성화된 메뉴 */
  .nav-btn.active {
    color: black;
    font-weight: bold;
  }
  
  /* ✅ 앱 다운로드 버튼 */
  .download-btn {
    color: #FF6F00;
    font-weight: bold;
    padding: 8px 16px;
    border-radius: 8px;
  }
  
  /* ✅ 로그인/로그아웃 버튼 */
  .auth-btn {
    color: black;
  }
  </style>
  