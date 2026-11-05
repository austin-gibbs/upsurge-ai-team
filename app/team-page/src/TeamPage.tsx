// TeamPage: the AI Team Heartbeat Page (route /team, behind the Desk
// passcode gate, nav link "Your Team").
//
// Sections render in spec order (section 1): masthead, pulse strip, the
// three lanes, recent wins, board summary, footer. Every number and
// status on this page derives from real Desk rows; see useTeamData.
import type { SupabaseClient } from '@supabase/supabase-js';
import { useTeamData } from './hooks/useTeamData';
import { Masthead } from './components/Masthead';
import { PulseStrip } from './components/PulseStrip';
import { LaneColumn } from './components/LaneColumn';
import { WinsFeed } from './components/WinsFeed';
import { BoardSummary } from './components/BoardSummary';

interface TeamPageProps {
  /** The Desk app passes its existing Supabase client. */
  supabase: SupabaseClient;
  /** Route of the existing Desk board view. Defaults to the board root. */
  boardHref?: string;
}

function LoadingSkeleton() {
  // Skeleton blocks matching the final layout shapes, shown only during
  // the initial fetch (spec 4.3). No shimmer loop.
  return (
    <div className="mx-auto flex w-full max-w-7xl flex-col gap-6 p-4 sm:p-6">
      <div className="h-16 rounded-2xl bg-slate-100" />
      <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
        {[0, 1, 2, 3].map((i) => (
          <div key={i} className="h-24 rounded-2xl bg-slate-100" />
        ))}
      </div>
      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
        {[0, 1, 2].map((i) => (
          <div key={i} className="flex flex-col gap-3">
            <div className="h-10 rounded-xl bg-slate-100" />
            <div className="h-32 rounded-2xl bg-slate-100" />
            <div className="h-28 rounded-2xl bg-slate-100" />
            <div className="h-28 rounded-2xl bg-slate-100" />
          </div>
        ))}
      </div>
    </div>
  );
}

export function TeamPage({ supabase, boardHref = '/' }: TeamPageProps) {
  const { data, loading, connection, lastUpdatedAt, highlightMemberIds, pulseChanged } =
    useTeamData(supabase);

  if (loading || !data) return <LoadingSkeleton />;

  const { config, pulse, lanes, wins, board } = data;
  const updatedLabel = lastUpdatedAt
    ? new Intl.DateTimeFormat('en-US', {
        timeZone: config.timezone,
        hour: 'numeric',
        minute: '2-digit',
      }).format(lastUpdatedAt)
    : null;

  return (
    <div className="mx-auto flex w-full max-w-7xl flex-col gap-6 p-4 sm:p-6">
      <Masthead config={config} connection={connection} />

      <PulseStrip pulse={pulse} changed={pulseChanged} />

      <div className="grid items-start gap-6 md:grid-cols-2 xl:grid-cols-3">
        {lanes.map((lane, index) => (
          <div
            key={lane.lane}
            className={index === 2 ? 'md:col-span-2 xl:col-span-1' : undefined}
          >
            <LaneColumn
              lane={lane}
              highlightMemberIds={highlightMemberIds}
              wideMembers={index === 2}
            />
          </div>
        ))}
      </div>

      <WinsFeed wins={wins} timezone={config.timezone} />

      <BoardSummary board={board} boardHref={boardHref} />

      <footer className="flex flex-wrap items-center justify-between gap-2 border-t border-slate-200 pt-4 text-xs text-slate-400">
        <span>Your AI Team by UpSurge</span>
        {updatedLabel && <span>Updated {updatedLabel}</span>}
      </footer>
    </div>
  );
}

export default TeamPage;
