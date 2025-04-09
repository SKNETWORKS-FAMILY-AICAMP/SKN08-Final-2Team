import type { BoardModify } from "./BoardModifyType"; 

export const boardModifyState = () => ({
  board: null as BoardModify | null, 
  isLoading: false, 
  isSuccess: false, 
  errorMessage: null as string | null, 
});
