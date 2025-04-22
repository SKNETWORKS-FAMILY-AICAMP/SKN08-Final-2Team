import * as axiosUtility from "../../../utility/axiosInstance";
import type { BoardModify } from "./BoardModifyType";
import { useBoardModifyStore } from "./BoardModifyStore";

export const boardModifyAction = {
  async requestModifyBoard(boardId: number, boardDetails: BoardModify) {
    const store = useBoardModifyStore();

    try {
      const { djangoAxiosInstance } = axiosUtility.createAxiosInstances();
      store.isLoading = true;

      if (!boardDetails.title?.trim() || !boardDetails.content?.trim() || !boardDetails.end_time) {
        throw new Error("제목, 내용, 종료일은 필수입니다.");
      }

      const formData = new FormData();
      formData.append("title", boardDetails.title);
      formData.append("content", boardDetails.content);
      formData.append("end_time", boardDetails.end_time);

      if (boardDetails.restaurant_id) {
        formData.append("restaurant", boardDetails.restaurant_id.toString());
      }

      if (typeof boardDetails.image === "string") {
        // 기존 이미지 URL이므로 변경하지 않음 (이미 존재함)
        console.log("ℹ️ 기존 이미지 유지:", boardDetails.image);
        // 아무것도 추가하지 않으면 서버에서 이미지 필드는 그대로 유지
      } else if (boardDetails.image instanceof File) {
        formData.append("image", boardDetails.image); // ✅ 새 이미지로 교체
      } else if (boardDetails.image === null) {
        formData.append("image", ""); // ✅ 이미지 제거
      }

      console.log("📤 게시글 수정 요청 FormData.entries():");
      for (let [key, value] of formData.entries()) {
        console.log(key, ":", value);
      }

      formData.append("_method", "PUT");

      const res = await djangoAxiosInstance.post(`board/update/${boardId}/`, formData, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("userToken")}`,
          "Content-Type": undefined, 
        },
      });

      console.log("✅ 게시글 수정 성공:", res.data);

      store.board = res.data;
      store.isSuccess = true;
      store.errorMessage = null;
    } catch (error) {
      console.error("❌ 게시글 수정 중 에러:", error);
      store.isSuccess = false;
      store.errorMessage = "게시글 수정 실패";
      throw error;
    } finally {
      store.isLoading = false;
    }
  }
};
