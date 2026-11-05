# AI Team Heartbeat Page: Template Package

The client-facing team page for a Surge Command Desk install. One page that shows the client their whole AI organization alive: who is on the team, which lane each member sits in, what is moving right now, and what has been delivered. Built to the heartbeat page spec; the spec's data honesty rules are binding on this code:

- Every number, status, and feed item derives from a real row in the Desk database. If the data does not exist, the page shows an honest empty state, never a placeholder number.
- Member status is computed from `requests` at fetch time (Working now, Queued, Available), never stored as a manual flag.
- Wins come only from projects with status Done that carry a `client_summary`. A completed project without a summary does not appear; the summary is the publish action.
- The page never selects the internal text column of `request_updates`, nor `requests` description, brief, blocker, or next_step. Client updates are read through `client_summary` on rows with `visibility = 'client'` only.
- Roster is data in the `team_roster` table. Adding or moving a member is a data edit, never a deploy.

## Package layout

- `migrations/0001_team_page.sql`: schema additions (spec section 3). Additive and idempotent: `requests` gains lane, specialist_id, completed_at, client_visible, client_summary; `request_updates` gains visibility (default internal) and client_summary with the check constraint; new `team_roster` and `workspace_config` tables; realtime publication statements included as guarded raw SQL at the end.
- `migrations/0002_roster_seed.sql`: the default roster (spec section 3.5): Maive leading Muse, Marcus leading Claude and Grok, and the default specialists per lane. Idempotent upsert on (slug, lane).
- `src/TeamPage.tsx`: the page. Sections in spec order: masthead, pulse strip, three lanes (Muse, Claude, Grok), recent wins, board summary, footer.
- `src/components/`: Masthead, PulseStrip, LaneColumn, MemberCard, WinsFeed, BoardSummary.
- `src/hooks/useTeamData.ts`: the data layer and realtime behavior. Fetches all data groups, derives pulse stats, member and lane status, and the board summary, then keeps them fresh: one Supabase realtime channel, 300 ms debounce refetch on any event, 60 second polling fallback while the channel is down, and a Live or Reconnecting connection state for the masthead.
- `src/lib/statusLabels.ts`: the one shared map from Desk statuses to client labels (Waiting on Austin renders as Waiting on UpSurge, and so on).
- `src/lib/lanes.ts`: lane order, taglines, and lane colors. `src/lib/time.ts`: workspace timezone boundaries (today, Monday week start) computed with Intl.
- `src/types.ts`: shared types. The request and update types deliberately contain only the columns the page may read.

## Dropping it into the Command App template

GitHub first, per the standing rule: all work happens in the GitHub repo synced with the app, never by editing in Lovable.

1. Branch `feature/heartbeat-page` off `main` in the template repo (`austin-gibbs/surge-command-desk`, or the service repo's app template copy).
2. Apply `migrations/0001_team_page.sql` as the next migration. If the project uses drizzle, paste the SQL into the generated migration file; do not hand edit migration snapshot JSON. Known template residual: `drizzle/migrations/meta/0004_snapshot.json` is missing in the template repo while the live database is correct; leave it alone and generate forward from the live schema state.
3. Run `migrations/0002_roster_seed.sql`. Safe to rerun.
4. Insert the one `workspace_config` row for the install (id 1): client name, timezone, brand color, logo URL.
5. Copy `src/` into the app source tree. Dependencies: React, Tailwind, and `@supabase/supabase-js` only. The page takes the app's existing Supabase client as a prop, so no second client or new environment variable is introduced:

```tsx
import { TeamPage } from './team-page/TeamPage';
import { supabase } from './lib/supabase'; // the Desk app's existing client

<Route path="/team" element={<TeamPage supabase={supabase} boardHref="/board" />} />
```

6. Add the `/team` route behind the existing passcode gate, next to the board routes, and add the nav link labeled `Your Team`.
7. Verify the realtime publication statements at the end of migration 0001 ran (they are guarded DO blocks; check `pg_publication_tables` for requests, request_updates, and team_roster in `supabase_realtime`).
8. Create the install's first real project, titled `AI Team install`, and work it like any other project. When it completes with its client summary, it becomes the first genuine win in the feed.

Per client clone: new repo from the template, run migrations and seed, set the `workspace_config` row, create the `AI Team install` project, hand over the passcode.

## Notes and interpretations

- The Supabase client is dependency injected (a `supabase` prop on `TeamPage`) so this package resolves every import internally and stays portable across installs. The host app passes the same client the board already uses.
- `boardHref` defaults to `/`; set it to the Desk board route in the host app's router.
- Status derivation, pulse aggregates, wins selection, and the board list are computed in `useTeamData` from the fetched visible rows rather than in separate SQL aggregate queries. At Desk data volumes this keeps one code path for every number on the page, and every query still filters on `client_visible = true` and selects exactly the allowed columns.
- The only looping animation is the connection pulse while the channel is subscribed. Highlights fire once per real change, transitions are 300 ms, and `prefers-reduced-motion` disables all of it through Tailwind `motion-reduce` variants.

## QA acceptance checklist (Dex, from the spec)

Every item must pass on the template before the first client clone.

- [ ] Each pulse tile number matches a hand run SQL count on the same dataset, including the timezone boundary cases (a project completed at 11:30 PM client time counts today; one at 12:30 AM counts tomorrow).
- [ ] A member card flips to Working now within one realtime cycle of a project being set In Progress for that member and lane, and flips back when it completes.
- [ ] A specialist seeded in two lanes lights up only in the lane of the active project.
- [ ] An internal `request_updates` row's internal text appears nowhere in the rendered page, the page source, or the network payloads of the heartbeat queries. Grep the data layer: no select of the internal text column.
- [ ] A project marked Done without a `client_summary` does not appear in the wins feed; adding the summary makes it appear.
- [ ] A project with `client_visible = false` appears in no count, feed, list, or member status.
- [ ] Status labels on the page match the client label map; the raw Desk status strings never render.
- [ ] Dropping the realtime connection turns the masthead indicator amber within one channel timeout, shows Reconnecting, and data still refreshes on the 60 second poll.
- [ ] With `prefers-reduced-motion` on, no looping or transitional animation runs.
- [ ] At 375 px wide there is no horizontal scroll, lanes stack Muse first, and the pulse strip is 2 by 2.
- [ ] On a fresh database with only seed data, the page renders complete: full roster, honest zeros, placeholder win card, no errors.
- [ ] Reopening a completed project clears `completed_at` and removes it from Completed today and the wins feed on the next refetch.
