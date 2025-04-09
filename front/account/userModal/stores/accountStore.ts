import { defineStore } from 'pinia';
import {accountState} from './accountState'
import {accountAction} from './accountActions'

export const useAccountStore = defineStore('accountStore', {
  state: accountState,
  actions: accountAction,
});