import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api/v1/user': {
        target: 'http://localhost:8001',
        changeOrigin: true,
      },
      '/api/v1/itinerary': {
        target: 'http://localhost:8002',
        changeOrigin: true,
      },
      '/api/v1/search': {
        target: 'http://localhost:8003',
        changeOrigin: true,
      },
      '/api/v1/payment': {
        target: 'http://localhost:8004',
        changeOrigin: true,
      },
      '/api/v1/notification': {
        target: 'http://localhost:8005',
        changeOrigin: true,
      },
      '/api/v1/review': {
        target: 'http://localhost:8007',
        changeOrigin: true,
      },
      '/ws': {
        target: 'ws://localhost:8005',
        ws: true,
      },
    },
  },
})