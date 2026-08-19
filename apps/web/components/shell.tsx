"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
const groups = [
  { label: "Resumen", items: [["Resumen", "/dashboard"]] },
  { label: "Análisis de partidos", items: [["Partidos", "/matches"], ["En vivo", "#"], ["Equipos", "#"], ["Competiciones", "#"]] },
  { label: "Mercados", items: [["Mercados", "/markets"], ["Cuotas", "#"], ["Tendencias", "#"]] },
  { label: "Combinadas", items: [["Analizador de combinadas", "/parlay"], ["Constructor de combinadas", "/parlay/builder"], ["Combinadas guardadas", "#"]] },
  { label: "Analítica", items: [["Análisis histórico", "/matches"], ["Backtesting", "#"]] },
  { label: "Datos", items: [["Proveedores de datos", "#"], ["Calidad de datos", "#"]] },
  { label: "Sistema", items: [["Configuración", "#"]] },
];
export function Shell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  return <div className="min-h-screen lg:grid lg:grid-cols-[238px_1fr]"><aside className="border-b border-slate-800 bg-[#091522] px-5 py-6 lg:border-b-0 lg:border-r"><Link href="/dashboard" className="mb-8 block text-xl font-bold tracking-tight text-white">PARACO<span className="text-cyan-400">BET</span></Link><nav className="max-h-[calc(100vh-170px)] space-y-5 overflow-y-auto pr-1">{groups.map((group) => <div key={group.label}><p className="mb-2 text-[10px] font-semibold uppercase tracking-[0.18em] text-slate-500">{group.label}</p>{group.items.map(([label, href]) => href === "#" ? <span key={label} className="mb-1 flex items-center justify-between rounded-md px-3 py-2 text-sm text-slate-600" title="Disponible próximamente">{label}<span className="text-[9px] uppercase tracking-wider">Próximamente</span></span> : <Link key={label} href={href} className={`mb-1 block rounded-md border px-3 py-2 text-sm transition ${pathname === href || (href !== "/dashboard" && pathname.startsWith(`${href}/`)) ? "border-cyan-500/30 bg-cyan-500/10 text-cyan-200" : "border-transparent text-slate-300 hover:border-slate-700 hover:bg-slate-800/70 hover:text-white"}`}>{label}</Link>)}</div>)}</nav><div className="mt-10 border-t border-slate-800 pt-4 text-xs text-slate-500"><span className="mr-2 inline-block h-2 w-2 rounded-full bg-amber-400" />Datos sintéticos · Mock</div></aside><main className="p-5 sm:p-8">{children}</main></div>;
}
