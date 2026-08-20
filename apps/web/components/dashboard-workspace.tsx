"use client";

import Link from "next/link";
import { useState } from "react";
import type { MarketQuote, Match, Sport } from "@/lib/types";
import { sportLabels } from "@/lib/sport-labels";
import { CompetitionGroups } from "@/components/competition-groups";

const dayKey = (date: Date) => date.toISOString().slice(0, 10);
const dateAtOffset = (offset: number) => { const date = new Date(); date.setHours(12, 0, 0, 0); date.setDate(date.getDate() + offset); return date; };
const dayLabel = (offset: number) => offset === -1 ? "Ayer" : offset === 0 ? "Hoy" : "Mañana";

export function DashboardWorkspace({ sport, matches, markets }: { sport: Sport; matches: Match[]; markets: MarketQuote[] }) {
  const [offset, setOffsetState] = useState(0);
  const [visibleMatches, setVisibleMatches] = useState(matches);
  const [, setLoading] = useState(false);
  const selectDay = async (nextOffset: number) => {
    setOffsetState(nextOffset);
    if (sport === "tennis" || !process.env.NEXT_PUBLIC_API_URL) { setVisibleMatches(matches); return; }
    setLoading(true);
    try {
      const date = dayKey(dateAtOffset(nextOffset));
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/matches?date=${date}&timezone=America%2FBogota`, { cache: "no-store" });
      setVisibleMatches(response.ok ? await response.json() : matches);
    } catch { setVisibleMatches(matches); } finally { setLoading(false); }
  };
  const setOffset = (nextOffset: number) => { void selectDay(nextOffset); };
  const dayMatches = visibleMatches.filter((match) => dayKey(new Date(match.starts_at)) === dayKey(dateAtOffset(offset)));
  const matchIds = new Set(dayMatches.map((match) => match.id));
  const opportunities = markets.filter((market) => matchIds.has(market.match_id)).map((market) => {
    const match = dayMatches.find((item) => item.id === market.match_id);
    const implied = 1 / market.odds;
    const historical = sport === "tennis" ? 0.59 : 0.61;
    return { market, match, implied, historical, advantage: historical - implied, ev: historical * market.odds - 1 };
  }).sort((a, b) => b.advantage - a.advantage).slice(0, 4);
  const date = dateAtOffset(offset);

  return <div className="space-y-9">
    <section className="overflow-hidden rounded-2xl border border-slate-800 bg-[#0a1220]"><div className="flex items-center justify-between gap-4 border-b border-slate-800 px-5 py-4"><div><p className="eyebrow">Calendario operativo</p><p className="mt-1 text-sm text-slate-300">Selecciona una jornada para actualizar las señales.</p></div><span className="hidden rounded-full border border-slate-700 px-3 py-1 text-[10px] uppercase tracking-[.16em] text-slate-500 sm:block">{sportLabels[sport]}</span></div><div className="grid grid-cols-3 divide-x divide-slate-800">{[-1, 0, 1].map((item) => { const itemDate = dateAtOffset(item); return <button key={item} onClick={() => setOffset(item)} className={`relative px-3 py-5 text-center transition sm:px-8 ${offset === item ? "bg-cyan-300 text-slate-950" : "text-slate-400 hover:bg-slate-800/70 hover:text-slate-200"}`}><span className="block text-[10px] font-semibold uppercase tracking-[.18em]">{dayLabel(item)}</span><span className="mt-2 block text-2xl font-semibold">{itemDate.getDate()}</span><span className="mt-1 block text-[10px] uppercase tracking-wider">{new Intl.DateTimeFormat("es", { month: "short" }).format(itemDate)}</span>{offset === item && <span className="absolute bottom-0 left-1/2 h-1 w-10 -translate-x-1/2 rounded-t bg-slate-950" />}</button>; })}</div></section>

    <section className="grid gap-5 xl:grid-cols-[1.45fr_.55fr]"><div><div className="mb-4 flex items-end justify-between"><div><p className="eyebrow">Agenda seleccionada</p><h2 className="mt-1 text-2xl font-semibold text-white">Eventos del {date.toLocaleDateString("es", { day: "numeric", month: "long" })}</h2></div><span className="text-xs text-slate-500">{dayMatches.length} en seguimiento</span></div><CompetitionGroups matches={dayMatches} sport={sport} /></div><aside className="rounded-2xl border border-slate-800 bg-[linear-gradient(160deg,#101c31,#0a111e)] p-5"><p className="eyebrow">Pulso del día</p><div className="mt-6 space-y-5"><Pulse value={dayMatches.length} label="Eventos activos" width="w-2/5" /><Pulse value={markets.filter((market) => matchIds.has(market.match_id)).length} label="Mercados leídos" width="w-3/4" /><Pulse value={opportunities.length} label="Valor detectado" width="w-1/2" /><div className="border-t border-slate-800 pt-4"><p className="text-xs leading-5 text-slate-500">Las señales son simuladas y sirven para explorar el flujo analítico del MVP.</p></div></div></aside></section>

    <section><div className="mb-4 flex flex-wrap items-end justify-between gap-3"><div><p className="eyebrow">Radar de valor</p><h2 className="mt-1 text-2xl font-semibold text-white">Diferencias que merecen contexto</h2><p className="mt-1 text-sm text-slate-400">Comparación entre la lectura del mercado y la señal histórica.</p></div><span className="rounded-full bg-emerald-400/10 px-3 py-1 text-xs text-emerald-300">{opportunities.length} señales</span></div>{opportunities.length ? <div className="grid gap-4 lg:grid-cols-2">{opportunities.map(({ market, match, implied, historical, advantage, ev }) => <article key={market.id} className="group overflow-hidden rounded-2xl border border-slate-800 bg-slate-900/55 transition hover:border-cyan-400/35"><div className="border-b border-slate-800 bg-slate-950/35 px-5 py-4"><div className="flex items-start justify-between gap-4"><div><p className="text-[10px] uppercase tracking-[.16em] text-slate-500">{match?.competition}</p><h3 className="mt-1 font-semibold text-slate-100">{match?.home_team} <span className="text-slate-500">vs</span> {match?.away_team}</h3><p className="mt-1 text-xs text-slate-500">{match && new Date(match.starts_at).toLocaleDateString("es", { weekday: "short", day: "numeric", month: "short" })} · {match && new Date(match.starts_at).toLocaleTimeString("es", { hour: "2-digit", minute: "2-digit" })}</p></div><span className="rounded-full border border-emerald-400/20 bg-emerald-400/10 px-2 py-1 text-[10px] font-semibold text-emerald-300">VALOR DETECTADO</span></div></div><div className="p-5"><div className="flex items-end justify-between gap-4"><div><p className="text-sm font-medium text-slate-200">{market.market}</p><p className="mt-1 text-xs text-slate-500">{market.selection}</p></div><p className="text-2xl font-semibold text-cyan-200">{market.odds.toFixed(2)}</p></div><div className="mt-5 space-y-3"><Probability label="Probabilidad implícita" value={implied} tone="bg-slate-500" /><Probability label="Probabilidad histórica" value={historical} tone="bg-cyan-300" /></div><div className="mt-5 grid grid-cols-2 border-t border-slate-800 pt-4"><div><p className="text-[10px] uppercase tracking-[.15em] text-slate-500">Ventaja estimada</p><p className="mt-1 text-xl font-semibold text-emerald-300">+{(advantage * 100).toFixed(1)} pp</p></div><div><p className="text-[10px] uppercase tracking-[.15em] text-slate-500">EV estimado</p><p className="mt-1 text-xl font-semibold text-emerald-300">+{(ev * 100).toFixed(1)}%</p></div></div><Link href={`/matches/${market.match_id}`} className="mt-5 inline-flex text-sm font-medium text-cyan-300 hover:text-cyan-100">Abrir inteligencia del evento →</Link></div></article>)}</div> : <div className="rounded-2xl border border-dashed border-slate-700 p-8 text-sm text-slate-500">No hay señales disponibles para este día.</div>}</section>
  </div>;
}

function Pulse({ value, label, width }: { value: number; label: string; width: string }) { return <div><div className="flex items-end justify-between"><span className="text-sm text-slate-400">{label}</span><strong className="text-2xl font-semibold text-white">{value}</strong></div><div className="mt-2 h-1.5 overflow-hidden rounded-full bg-slate-800"><span className={`block h-full ${width} rounded-full bg-cyan-300`} /></div></div>; }
function Probability({ label, value, tone }: { label: string; value: number; tone: string }) { return <div><div className="mb-1 flex justify-between text-[11px]"><span className="text-slate-500">{label}</span><span className="font-medium text-slate-300">{(value * 100).toFixed(1)}%</span></div><div className="h-2 overflow-hidden rounded-full bg-slate-800"><span className={`block h-full rounded-full ${tone}`} style={{ width: `${Math.min(value * 100, 100)}%` }} /></div></div>; }
