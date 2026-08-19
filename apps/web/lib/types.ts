export type Sport = "football" | "tennis";
export type Match = {
  id: string; sport?: Sport; competition: string; country: string; home_team: string; away_team: string;
  starts_at: string; status: string; score?: string | null; source: string;
  surface?: string; round?: string; sets?: string;
};
export type MarketQuote = { id: string; match_id: string; market: string; selection: string; line?: number | null; odds: number; bookmaker: string; source: string };
export type MatchDetail = Match & { venue: string; statistics: Record<string, Record<string, number>>; recent_form: Record<string, number[]>; markets: MarketQuote[] };
export type PickStatus = "won" | "lost" | "pending";
export type ParlayPick = { event: string; market: string; selection: string; odds: number; status: PickStatus };
export type ParlayHistoryEntry = { id: string; date: string; title: string; sport: Sport; picks: ParlayPick[]; status: PickStatus };
