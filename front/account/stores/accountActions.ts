import * as axiosUtility from "../../utility/axiosInstance";
import type { AxiosResponse } from "axios";
import { useAccountStore } from "./accountStore";

export const accountAction = {
  async getAccount(): Promise<void> {
    const { djangoAxiosInstance } = axiosUtility.createAxiosInstances();
    try {
      const accountRes: AxiosResponse = await djangoAxiosInstance.get("/account/get");

      console.log("✅ 계정 정보 응답:", accountRes.data);

      useAccountStore().$patch({
        email: accountRes.data.email,
        accountPath: accountRes.data.account_path,
        accountRegister: accountRes.data.account_register,
      });

    } catch (error) {
      console.error("❌ getAccount() 오류:", error);
    }
  },

  async getProfile(): Promise<void> {
    const { djangoAxiosInstance } = axiosUtility.createAxiosInstances();
    try {
      const profileRes: AxiosResponse = await djangoAxiosInstance.get("/account-profile/get");

      console.log("✅ 프로필 정보 응답:", profileRes.data);

      useAccountStore().$patch({
        name: profileRes.data.account_name,
        nickname: profileRes.data.account_nickname,
        phoneNum: profileRes.data.phone_num,
        address: profileRes.data.account_add,
        gender: profileRes.data.account_sex,
        birth: profileRes.data.account_birth,
        payment: profileRes.data.account_pay,
        subscribe: profileRes.data.account_sub,
        age: profileRes.data.account_age,
      });

    } catch (error) {
      console.error("❌ getProfile() 오류:", error);
    }
  },

  async getAccountAndProfile(): Promise<void> {
    try {
      await this.getAccount();
      await this.getProfile();
    } catch (error) {
      console.error("❌ getAccountAndProfile() 오류:", error);
    }
  },
};
