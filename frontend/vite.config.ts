import { fileURLToPath } from "node:url";
import react from "@vitejs/plugin-react";
import { defineConfig, loadEnv } from "vite";

// Directory of this config file, and the design system next to frontend/.
// Allowing ".." would be the repo on the host and / inside the image.
const frontendRoot = fileURLToPath(new URL(".", import.meta.url));
const designDir = fileURLToPath(new URL("../design", import.meta.url));

// Vitest reads the `test` key from this Vite config.
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const apiProxyTarget = env.VITE_API_PROXY_TARGET || "http://127.0.0.1:8000";

  return {
    plugins: [react()],
    server: {
      host: true,
      port: 5173,
      strictPort: true,
      fs: {
        allow: [frontendRoot, designDir],
      },
      proxy: {
        "/api": {
          target: apiProxyTarget,
          changeOrigin: true,
        },
      },
    },
    test: {
      environment: "node",
      include: ["src/**/*.test.ts"],
    },
  };
});
