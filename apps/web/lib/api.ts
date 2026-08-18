import type { Match, MatchDetail, MarketQuote } from "./types";

const base = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
async function request<T>(path: string, fallback: T): Promise<T> {
  try {
    const response = await fetch(`${base}${path}`, { next: { revalidate: 30 } });
    return response.ok ? await response.json() : fallback;
  } catch {
    return fallback;
  }
}
export const getMatches = () => request<Match[]>("/api/v1/matches", []);
export const getMatch = (id: string) => request<MatchDetail | null>(`/api/v1/matches/${id}`, null);
export const getMarkets = () => request<MarketQuote[]>("/api/v1/markets", []);
