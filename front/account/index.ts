import { defineNuxtModule } from "@nuxt/kit";
import { resolve } from "path";

export default defineNuxtModule({
  meta: {
    name: "account",
    configKey: "account",
  },

  setup(moduleOptions, nuxt) {
    const themeDir = resolve(__dirname, "..");

    nuxt.hook("pages:extend", (pages) => {
      
      pages.push(
        {
          name: "OAuthRedirection",
          path: "/:provider-oauth/redirect-access-token",
          file: resolve(themeDir, "account/login/pages/OAuthRedirection.vue"),
        },
        {
          name: "AccountLoginPage",
          path: "/account/login",
          file: resolve(themeDir, "account/login/pages/AccountLoginPage.vue"),
        },
        {
          name: "UserModal",
          path: "/account/userModal",
          file: resolve(themeDir, "account/userModal/pages/UserModal.vue"),
        }
      );
    });

    nuxt.hook("imports:dirs", (dirs) => {
      dirs.push(resolve(__dirname, "store"));
    });
  }
});
