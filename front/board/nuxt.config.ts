import { defineNuxtConfig } from "nuxt/config";

export default defineNuxtConfig({
    // pages: true, // ✅ Nuxt가 자동으로 `pages/` 디렉터리를 감지하도록 설정
    router: {
        options: {
            strict: true,
        },
    },
});
