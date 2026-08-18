"use client";

import { useMemo, useState } from "react";

type Selection = { name: string; decimal_odds: number; model_probability: number; historical_frequency: number };
const defaultSelections: Selection[] = [
  { name: "Over 2.5 goles", decimal_odds: 1.82, model_probability: 0.62, historical_frequency: 0.66 },
  { name: "Over 8.5 corners", decimal_odds: 1.91, model_probability: 0.57, historical_frequency: 0.60 },
];
const pct = (value: number) => `${(value * 100).toFixed(1)}%`;

export function ParlayAnalyzer() {
  const [selections, setSelections] = useState(defaultSelections);
  const [error, setError] = useState("");
  const result = useMemo(() => {
    const odds = selections.reduce((total, selection) => total * selection.decimal_odds, 1);
    const model = selections.reduce((total, selection) => total * selection.model_probability, 1);
    return { odds, model, implied: 1 / odds, ev: model * odds - 1 };
  }, [selections]);
  const update = (index: number, field: keyof Selection, value: string) => setSelections(current => current.map((item, itemIndex) => itemIndex === index ? { ...item, [field]: field === "name" ? value : Number(value) } : item));
  async function validateApi() { try { const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"}/api/v1/parlay/analyze`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ selections }) }); if (!response.ok) throw new Error(); setError("Análisis contrastado con la API mock."); } catch { setError("Vista calculada localmente; API no disponible."); } }
  return <div><div className="panel overflow-hidden"><div className="overflow-x-auto"><table className="w-full min-w-[760px] text-left text-sm"><thead className="border-b border-slate-800 text-xs uppercase tracking-wider text-slate-500"><tr><th className="px-4 py-3">Selección</th><th className="px-4 py-3">Cuota</th><th className="px-4 py-3">Freq. hist.</th><th className="px-4 py-3">Modelo</th><th className="px-4 py-3">Implícita</th><th className="px-4 py-3">Edge</th><th /></tr></thead><tbody>{selections.map((selection, index) => <tr key={index} className="border-b border-slate-800"><td className="px-4 py-3"><input value={selection.name} onChange={event => update(index, "name", event.target.value)} className="w-full bg-transparent text-slate-100 outline-none" /></td><td className="px-4 py-3"><input type="number" step="0.01" value={selection.decimal_odds} onChange={event => update(index, "decimal_odds", event.target.value)} className="w-16 bg-transparent text-cyan-300 outline-none" /></td><td className="px-4 py-3"><input type="number" step="0.01" value={selection.historical_frequency} onChange={event => update(index, "historical_frequency", event.target.value)} className="w-14 bg-transparent outline-none" /></td><td className="px-4 py-3"><input type="number" step="0.01" value={selection.model_probability} onChange={event => update(index, "model_probability", event.target.value)} className="w-14 bg-transparent outline-none" /></td><td className="px-4 py-3 text-slate-400">{pct(1 / selection.decimal_odds)}</td><td className="px-4 py-3 text-emerald-400">{pct(selection.model_probability - 1 / selection.decimal_odds)}</td><td className="px-4 py-3"><button aria-label="Eliminar selección" onClick={() => setSelections(current => current.filter((_, itemIndex) => itemIndex !== index))} className="text-slate-500 hover:text-red-300">×</button></td></tr>)}</tbody></table></div><button onClick={() => setSelections(current => [...current, { name: "Nueva selección", decimal_odds: 1.8, model_probability: 0.55, historical_frequency: 0.55 }])} className="m-4 rounded border border-slate-600 px-3 py-2 text-sm text-slate-300 hover:border-cyan-400">+ Añadir selección</button></div><section className="mt-6 grid gap-4 sm:grid-cols-4"><Metric label="Cuota combinada" value={result.odds.toFixed(2)} /><Metric label="Prob. modelo" value={pct(result.model)} /><Metric label="Prob. implícita" value={pct(result.implied)} /><Metric label="EV estimado" value={pct(result.ev)} positive={result.ev > 0} /></section><button onClick={validateApi} className="mt-6 rounded bg-cyan-500 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-cyan-400">Analizar combinación</button>{error && <p className="mt-3 text-xs text-slate-400">{error}</p>}<p className="mt-6 rounded border border-amber-500/20 bg-amber-400/5 p-4 text-sm leading-6 text-amber-100">La probabilidad conjunta usa independencia como aproximación del MVP. Las selecciones pueden tener correlación; el resultado no constituye una garantía ni una recomendación.</p></div>;
}

function Metric({ label, value, positive }: { label: string; value: string; positive?: boolean }) { return <div className="panel p-4"><p className="eyebrow">{label}</p><p className={`mt-2 text-xl font-semibold ${positive ? "text-emerald-400" : "text-white"}`}>{value}</p></div>; }
