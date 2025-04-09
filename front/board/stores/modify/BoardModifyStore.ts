import { defineStore } from "pinia";
import { boardModifyState } from "./BoardModifyState";
import { boardModifyAction } from "./BoardModifyActions";

export const useBoardModifyStore = defineStore("boardModifyStore", {
    state: boardModifyState, 
    actions: boardModifyAction,
  });
  