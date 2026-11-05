# AI Team Heartbeat Page: Build Spec

The client-facing team page inside the client's Surge Command Desk. One page that shows the client their whole AI organization alive: who is on the team, which lane each member sits in, what is moving right now, and what has been delivered. Buildable from this document alone.

## Ground rules (read first)

1. **No fake metrics.** Every number, status, and feed item on this page derives from a real row in the Desk database. If the data does not exist, the page shows an honest empty state, never a placeholder number.
2. **A member card shows active only when that lane has a genuinely open project assigned to that member.** Status is computed from `requests`, never stored as a manual flag and never set by hand.
3. **Internal data never renders.** The page reads `request_updates.client_summary` only. It must never select `request_updates.note`, `requests.description`, `requests.brief`, `requests.blocker`, or `requests.next_step`. Those fields are internal.
4. **Roster is data, not code.** Team membership, strengths, and lane placement live in the `team_roster` table. Adding or moving a member is a data edit, never a deploy.
5. **Motion means data changed.** The only looping animation is the live connection pulse. Every other animation fires once, in response to a real database event.

## 1. Page layout and sections

Route: `/team` in the Desk app, behind the existing passcode gate, linked from the board nav as "Your Team". Sections render top to bottom in this order.

### 1.1 Masthead

- Left: client logo (`workspace_config.logo_url`) or, if null, the client name as a wordmark in the brand color (`workspace_config.brand_color`, fallback to the Desk default palette).
- Title: `<client_name> AI Team` with the subline `Your team, live`.
- Right: live clock showing the current time in `workspace_config.timezone` (updates every second, format `h:mm:ss AM/PM`, with the timezone abbreviation under it), and a connection indicator: a pulsing dot plus the word `Live` when the realtime channel is subscribed, an amber steady dot plus `Reconnecting` when it is not.
- A thin brand color rule under the masthead.

### 1.2 Activity pulse strip

Four stat tiles in a row (2 by 2 grid on mobile). Definitions are exact; see section 2.2 for the queries.

| Tile | Label | Value |
|---|---|---|
| 1 | In flight now | Count of projects currently In Progress |
| 2 | Completed today | Count of projects completed since midnight, client timezone |
| 3 | Average turnaround | Mean completion time over the trailing 7 days |
| 4 | Requests this week | Count of projects submitted since Monday 00:00, client timezone |

Each tile: large number, small label, and a one line sublabel with context (for example tile 1 sublabel: `across all three teams`). No trend arrows, no percentages, no invented comparisons.

### 1.3 The three lanes

Three columns, one per lane, in this order left to right: **Muse**, **Claude**, **Grok**. The Muse lane is first because Maive is the client's front door and delegator.

Each lane column contains:

- **Lane header:** lane name (`Claude Team`, `Grok Team`, `Muse Team`), a one line lane tagline, and a lane rollup chip showing the count of open projects in that lane right now (for example `4 open`).
  - Muse tagline: `Connected apps, memory, and always on operations`
  - Claude tagline: `Deep reasoning, documents, and careful builds`
  - Grok tagline: `Speed, volume, and live signal`
- **Lane leader card** (pinned at the top of the column, visually larger): leaders are Maive (Muse lane), Marcus (Claude lane), and Marcus (Grok lane). Same card anatomy as a member card, plus the line `Team lead` and the lane rollup repeated as `N projects open in this team`.
- **Member cards** for every active roster row in that lane, ordered by `team_roster.sort_order`.

Member card anatomy:

- Avatar: initials in a circle, tinted by lane color (Muse teal, Claude terracotta, Grok slate). No photos; the team is AI and the page should look intentional about that.
- Name (`display_name`) and role (`role`).
- Strengths: up to 3 short tags from `strengths`.
- Status pill, computed per section 2.3: `Working now` (filled, lane color), `Queued` (outline), or `Available` (muted).
- Current work line, shown only when the member has an In Progress project: the project title, truncated to one line. If more than one, show the most recently updated title plus `+N more`.
- A soft colored ring on the card while status is `Working now`.

### 1.4 Recent wins feed

Section title: `Recent wins`. A vertical feed of the 8 most recent completed projects that carry a client summary (query in section 2.4). Each win card shows:

- Project title
- The client summary text (`requests.client_summary`)
- Completion date, formatted in the workspace timezone (for example `Tue, Nov 4`)
- A lane chip and the specialist's name

