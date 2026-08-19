export function StatCard({ label, value, detail }: { label: string; value: string; detail: string }) {
  return <article className="panel group p-5 transition hover:-translate-y-0.5 hover:border-cyan-400/30"><div className="flex items-center justify-between"><p className="eyebrow">{label}</p><span className="h-2 w-2 rounded-full bg-cyan-400/80 shadow-[0_0_12px_rgba(88,184,255,.45)]" /></div><p className="metric mt-3">{value}</p><p className="mt-2 text-xs text-slate-500">{detail}</p></article>;
}
