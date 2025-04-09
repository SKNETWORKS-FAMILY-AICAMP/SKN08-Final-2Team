import { defineStore } from "pinia";
import { state } from "./BoardDeleteState";
import { useBoardDeleteActions } from "./BoardDeleteActions";

export const useBoardDeleteStore = defineStore("boardDelete", () => {
  return {
    ...state,
    ...useBoardDeleteActions(),
  };
});
