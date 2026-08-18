export type Match = {
  id: string; competition: string; country: string; home_team: string; away_team: string;
  starts_at: string; status: string; score?: string | null; source: string;
};
export type MarketQuote = { id: string; match_id: string; market: string; selection: string; line?: number | null; odds: number; bookmaker: string; source: string };
export type MatchDetail = Match & { venue: string; statistics: Record<string, Record<string, number>>; recent_form: Record<string, number[]>; markets: MarketQuote[] };
