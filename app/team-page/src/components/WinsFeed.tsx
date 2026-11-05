// Recent wins feed (spec 1.4 and 2.4). Only completed projects that
// carry a client summary appear; a project without one is not a win yet.
// On a brand new install the feed shows one designed placeholder card.
import type { WinItem } from '../types';
import { LANE_META } from '../lib/lanes';
import { formatWinDate } from '../lib/time';

interface WinsFeedProps {
  wins: WinItem[];
  timezone: string;
}

export function WinsFeed({ wins, timezone }: WinsFeedProps) {
  return (
    <section aria-label="Recent wins" className="w-full">
      <h2 className="text-lg font-semibold text-slate-900">Recent wins</h2>
      <div className="mt-3 flex flex-col gap-3">
        {wins.length === 0 ? (
          <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-5 text-center">
            <p className="text-sm text-slate-500">
              Your first wins will appear here as projects complete.
            </p>
          </div>
        ) : (
          wins.map((win) => (
            <article
              key={win.id}
              className="rounded-2xl bg-white p-4 shadow-sm ring-1 ring-slate-200"
            >
              <div className="flex items-start justify-between gap-3">
                <h3 className="min-w-0 font-medium text-slate-900">
                  {win.title}
                </h3>
                <time className="shrink-0 text-sm text-slate-500">
                  {formatWinDate(win.completedAt, timezone)}
                </time>
              </div>
              <p className="mt-1 text-sm text-slate-600">{win.clientSummary}</p>
              <div className="mt-2 flex items-center gap-2 text-xs text-slate-500">
                {win.lane && (
                  <span
                    className={`rounded-full px-2 py-0.5 font-medium ${LANE_META[win.lane].chipClass}`}
                  >
                    {LANE_META[win.lane].teamName}
                  </span>
                )}
                {win.specialistName && <span>{win.specialistName}</span>}
              </div>
            </article>
          ))
        )}
      </div>
    </section>
  );
}
