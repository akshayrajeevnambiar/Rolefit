import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";

// Vitest turns a CSS import into an empty module. Read the file instead.
const source = readFileSync(new URL("./styles.css", import.meta.url), "utf8");

function withoutComments(css: string): string {
  return css.replace(/\/\*[\s\S]*?\*\//g, "");
}

describe("placeholder styles", () => {
  const css = withoutComments(source);

  it("imports the Proof token file", () => {
    expect(css).toContain('@import "../../design/tokens.css";');
  });

  it("loads Schibsted Grotesk and IBM Plex Mono from design/fonts", () => {
    expect(css).toContain('font-family: "Schibsted Grotesk"');
    expect(css).toContain('font-family: "IBM Plex Mono"');
    expect(css).toContain("schibsted-grotesk-latin.woff2");
    expect(css).toContain("ibm-plex-mono-400-latin.woff2");
    expect(css).toContain("ibm-plex-mono-500-latin.woff2");
  });
});
