import type { MarketQuote, Match, MatchDetail } from "./types";

const base = new Date();
base.setHours(base.getHours() + 4, 0, 0, 0);
export const tennisMatches: Match[] = [
  { id: "tennis-001", sport: "tennis", competition: "Circuito Ibérico", country: "España", home_team: "Lucía Soler", away_team: "Marta Vidal", starts_at: base.toISOString(), status: "scheduled", source: "mock", surface: "Tierra batida", round: "Cuartos de final" },
  { id: "tennis-002", sport: "tennis", competition: "Open de Datos", country: "Francia", home_team: "Nora Campos", away_team: "Elena Costa", starts_at: new Date(base.getTime() + 7200000).toISOString(), status: "scheduled", source: "mock", surface: "Dura", round: "Semifinal" },
  { id: "tennis-003", sport: "tennis", competition: "Circuito Ibérico", country: "España", home_team: "Paula Marín", away_team: "Irene León", starts_at: new Date(base.getTime() - 7200000).toISOString(), status: "finished", score: "2 - 1", source: "mock", surface: "Hierba", round: "Final" },
];
export const tennisMarkets: MarketQuote[] = [
  { id: "tennis-q-001", match_id: "tennis-001", market: "Ganador del partido", selection: "Lucía Soler", odds: 1.72, bookmaker: "MockBook", source: "mock" },
  { id: "tennis-q-002", match_id: "tennis-001", market: "Total de juegos", selection: "Más de 22.5", line: 22.5, odds: 1.87, bookmaker: "MockBook", source: "mock" },
  { id: "tennis-q-003", match_id: "tennis-001", market: "Hándicap de juegos", selection: "Lucía Soler -2.5", line: -2.5, odds: 1.91, bookmaker: "MockBook", source: "mock" },
];
export const tennisDetail: MatchDetail = { ...tennisMatches[0], venue: "Centro de Datos Tennis", markets: tennisMarkets, statistics: { sets: { home: 2, away: 1 }, games: { home: 18, away: 15 }, aces: { home: 6, away: 4 }, double_faults: { home: 2, away: 3 } }, recent_form: { home: [2, 2, 1, 2, 2], away: [1, 2, 2, 1, 2] } };
