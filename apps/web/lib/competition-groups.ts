import type { Match } from "./types";

export const primaryCompetitions = [
  { id: 39, label: "Premier League" }, { id: 140, label: "LaLiga" }, { id: 135, label: "Serie A" },
  { id: 78, label: "Bundesliga" }, { id: 61, label: "Ligue 1" }, { id: 2, label: "UEFA Champions League" },
  { id: 3, label: "UEFA Europa League" }, { id: 848, label: "UEFA Conference League" }, { id: 13, label: "Copa Libertadores" },
  { id: 11, label: "Copa Sudamericana" }, { id: 253, label: "MLS" }, { id: 262, label: "Liga MX" },
  { id: 71, label: "Brasileirão" }, { id: 128, label: "Liga Argentina" },
] as const;

type CompetitionGroup = { key: string; label: string; matches: Match[]; primary: boolean };
export function groupMatchesByCompetition(matches: Match[]): CompetitionGroup[] {
  const groups = new Map<string, CompetitionGroup>();
  for (const match of matches) {
    const primary = primaryCompetitions.find((item) => item.id === match.competition_id || item.label.toLowerCase() === match.competition.toLowerCase());
    const key = primary ? `primary-${primary.id}` : `other-${match.competition.toLowerCase()}`;
    const current = groups.get(key) ?? { key, label: primary?.label ?? match.competition, matches: [], primary: Boolean(primary) };
    current.matches.push(match); groups.set(key, current);
  }
  const main = primaryCompetitions.map((item) => groups.get(`primary-${item.id}`)).filter((group): group is CompetitionGroup => Boolean(group));
  const other = [...groups.values()].filter((group) => !group.primary).sort((a, b) => a.label.localeCompare(b.label, "es"));
  return [...main, ...(other.length ? [{ key: "other", label: "Otras ligas y competiciones", matches: other.flatMap((group) => group.matches), primary: false }] : [])];
}
export function groupSecondary(matches: Match[]) { return [...new Map(matches.map((match) => [match.competition, matches.filter((item) => item.competition === match.competition)])).entries()].sort(([a], [b]) => a.localeCompare(b, "es")); }
