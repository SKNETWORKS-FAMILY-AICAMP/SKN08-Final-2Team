import { djangoAxiosInstance } from "~/utility/axiosInstance";
import type { Comment } from "./CommentType";

export const useCommentActions = () => {
  const fetchCommentsByBoard = async (boardId: number, page: number = 1): Promise<{ comments: Comment[], total: number }> => {
    const response = await djangoAxiosInstance?.get(`/comment/board/${boardId}/?page=${page}&page_size=10`);
    return {
      comments: response?.data?.comments || [],
      total: response?.data?.total || 0
    };
  };

  const createComment = async (payload: { board_id: number; content: string; author_id: number }): Promise<Comment> => {
    const response = await djangoAxiosInstance?.post(`/comment/create/`, payload);
    return response?.data;
  };

  const createReply = async (payload: { board_id: number; content: string; parent_id: number; author_id: number }): Promise<Comment> => {
    const response = await djangoAxiosInstance?.post(`/comment/reply/`, payload);
    return response?.data;
  };

  const deleteComment = async (commentId: number): Promise<boolean> => {
    const response = await djangoAxiosInstance?.delete(`/comment/delete/${commentId}/`);
    return response?.data.success === true;
  };

  return {
    fetchCommentsByBoard,
    createComment,
    createReply,
    deleteComment,
  };
};