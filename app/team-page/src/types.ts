// Shared types for the AI Team Heartbeat Page.
// Queries in this package only ever select the columns named here.
// Internal fields (request_updates internal text, requests description,
// brief, blocker, next_step) are deliberately absent from every type.

export type Lane = 'muse' | 'claude' | 'grok';

export type DeskStatus =
  | 'New'
  | 'In Progress'
  | 'Waiting on Austin'
  | 'Waiting on Client'
  | 'Blocked'
  | 'Done';

export type ClientStatusLabel =
  | 'Received'
  | 'In progress'
  | 'Waiting on UpSurge'
  | 'Waiting on you'
  | 'Needs attention'
  | 'Completed';

export interface WorkspaceConfig {
  client_name: string;
  timezone: string;
  brand_color: string | null;
  logo_url: string | null;
}

export interface RosterRow {
  id: string;
  slug: string;
  lane: Lane;
  display_name: string;
  role: string;
  strengths: string[];
  is_leader: boolean;
  sort_order: number;
  is_active: boolean;
}

/** The only requests columns the heartbeat page may read. */
export interface RequestRow {
  id: string;
  title: string;
  status: DeskStatus;
  priority: string | null;
  lane: Lane | null;
  specialist_id: string | null;
  requested_at: string;
  updated_at: string;
  completed_at: string | null;
  client_visible: boolean;
  client_summary: string | null;
}

/** The only request_updates columns the heartbeat page may read. */
export interface ClientUpdateRow {
  request_id: string;
  client_summary: string;
  created_at: string;
}

export type MemberStatus = 'working' | 'queued' | 'available';

export interface MemberView {
  roster: RosterRow;
  status: MemberStatus;
  /** Title of the most recently updated In Progress project, when working. */
  currentWorkTitle: string | null;
  /** Additional In Progress projects beyond the one shown. */
  moreCount: number;
}

export interface LaneView {
  lane: Lane;
  leader: MemberView | null;
  members: MemberView[];
  openCount: number;
}

export interface PulseStats {
  inFlight: number;
  completedToday: number;
  /** Null when there are no completions in the trailing 7 days. */
  avgTurnaroundMs: number | null;
  requestsThisWeek: number;
}

export interface WinItem {
  id: string;
  title: string;
  clientSummary: string;
  completedAt: string;
  lane: Lane | null;
  specialistName: string | null;
}

export interface BoardProject {
  request: RequestRow;
  specialistName: string | null;
  latestClientUpdate: { summary: string; createdAt: string } | null;
}

export interface BoardData {
  counts: { status: DeskStatus; label: ClientStatusLabel; count: number }[];
  openProjects: BoardProject[];
}

export interface TeamData {
  config: WorkspaceConfig;
  pulse: PulseStats;
  lanes: LaneView[];
  wins: WinItem[];
  board: BoardData;
}

export type ConnectionState = 'live' | 'reconnecting';

export interface TeamDataResult {
  data: TeamData | null;
  loading: boolean;
  connection: ConnectionState;
  /** When the page last received a realtime event or completed a fetch. */
  lastUpdatedAt: Date | null;
  /** Roster ids whose status changed on the latest refetch (one time highlight). */
  highlightMemberIds: ReadonlySet<string>;
  /** True for one render cycle after any pulse value changes. */
  pulseChanged: boolean;
}
