import type { Match } from "./types";

export const primaryCompetitions = [
  { id: 39, label: "Premier League", country: "England", priority: 1 }, { id: 140, label: "LaLiga", country: "Spain", priority: 2 },
  { id: 135, label: "Serie A", country: "Italy", priority: 3 }, { id: 78, label: "Bundesliga", country: "Germany", priority: 4 },
  { id: 61, label: "Ligue 1", country: "France", priority: 5 }, { id: 2, label: "UEFA Champions League", country: null, priority: 6 },
  { id: 3, label: "UEFA Europa League", country: null, priority: 7 }, { id: 848, label: "UEFA Conference League", country: null, priority: 8 },
  { id: 13, label: "Copa Libertadores", country: null, priority: 9 }, { id: 11, label: "Copa Sudamericana", country: null, priority: 10 },
  { id: 253, label: "MLS", country: "USA", priority: 11 }, { id: 262, label: "Liga MX", country: "Mexico", priority: 12 },
  { id: 71, label: "Brasileirão", country: "Brazil", priority: 13 }, { id: 128, label: "Liga Argentina", country: "Argentina", priority: 14 },
] as const;

type CompetitionGroup = { key: string; label: string; logo?: string | null; matches: Match[]; primary: boolean };
export function groupMatchesByCompetition(matches: Match[]): CompetitionGroup[] {
  const groups = new Map<string, CompetitionGroup>();
  for (const match of matches) {
    const primary = primaryCompetitions.find((item) => item.id === match.competition_id);
    const key = primary ? `primary-${primary.id}` : `other-${match.competition.toLowerCase()}`;
    const current = groups.get(key) ?? { key, label: primary?.label ?? match.competition, logo: match.competition_logo, matches: [], primary: Boolean(primary) };
    current.matches.push(match); groups.set(key, current);
  }
  const main = primaryCompetitions.map((item) => groups.get(`primary-${item.id}`)).filter((group): group is CompetitionGroup => Boolean(group));
  const other = [...groups.values()].filter((group) => !group.primary).sort((a, b) => a.label.localeCompare(b.label, "es"));
  return [...main, ...(other.length ? [{ key: "other", label: "Otras ligas y competiciones", matches: other.flatMap((group) => group.matches), primary: false }] : [])];
}
export function groupSecondary(matches: Match[]) { return [...new Map(matches.map((match) => [match.competition, matches.filter((item) => item.competition === match.competition)])).entries()].sort(([a], [b]) => a.localeCompare(b, "es")); }
