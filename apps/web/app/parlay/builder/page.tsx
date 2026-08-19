import { BuilderPanel } from "@/components/builder-panel";
import { Shell } from "@/components/shell";
import { getMarkets } from "@/lib/api";

export default async function BuilderPage() {
  const markets = await getMarkets();
  return <Shell><p className="eyebrow">Generación de candidatas mock</p><h1 className="mt-2 text-3xl font-semibold text-white">Constructor de combinadas</h1><p className="mt-2 text-sm text-slate-400">Construye y valida una combinación con las cuotas sintéticas disponibles.</p><div className="mt-7"><BuilderPanel markets={markets} /></div></Shell>;
}
