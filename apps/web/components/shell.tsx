import Link from "next/link";

const nav = [
  ["Dashboard", "/dashboard"], ["Partidos", "/matches"], ["Mercados", "/markets"],
  ["Parlay Analyzer", "/parlay"], ["Builder", "/parlay/builder"],
];
const upcoming = ["Backtesting", "Models", "Data", "Settings"];

export function Shell({ children }: { children: React.ReactNode }) {
  return <div className="min-h-screen lg:grid lg:grid-cols-[238px_1fr]">
    <aside className="border-b border-slate-800 bg-[#091522] px-5 py-6 lg:border-b-0 lg:border-r">
      <Link href="/dashboard" className="mb-8 block text-xl font-bold tracking-tight text-white">PARACO<span className="text-cyan-400">BET</span></Link>
      <p className="mb-3 text-[10px] font-semibold uppercase tracking-[0.18em] text-slate-500">Analysis workspace</p>
      <nav className="flex gap-2 overflow-x-auto lg:block">{nav.map(([label, href]) => <Link key={href} href={href} className="mb-1 block whitespace-nowrap rounded-md px-3 py-2 text-sm text-slate-300 hover:bg-slate-800 hover:text-white">{label}</Link>)}</nav>
      <p className="mb-3 mt-8 text-[10px] font-semibold uppercase tracking-[0.18em] text-slate-500">Próximamente</p>
      {upcoming.map(item => <span key={item} className="mb-1 block px-3 py-2 text-sm text-slate-600">{item}</span>)}
      <div className="mt-10 border-t border-slate-800 pt-4 text-xs text-slate-500"><span className="mr-2 inline-block h-2 w-2 rounded-full bg-amber-400" />Datos sintéticos · Mock</div>
    </aside>
    <main className="p-5 sm:p-8">{children}</main>
  </div>;
}
