// useTeamData: data layer and realtime behavior for the heartbeat page.
//
// Spec sections 2 and 4.1:
// - On load, fetch all data groups (config, visible requests, roster,
//   wins, latest client updates), then derive pulse stats, member and
//   lane status, and the board summary on the client. Status is always
//   computed from real request rows, never stored.
// - One realtime channel on requests (all events), request_updates
//   (insert only), and team_roster (all events). Any event debounces
//   300 ms, then refetches. V1 refetches rather than patching state.
// - Channel state drives the connection indicator. When the channel is
//   not subscribed, polling fallback runs at 60 second intervals and
//   stops when the channel resubscribes.
//
// The Supabase client is injected by the host app (the Desk already has
// one), so this package never creates a second client or reads config.
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import type { RealtimeChannel, SupabaseClient } from '@supabase/supabase-js';
import type {
  BoardData,
  ClientUpdateRow,
  ConnectionState,
  DeskStatus,
  Lane,
  LaneView,
  MemberStatus,
  MemberView,
  PulseStats,
  RequestRow,
  RosterRow,
  TeamData,
  TeamDataResult,
  WinItem,
  WorkspaceConfig,
} from '../types';
import { LANE_ORDER } from '../lib/lanes';
import { CLIENT_STATUS_LABELS, STATUS_DISPLAY_ORDER } from '../lib/statusLabels';
import { startOfTodayUtc, startOfWeekUtc } from '../lib/time';

const REQUEST_COLUMNS =
  'id, title, status, priority, lane, specialist_id, requested_at, updated_at, completed_at, client_visible, client_summary';
const ROSTER_COLUMNS =
  'id, slug, lane, display_name, role, strengths, is_leader, sort_order, is_active';
// Client updates are read through client_summary only, on rows the team
// deliberately marked visible to the client. The internal text column of
// request_updates is never selected anywhere in this package.
const UPDATE_COLUMNS = 'request_id, client_summary, created_at';

const QUEUED_STATUSES: DeskStatus[] = [
  'New',
  'Waiting on Austin',
  'Waiting on Client',
  'Blocked',
];

const PRIORITY_RANK: Record<string, number> = { P0: 0, P1: 1, P2: 2, P3: 3 };

interface RawGroups {
  config: WorkspaceConfig;
  roster: RosterRow[];
  requests: RequestRow[];
  wins: WinItem[];
  latestUpdates: Map<string, { summary: string; createdAt: string }>;
}

