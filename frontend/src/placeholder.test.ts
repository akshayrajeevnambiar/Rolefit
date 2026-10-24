import { describe, expect, it } from "vitest";
import { placeholderMessage } from "./placeholder";

describe("placeholderMessage", () => {
  it("names RoleFit", () => {
    expect(placeholderMessage()).toContain("RoleFit");
  });
});
