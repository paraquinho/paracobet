import { BuilderPanel } from "@/components/builder-panel";
import { Shell } from "@/components/shell";
import { getMarkets } from "@/lib/api";
import { getActiveSport, sportLabels } from "@/lib/sport";

export default async function BuilderPage() { const sport = await getActiveSport(); const markets = await getMarkets(sport); return <Shell><p className="eyebrow">Generación de candidatas mock · {sportLabels[sport]}</p><h1 className="mt-2 text-3xl font-semibold text-white">Constructor de combinadas</h1><p className="mt-2 text-sm text-slate-400">Construye una combinación con mercados de {sportLabels[sport].toLowerCase()}.</p><div className="mt-7"><BuilderPanel markets={markets} /></div></Shell>; }