### 1.5 Board summary

Section title: `Your board right now`. Two parts:

- **Status counts row:** one chip per status with its count, using the client facing labels from section 2.5 (Received, In progress, Waiting on UpSurge, Waiting on you, Needs attention, Completed).
- **Open project list:** every open project (status not Done, `client_visible = true`), ordered by priority (P0 first) then most recently updated. Each row: title, status chip, lane and specialist name, and the latest client update if one exists (the newest `request_updates` client summary for that project, with relative time such as `2h ago`).
- A link at the bottom: `Open the full board`, pointing at the existing Desk board view.

### 1.6 Footer

One small line: `Your AI Team by UpSurge` and `Updated <time>` where the time is the moment the page last received a realtime event or completed a fetch.

## 2. Data sources: every element mapped

All queries run through the existing Supabase client the Desk board already uses. Timezone boundaries (today, this week) are computed in `workspace_config.timezone` using `Intl` APIs in the client, then passed to queries as UTC timestamps.

### 2.1 Masthead and config

Single row from `workspace_config` (new table, section 3.3): `client_name`, `timezone`, `brand_color`, `logo_url`. Clock is the viewer's browser clock rendered in the configured timezone; it is a clock, not a metric. Connection state comes from the Supabase realtime channel status callback.

### 2.2 Pulse strip queries

All four tiles count only rows with `requests.client_visible = true`.

1. **In flight now:** `count(requests where status = 'In Progress')`.
2. **Completed today:** `count(requests where status = 'Done' and completed_at >= <today 00:00 in workspace tz>)`. Depends on the new `completed_at` field (section 3.1).
3. **Average turnaround:** `avg(completed_at - requested_at)` over requests with `status = 'Done'` and `completed_at` in the trailing 7 days. Display format: under 60 minutes `Xm`; under 24 hours `X.X hrs`; otherwise `X.X days`. If no completions in the window, the tile shows `Building history` in place of a number (honest empty state, section 4.3).
4. **Requests this week:** `count(requests where requested_at >= <Monday 00:00 in workspace tz>)`.

### 2.3 Member and lane status derivation

For each `team_roster` row (lane L, member M):

- `Working now`: at least one request exists with `specialist_id = M.id`, `lane = L`, `status = 'In Progress'`, `client_visible = true`.
- `Queued`: no In Progress request, but at least one request exists with the same assignment and status in (`New`, `Waiting on Austin`, `Waiting on Client`, `Blocked`).
- `Available`: neither of the above.

Current work line: among the member's In Progress requests, the one with the greatest `updated_at`; show its `title`. The `+N more` count is the remaining In Progress count.

Lane rollup chip: count of requests with `lane = L` and status not `Done` and `client_visible = true`.

Leaders derive status by the same rule (leaders hold projects too; Maive holds most intake). The leader card's `N projects open in this team` is the lane rollup count.

### 2.4 Wins feed query

`requests where status = 'Done' and client_summary is not null and client_visible = true`, ordered by `completed_at` descending, limit 8. Specialist name and lane come from a join to `team_roster` on `specialist_id`. A completed project without a client summary does not appear. That is deliberate: the feed is a publishing surface, and the summary is the publish action (section 3.2).

### 2.5 Board summary and client status labels

Status counts: `count(requests) group by status`, `client_visible = true` only. Open list: `requests where status != 'Done' and client_visible = true`, order by priority then `updated_at` descending. Latest client update per project: the newest `request_updates` row with `request_id = project` and `visibility = 'client'`, reading `client_summary` and `created_at` only.

Internal statuses map to client labels exactly as follows. The raw status values never display.

| Desk status | Client label |
|---|---|
| New | Received |
| In Progress | In progress |
| Waiting on Austin | Waiting on UpSurge |
| Waiting on Client | Waiting on you |
| Blocked | Needs attention |
| Done | Completed |

## 3. Schema additions

All changes are additive. Existing tables, the status check constraint, and the assignee check (`Maive`, `Marcus`) are unchanged. `lane` and `specialist_id` are the heartbeat source of truth for who is doing what; `assignee` remains the lane leader of record.

### 3.1 `requests` new columns

