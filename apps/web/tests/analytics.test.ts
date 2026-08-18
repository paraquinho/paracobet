import { describe, expect, it } from "vitest";
import { calculateEdge, impliedProbability } from "@/lib/analytics";

describe("analytics", () => {
  it("calculates implied probability", () => expect(impliedProbability(1.7)).toBeCloseTo(0.588235));
  it("calculates edge", () => expect(calculateEdge(0.64, 1.7)).toBeCloseTo(0.051765));
});
