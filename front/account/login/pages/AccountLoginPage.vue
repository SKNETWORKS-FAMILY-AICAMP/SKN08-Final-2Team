<template>
  <div class="login-wrapper">
    <div class="login-container">
      <!-- ✅ 말풍선 -->
      <SpeechBubble text="⚡ 3초만에 빠른 회원가입" />

      <!-- ✅ 카카오 & 네이버 로그인 버튼 -->
      <button class="custom-btn kakao-btn" @click="handleLogin('kakao')">
        🗨️ 카카오로 로그인하기
      </button>

      <button class="custom-btn naver-btn" @click="handleLogin('naver')">
        <span class="naver-icon">N</span> 네이버로 로그인하기
      </button>

      <!-- ✅ 로그인 에러 메시지 -->
      <ErrorMessage v-if="errorMessage" :message="errorMessage" />

      <!-- ✅ 로그인 문제 텍스트 -->
      <p class="login-issue-text">로그인에 문제가 있으신가요?</p>

      <!-- ✅ 돌아가기 -->
      <div class="bottom-buttons">
        <p class="back-text" @click="goToHome">돌아가기</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
import { useAuthenticationStore } from "~/account/login/stores/authenticationStore";
import { ref } from "vue";
import SpeechBubble from "./components/SpeechBubble.vue";
import ErrorMessage from "./components/ErrorMessage.vue";
import "./AccountLoginPage.css";

const router = useRouter();
const authentication = useAuthenticationStore();
const errorMessage = ref("");

// ✅ 로그인 요청 (카카오 or 네이버)
const handleLogin = async (provider) => {
  try {
    const response = await authentication.requestLoginToDjango(provider);
    const data = response?.data || response;
    if (!data.success && data.error_message) {
      errorMessage.value = data.error_message;
      return;
    }
    errorMessage.value = "";
    router.push("/home");
  } catch (error) {
    handleLoginError(error);
  }
};

// ✅ 로그인 오류 처리 함수
const handleLoginError = (error) => {
  if (error.response) {
    errorMessage.value = error.response.data.error_message || "로그인 중 오류 발생";
  } else {
    errorMessage.value = "네트워크 오류 또는 서버 문제로 인해 로그인 실패";
  }
};

// ✅ 홈으로 돌아가기
const goToHome = () => {
  router.push("/");
};
</script>
