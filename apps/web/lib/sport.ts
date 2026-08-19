import { cookies } from "next/headers";
import type { Sport } from "./types";
export { sportLabels } from "./sport-labels";

export async function getActiveSport(): Promise<Sport> {
  const value = (await cookies()).get("paracobet-sport")?.value;
  return value === "tennis" ? "tennis" : "football";
}
