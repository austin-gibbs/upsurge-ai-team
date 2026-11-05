// Activity pulse strip (spec 1.2 and 2.2). Four tiles, real counts only,
// no trend arrows, no percentages, no invented comparisons. The average
// turnaround tile shows the honest empty state when there is no history.
import type { PulseStats } from '../types';
import { formatTurnaround } from '../lib/time';

interface PulseStripProps {
  pulse: PulseStats;
  /** One time highlight after a realtime driven change (spec 4.2). */
  changed: boolean;
}

export function PulseStrip({ pulse, changed }: PulseStripProps) {
  const tiles: { label: string; value: string; sublabel: string }[] = [
    {
      label: 'In flight now',
      value: String(pulse.inFlight),
      sublabel: 'across all three teams',
    },
    {
      label: 'Completed today',
      value: String(pulse.completedToday),
      sublabel: 'delivered so far today',
    },
    {
      label: 'Average turnaround',
      value:
        pulse.avgTurnaroundMs === null
          ? 'Building history'
          : formatTurnaround(pulse.avgTurnaroundMs),
      sublabel: 'over the last 7 days',
    },
    {
      label: 'Requests this week',
      value: String(pulse.requestsThisWeek),
      sublabel: 'submitted since Monday',
    },
  ];

  return (
    <section
      aria-label="Activity"
      className={`grid grid-cols-2 gap-3 rounded-2xl transition-colors duration-300 motion-reduce:transition-none lg:grid-cols-4 ${
        changed ? 'bg-slate-50' : ''
      }`}
    >
      {tiles.map((tile) => (
        <div
          key={tile.label}
          className="rounded-2xl bg-white p-4 shadow-sm ring-1 ring-slate-200"
        >
          <div className="text-3xl font-semibold text-slate-900 tabular-nums">
            {tile.value}
          </div>
          <div className="mt-1 text-sm font-medium text-slate-700">
            {tile.label}
          </div>
          <div className="text-xs text-slate-500">{tile.sublabel}</div>
        </div>
      ))}
    </section>
  );
}
