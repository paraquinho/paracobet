export function StatCard({ label, value, detail }: { label: string; value: string; detail: string }) {
  return <article className="panel p-5"><p className="eyebrow">{label}</p><p className="metric mt-3">{value}</p><p className="mt-2 text-xs text-slate-500">{detail}</p></article>;
}
