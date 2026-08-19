"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import type { Match } from "@/lib/types";

export function MatchExplorer({ matches }: { matches: Match[] }) {
  const [team, setTeam] = useState("");
  const [competition, setCompetition] = useState("");
  const [status, setStatus] = useState("");
  const [date, setDate] = useState("");
  const filtered = useMemo(() => matches.filter(match => {
    const haystack = `${match.home_team} ${match.away_team}`.toLowerCase();
    return (!team || haystack.includes(team.toLowerCase())) &&
      (!competition || match.competition === competition) &&
      (!status || match.status === status) &&
      (!date || match.starts_at.slice(0, 10) === date);
  }), [matches, team, competition, status, date]);
  const competitions = [...new Set(matches.map(match => match.competition))];
  return <>
    <div className="panel grid gap-3 p-4 sm:grid-cols-2 xl:grid-cols-4">
      <input aria-label="Buscar equipo" value={team} onChange={event => setTeam(event.target.value)} placeholder="Equipo" className="rounded border border-slate-700 bg-slate-950 px-3 py-2 text-sm" />
      <select aria-label="Competición" value={competition} onChange={event => setCompetition(event.target.value)} className="rounded border border-slate-700 bg-slate-950 px-3 py-2 text-sm"><option value="">Todas las competiciones</option>{competitions.map(item => <option key={item}>{item}</option>)}</select>
      <select aria-label="Estado" value={status} onChange={event => setStatus(event.target.value)} className="rounded border border-slate-700 bg-slate-950 px-3 py-2 text-sm"><option value="">Todos los estados</option><option value="scheduled">Programados</option><option value="finished">Finalizados</option></select>
      <input aria-label="Fecha" type="date" value={date} onChange={event => setDate(event.target.value)} className="rounded border border-slate-700 bg-slate-950 px-3 py-2 text-sm" />
    </div>
    <p className="my-4 text-xs text-slate-500">{filtered.length} partido{filtered.length === 1 ? "" : "s"} · fuente API mock</p>
    {filtered.length === 0 ? <div className="panel p-8 text-center text-sm text-slate-400">No hay partidos para estos filtros.</div> : <div className="panel overflow-hidden"><div className="overflow-x-auto"><table className="w-full min-w-[760px] text-left text-sm"><thead className="border-b border-slate-800 bg-slate-950/50 text-[10px] uppercase tracking-[0.16em] text-slate-500"><tr><th className="px-5 py-3">Inicio</th><th className="px-5 py-3">Competición</th><th className="px-5 py-3">Partido</th><th className="px-5 py-3">Local / visitante</th><th className="px-5 py-3">Estado</th><th className="px-5 py-3">Análisis</th></tr></thead><tbody>{filtered.map(match => <tr key={match.id} className="border-b border-slate-800/70 last:border-0 hover:bg-slate-800/30"><td className="px-5 py-4 text-slate-400">{new Intl.DateTimeFormat("es", { dateStyle: "short", timeStyle: "short" }).format(new Date(match.starts_at))}</td><td className="px-5 py-4 text-slate-400">{match.competition}</td><td className="px-5 py-4 font-medium text-slate-100"><Link className="hover:text-cyan-300" href={`/matches/${match.id}`}>{match.home_team} <span className="text-slate-500">vs</span> {match.away_team}</Link></td><td className="px-5 py-4 text-xs text-slate-500"><span className="text-slate-300">H</span> {match.home_team} · <span className="text-slate-300">A</span> {match.away_team}</td><td className="px-5 py-4"><span className={`rounded-full border px-2 py-1 text-[11px] ${match.status === "scheduled" ? "border-cyan-500/30 bg-cyan-500/10 text-cyan-200" : "border-slate-700 bg-slate-800 text-slate-300"}`}>{match.score ?? match.status}</span></td><td className="px-5 py-4"><Link href={`/matches/${match.id}`} className="text-xs font-medium text-cyan-400 hover:text-cyan-200">Abrir →</Link></td></tr>)}</tbody></table></div></div>}
  </>;
}
