import { MatchExplorer } from "@/components/match-explorer";
import { Shell } from "@/components/shell";
import { getMatches } from "@/lib/api";

export default async function MatchesPage() { const matches = await getMatches(); return <Shell><p className="eyebrow">Explorador de partidos</p><h1 className="mt-2 text-3xl font-semibold text-white">Partidos</h1><p className="mt-2 text-sm text-slate-400">Filtra por fecha, competición, equipo y estado. Los resultados proceden de la API mock.</p><div className="mt-6"><MatchExplorer matches={matches} /></div></Shell>; }
