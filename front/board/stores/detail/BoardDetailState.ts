import type { BoardDetail } from "./BoardDetailType";

export interface BoardDetailState {
  board: BoardDetail | null;
  isLoading: boolean;
  isSuccess: boolean;
  errorMessage: string | null;
}

export const boardDetailState = (): BoardDetailState => ({
  board: null,
  isLoading: false,
  isSuccess: false,
  errorMessage: null
});
