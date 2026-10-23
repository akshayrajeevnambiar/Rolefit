import react from "@vitejs/plugin-react";
import { defineConfig, loadEnv } from "vite";

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
        // Repo root stays readable so src/styles.css can import
        // ../../design/tokens.css once the design PR is on main.
        allow: [".."],
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
