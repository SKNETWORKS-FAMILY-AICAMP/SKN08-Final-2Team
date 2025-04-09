import { defineNuxtModule } from '@nuxt/kit';
import { resolve } from 'path';

export default defineNuxtModule({
    meta: {
        name: 'home',
        configKey: 'home',
    },

    setup(moduleOptions, nuxt) {
        const themeDir = resolve(__dirname, '..');

        nuxt.hook('pages:extend', (pages) => {
            pages.push({
                name: 'HomePage',
                path: '/',
                file: resolve(themeDir, 'home/pages/HomePage.vue'),
            })
        })
    },
});

