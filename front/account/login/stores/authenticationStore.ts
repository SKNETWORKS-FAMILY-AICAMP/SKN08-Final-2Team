import { defineStore } from "pinia";
import { authenticationState } from "./authenticationState";
import { authenticationAction } from "./authenticationActions";

//TODO:  통합 store 후에 다른 인증방식 추가되면 추가할 예정 
export const useAuthenticationStore = defineStore("authenticationStore", {
    state: authenticationState,
    actions: authenticationAction,
});
