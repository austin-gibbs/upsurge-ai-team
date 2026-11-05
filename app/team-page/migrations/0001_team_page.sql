-- 0001_team_page.sql
-- AI Team Heartbeat Page: schema additions (spec section 3).
-- All changes are additive and idempotent: safe to rerun.
-- Existing tables, the status check constraint, and the assignee check
-- ('Maive', 'Marcus') are unchanged. Plain SQL in the repo's migration style.

-- ---------------------------------------------------------------------------
-- 3.3 New table: team_roster (created first; requests.specialist_id references it)
-- ---------------------------------------------------------------------------

create table if not exists public.team_roster (
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

-- Exactly one leader per lane, enforced by a partial unique index.
create unique index if not exists team_roster_one_leader_per_lane
  on public.team_roster (lane) where is_leader;

-- ---------------------------------------------------------------------------
-- 3.4 New table: workspace_config (one row per install, id is always 1)
-- ---------------------------------------------------------------------------

create table if not exists public.workspace_config (
  id int primary key default 1 check (id = 1),
  client_name text not null,
  timezone text not null default 'America/Denver',
  brand_color text,
  logo_url text
);

-- ---------------------------------------------------------------------------
-- 3.1 requests: new columns
-- ---------------------------------------------------------------------------

alter table public.requests add column if not exists lane text;
alter table public.requests add column if not exists specialist_id uuid references public.team_roster(id);
alter table public.requests add column if not exists completed_at timestamptz;
alter table public.requests add column if not exists client_visible boolean not null default true;
alter table public.requests add column if not exists client_summary text;

-- Lane value check, added by name so reruns do not duplicate it.
do $$
begin
  if not exists (
    select 1 from pg_constraint where conname = 'requests_lane_check'
  ) then
    alter table public.requests
      add constraint requests_lane_check check (lane in ('claude', 'grok', 'muse'));
  end if;
end $$;

create index if not exists requests_lane_status_idx on public.requests (lane, status);
create index if not exists requests_specialist_status_idx on public.requests (specialist_id, status);
create index if not exists requests_completed_at_idx on public.requests (completed_at);
create index if not exists requests_requested_at_idx on public.requests (requested_at);

-- ---------------------------------------------------------------------------
-- 3.2 request_updates: client summary discipline
-- visibility defaults to 'internal', so nothing already written can leak
-- when this ships. A client facing row must carry a client_summary.
-- ---------------------------------------------------------------------------

alter table public.request_updates add column if not exists visibility text not null default 'internal';
alter table public.request_updates add column if not exists client_summary text;

do $$
begin
  if not exists (
    select 1 from pg_constraint where conname = 'request_updates_visibility_check'
  ) then
    alter table public.request_updates
      add constraint request_updates_visibility_check
      check (visibility in ('internal', 'client'));
  end if;

  if not exists (
    select 1 from pg_constraint where conname = 'request_updates_client_summary_required'
  ) then
    alter table public.request_updates
      add constraint request_updates_client_summary_required
      check (visibility = 'internal' or client_summary is not null);
  end if;
end $$;

create index if not exists request_updates_client_idx
  on public.request_updates (request_id, visibility, created_at desc);

-- ---------------------------------------------------------------------------
-- 4.1 Realtime: enable Supabase realtime on the three tables.
-- Not drizzle managed; guarded so reruns do not fail when a table is
-- already in the publication. Verify these ran after applying (README).
-- ---------------------------------------------------------------------------

do $$
begin
  begin
    alter publication supabase_realtime add table public.requests;
  exception when duplicate_object then null;
  end;
  begin
    alter publication supabase_realtime add table public.request_updates;
  exception when duplicate_object then null;
  end;
  begin
    alter publication supabase_realtime add table public.team_roster;
  exception when duplicate_object then null;
  end;
end $$;
