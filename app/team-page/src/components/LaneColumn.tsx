// Lane column (spec 1.3 and 4.4): header with tagline and open count
// chip, leader card pinned on top, member cards below in roster order.
import type { LaneView } from '../types';
import { LANE_META } from '../lib/lanes';
import { MemberCard } from './MemberCard';

interface LaneColumnProps {
  lane: LaneView;
  highlightMemberIds: ReadonlySet<string>;
  /**
   * At tablet widths the wrapped third lane spans full width and its
   * member cards lay out in two columns (spec 4.4).
   */
  wideMembers?: boolean;
}

export function LaneColumn({
  lane,
  highlightMemberIds,
  wideMembers = false,
}: LaneColumnProps) {
  const meta = LANE_META[lane.lane];

  return (
    <section aria-label={meta.teamName} className="flex min-w-0 flex-col gap-3">
      <div className="flex items-center justify-between gap-2">
        <div className="min-w-0">
          <h2 className="truncate text-lg font-semibold text-slate-900">
            {meta.teamName}
          </h2>
          <p className="truncate text-sm text-slate-500">{meta.tagline}</p>
        </div>
        <span
          className={`shrink-0 rounded-full px-2.5 py-1 text-xs font-medium ${meta.chipClass}`}
        >
          {lane.openCount} open
        </span>
      </div>

      {lane.leader && (
        <MemberCard
          member={lane.leader}
          isLeader
          laneOpenCount={lane.openCount}
          highlighted={highlightMemberIds.has(lane.leader.roster.id)}
        />
      )}

      <div
        className={`grid gap-3 ${wideMembers ? 'md:grid-cols-2 xl:grid-cols-1' : ''}`}
      >
        {lane.members.map((member) => (
          <MemberCard
            key={member.roster.id}
            member={member}
            highlighted={highlightMemberIds.has(member.roster.id)}
          />
        ))}
      </div>
    </section>
  );
}
