"use client";

import { useEffect, useState } from "react";

type History = { average?: number; median?: number; minimum?: number; maximum?: number; standard_deviation?: number; over_frequency?: number; under_frequency?: number; distribution?: number[]; window: number; venue: string };
const api = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export function HistoryPanel({ matchId, initial }: { matchId: string; initial: Record<string, number[]> }) {
  const [window, setWindow] = useState(5);
  const [venue, setVenue] = useState("all");
  const [history, setHistory] = useState<History | null>(null);
  const [error, setError] = useState("");
  useEffect(() => { let active = true; fetch(`${api}/api/v1/matches/${matchId}/history?window=${window}&venue=${venue}&line=2.5`).then(response => { if (!response.ok) throw new Error(); return response.json(); }).then(data => { if (active) { setHistory(data); setError(""); } }).catch(() => { if (active) setError("No se pudo cargar el histórico."); }); return () => { active = false; }; }, [matchId, window, venue]);
  const fallback = venue === "home" ? initial.home : venue === "away" ? initial.away : [...initial.home, ...initial.away];
  const values = history?.distribution ?? fallback.slice(-window);
  return <div className="panel p-5"><div className="flex flex-wrap items-center justify-between gap-3"><h2 className="text-lg font-medium text-white">Histórico de goles</h2><div className="flex gap-2">{[5, 10, 15, 20].map(item => <button key={item} onClick={() => setWindow(item)} className={`rounded px-2 py-1 text-xs ${window === item ? "bg-cyan-500 text-slate-950" : "bg-slate-800 text-slate-300"}`}>Últimos {item}</button>)}<select aria-label="Filtro de localía" value={venue} onChange={event => setVenue(event.target.value)} className="rounded bg-slate-800 px-2 py-1 text-xs"><option value="all">Todos</option><option value="home">Local</option><option value="away">Visitante</option></select></div></div>{error && <p className="mt-4 text-sm text-amber-300">{error} Mostrando datos disponibles.</p>}<div className="mt-5 grid grid-cols-2 gap-3 sm:grid-cols-4"><Metric label="Promedio" value={history?.average ?? values.reduce((sum, value) => sum + value, 0) / Math.max(values.length, 1)} /><Metric label="Mediana" value={history?.median ?? values[Math.floor(values.length / 2)] ?? 0} /><Metric label="Mínimo" value={history?.minimum ?? Math.min(...values)} /><Metric label="Máximo" value={history?.maximum ?? Math.max(...values)} /></div><div className="mt-5 flex flex-wrap gap-2 text-xs text-slate-400"><span>Desv. estándar: {(history?.standard_deviation ?? 0).toFixed(2)}</span><span>Más de 2.5: {((history?.over_frequency ?? 0) * 100).toFixed(1)}%</span><span>Menos de 2.5: {((history?.under_frequency ?? 0) * 100).toFixed(1)}%</span></div></div>;
}
function Metric({ label, value }: { label: string; value: number }) { return <div className="rounded border border-slate-800 bg-slate-950/50 p-3"><p className="text-xs text-slate-500">{label}</p><p className="mt-1 text-lg font-semibold text-white">{value.toFixed(2)}</p></div>; }
