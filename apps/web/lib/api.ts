import type { Match, MatchDetail, MarketQuote } from "./types";
import { mockDetail, mockMarkets, mockMatches } from "./mock-data";
import { tennisDetail, tennisMarkets, tennisMatches } from "./tennis-mock-data";
import type { Sport } from "./types";

/**
 * The MVP is self-contained when no public API URL is configured. This is
 * important for Vercel prerendering: a build must never wait on localhost.
 * Once FastAPI is published, setting NEXT_PUBLIC_API_URL opts into the API.
 */
const base = process.env.NEXT_PUBLIC_API_URL?.trim();
async function request<T>(path: string, fallback: T): Promise<T> {
  if (!base) return fallback;
  try {
    const response = await fetch(`${base}${path}`, { next: { revalidate: 30 } });
    return response.ok ? await response.json() : fallback;
  } catch {
    return fallback;
  }
}
export const getMatches = (sport: Sport = "football", date?: string) => sport === "tennis" ? Promise.resolve(tennisMatches) : request<Match[]>(`/api/v1/matches?timezone=America%2FBogota${date ? `&date=${date}` : ""}`, mockMatches);
export const getMatch = (id: string, sport: Sport = "football") => sport === "tennis" ? Promise.resolve(id === tennisDetail.id ? tennisDetail : null) : request<MatchDetail | null>(`/api/v1/matches/${id}`, id === mockDetail.id ? mockDetail : null);
export const getMarkets = (sport: Sport = "football") => sport === "tennis" ? Promise.resolve(tennisMarkets) : request<MarketQuote[]>("/api/v1/markets", mockMarkets);