function derive(
  raw: RawGroups,
): { data: TeamData; statusByMember: Map<string, MemberStatus> } {
  const { config, roster, requests, wins, latestUpdates } = raw;
  const tz = config.timezone;
  const now = new Date();
  const todayStart = startOfTodayUtc(tz, now).getTime();
  const weekStart = startOfWeekUtc(tz, now).getTime();
  const sevenDaysAgo = now.getTime() - 7 * 24 * 60 * 60 * 1000;

  // Pulse strip (spec 2.2). `requests` already holds client_visible rows only.
  const turnarounds: number[] = [];
  let inFlight = 0;
  let completedToday = 0;
  let requestsThisWeek = 0;
  for (const r of requests) {
    if (r.status === 'In Progress') inFlight += 1;
    if (r.requested_at && new Date(r.requested_at).getTime() >= weekStart) {
      requestsThisWeek += 1;
    }
    if (r.status === 'Done' && r.completed_at) {
      const completed = new Date(r.completed_at).getTime();
      if (completed >= todayStart) completedToday += 1;
      if (completed >= sevenDaysAgo) {
        turnarounds.push(
          completed - new Date(r.requested_at).getTime(),
        );
      }
    }
  }
  const pulse: PulseStats = {
    inFlight,
    completedToday,
    avgTurnaroundMs: turnarounds.length
      ? turnarounds.reduce((a, b) => a + b, 0) / turnarounds.length
      : null,
    requestsThisWeek,
  };

  // Member and lane status derivation (spec 2.3), computed per roster row,
  // so a specialist in two lanes lights up only in the active project's lane.
  const statusByMember = new Map<string, MemberStatus>();
  const lanes: LaneView[] = LANE_ORDER.map((lane) => {
    const laneRequests = requests.filter((r) => r.lane === lane);
    const openCount = laneRequests.filter((r) => r.status !== 'Done').length;

    const toMemberView = (member: RosterRow): MemberView => {
      const mine = laneRequests.filter((r) => r.specialist_id === member.id);
      const inProgress = mine
        .filter((r) => r.status === 'In Progress')
        .sort((a, b) => b.updated_at.localeCompare(a.updated_at));
      const hasQueued = mine.some((r) => QUEUED_STATUSES.includes(r.status));
      const status: MemberStatus = inProgress.length
        ? 'working'
        : hasQueued
          ? 'queued'
          : 'available';
      statusByMember.set(member.id, status);
      return {
        roster: member,
        status,
        currentWorkTitle: inProgress.length ? inProgress[0].title : null,
        moreCount: inProgress.length ? inProgress.length - 1 : 0,
      };
    };

    const laneRoster = roster
      .filter((m) => m.lane === lane)
      .sort((a, b) => a.sort_order - b.sort_order);
    const leaderRow = laneRoster.find((m) => m.is_leader) ?? null;
    return {
      lane,
      leader: leaderRow ? toMemberView(leaderRow) : null,
      members: laneRoster.filter((m) => !m.is_leader).map(toMemberView),
      openCount,
    } satisfies LaneView;
  });

  // Board summary (spec 2.5).
  const counts = STATUS_DISPLAY_ORDER.map((status) => ({
    status,
    label: CLIENT_STATUS_LABELS[status],
    count: requests.filter((r) => r.status === status).length,
  }));
  const nameById = new Map(roster.map((m) => [m.id, m.display_name]));
  const openProjects = requests
    .filter((r) => r.status !== 'Done')
    .sort((a, b) => {
      const pa = PRIORITY_RANK[a.priority ?? 'P3'] ?? 3;
      const pb = PRIORITY_RANK[b.priority ?? 'P3'] ?? 3;
      if (pa !== pb) return pa - pb;
      return b.updated_at.localeCompare(a.updated_at);
    })
    .map((request) => ({
      request,
      specialistName: request.specialist_id
        ? (nameById.get(request.specialist_id) ?? null)
        : null,
      latestClientUpdate: latestUpdates.get(request.id) ?? null,
    }));
  const board: BoardData = { counts, openProjects };

  return { data: { config, pulse, lanes, wins, board }, statusByMember };
}