```sql
alter table public.requests
  add column lane text check (lane in ('claude', 'grok', 'muse')),
  add column specialist_id uuid references public.team_roster(id),
  add column completed_at timestamptz,
  add column client_visible boolean not null default true,
  add column client_summary text;

create index requests_lane_status_idx on public.requests (lane, status);
create index requests_specialist_status_idx on public.requests (specialist_id, status);
create index requests_completed_at_idx on public.requests (completed_at);
create index requests_requested_at_idx on public.requests (requested_at);
```

Field rules:

- `lane`: null at intake, set at triage when Maive routes the project. Null lane projects count in board totals but in no lane rollup and no member status.
- `specialist_id`: the roster row doing the work. Null until assigned.
- `completed_at`: set by the app in the same update that sets `status = 'Done'`; cleared back to null if a project is reopened. Never edited by hand.
- `client_visible`: default true. Set false for test projects and internal-only work so they never surface on this page or in any count.
- `client_summary`: written by the owning team when a project completes, in client language, 1 to 3 sentences, what was delivered and where to find it. Required by team process before marking Done in a client install; enforced by the wins query (no summary, no win) rather than a database constraint, so internal flows are never blocked.

### 3.2 `request_updates` client summary discipline

```sql
alter table public.request_updates
  add column visibility text not null default 'internal'
    check (visibility in ('internal', 'client')),
  add column client_summary text,
  add constraint request_updates_client_summary_required
    check (visibility = 'internal' or client_summary is not null);

create index request_updates_client_idx
  on public.request_updates (request_id, visibility, created_at desc);
```

The discipline, stated once and binding on every writer (human, lane leader, or automation):

- `note` is internal. It is written for the team and is never selected by any client facing query.
- A client facing update is a separate, deliberate act: insert a row with `visibility = 'client'` and a `client_summary` written for the client (what changed, what it means for them, no internal names of systems, no raw IDs, no internal shorthand).
- Existing rows default to `internal`, so nothing already written can leak when this ships.
- Heartbeat page queries select `client_summary` and `created_at` from `request_updates`, filtered to `visibility = 'client'`. The column `note` must not appear in the page's query code at all (QA grep check, section 5).

### 3.3 New table: `team_roster`

```sql
create table public.team_roster (
  id uuid primary key default gen_random_uuid(),
  slug text not null,
  lane text not null check (lane in ('claude', 'grok', 'muse')),
  display_name text not null,
  role text not null,
  strengths text[] not null default '{}',
  is_leader boolean not null default false,
  sort_order int not null default 0,
  is_active boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (slug, lane)
);

create unique index team_roster_one_leader_per_lane
  on public.team_roster (lane) where is_leader;
```

Notes:

- Unique on (`slug`, `lane`): the same specialist can sit in more than one lane (one row per lane, with lane specific strengths). Status is computed per row, so a specialist working a Claude lane project lights up in the Claude column only.
- `is_active = false` retires a member from the page without deleting history; historical projects keep their `specialist_id` join.
- Exactly one leader per lane, enforced by the partial unique index.

### 3.4 New table: `workspace_config`

```sql
create table public.workspace_config (
  id int primary key default 1 check (id = 1),
  client_name text not null,
  timezone text not null default 'America/Denver',
  brand_color text,
  logo_url text
);
```

One row per install, written at provision time.

### 3.5 Default roster seed

Seed at provision time. Leaders first (`sort_order` 0), then specialists. Strengths are the default set; the account team can edit rows per install. Default placement:

