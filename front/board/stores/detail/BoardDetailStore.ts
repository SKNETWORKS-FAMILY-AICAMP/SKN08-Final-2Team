import { defineStore } from "pinia";
import { boardDetailState } from "./BoardDetailState";
import { useBoardDetailActions } from "./BoardDetailActions";

export const useBoardDetailStore = defineStore("boardDetailStore", {
  state: boardDetailState,
  actions: {
    async requestDetailBoard(boardId: number) {
      this.isLoading = true;
      try {
        const result = await useBoardDetailActions.requestDetailBoard(boardId);
        if (result && result.success) {
          this.board = result;
          this.isSuccess = true;
          this.errorMessage = null;
        } else {
          this.errorMessage = result?.error || "상세 데이터를 불러오지 못했습니다.";
          this.isSuccess = false;
        }
      } catch (error) {
        console.error("❌ 상세 요청 중 오류:", error);
        this.errorMessage = "서버 오류가 발생했습니다.";
        this.isSuccess = false;
      } finally {
        this.isLoading = false;
      }
    },
  },
});
