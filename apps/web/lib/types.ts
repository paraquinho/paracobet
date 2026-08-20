export type Sport = "football" | "tennis";
export type Match = {
  id: string; sport?: Sport; competition: string; country: string; home_team: string; away_team: string;
  starts_at: string; status: string; score?: string | null; source: string;
  home_team_id?: number | null; away_team_id?: number | null; home_logo?: string | null; away_logo?: string | null;
  season?: number | null;
  competition_id?: number | null;
  competition_logo?: string | null;
  surface?: string; round?: string; sets?: string;
};
export type MarketQuote = { id: string; match_id: string; market: string; selection: string; line?: number | null; odds: number; bookmaker: string; source: string };
export type MatchDetail = Match & { venue: string; statistics: Record<string, Record<string, number>>; recent_form: Record<string, number[]>; markets: MarketQuote[] };
export type PerformanceStats = { played?: number | null; wins?: number | null; draws?: number | null; losses?: number | null; goals_for?: number | null; goals_against?: number | null; goals_for_avg?: number | null; goals_against_avg?: number | null; clean_sheets?: number | null; failed_to_score?: number | null };
export type TeamStatistics = { team_id: number; team_name: string; logo?: string | null; country?: string | null; competition_id: number; season: number; source: string; general: PerformanceStats; home: PerformanceStats; away: PerformanceStats };
export type FormWindow = { window: number; sample_size: number; wins: number; draws: number; losses: number; goals_for: number; goals_against: number; average_goals_for: number; average_goals_against: number; points: number; possible_points: number; points_percentage: number; matches: Array<{ fixture_id: number; date: string; opponent: string; result: string; goals_for?: number | null; goals_against?: number | null; is_home: boolean }> };
export type TeamForm = { team_id: number; team_name: string; competition_id: number; season: number; source: string; windows: Record<string, FormWindow> };
export type PickStatus = "won" | "lost" | "pending";
export type ParlayPick = { event: string; market: string; selection: string; odds: number; status: PickStatus };
export type ParlayHistoryEntry = { id: string; date: string; title: string; sport: Sport; picks: ParlayPick[]; status: PickStatus };