| Slug | Name | Role | Lane | Strengths |
|---|---|---|---|---|
| maive | Maive | Team Lead and Delegator | muse | Intake and routing, Connected apps, Memory |
| marcus | Marcus | Team Lead, Claude Team | claude | Deep research, Long form writing, Careful builds |
| marcus | Marcus | Team Lead, Grok Team | grok | Speed execution, Volume work, Live signal |
| owen | Owen | Onboarding Orchestrator | muse | New client setup, Install sequencing |
| lena | Lena | Memory Librarian | muse | Knowledge base, Recall, Records |
| felix | Felix | Fulfillment Lead | muse | Delivery pipeline, Task flow |
| diego | Diego | CRM Architect | muse | HighLevel builds, Pipelines, Automations |
| dana | Dana | CRM Data Ops | muse | Data cleanup, Imports, Lists |
| remy | Remy | Voice Agent Provisioner | muse | Retell agents, AI calling, Phone systems |
| wes | Wes | Web Dev Lead | muse | Websites, Landing pages, Apps |
| dex | Dex | Delivery QA | muse | Quality checks, Verification, Sign off |
| aria | Aria | A2P Compliance | muse | Texting compliance, Registrations |
| hazel | Hazel | Client Success Lead | muse | Client communication, Follow through |
| quinn | Quinn | Call QA Auditor | muse | Call review, Conversation quality |
| kai | Kai | SEO and AEO Lead | claude | Search visibility, Content plans, Blog drafting |
| sage | Sage | SOP and Skill Writer | claude | Procedures, Documentation, Training packs |
| iris | Iris | Visionary | claude | Product concepts, Page and experience specs |
| malik | Malik | Client Reporting | claude | Reports, Analysis, Summaries |
| theo | Theo | Meeting to Action | claude | Meeting notes, Action extraction |
| finn | Finn | Finance Controller | claude | Invoices, Billing checks, Numbers |
| heath | Heath | CFO | claude | Financial strategy, Forecasting |
| milo | Milo | Ad Creative Producer | grok | Ad creative, Video cuts, Variants |
| greta | Greta | Growth and Sales Lead | grok | Campaigns, Outreach, Pipeline growth |
| parker | Parker | Performance Analyst | grok | Metrics, Live monitoring, Trends |
| nova | Nova | Service Innovation | grok | New offers, Experiments |
| tara | Tara | Talent Ops | grok | Roster growth, Specialist coverage |

## 4. Realtime behavior, motion, empty states, mobile

### 4.1 Realtime (Supabase subscriptions)

Enable realtime on the three tables:

```sql
alter publication supabase_realtime add table public.requests;
alter publication supabase_realtime add table public.request_updates;
alter publication supabase_realtime add table public.team_roster;
```

Client behavior:

- On page load, fetch all five data groups (config, pulse aggregates, roster with derived status, wins, board summary), then open one realtime channel subscribed to `postgres_changes` on `requests` (all events), `request_updates` (insert only), and `team_roster` (all events).
- On any event, debounce 300 ms, then refetch the affected groups. V1 refetches rather than patching state incrementally; correctness beats cleverness at this data volume.
- Track channel state: `SUBSCRIBED` drives the masthead Live indicator. On channel error or close, the dot turns amber with the label `Reconnecting`, polling fallback starts at 60 second intervals, and polling stops when the channel resubscribes.
- Updates to `request_updates` with `visibility = 'internal'` will still fire events; the refetch simply returns no new client data. That is acceptable. The internal row content is never fetched by the page's queries.

### 4.2 Motion design

- **Masthead pulse:** the connection dot runs a 2 second CSS pulse (scale and opacity) only while the channel is subscribed. It indicates a live connection, nothing more.
- **Event highlight:** when a realtime event changes a member's status or a pulse number, the affected card or tile gets a one time highlight (background tint fading out over 1.2 seconds). Implement by keeping the last event timestamp and target IDs in state and applying a highlight class once.
- **Status transitions:** the Working now ring and status pill colors transition over 300 ms.
- **Number changes:** pulse tile values crossfade on change. No count up tween in v1; a tween implies measurement precision the data does not need.
- **Reduced motion:** under `prefers-reduced-motion`, the pulse loop, highlights, and transitions are all disabled. The page remains fully informative as a static page.
- No other animation. No skeleton shimmer loops beyond initial load, no decorative motion anywhere else on the page.

### 4.3 Empty states (must still look premium)

- **Brand new install (zero projects):** the roster renders in full, so the page looks complete on day one. Pulse tiles show `0`, `0`, `Building history`, `0`. The wins feed shows one designed placeholder card: `Your first wins will appear here as projects complete.` The board summary shows the install project itself (provisioning creates a real first project, `AI Team install`, which is worked and completed like any other; when it completes with its client summary, it becomes the first genuine win in the feed).
- **Quiet day (history exists, nothing today):** Completed today shows `0` with no apology copy. Wins keep showing history because the feed is not day scoped. Member cards show `Available`, which reads as a team at the ready, not a team idle.
- **No logo or brand color set:** wordmark in the default palette. The layout must not depend on the logo existing.
- **Loading:** skeleton blocks matching the final layout shapes, shown only during the initial fetch.

### 4.4 Mobile behavior

