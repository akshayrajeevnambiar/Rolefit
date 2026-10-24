import { realpathSync } from "node:fs";
import { resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { loadConfigFromFile, type ConfigEnv } from "vite";
import { describe, expect, it } from "vitest";

// Computed here, not read from the names in vite.config.ts. A later edit
// that pointed those variables at "/" would still contain the old text.
const frontendRoot = fileURLToPath(new URL("..", import.meta.url));
const designDir = fileURLToPath(new URL("../../design", import.meta.url));

describe("vite file access", () => {
  it("allows the resolved frontend and design directories only", async () => {
    const env: ConfigEnv = { command: "serve", mode: "development" };
    const loaded = await loadConfigFromFile(
      env,
      resolve(frontendRoot, "vite.config.ts"),
    );
    const allow = loaded?.config.server?.fs?.allow ?? [];
    const resolved = allow.map((entry) => realpathSync(entry));

    expect(resolved).toEqual([realpathSync(frontendRoot), realpathSync(designDir)]);
    expect(resolved).not.toContain(realpathSync(resolve(frontendRoot, "..")));
    expect(resolved).not.toContain("/");
  });
});
