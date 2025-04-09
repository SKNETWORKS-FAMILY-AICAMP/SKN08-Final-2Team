import { defineStore } from "pinia";
import { boardDetailState } from "./BoardDetailState";
import { boardDetailAction } from "./BoardDetailActions";

export const useBoardDetailStore = defineStore("boardDetailStore", {
  state: boardDetailState,
  actions: {
    async requestDetailBoard(boardId: number) {
      return await boardDetailAction.requestDetailBoard(boardId);
    }
  },
});
