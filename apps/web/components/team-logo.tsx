import Image from "next/image";

export function TeamLogo({ name, src, size = 48 }: { name: string; src?: string | null; size?: number }) {
  const initials = name.split(" ").map((part) => part[0]).slice(0, 2).join("").toUpperCase();
  return <span className="relative mx-auto flex shrink-0 items-center justify-center overflow-hidden rounded-full border border-slate-700 bg-slate-950 text-xs font-semibold text-cyan-200" style={{ width: size, height: size }} aria-label={`Logo de ${name}`}>
    {src ? <Image src={src} alt={`Logo de ${name}`} fill sizes={`${size}px`} className="object-contain p-1" /> : initials}
  </span>;
}
