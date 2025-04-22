import { defineStore } from "pinia";
import { commentState } from "./CommentState";
import { useCommentActions } from "./CommentActions";

export const useCommentStore = defineStore("commentStore", {
  state: commentState,
  actions: {
    async loadComments(boardId: number, page: number = 1) {
      this.isLoading = true;
      try {
        const res = await useCommentActions().fetchCommentsByBoard(boardId, page);
        this.comments = res.comments;
        this.total = res.total;
        this.isSuccess = true;
      } catch (error) {
        this.errorMessage = "댓글 불러오기 실패";
        this.isSuccess = false;
      } finally {
        this.isLoading = false;
      }
    },

    async addComment(payload: { board_id: number; content: string }) {
      try {
        await useCommentActions().createComment({
          board_id: payload.board_id,
          content: payload.content,
          author_id: Number(localStorage.getItem("account_id"))
        });
      } catch (error) {
        console.error("댓글 등록 실패:", error);
      }
    },

    async addReply(payload: { board_id: number; content: string; parent_id: number }) {
      try {
        await useCommentActions().createReply({
          board_id: payload.board_id,
          content: payload.content,
          parent_id: payload.parent_id,
          author_id: Number(localStorage.getItem("account_id"))
        });
      } catch (error) {
        console.error("답글 등록 실패:", error);
      }
    },

    async removeComment(commentId: number) {
      try {
        await useCommentActions().deleteComment(commentId);
      } catch (error) {
        console.error("댓글 삭제 실패:", error);
      }
    },
  },
});