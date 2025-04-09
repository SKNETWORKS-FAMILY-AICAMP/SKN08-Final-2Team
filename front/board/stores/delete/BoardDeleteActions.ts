import * as axiosUtility from "../../../utility/axiosInstance";

export const useBoardDeleteActions = () => {
  const requestDeleteBoard = async (boardId: number, passedUserId?: number): Promise<boolean> => {
    const userId = typeof passedUserId === "number" && !isNaN(passedUserId)
      ? passedUserId
      : Number(localStorage.getItem("account_id"));

    if (!userId) {
      console.warn("❗ userId가 없음, 삭제 불가");
      throw new Error("userId가 유효하지 않습니다.");
    }

    console.log("🗑 삭제 시도 - 현재 유저 id:", userId);

    try {
      const response = await axiosUtility.djangoAxiosInstance?.delete(
        `/board/delete/${boardId}/`,
        {
          params: { user_id: userId }, // 👈 query param으로 전달
        }
      );

      if (response?.data?.success) {
        console.log("✅ 게시글 삭제 성공");
        return true;
      } else {
        console.warn("⚠️ 게시글 삭제 실패: ", response?.data?.error || "응답 없음");
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
