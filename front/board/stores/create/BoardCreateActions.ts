import * as axiosUtility from "../../../utility/axiosInstance";
import { useAccountStore } from "../../../account/stores/accountStore";

export const boardAction = {
  async requestCreateBoard(payload) {
    console.log("🧪 payload 내용 확인:", payload);

    const { djangoAxiosInstance } = axiosUtility.createAxiosInstances();
    const accountStore = useAccountStore();

    const { title, content, image, end_time, restaurant_id } = payload;
    const author_id = payload.author_id || localStorage.getItem("account_id");

    if (!title || !author_id) {
      console.error("❌ 필수 필드 누락: 제목과 author_id는 필수입니다.");
      throw new Error("제목과 로그인은 필수 입력값입니다.");
    }

    try {
      const formData = new FormData();
      formData.append("title", title);
      formData.append("content", content);
      formData.append("author_id", String(author_id));
      formData.append("end_time", new Date(end_time).toISOString());

      // ✅ image가 File일 경우에만 append
      if (image instanceof File) {
        formData.append("image", image);
      } else if (image) {
        console.warn("⚠️ image가 File 타입이 아님. 무시됨:", image);
      } else {
        console.log("ℹ️ 이미지 없음 (선택사항)");
      }

      if (restaurant_id) {
        formData.append("restaurant_id", String(restaurant_id));
      }

      console.log("📤 게시글 생성 요청 FormData.entries():");
      for (let [key, value] of formData.entries()) {
        console.log(key, ":", value);
      }

      const res = await djangoAxiosInstance.post("/board/create/", formData, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("userToken")}`,
          "Content-Type": undefined  // ✅ 핵심!
        },
      });

      console.log("✅ 게시글 생성 성공:", res.data);
      return res.data;
    } catch (error) {
      console.error(
        "❌ requestCreateBoard() 중 에러:",
        error.response ? error.response.data : error.message
      );
      throw error;
    }
  }
};
