import { MatchExplorer } from "@/components/match-explorer";
import { Shell } from "@/components/shell";
import { getMatches } from "@/lib/api";
import { getActiveSport, sportLabels } from "@/lib/sport";

export default async function MatchesPage() { const sport = await getActiveSport(); const matches = await getMatches(sport); return <Shell><p className="eyebrow">Explorador de {sportLabels[sport].toLowerCase()}</p><h1 className="mt-2 text-3xl font-semibold text-white">Partidos · {sportLabels[sport]}</h1><p className="mt-2 text-sm text-slate-400">Filtra por fecha, competición o participante. Los resultados proceden de la API mock.</p><div className="mt-6"><MatchExplorer matches={matches} /></div></Shell>; }
