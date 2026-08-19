import { ParlayAnalyzer } from "@/components/parlay-analyzer";
import { Shell } from "@/components/shell";
import { getActiveSport, sportLabels } from "@/lib/sport";

export default async function ParlayPage() { const sport = await getActiveSport(); return <Shell><p className="eyebrow">Análisis explicable · {sportLabels[sport]}</p><h1 className="mt-2 text-3xl font-semibold text-white">Analizador de combinadas</h1><p className="mt-2 max-w-3xl text-sm leading-6 text-slate-400">Compara selecciones de {sportLabels[sport].toLowerCase()}, frecuencia histórica y probabilidad implícita. La combinación es una aproximación independiente del MVP.</p><div className="mt-7"><ParlayAnalyzer sport={sport} /></div></Shell>; }