export function useTeamData(supabase: SupabaseClient): TeamDataResult {
  const [data, setData] = useState<TeamData | null>(null);
  const [loading, setLoading] = useState(true);
  const [connection, setConnection] = useState<ConnectionState>('reconnecting');
  const [lastUpdatedAt, setLastUpdatedAt] = useState<Date | null>(null);
  const [highlightMemberIds, setHighlightMemberIds] = useState<
    ReadonlySet<string>
  >(new Set());
  const [pulseChanged, setPulseChanged] = useState(false);

  const statusRef = useRef<Map<string, MemberStatus>>(new Map());
  const pulseRef = useRef<PulseStats | null>(null);
  const highlightTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  const fetchAll = useCallback(async () => {
    const [configRes, rosterRes, requestsRes, winsRes, updatesRes] =
      await Promise.all([
        supabase
          .from('workspace_config')
          .select('client_name, timezone, brand_color, logo_url')
          .eq('id', 1)
          .maybeSingle(),
        supabase
          .from('team_roster')
          .select(ROSTER_COLUMNS)
          .eq('is_active', true)
          .order('sort_order', { ascending: true }),
        supabase
          .from('requests')
          .select(REQUEST_COLUMNS)
          .eq('client_visible', true),
        supabase
          .from('requests')
          .select(REQUEST_COLUMNS)
          .eq('client_visible', true)
          .eq('status', 'Done')
          .not('client_summary', 'is', null)
          .not('completed_at', 'is', null)
          .order('completed_at', { ascending: false })
          .limit(8),
        supabase
          .from('request_updates')
          .select(UPDATE_COLUMNS)
          .eq('visibility', 'client')
          .order('created_at', { ascending: false })
          .limit(500),
      ]);

    if (configRes.error || !configRes.data) {
      // Without config the page cannot render honestly; stay in loading
      // and let the next poll or realtime resubscribe retry.
      return;
    }

    const roster = (rosterRes.data ?? []) as RosterRow[];
    const requests = (requestsRes.data ?? []) as RequestRow[];
    const nameById = new Map(roster.map((m) => [m.id, m.display_name]));
    const wins: WinItem[] = ((winsRes.data ?? []) as RequestRow[]).map(
      (r) => ({
        id: r.id,
        title: r.title,
        clientSummary: r.client_summary as string,
        completedAt: r.completed_at as string,
        lane: r.lane,
        specialistName: r.specialist_id
          ? (nameById.get(r.specialist_id) ?? null)
          : null,
      }),
    );
    const latestUpdates = new Map<
      string,
      { summary: string; createdAt: string }
    >();
    for (const u of (updatesRes.data ?? []) as ClientUpdateRow[]) {
      if (!latestUpdates.has(u.request_id)) {
        latestUpdates.set(u.request_id, {
          summary: u.client_summary,
          createdAt: u.created_at,
        });
      }
    }

    const { data: next, statusByMember } = derive({
      config: configRes.data as WorkspaceConfig,
      roster,
      requests,
      wins,
      latestUpdates,
    });

    // One time highlights: members whose status changed, and the pulse
    // strip when any value moved (spec 4.2). Never a loop.
    const changed = new Set<string>();
    for (const [id, status] of statusByMember) {
      if (statusRef.current.get(id) !== status) changed.add(id);
    }
    statusRef.current = statusByMember;
    const prevPulse = pulseRef.current;
    const pulseMoved =
      prevPulse !== null &&
      (prevPulse.inFlight !== next.pulse.inFlight ||
        prevPulse.completedToday !== next.pulse.completedToday ||
        prevPulse.requestsThisWeek !== next.pulse.requestsThisWeek ||
        prevPulse.avgTurnaroundMs !== next.pulse.avgTurnaroundMs);
    pulseRef.current = next.pulse;

    setData(next);
    setLoading(false);
    setLastUpdatedAt(new Date());
    if (changed.size || pulseMoved) {
      setHighlightMemberIds(changed);
      setPulseChanged(pulseMoved);
      if (highlightTimer.current) clearTimeout(highlightTimer.current);
      highlightTimer.current = setTimeout(() => {
        setHighlightMemberIds(new Set());
        setPulseChanged(false);
      }, 1200);
    }
  }, [supabase]);

  useEffect(() => {
    let cancelled = false;
    let debounce: ReturnType<typeof setTimeout> | null = null;
    let poll: ReturnType<typeof setInterval> | null = null;
    let channel: RealtimeChannel | null = null;

    const startPolling = () => {
      if (poll || cancelled) return;
      poll = setInterval(() => {
        void fetchAll();
      }, 60000);
    };
    const stopPolling = () => {
      if (poll) {
        clearInterval(poll);
        poll = null;
      }
    };
    const scheduleRefetch = () => {
      if (debounce) clearTimeout(debounce);
      debounce = setTimeout(() => {
        void fetchAll();
      }, 300);
    };

    void fetchAll();

    channel = supabase
      .channel('team-page')
      .on(
        'postgres_changes',
        { event: '*', schema: 'public', table: 'requests' },
        scheduleRefetch,
      )
      .on(
        'postgres_changes',
        { event: 'INSERT', schema: 'public', table: 'request_updates' },
        scheduleRefetch,
      )
      .on(
        'postgres_changes',
        { event: '*', schema: 'public', table: 'team_roster' },
        scheduleRefetch,
      )
      .subscribe((status) => {
        if (cancelled) return;
        if (status === 'SUBSCRIBED') {
          setConnection('live');
          stopPolling();
          void fetchAll();
        } else if (
          status === 'CHANNEL_ERROR' ||
          status === 'TIMED_OUT' ||
          status === 'CLOSED'
        ) {
          setConnection('reconnecting');
          startPolling();
        }
      });

    return () => {
      cancelled = true;
      if (debounce) clearTimeout(debounce);
      stopPolling();
      if (channel) void supabase.removeChannel(channel);
    };
  }, [fetchAll, supabase]);

  return useMemo(
    () => ({
      data,
      loading,
      connection,
      lastUpdatedAt,
      highlightMemberIds,
      pulseChanged,
    }),
    [data, loading, connection, lastUpdatedAt, highlightMemberIds, pulseChanged],
  );
}
