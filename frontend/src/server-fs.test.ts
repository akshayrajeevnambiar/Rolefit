import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";

const source = readFileSync(new URL("../vite.config.ts", import.meta.url), "utf8");

describe("vite file access", () => {
  it("allows the frontend and design directories, not the parent", () => {
    expect(source).toContain("allow: [frontendRoot, designDir]");
    expect(source).not.toMatch(/allow:\s*\[\s*["']\.\.["']\s*\]/);
  });
});
