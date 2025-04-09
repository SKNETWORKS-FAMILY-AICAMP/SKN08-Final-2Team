import * as axiosUtility from "../../../utility/axiosInstance";
import type { BoardModify } from "./BoardModifyType";
import { useBoardModifyStore } from "./BoardModifyStore"; 

// 여러 개의 데이터 전달해야해서 boardDetails로 묶음
export const boardModifyAction = {
  async requestModifyBoard(boardId: number, boardDetails: BoardModify) {
    const store = useBoardModifyStore(); 
    const userId = boardDetails.user_id || Number(localStorage.getItem("account_id"));

    try {
      const { djangoAxiosInstance } = axiosUtility.createAxiosInstances();
      store.isLoading = true; 

      // 필수값 검증 (공백 문자열 포함 방지)
      if (
        !userId ||
        !boardDetails.title?.trim() ||
        !boardDetails.content?.trim() ||
        !boardDetails.end_time
      ) {
        console.error("❌ 필수 필드 누락: user_id, title, content, end_time");
        throw new Error("제목, 내용, 종료일은 비워둘 수 없습니다.");
      }

      // FormData 생성
      const formData = new FormData();
      formData.append("user_id", userId.toString());
      formData.append("title", boardDetails.title);
      formData.append("content", boardDetails.content);
      formData.append("end_time", boardDetails.end_time);

      //  restaurant_id가 있을 경우 추가
      if (boardDetails.restaurant_id) {
        formData.append("restaurant", boardDetails.restaurant_id.toString());
      }

      // 이미지 처리
      if (boardDetails.image) {
          if (boardDetails.image instanceof File) {
              // 새 이미지 업로드
              formData.append("image", boardDetails.image);
          } else if (boardDetails.image === null) {
              // 기존 이미지 삭제 요청
              formData.append("image", ""); // 
          }
      }

      console.log("📤 수정 요청 데이터:", Object.fromEntries(formData.entries()));

      const res = await djangoAxiosInstance.put(`board/update/${boardId}/`, formData);
      console.log("게시글 수정 성공:", res.data);
      
      store.board = res.data; 
      store.isSuccess = true;
      store.errorMessage = null;
    } catch (error) {
      console.error("게시글 수정 요청 중 에러 발생:", error);
      store.isSuccess = false;
      store.errorMessage = "게시글 수정 실패";
      throw error;
    } finally {
      store.isLoading = false; 
    }
  },
};
