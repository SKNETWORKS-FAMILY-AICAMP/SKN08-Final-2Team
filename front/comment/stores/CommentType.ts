export interface Comment {
  comment_id: number;
  content: string;
  author_nickname: string;
  created_at: string;
  author_account_id?: number;
  is_deleted?: boolean;
  is_author?: boolean;
  parent_id?: number;
  replies?: Comment[];
  is_liked?: boolean;
  like_count?: number;
}

export interface CommentState {
  comments: Comment[];
  total: number;
  isLoading: boolean;
  isSuccess: boolean;
  errorMessage: string | null;
}