import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    target: 'esnext',
    minify: 'esbuild',
    rollupOptions: {
      onwarn(warning, warn) {
        console.warn('ROLLUP WARNING:', warning.message);
        warn(warning);
      }
    }
  }
})
