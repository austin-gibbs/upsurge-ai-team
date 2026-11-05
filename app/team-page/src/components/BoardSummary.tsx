// Board summary (spec 1.5 and 2.5): status counts with client facing
// labels, then the open project list ordered by priority and recency,
// each row carrying the latest client visible update when one exists.
import type { BoardData } from '../types';
import { CLIENT_STATUS_LABELS } from '../lib/statusLabels';
import { LANE_META } from '../lib/lanes';
import { formatRelative } from '../lib/time';

interface BoardSummaryProps {
  board: BoardData;
  /** Route of the existing Desk board view. */
  boardHref: string;
}

export function BoardSummary({ board, boardHref }: BoardSummaryProps) {
  return (
    <section aria-label="Board summary" className="w-full">
      <h2 className="text-lg font-semibold text-slate-900">
        Your board right now
      </h2>

      <ul className="mt-3 flex flex-wrap gap-2">
        {board.counts.map((entry) => (
          <li
            key={entry.status}
            className="rounded-full bg-white px-3 py-1.5 text-sm text-slate-600 ring-1 ring-slate-200"
          >
            {entry.label}{' '}
            <span className="font-semibold text-slate-900 tabular-nums">
              {entry.count}
            </span>
          </li>
        ))}
      </ul>

      <div className="mt-3 flex flex-col gap-2">
        {board.openProjects.length === 0 ? (
          <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-5 text-center">
            <p className="text-sm text-slate-500">
              Nothing open right now. Submit a request and it will appear here.
            </p>
          </div>
        ) : (
          board.openProjects.map(({ request, specialistName, latestClientUpdate }) => (
            <article
              key={request.id}
              className="rounded-2xl bg-white p-4 shadow-sm ring-1 ring-slate-200"
            >
              <div className="flex items-start justify-between gap-3">
                <h3 className="min-w-0 font-medium text-slate-900">
                  {request.title}
                </h3>
                <span className="shrink-0 rounded-full bg-slate-100 px-2.5 py-1 text-xs font-medium text-slate-600">
                  {CLIENT_STATUS_LABELS[request.status]}
                </span>
              </div>
              <p className="mt-1 text-xs text-slate-500">
                {request.lane ? LANE_META[request.lane].teamName : 'Your team'}
                {specialistName ? ` · ${specialistName}` : ''}
              </p>
              {latestClientUpdate && (
                <p className="mt-2 text-sm text-slate-600">
                  {latestClientUpdate.summary}{' '}
                  <span className="whitespace-nowrap text-xs text-slate-400">
                    {formatRelative(latestClientUpdate.createdAt)}
                  </span>
                </p>
              )}
            </article>
          ))
        )}
      </div>

      <a
        href={boardHref}
        className="mt-4 inline-block text-sm font-medium text-slate-700 underline decoration-slate-300 underline-offset-4 hover:text-slate-900"
      >
        Open the full board
      </a>
    </section>
  );
}
