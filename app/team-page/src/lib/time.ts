// Timezone helpers built on Intl (spec section 2).
// Day and week boundaries are computed in the workspace timezone, then
// converted to UTC instants for query comparisons.

/** Offset in ms of `timeZone` at the given instant (tz local time minus UTC). */
function tzOffsetMs(timeZone: string, instant: Date): number {
  const parts = new Intl.DateTimeFormat('en-US', {
    timeZone,
    hourCycle: 'h23',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  }).formatToParts(instant);
  const get = (type: string) =>
    Number(parts.find((p) => p.type === type)?.value ?? 0);
  const asUtc = Date.UTC(
    get('year'),
    get('month') - 1,
    get('day'),
    get('hour'),
    get('minute'),
    get('second'),
  );
  return asUtc - Math.floor(instant.getTime() / 1000) * 1000;
}

/** The UTC instant of a wall clock time in `timeZone`. */
function zonedTimeToUtc(
  timeZone: string,
  year: number,
  month: number,
  day: number,
  hour = 0,
  minute = 0,
  second = 0,
): Date {
  const guess = Date.UTC(year, month - 1, day, hour, minute, second);
  const offset = tzOffsetMs(timeZone, new Date(guess));
  return new Date(guess - offset);
}

/** Year, month (1 based), day, and weekday of `instant` in `timeZone`. */
function localParts(
  timeZone: string,
  instant: Date,
): { year: number; month: number; day: number; weekday: number } {
  const parts = new Intl.DateTimeFormat('en-US', {
    timeZone,
    year: 'numeric',
    month: 'numeric',
    day: 'numeric',
    weekday: 'short',
  }).formatToParts(instant);
  const get = (type: string) =>
    parts.find((p) => p.type === type)?.value ?? '';
  const weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  return {
    year: Number(get('year')),
    month: Number(get('month')),
    day: Number(get('day')),
    weekday: weekdays.indexOf(get('weekday')),
  };
}

/** UTC instant of today 00:00 in the workspace timezone. */
export function startOfTodayUtc(timeZone: string, now = new Date()): Date {
  const p = localParts(timeZone, now);
  return zonedTimeToUtc(timeZone, p.year, p.month, p.day);
}

/** UTC instant of Monday 00:00 of this week in the workspace timezone. */
export function startOfWeekUtc(timeZone: string, now = new Date()): Date {
  const p = localParts(timeZone, now);
  const daysSinceMonday = (p.weekday + 6) % 7;
  const monday = new Date(
    zonedTimeToUtc(timeZone, p.year, p.month, p.day).getTime() -
      daysSinceMonday * 24 * 60 * 60 * 1000,
  );
  // Recompute through the timezone so DST transitions stay correct.
  const mp = localParts(timeZone, monday);
  return zonedTimeToUtc(timeZone, mp.year, mp.month, mp.day);
}

/** Spec section 2.2 display format for average turnaround. */
export function formatTurnaround(ms: number): string {
  const minutes = ms / 60000;
  if (minutes < 60) return `${Math.max(1, Math.round(minutes))}m`;
  const hours = minutes / 60;
  if (hours < 24) return `${hours.toFixed(1)} hrs`;
  return `${(hours / 24).toFixed(1)} days`;
}

/** Completion date for the wins feed, for example `Tue, Nov 4`. */
export function formatWinDate(iso: string, timeZone: string): string {
  return new Intl.DateTimeFormat('en-US', {
    timeZone,
    weekday: 'short',
    month: 'short',
    day: 'numeric',
  }).format(new Date(iso));
}

/** Relative time for board update lines, for example `2h ago`. */
export function formatRelative(iso: string, now = new Date()): string {
  const seconds = Math.max(
    0,
    Math.floor((now.getTime() - new Date(iso).getTime()) / 1000),
  );
  if (seconds < 60) return 'just now';
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  return `${days}d ago`;
}
