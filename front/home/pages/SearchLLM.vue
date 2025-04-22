<template>
    <div class="search-container" :class="{ 'expanded': isExpanded }" @click.stop>
        <!-- ✅ 왼쪽 드롭다운 메뉴 -->
        <div class="category-dropdown">
            <button @click="toggleDropdown" class="category-btn">
                {{ selectedCategory }}
                <v-icon size="18">mdi-chevron-down</v-icon>
            </button>
            <ul v-if="dropdownOpen" class="dropdown-menu">
                <li v-for="(category, index) in categories" :key="index" @click="selectCategory(category)">
                    {{ category }}
                </li>
            </ul>
        </div>

        <!-- ✅ 검색 입력창 -->
        <input
            type="text"
            v-model="searchQuery"
            class="search-input"
            placeholder="무엇을 찾고 계신가요?"
            @focus="expandSearch"
            @keyup.enter="search"
        />

        <!-- ✅ 오른쪽 검색 버튼 (대화 아이콘 + 주황색 배경) -->
        <button class="search-btn" @click="search">
            <v-icon size="18">mdi-chat</v-icon>
        </button>
    </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import * as axiosUtility from "../../utility/axiosInstance";

const searchQuery = ref("");
const responseText = ref("");
const userToken = ref("");
const accountId = ref<number | null>(null);
const { fastapiAxiosInst } = axiosUtility.createAxiosInstances();

onMounted(() => {
  // 로그인 후 localStorage에 저장된 토큰, 계정 ID 가져오기
  userToken.value = localStorage.getItem("userToken") || "";
  const idFromStorage = localStorage.getItem("account_id");
  accountId.value = idFromStorage ? parseInt(idFromStorage) : null;
});

const search = async () => {
  console.log("🔍 searchQuery:", searchQuery.value);
  console.log("🔍 userToken:", userToken.value);
  console.log("🔍 accountId:", accountId.value);
  
  if (!searchQuery.value || !userToken.value || !accountId.value) {
    alert("로그인 또는 검색어 확인이 필요합니다.");
    return;
  }

  try {
    const response = await fastapiAxiosInst.post("/llm/search", {
      query: searchQuery.value,
    }, {
      headers: {
        userToken: userToken.value,
        "account-id": accountId.value,
        "Content-Type": "application/json",
      },
    });

    const resultText = response.data?.response || "응답 없음";
    responseText.value = resultText;

    // Chat History 저장
    await fastapiAxiosInst.post("/chat-history/save", {
      user_message: searchQuery.value,
      bot_response: resultText,
    }, {
      headers: {
        userToken: userToken.value,
        "account-id": accountId.value?.toString(),
        "Content-Type": "application/json",
      },
    });
  } catch (error) {
    console.error("검색 중 오류 발생:", error);
    responseText.value = "에러가 발생했습니다.";
  }
};
</script>

<style scoped>
/* ✅ 검색창 전체 컨테이너 */
.search-container {
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid #ddd;
    border-radius: 30px;
    padding: 5px 10px;
    background: white;
    width: 500px;
    max-width: 700px;
    transition: width 0.3s ease-in-out;
}

/* ✅ 마우스를 올리면 확장 */
.search-container:hover {
    width: 700px;
}

/* ✅ 클릭(포커스) 시 확장 유지 */
.search-container.expanded {
    width: 700px;
}

/* ✅ 드롭다운 버튼 */
.category-dropdown {
    position: relative;
    display: flex;
    align-items: center;
    flex-shrink: 0; /* ✅ 크기가 줄어들지 않도록 설정 */
}

.category-btn {
    background: transparent;
    border: none;
    color: #555;
    font-weight: bold;
    display: flex;
    align-items: center;
    gap: 5px;
    cursor: pointer;
    padding: 5px 10px; /* ✅ 좌우 10px 여백 유지 */
    min-width: fit-content;
    white-space: nowrap; /* ✅ 글자가 줄바꿈되지 않도록 설정 */
}

/* ✅ 드롭다운 메뉴 */
.dropdown-menu {
    position: absolute;
    top: 100%;
    left: 0;
    background: white;
    border: 1px solid #ddd;
    border-radius: 5px;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    list-style: none;
    padding: 5px 0;
    margin: 0;
    width: 120px;
}

.dropdown-menu li {
    padding: 8px 12px;
    cursor: pointer;
}

.dropdown-menu li:hover {
    background: #f5f5f5;
}

/* ✅ 검색 입력창 */
.search-input {
    border: none;
    outline: none;
    padding: 8px 12px;
    font-size: 16px;
    flex-grow: 1;
    transition: width 0.3s ease-in-out;
    width: 100%;
}

/* ✅ 검색 버튼 (대화 아이콘 + 주황색 배경) */
.search-btn {
    background: #E76200; /* ✅ 주황색 적용 */
    color: white;
    border: none;
    border-radius: 50%;
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    flex-shrink: 0; /* ✅ 크기 유지 */
}
</style>
