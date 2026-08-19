"use client";
import { useEffect, useState } from "react";
import type { Sport } from "@/lib/types";

export function SportSwitch({ prominent = false }: { prominent?: boolean }) {
  const [sport, setSport] = useState<Sport>("football");
  useEffect(() => {
    const value = document.cookie.split(";").map((item) => item.trim()).find((item) => item.startsWith("paracobet-sport="))?.split("=")[1];
    if (value !== "tennis") return;
    const timer = window.setTimeout(() => setSport("tennis"), 0);
    return () => window.clearTimeout(timer);
  }, []);
  // The cookie is the intentional persistence boundary for the global context.
  // eslint-disable-next-line react-hooks/immutability
  function select(value: Sport) { document.cookie = `paracobet-sport=${value}; path=/; max-age=31536000; SameSite=Lax`; window.location.reload(); }
  return <div className={`${prominent ? "mx-auto max-w-md border-cyan-500/30 bg-cyan-500/5 p-3" : "mb-7 bg-slate-950/50 p-2"} rounded-lg border border-slate-700/70`}><p className={`${prominent ? "text-center" : "px-2"} pb-2 text-[10px] font-semibold uppercase tracking-[0.16em] text-slate-500`}>Deporte activo</p><div className="grid grid-cols-2 gap-1">{(["football", "tennis"] as Sport[]).map((item) => <button key={item} type="button" onClick={() => select(item)} className={`rounded-md px-2 py-2 text-xs font-medium transition ${sport === item ? "bg-cyan-500 text-slate-950" : "text-slate-400 hover:bg-slate-800 hover:text-white"}`}>{item === "football" ? "⚽ FÚTBOL" : "🎾 TENIS"}</button>)}</div></div>;
}
