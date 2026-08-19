import type { MarketQuote, Match, MatchDetail } from "./types";

const date = new Date();
date.setHours(date.getHours() + 3, 0, 0, 0);
export const mockMatches: Match[] = [
  { id: "mock-001", competition: "Liga Ibérica de Analítica", country: "España", home_team: "Atlético Norte", away_team: "Costa Azul", starts_at: date.toISOString(), status: "scheduled", source: "mock" },
  { id: "mock-002", competition: "Liga Ibérica de Analítica", country: "España", home_team: "Real Montaña", away_team: "Deportivo Río", starts_at: new Date(date.getTime() + 7200000).toISOString(), status: "scheduled", source: "mock" },
  { id: "mock-003", competition: "Métricas Premier", country: "Inglaterra", home_team: "West Harbour", away_team: "Kingsbridge", starts_at: new Date(date.getTime() - 18000000).toISOString(), status: "finished", score: "2 - 1", source: "mock" },
  { id: "mock-004", competition: "Liga Ibérica de Analítica", country: "España", home_team: "Valle Central", away_team: "Puerto Real", starts_at: new Date(date.getTime() + 86400000).toISOString(), status: "scheduled", source: "mock" },
  { id: "mock-005", competition: "Métricas Premier", country: "Inglaterra", home_team: "East Borough", away_team: "River Town", starts_at: new Date(date.getTime() + 172800000).toISOString(), status: "scheduled", source: "mock" },
];
export const mockMarkets: MarketQuote[] = [
  { id: "q-001", match_id: "mock-001", market: "Total de goles", selection: "Más de 2.5", line: 2.5, odds: 1.82, bookmaker: "MockBook", source: "mock" },
  { id: "q-002", match_id: "mock-001", market: "Total de córners", selection: "Más de 8.5", line: 8.5, odds: 1.91, bookmaker: "MockBook", source: "mock" },
  { id: "q-003", match_id: "mock-001", market: "Ambos equipos marcan", selection: "Sí", odds: 1.74, bookmaker: "MockBook", source: "mock" },
  { id: "q-004", match_id: "mock-004", market: "Total de goles", selection: "Más de 2.5", line: 2.5, odds: 1.88, bookmaker: "MockBook", source: "mock" },
  { id: "q-005", match_id: "mock-005", market: "Resultado", selection: "Local", odds: 2.04, bookmaker: "MockBook", source: "mock" },
];
export const mockDetail: MatchDetail = { ...mockMatches[0], venue: "Estadio de Datos", markets: mockMarkets, statistics: { goals: { home: 1.6, away: 1.2 }, shots: { home: 13.4, away: 10.8 }, shots_on_target: { home: 5.1, away: 4.2 }, corners: { home: 5.8, away: 4.9 }, cards: { home: 2.1, away: 2.5 }, fouls: { home: 11.2, away: 12.7 }, possession: { home: 53, away: 47 } }, recent_form: { home: [2, 1, 3, 1, 2], away: [1, 2, 0, 2, 1] } };
