import * as axiosUtility from "../../../utility/axiosInstance";
// action 통합

export const authenticationAction = {
    async requestLoginToDjango(provider: "kakao" | "naver"): Promise<void> {
        const { djangoAxiosInstance } = axiosUtility.createAxiosInstances();

        try {
            const url = provider === "kakao"
                ? "/kakao-oauth/request-login-url"
                : "/naver-oauth/request-login-url";

            return djangoAxiosInstance.get(url).then((res) => {
                console.log(`res: ${res}`);
                window.location.href = res.data.url;
            });
        } catch (error) {
            console.log(`request${provider.toUpperCase()}OauthRedirectionToDjango() 중 에러:`, error);
        }
    },

    async requestAccessToken(provider: "kakao" | "naver", code: string): Promise<{ userToken: string, accountId: string } | null> {
        const { djangoAxiosInstance } = axiosUtility.createAxiosInstances();

        try {
            const url = provider === "kakao"
                ? "/kakao-oauth/redirect-access-token"
                : "/naver-oauth/redirect-access-token";

            const response = await djangoAxiosInstance.post(url, { code });

            console.log("🧪 OAuth 응답 전체:", response);
            console.log("🧪 response.headers:", response.headers);
            console.log("🧪 response.data:", response.data);

            const userToken = response.headers["usertoken"] || response.data.userToken;
            const accountId = response.headers["account_id"] || response.data.account_id;

            if (!userToken || !accountId) {
            throw new Error("로그인 응답에 필요한 정보가 없습니다.");
            }
            return { userToken, accountId};
        } catch (error) {
            console.log(`${provider.toUpperCase()} Access Token 요청 중 문제 발생:`, error);
            throw error;
        }
    },

    async requestLogout(provider: "kakao" | "naver", userToken: string): Promise<void> {
        const { djangoAxiosInstance } = axiosUtility.createAxiosInstances();

        try {
            const url = provider === "kakao"
                ? "/authentication/kakao-logout"
                : "/authentication/naver-logout";

            await djangoAxiosInstance.post(url, { userToken });

            localStorage.removeItem("userToken");
            localStorage.removeItem("account_id");
        } catch (error) {
            console.log(`requestLogout(${provider}) 중 에러:`, error);
        }
    },

    async requestValidationUserToken(userToken: string): Promise<boolean> {
        const { djangoAxiosInstance } = axiosUtility.createAxiosInstances();

        try {
            const response = await djangoAxiosInstance.post("/authentication/validation", { userToken });

            if (response.data && response.data.valid !== undefined) {
                return response.data.valid;
            } else {
                console.error("Invalid response structure:", response.data);
                return false;
            }
        } catch (error) {
            console.log("requestValidationUserToken() 중 에러:", error);
            return false;
        }
    },
};