- **1200 px and up:** three lane columns side by side. Pulse strip in one row of four.
- **768 to 1199 px:** two lane columns; the third lane wraps to a full width row with its member cards in a two column grid. Pulse strip in one row of four, smaller type.
- **Under 768 px:** single column. Lane order: Muse, Claude, Grok. Member cards become horizontal rows (avatar left, name and role stacked, status pill right, current work line under). Pulse strip becomes a 2 by 2 grid. Wins feed and board list go full width. Masthead stacks: wordmark first, clock and Live indicator on a second row.
- No horizontal scrolling at any width. Minimum touch target 44 px. Text truncation uses ellipsis with the full title available on tap through the board link.

## 5. Build sequence (GitHub first, per client clone)

All code work happens in the GitHub repo synced with the Lovable app, following the standing rule: never edit in Lovable when a synced repo exists. The template repo is `austin-gibbs/surge-command-desk`; each client install is a clone of it with its own Lovable project and Supabase database, provisioned from the template.

1. **Branch:** `feature/heartbeat-page` off `main` in the template repo.
2. **Migration:** add the section 3 SQL as the next drizzle migration. Generate snapshots with drizzle-kit; do not hand edit migration JSON. Known template residual: `drizzle/migrations/meta/0004_snapshot.json` is missing in the repo while the live database is correct; leave that alone in this branch and let the new migration generate forward from the live schema state. The `alter publication` statements are not drizzle managed; ship them as a clearly marked raw SQL block at the end of the migration file and verify they ran.
3. **Seed:** roster seed and the `workspace_config` insert as an idempotent SQL seed file (`seed/heartbeat-seed.sql`, safe to rerun: upsert on the unique keys).
4. **Data layer:** `src/lib/heartbeat/` with one module per data group (`config.ts`, `pulse.ts`, `roster.ts`, `wins.ts`, `board.ts`). Queries select exactly the columns in section 2. The string `note` must not appear as a selected column in this folder.
5. **Components:** `src/components/heartbeat/` with `Masthead`, `PulseStrip`, `LaneColumn`, `MemberCard`, `WinsFeed`, `BoardSummary`. Status label map from section 2.5 lives in one shared file.
6. **Realtime hook:** `useHeartbeatRealtime` implementing section 4.1 (subscribe, debounce refetch, connection state, polling fallback).
7. **Route:** add `/team` behind the existing passcode gate and the nav link `Your Team`.
8. **QA pass (Dex checklist below)** on the template deployment with seeded test data, including at least one project per status and one per lane.
9. **Merge and verify:** merge to `main`, confirm Lovable syncs from GitHub, and verify the page on the published template app (data and realtime, not click through alone).
10. **Per client clone:** create the client's repo from the template, connect their Lovable project, run migrations and seed, set the `workspace_config` row (client name, timezone, brand color, logo), create the `AI Team install` project, and hand over the passcode. The first win lands when the install project completes with its client summary.

## 6. QA acceptance checklist (Dex)

Every item must pass on the template before the first client clone.

- [ ] Each pulse tile number matches a hand run SQL count on the same dataset, including the timezone boundary cases (a project completed at 11:30 PM client time counts today; one at 12:30 AM counts tomorrow).
- [ ] A member card flips to `Working now` within one realtime cycle of a project being set In Progress for that member and lane, and flips back when it completes.
- [ ] A specialist seeded in two lanes lights up only in the lane of the active project.
- [ ] An internal `request_updates` row's `note` text appears nowhere in the rendered page, the page source, or the network payloads of the heartbeat queries. Grep the data layer: no select of the `note` column.
- [ ] A project marked Done without a `client_summary` does not appear in the wins feed; adding the summary makes it appear.
- [ ] A project with `client_visible = false` appears in no count, feed, list, or member status.
- [ ] Status labels on the page match the section 2.5 map; the raw Desk status strings never render.
- [ ] Dropping the realtime connection turns the masthead indicator amber within one channel timeout, shows `Reconnecting`, and data still refreshes on the 60 second poll.
- [ ] With `prefers-reduced-motion` on, no looping or transitional animation runs.
- [ ] At 375 px wide there is no horizontal scroll, lanes stack Muse first, and the pulse strip is 2 by 2.
- [ ] On a fresh database with only seed data, the page renders complete: full roster, honest zeros, placeholder win card, no errors.
- [ ] Reopening a completed project clears `completed_at` and removes it from Completed today and the wins feed on the next refetch.
