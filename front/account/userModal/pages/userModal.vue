<template>
  <v-dialog :model-value="show" @update:model-value="updateShow" max-width="320px">
    <v-card class="modal-card">
      <v-card-title class="modal-title">계정 정보</v-card-title>
      <v-card-text>
        <p>이메일: {{ account.email }}</p>
        <p>가입경로: {{ account.accountPath }}</p>
        <p>가입날짜: {{ account.accountRegister }}</p>
        <p>이름: {{ account.name }}</p>
        <p>닉네임: {{ account.nickname }}</p>
        <p>전화번호: {{ account.phoneNum }}</p>
        <p>주소: {{ account.address }}</p>
        <p>성별: {{ account.gender }}</p>
        <p>생년월일: {{ account.birth }}</p>
        <p>결제수단: {{ account.payment }}</p>
        <p>구독여부: {{ account.subscribe ? "구독" : "미구독" }}</p>
        <p>나이: {{ account.age }}</p>
      </v-card-text>
      <v-card-actions>
        <v-btn color="red" @click="emit('logout')">로그아웃</v-btn>
        <v-btn @click="updateShow(false)">닫기</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { defineProps, defineEmits, watch } from "vue";
import { useAccountStore } from "@/account/userModal/stores/accountStore";
import { accountAction } from "@/account/userModal/stores/accountActions";

const props = defineProps({
  show: Boolean,
});

const emit = defineEmits(["update:show", "logout"]);
const account = useAccountStore();

// ✅ 모달 상태 변경 시 show 값을 업데이트
const updateShow = (value) => {
  emit("update:show", value);
};

// ✅ show가 true일 때만 계정 정보 불러오기
watch(
  () => props.show,
  async (visible) => {
    if (visible) {
      console.log("🚀 모달 열림 → 사용자 정보 로딩");
      await accountAction.getAccountAndProfile();
    }
  }
);
</script>

<style scoped>
.modal-card {
  padding: 20px;
}
.modal-title {
  font-size: 18px;
  font-weight: bold;
}
</style>
