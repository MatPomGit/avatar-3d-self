import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

export default defineConfig({
  base: '/avatar-3d-self/',
  plugins: [react()],
  server: { port: 5173 },
  build: { outDir: 'dist' },
})
