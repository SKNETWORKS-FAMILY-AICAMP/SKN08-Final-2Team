import type { CommentState } from "./CommentType";

export const commentState = (): CommentState => ({
  comments: [],
  total: 0,
  isLoading: false,
  isSuccess: false,
  errorMessage: null,
});