import * as axiosUtility from "../../../utility/axiosInstance";

export const useBoardDeleteActions = () => {
  const requestDeleteBoard = async (boardId: number): Promise<boolean> => {
    try {
      const response = await axiosUtility.djangoAxiosInstance?.delete(
        `/board/delete/${boardId}/`
      );

      if (response?.data?.success) {
        console.log("✅ 게시글 삭제 성공");
        return true;
      } else {
        console.warn("⚠️ 게시글 삭제 실패: ", response?.data?.message || "응답 없음");
        return false;
      }
    } catch (error) {
      console.error("❌ 게시글 삭제 중 예외 발생:", error);
      throw error;
    }
  };

  return {
    requestDeleteBoard,
  };
};