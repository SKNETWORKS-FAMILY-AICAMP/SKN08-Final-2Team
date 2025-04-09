import { defineStore } from 'pinia';
import {accountState} from './accountState'
import {accountAction} from './accountActions'

export const useAccountStore = defineStore('accountStore', {
  state: accountState,
  actions: accountAction,
  // 예: accountStore.ts 또는 로그인 후 응답 처리 부분
});