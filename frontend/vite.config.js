import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

const DIRECCION_DEL_API = 'http://127.0.0.1:8000'
const PREFIJO_PROXY = /^\/api/

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: DIRECCION_DEL_API,
        rewrite: (ruta) => ruta.replace(PREFIJO_PROXY, ''),
      },
    },
  },
})
