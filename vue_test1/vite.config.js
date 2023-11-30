import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
  ,build: {
    rollupOptions: {
      external: [
                'src/components/images/com_4.jpeg',
                'src/components/images/com_5.jpg',
                'src/components/images/com_23.png',
                'src/components/images/com_24.png',
                'src/components/images/com_38.jpg'
                ]
                // 将此项添加到external数组中
    },
  },
})
