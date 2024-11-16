import {TanStackRouterVite} from "@tanstack/router-plugin/vite"
import react from "@vitejs/plugin-react"
import path from "path"
import {visualizer} from "rollup-plugin-visualizer"
import {defineConfig} from "vite"

// https://vitejs.dev/config/
export default defineConfig({
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  build: {
    chunkSizeWarningLimit: 1000,
    rollupOptions: {
      output: {
        manualChunks: (id) => {
          // our big bundles mainly consist of threejs (used by google model viewer)
          // our graphql queries and all other vendor packages
          if (id.includes("node_modules/three")) return "threejs"
          else if (id.includes("node_modules/@google/model-viewer"))
            return "model-viewer"
          else if (id.includes("src/gql")) return "gql"
          else if (id.includes("node_modules")) return "vendor"
        },
      },
    },
  },
  plugins: [TanStackRouterVite(), visualizer(), react()],
})
