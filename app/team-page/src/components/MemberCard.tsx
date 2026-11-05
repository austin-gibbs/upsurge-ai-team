// Member card (spec 1.3). Status is computed upstream from real request
// rows; this component only renders it. Initials avatar tinted by lane,
// no photos: the team is AI and the page is intentional about that.
import type { MemberView } from '../types';
import { LANE_META } from '../lib/lanes';

interface MemberCardProps {
  member: MemberView;
  /** Leader cards render larger, pinned at the top of the lane column. */
  isLeader?: boolean;
  /** Lane wide open count, shown on the leader card only. */
  laneOpenCount?: number;
  /** One time highlight after a realtime driven status change. */
  highlighted?: boolean;
}

function initials(name: string): string {
  return name
    .split(/\s+/)
    .map((part) => part[0])
    .filter(Boolean)
    .slice(0, 2)
    .join('')
    .toUpperCase();
}

const STATUS_LABEL = {
  working: 'Working now',
  queued: 'Queued',
  available: 'Available',
} as const;

export function MemberCard({
  member,
  isLeader = false,
  laneOpenCount,
  highlighted = false,
}: MemberCardProps) {
  const meta = LANE_META[member.roster.lane];
  const { roster, status } = member;

  const pillClass =
    status === 'working'
      ? meta.pillClass
      : status === 'queued'
        ? 'bg-white text-slate-600 ring-1 ring-slate-300'
        : 'bg-slate-100 text-slate-400';

  return (
    <article
      className={`rounded-2xl bg-white shadow-sm ring-1 ring-slate-200 transition-shadow duration-300 motion-reduce:transition-none ${
        status === 'working' ? meta.ringClass : ''
      } ${highlighted ? meta.highlightClass : ''} ${isLeader ? 'p-5' : 'p-4'}`}
    >
      <div className="flex items-start gap-3">
        <span
          aria-hidden
          className={`flex shrink-0 items-center justify-center rounded-full font-semibold ${meta.avatarClass} ${
            isLeader ? 'h-12 w-12 text-base' : 'h-10 w-10 text-sm'
          }`}
        >
          {initials(roster.display_name)}
        </span>
        <div className="min-w-0 flex-1">
          <div className="flex items-start justify-between gap-2">
            <div className="min-w-0">
              <h3
                className={`truncate font-semibold text-slate-900 ${
                  isLeader ? 'text-lg' : 'text-base'
                }`}
              >
                {roster.display_name}
              </h3>
              <p className="truncate text-sm text-slate-500">
                {roster.role}
                {isLeader ? ' · Team lead' : ''}
              </p>
            </div>
            <span
              className={`shrink-0 rounded-full px-2.5 py-1 text-xs font-medium transition-colors duration-300 motion-reduce:transition-none ${pillClass}`}
            >
              {STATUS_LABEL[status]}
            </span>
          </div>

          {roster.strengths.length > 0 && (
            <ul className="mt-2 flex flex-wrap gap-1.5">
              {roster.strengths.slice(0, 3).map((strength) => (
                <li
                  key={strength}
                  className="rounded-full bg-slate-100 px-2 py-0.5 text-xs text-slate-600"
                >
                  {strength}
                </li>
              ))}
            </ul>
          )}

          {isLeader && typeof laneOpenCount === 'number' && (
            <p className="mt-2 text-sm text-slate-600">
              {laneOpenCount} projects open in this team
            </p>
          )}

          {status === 'working' && member.currentWorkTitle && (
            <p className="mt-2 truncate text-sm text-slate-700">
              <span className="text-slate-400">Now: </span>
              {member.currentWorkTitle}
              {member.moreCount > 0 ? ` +${member.moreCount} more` : ''}
            </p>
          )}
        </div>
      </div>
    </article>
  );
}
