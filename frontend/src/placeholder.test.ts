import { describe, expect, it } from "vitest";
import { placeholderMessage, placeholderMeta } from "./placeholder";

describe("placeholderMessage", () => {
  it("names RoleFit", () => {
    expect(placeholderMessage()).toContain("RoleFit");
  });
});

describe("placeholderMeta", () => {
  it("is the short data line, not a second screen", () => {
    expect(placeholderMeta()).toBe("Local only");
  });
});
