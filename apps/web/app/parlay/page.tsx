import { ParlayAnalyzer } from "@/components/parlay-analyzer";
import { Shell } from "@/components/shell";

export default function ParlayPage() { return <Shell><p className="eyebrow">Análisis de probabilidades explicable</p><h1 className="mt-2 text-3xl font-semibold text-white">Analizador de combinadas</h1><p className="mt-2 max-w-3xl text-sm leading-6 text-slate-400">Compara frecuencia histórica, probabilidad del modelo y probabilidad implícita. Todos los valores son demostrativos y proceden de datos mock.</p><div className="mt-7"><ParlayAnalyzer /></div></Shell>; }
