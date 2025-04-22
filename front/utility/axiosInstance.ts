import axios, { type AxiosInstance } from "axios";
import { useRuntimeConfig } from "nuxt/app";

export let djangoAxiosInstance: AxiosInstance | null = null;
export let fastapiAxiosInst: AxiosInstance | null = null;

export function createAxiosInstances() {
    const config = useRuntimeConfig();

    const mainApiUrl: string = config.public.MAIN_API_URL as string;
    const aiBaseUrl: string = config.public.AI_BASE_URL as string;

    console.log('mainApiUrl :', mainApiUrl);
    console.log('aiBaseUrl :', aiBaseUrl);

    const token = typeof window !== 'undefined' ? localStorage.getItem('userToken') : null;

    if (!djangoAxiosInstance) {
        djangoAxiosInstance = axios.create({
            baseURL: mainApiUrl,
            timeout: 5000,
            headers: {
                "Content-Type": "application/json",
                ...(token ? { Authorization: `Bearer ${token}` } : {}),
            },
            withCredentials: true,
        });
        djangoAxiosInstance.interceptors.request.use(
            (config) => {
              if (typeof window !== "undefined") {
                const userToken = localStorage.getItem("userToken");
                const accountId = localStorage.getItem("account_id");
          
                if (userToken) {
                  config.headers["userToken"] = userToken;
                  config.headers["Authorization"] = `Bearer ${userToken}`;
                }
                if (accountId) {
                  config.headers["Account-Id"] = String(accountId);
                }
              }
          
              return config;
            },
            (error) => Promise.reject(error)
          );
    }

    if (!fastapiAxiosInst) {
        fastapiAxiosInst = axios.create({
            baseURL: aiBaseUrl,
            timeout: 10000,
        });
    }

    return { djangoAxiosInstance, fastapiAxiosInst };
}
