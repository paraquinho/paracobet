import { ParlayHistory } from "@/components/parlay-history";
import { Shell } from "@/components/shell";
import { parlayHistoryMock } from "@/lib/parlay-history-mock";

export default function HistoryPage() { return <Shell><ParlayHistory entries={parlayHistoryMock} /></Shell>; }
