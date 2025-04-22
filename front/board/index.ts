import { defineNuxtModule } from '@nuxt/kit';
import { resolve } from 'path';

export default defineNuxtModule({
    meta: {
        name: 'board',
        configKey: 'board',
    },

    setup(moduleOptions, nuxt) {
        const themeDir = resolve(__dirname, '..');

        nuxt.hook('pages:extend', (pages) => {
            // 게시판 리스트 페이지 추가
            pages.push({
                name: 'BoardList',
                path: '/board/all',
                file: resolve(themeDir, 'board/pages/list/List.vue'),
            });

            // 게시판 생성 페이지 추가
            pages.push({
                name: 'BoardCreate',
                path: '/board/create',
                file: resolve(themeDir, 'board/pages/create/Create.vue'),
            });
            pages.push({
                name: 'BoardDetail',
                path: '/board/:id',
                file: resolve(themeDir, 'board/pages/detail/Detail.vue'),
              });
            pages.push({
                name: 'BoardModify',
                path: '/board/modify/:id',
                file: resolve(themeDir, 'board/pages/modify/Modify.vue'),
              });
            
        });

        nuxt.hook('imports:dirs', (dirs) => {
            dirs.push(resolve(__dirname, 'store'));
        });
    },
});
