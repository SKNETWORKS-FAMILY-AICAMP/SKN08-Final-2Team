import { defineNuxtModule } from '@nuxt/kit';
import { resolve } from 'path';

export default defineNuxtModule({
  meta: {
    name: 'comment',
    configKey: 'comment',
  },
  setup(_options, nuxt) {
    const themeDir = resolve(__dirname);

    // store 자동 등록
    nuxt.hook('imports:dirs', (dirs) => {
      dirs.push(resolve(themeDir, 'stores'));
    });
  },
});
