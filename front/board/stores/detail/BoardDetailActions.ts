import * as axiosUtility from "../../../utility/axiosInstance";
import type { BoardDetail } from "./BoardDetailType";

export const useBoardDetailActions = {
  async requestDetailBoard(boardId: number): Promise<BoardDetail | null> {
    try {
      const { djangoAxiosInstance } = axiosUtility.createAxiosInstances();
      const res = await djangoAxiosInstance.get(`/board/${boardId}/`);
      console.log("✅ 상세 게시글 조회 결과:", res.data);
      return res.data;
    } catch (error) {
      console.error("❌ 게시글 상세 조회 실패:", error);
      return null;
    }
  },
};
