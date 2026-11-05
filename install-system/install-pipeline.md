# AI Team Install Pipeline Spec

Status: Draft v1, 2026-11-04
Owner: Wes (web-dev-lead), Muse lane, for Maive (delegator of record)
Scope: Fully automated install of the AI Team product for one client business: a Surge Command Desk instance, a three lane AI team (Muse, Grok, Claude), a versioned Craft layer (Team Pack), and an isolated Client layer (client memory).
Out of scope: Pricing, contract terms, sales motion, ongoing task execution after go live (covered by the MAV to Desk project loop and the execution brief standard).

## 1. Design principles

1. One front door. The client talks to Maive only. Lane routing, specialist assignment, and QA happen behind the door and are never the client's job.
2. Two memory layers, hard boundary. The Craft layer (Team Pack) is UpSurge IP and is pushed one way into every install. The Client layer holds that client's facts only, is readable only inside that install, and never flows into the Craft layer or into another client.
3. Idempotent by construction. Every automated action runs under an idempotency key and checks for the existing object by natural key before creating it. Re-running any stage is safe and converges to the same end state.
4. No deletions. Rollback and cleanup archive objects inside their system (repo archive path, Desk status, Slack channel archive). Nothing is hard deleted, matching the standing repo rule.
5. Secrets are pointers only. No credential value is stored in the manifest, the repo, Desk fields, or Slack. The manifest stores a pointer (vault entry name, connector name, env var name) and a verified flag.
6. Client sees outcomes, not machinery. Client facing surfaces show status, deliverables, and summaries written for the client. Internal notes, prompts, playbooks, and lane mechanics are never copied into client visible fields.
7. Human touchpoints are named, minimal, and blocking only where a human act is legally or technically required (an OAuth tap, a seat invite acceptance, a go live approval).

## 2. Core identifiers and records

- install_id: UUID minted at Stage 1 start. Primary key for the whole install.
- client_slug: lowercase hyphenated slug, unique across installs. Used in repo paths, Desk client field, channel names, and manifest keys.
- Install manifest: the single machine readable record of everything created for the install (Section 8). Stored in the UpSurge ops repo under the Muse lane at memory/muse/installs/<client_slug>/manifest.json, with a mirrored summary row in the UpSurge internal Desk.
- Install state record: one row per install in the install state store (Section 10). Holds current state, per stage status, per step attempt counts, and last error. This is the resume point after any crash.
- Team Pack version: semantic version string (for example pack 1.0.0) recorded in the manifest. Every install step that consumes the Pack records the version it used.

## 3. Stage overview

| Stage | Name | Trigger | Primary systems | Client visible |
|---|---|---|---|---|
| 1 | Provision | Signed agreement record created | Lovable, GitHub, Slack | Welcome message, install started |
| 2 | Connect | Stage 1 done | Connectors, client apps | Connect checklist filling in |
| 3 | Seat platforms | Stage 2 core apps done | Muse, Grok, Claude seats | Team Pack confirmation |
| 4 | Seed knowledge | Stage 3 done | Drive, website, CRM, GitHub | Knowledge v1 review link |
| 5 | Go live | QA gate approved | Desk, Slack, heartbeat page | Live org heartbeat page, first task |

Stages run in order. A stage may start its read only preparation while the prior stage finishes (for example, website crawl during Stage 3), but no stage marks done out of order.

## 4. Stage 1: Provision

Trigger: A signed agreement record appears in the UpSurge CRM (or an operator runs the install command with client_slug, legal name, sponsor name, sponsor email, intake mode, and timezone). The orchestrator mints install_id and writes the install state record in state `provisioning`.

Automated actions, in order:
1. Create the Client layer memory structure in the repo at memory/muse/clients/<client_slug>/ with the standard file set: profile.md, people.md, brand.md, systems.md, decisions.md, open-items.md, and an intake/ folder. Seed each file from the Team Pack client template with agreement facts only.
2. Create the client's Desk workspace: insert the client record and standard configuration into the Surge Command Desk data model via Lovable query_database (client row, default statuses New / In Progress / Waiting on Austin / Waiting on Client / Blocked / Done, priority set P0 to P3, assignee set Maive / Marcus). If the deployment model moves to one Desk project per client, record the new Lovable project id in the manifest instead; the data steps are identical.
3. Generate the Desk passcode on the server side, store it in the server environment (pointer name SURGE_PASSCODE_<CLIENT_SLUG>), and record only the pointer in the manifest. The passcode value never enters the repo, Desk, or Slack.
4. Create Slack surface: one client internal ops channel in the UpSurge workspace (name pattern ops-<client_slug>) and register the client's sponsor contact for notifications. Client facing conversation stays in the client's chosen surface (Section 9), not in UpSurge Slack.
5. Create the roster record for the install: the lane leaders (Maive for Muse, Marcus for Grok, Marcus for Claude) and the specialist roster from the current Team Pack, each with role, lane, strengths, and a client safe bio.
6. Create webhook endpoints for the install (Section 8): intake webhook, PM system webhook (if that intake mode is chosen), and install status callback. Register each URL in the manifest with a pointer to its signing secret.
7. Write the manifest v1 to the repo and post the internal start notice to #ai-command with install_id and client_slug.

Systems touched: GitHub (repo writes via the GitHub connector), Lovable query_database (Desk), Slack (channel create, message), server environment (passcode pointer only).

What the client sees: A welcome message from Maive in the chosen intake surface: install started, the five stages in plain language, the connect link for Stage 2, and the name of their single point of contact. No internal channel names, no repo paths.

Human touchpoints: None in the happy path. Exception only: an operator resolves a client_slug collision or a failed channel create after automated retries exhaust.

Failure handling and retries:
- Every create is check first by natural key (repo path exists, Desk client row by slug, channel by name). A retry after a partial failure resumes at the first missing object.
- GitHub push conflicts (concurrent commits): rebase on latest main and retry up to 3 times with backoff 30s, 120s, 480s. On third failure, state moves to failed_retryable and an alert posts to #ai-command.
- Lovable query_database errors: retry idempotent inserts up to 3 times. A schema mismatch error is terminal for the stage (failed_terminal) because retrying cannot fix it; it pages the operator with the exact SQL error text.
- Slack channel name collision: append a numeric suffix once and record the actual name in the manifest.

Definition of done: Manifest v1 committed and read back from the repo; Desk client row verified by a read query; ops channel exists and the start notice is posted; passcode pointer recorded and a test read of the pointer succeeds; install state = provisioned.

## 5. Stage 2: Connect

Trigger: Install state = provisioned and the sponsor opens the connect flow (link from the welcome message) or the scheduled connect reminder fires at 24 hours after provision.

Automated actions, in order:
1. Present the connect checklist in priority order for the client's stack: email, calendar, file storage, CRM, then client specific apps (for example HighLevel, Retell, Meta Ads) as named in the agreement. Each item is one connector authorization in Muse's secure connection flow.
2. On each authorization success, run that connector's read only verification (status check plus one harmless list or read call) and record in the manifest: connector name, account label, scopes granted, verified timestamp, pointer only.
3. For API key based apps with no OAuth connector, send the secure capture form for that one key at the moment that app is reached. One key at a time, stored in secure storage, pointer recorded. Never bulk collect keys.
4. For apps with no connector and no API path, record a manual access entry in the manifest (system name, access method, owner) and flag the affected capabilities as limited in the roster page. Do not invent a connection flow.
5. Verify the primary CRM end to end: read one pipeline or list, confirm write path exists where the agreement requires it, and record location or account ids (ids are identifiers, not credentials, and are safe to store).
6. When all required apps verify, mark the stage done. Optional apps may remain pending without blocking; they are listed as pending in the manifest and in the client's checklist.

Systems touched: Muse connectors (Gmail, Google Calendar, Google Drive, Google Docs, Google Sheets, Slack, HighLevel, Lovable, Vercel, Meta Ads, GitHub as applicable), custom connectors under ~/workspace/custom-connectors/, the client apps themselves.

What the client sees: A checklist that ticks itself as each connection verifies, written in business terms ("Email connected", "CRM connected and verified"), plus a single line when a key is needed with the secure form link. They never see scopes, tokens, or error codes.

Human touchpoints (named, required by the platforms):
- Client Sponsor or Client Admin: performs each OAuth authorization tap and each secure key entry. This cannot be automated away; it is the account owner's act.
- UpSurge Operator: only on a connector that fails verification 3 times; the operator gets the error and the account label, never the credential.

Failure handling and retries:
- First call to a newly approved host can time out in the proxy tunnel (known behavior). Retry once before treating it as a credential problem.
- Cloudflare protected APIs (verified on Instantly and Resend, 2026-11-04) reject the default Python user agent with error 1010. All custom connector helpers send a browser User Agent header. A 403 from these APIs is checked against this cause before it is reported as a bad key.
- A 429 from any provider is a hard stop for that provider in this run. The stage pauses that app, continues with other apps, and schedules the retry. No alternate endpoints or parallel retries.
- Wrong account connected (account label mismatch with the agreement): halt that app, mark needs_human, and ask the sponsor to reconnect. Do not proceed on a wrong account.
- Verification failure after 3 attempts: app marked failed with reason code, stage completes as done_with_gaps only if the app is optional; a required app failure moves the install to paused_human with the exact ask written for the sponsor.

Definition of done: Every required app in the agreement has a manifest entry with verified = true and a passing read check timestamped within the stage window; pending optional apps are listed with owners; install state = connected.

## 6. Stage 3: Seat platforms

Trigger: Install state = connected (core apps: email, files, CRM verified). Seating may proceed before optional apps finish.

Automated actions, in order:
1. Determine the seat model from the agreement: client owned seats (default) or UpSurge managed seats. Record the model and each seat's account label in the manifest.
2. For the Muse seat: connect the client's Muse environment to the install by registering the client memory location, the Desk, and the connectors from Stage 2. Maive is recorded as delegator of record for the install.
3. For the Claude seat and the Grok seat: deliver the Team Pack bootstrap package to each seat: roster, lane routing rules, claim protocol, house style (no em dashes, dates absolute, pointers only), the execution brief standard, and a pointer to the Client layer. Delivery mechanism per platform: the platform's project or instructions surface, plus a bootstrap task that the seat must complete and report back (Section 11 covers the automation limit here).
4. Run the seat verification drill for each lane: a synthetic, client safe test task is routed to the lane (for example, "summarize the client profile back to the delegator"). The lane must claim it, complete it using the Client layer only, and return it in the handoff packet format. Pass criteria: correct facts, correct format, no cross client data, no internal process language.
5. Record per lane: seat account label, Pack version delivered, drill result, verified timestamp.
6. Publish the routing table for the install into the Client layer systems.md: task type to primary lane to fallback lane, from the Team Pack default with client specific overrides only where the agreement names them.

Systems touched: Muse (connector registrations), Claude and Grok platform accounts (client owned or managed), GitHub (Pack delivery artifacts and drill records), Desk (drill tasks may ride the Desk as internal projects, never client visible).

What the client sees: One confirmation message: their team is seated, the three lanes named with their leaders, and what each lane is strongest at, in plain language. They do not see bootstrap contents, drills, or routing tables.

Human touchpoints (named):
- Client Seat Owners: accept seat invites and complete any platform side account confirmation. One action per seat.
- UpSurge Operator: approves a lane that fails the drill twice; the operator reviews the drill output and decides between a Pack fix and a seat fix. No other routine involvement.

Failure handling and retries:
- Drill failure (wrong facts, format break, leaked internal language): the lane re-reads the Pack and the Client layer and retries once automatically. Second failure moves that lane to needs_human and the install continues with the remaining lanes; the failed lane receives no client work.
- Seat invite not accepted after 48 hours: one reminder to the seat owner, then the install moves that lane to pending and go live is blocked only if the missing lane is the Muse lane (the delegator lane is mandatory).
- Pack version mismatch across lanes: re-deliver the current Pack to the stale lane and re-run the drill before marking the stage done.

Definition of done: All three lanes recorded with the same Pack version; Muse lane drill passed (mandatory); at least one of Claude or Grok drill passed with the other explicitly pending and owned; routing table written; install state = seated.

## 7. Stage 4: Seed knowledge

Trigger: Install state = seated.

Automated actions, in order:
1. Ingest public and provided sources: client website crawl, brand assets from file storage, existing documents and SOPs from Drive or Docs, CRM structure (pipelines, stages, fields, locations), and any exported lists the agreement names. Each source is logged in the manifest with origin and ingest timestamp.
2. Draft Client layer v1: profile (business, offers, service area, hours), people (decision makers, team, key contacts with roles), brand (palette, fonts, voice rules, banned phrases), systems (apps, ids, access pointers, known limits), and open-items (every fact that could not be verified, stated as a question).
3. Strip and quarantine: remove every credential value, price or rate the client has marked do not publish, and any personal identifier not needed for operations. Quarantined items are listed by category in open-items, never copied into memory content.
4. Cross check facts against at least two sources where possible (website vs CRM vs document). Conflicts are not resolved by guessing; both values are recorded in open-items with sources, and the more recent dated source is used provisionally and flagged.
5. Generate the knowledge review package: a single client readable document summarizing what the team now knows, what it assumed, and what it still needs. Post it to the review surface (Desk client visible note or a shared doc, per intake mode).
6. Load the seeded memory into each seated lane by re-running the Stage 3 bootstrap pointer update, and run one knowledge drill per lane (three factual questions from the seeded profile; answers must match the Client layer exactly).

Systems touched: Client website (read), Google Drive and Docs, CRM via connector, GitHub (Client layer writes), Desk (review package pointer), the three platform seats (pointer refresh).

What the client sees: The review package and a short list of specific questions (open items). Nothing else. They never see raw ingest logs or the memory files themselves.

Human touchpoints (named):
- Client Sponsor: reviews the knowledge package and answers or corrects the open items. This is the one planned human review in the pipeline; target effort for the sponsor is under 30 minutes.
- UpSurge Operator: none in the happy path. The operator is pulled in only if ingest sources contradict on a fact the sponsor cannot resolve.

Failure handling and retries:
- Source unreachable (site blocks crawlers, export missing): record the gap in open-items, continue with remaining sources, and downgrade affected capabilities on the roster page to "limited until source provided". Never fabricate a missing fact.
- CRM read limits (for example, a locations list that paginates at 20): resolve named accounts by direct id lookup where the client provides ids; record unresolved accounts as open items rather than concluding they do not exist.
- Knowledge drill failure: re-seed the failing lane's pointer and retry once. A second failure returns the install to Stage 3 handling for that lane.
- Sponsor does not review within 3 business days: one reminder, then the install proceeds to the QA gate with assumptions flagged, except facts marked client facing critical (names, prices, service claims), which block go live until confirmed.

Definition of done: Client layer v1 committed; review package delivered; sponsor corrections applied or explicitly waived; all lanes pass the knowledge drill; open-items contains only non blocking questions; install state = seeded.

## 8. Provisioning manifest

One manifest per install, created in Stage 1 and updated by every stage. It is the install's bill of materials. Every object below is created or explicitly recorded as not applicable with a reason.

Identity and config:
- install_id, client_slug, legal name, sponsor name and email, timezone, intake mode, seat model, agreement date, Team Pack version, install state, stage status map.

Desk objects:
- Desk client row id; Desk configuration (statuses, priorities, assignees); passcode pointer (env var name only); Desk base URL; test project id used for verification (pattern: TEST access check, created once, marked Done, never deleted); roster table rows (one per team member per lane); heartbeat page URL.

Client layer (repo) objects:
- Client folder path; the standard file set (profile, people, brand, systems, decisions, open-items); installs manifest path; Team Pack delivery record per lane; drill records per lane; knowledge review package path.

Channels and surfaces:
- UpSurge ops Slack channel id and name; client notification target per intake mode (Section 9); sponsor contact record; escalation contact (UpSurge operator on call label).

Connected apps (one entry per app):
- Connector name; account label; scopes granted; verified flag and timestamp; account or location ids needed for operations; credential pointer (vault or secure storage entry name); known limits (for example, workflow API not enabled, list pagination caps); status (verified, pending, failed, not applicable).

Platform seats (one entry per lane):
- Lane (Muse, Grok, Claude); leader name (Maive or Marcus); seat model; account label; Pack version delivered; bootstrap delivery method; drill result and timestamp; status.

Webhook endpoints (one entry per endpoint):
- Purpose (intake, PM sync, status callback); URL; signing secret pointer; expected sender; last verified timestamp; retry policy reference.

Heartbeat and reporting:
- Heartbeat page URL; roster data source pointer; reporting cadence (weekly digest target); first sprint date placeholder.

## 9. Intake adapters

All three intake modes normalize into the same object: a Desk project plus an execution brief. Nothing enters a lane's queue in any other shape.

Common normalization pipeline (every mode):
1. Receive or fetch the raw request. Store the raw payload unchanged in the install's intake log (repo path memory/muse/installs/<client_slug>/intake/<yyyy-mm-dd>-<short-id>.json) before any transformation.
2. Extract fields: title, requester, client, description (verbatim), priority signal, due signal, attachments or links, source mode, external id (for dedupe).
3. Dedupe: if an open Desk project already exists with the same external id (PM modes) or the same normalized title plus requester within 24 hours (direct and SURGE modes), attach the new payload as an update to that project instead of creating a duplicate.
4. Rewrite into an execution brief by the owning team per the execution brief standard: Objective; System of record; Current state to find and verify; Exact changes (numbered); Verification; Definition of done; Open questions (blocking only). The original description is never edited; the brief lives in the Desk brief field.
5. Create the Desk project via Lovable query_database: status New, assignee by lane routing (Maive for Muse lane, Marcus for Grok or Claude lane work that Marcus leads), priority mapped to P0 to P3, source set to the intake mode, links carrying the external reference.
6. Route and notify: post the internal notice to the ops channel; if the project is owned by a Grok or Claude lane, post the NEW PROJECT FOR GROK format notice to #ai-command where that protocol applies. Claim is by first response per the claim protocol.
7. Acknowledge to the requester in their own surface with the project reference and the expected first update. Acknowledgement contains no internal detail.

Adapter A: Direct to Maive.
- Source: the client messages Maive in their connected chat surface (Muse chat or an approved messaging connector).
- Mechanics: Maive (or the intake sweep pattern already in production for UpSurge: scheduled scan plus real time hook where the surface supports it) detects a work request, runs the common pipeline, and confirms back in the same thread.
- Specifics: requester identity comes from the authenticated surface, never from message text. Ambiguous messages (question vs request) are clarified with one question before a project is created.
- Failure handling: if the sweep misses a request, the hourly backstop scan catches it; the client visible effect is a later acknowledgement, never a lost request, because raw messages persist in the surface.

Adapter B: Client PM system.
- Source: the client's own project tool (for example a MAV style board, Asana, ClickUp, Monday, or a client CRM task list).
- Mechanics: two connection patterns, chosen per client and recorded in the manifest: (1) webhook push from the PM system to the install's intake webhook endpoint, verified by signing secret pointer; (2) scheduled poll of the PM system API or export for items assigned to the UpSurge assignee label, on a 15 minute cycle, watermark stored in the install state record.
- Specifics: external id from the PM system is the dedupe key and is stored in the Desk project links. Status flows back one way only where the agreement allows: Desk completion writes the PM item to its done state, and no other field of the PM item is ever edited (this mirrors the standing MAV hard rule: no description edits, completion only).
- Failure handling: webhook delivery failure retries per the sender's policy; the poll pattern is the automatic backstop for missed webhooks. Poll API 429 is a hard stop for that cycle. A PM item that disappears upstream is flagged in the ops channel, never silently closed.

Adapter C: SURGE form (Surge Command Desk).
- Source: the client submits through their Desk instance (request form in the app).
- Mechanics: the submission already lands as a Desk request row in New status with source = surge-form. The adapter's job is enrichment only: run brief rewriting (step 4), lane routing and assignee set, and the internal notices (step 6). No external fetch is needed.
- Specifics: the passcode gate is the authentication for this mode; requester name comes from the form field and is treated as unauthenticated text, so client facing sends still require the standing approval rules.
- Failure handling: a malformed submission (empty description, missing title) is held in New with a blocker note and one clarification request to the submitter; it is never discarded.

Definition of done for intake (all modes): a raw payload stored, a Desk project created or correctly deduped, a brief present in the brief field, an assignee set by routing, an acknowledgement sent in the source surface, and the intake log entry linked from the Desk project.

## 10. Idempotency and install state tracking

State machine (install level):
- initiated -> provisioning -> provisioned -> connecting -> connected -> seating -> seated -> seeding -> seeded -> qa_gate -> going_live -> live
- From any active state: -> paused_human (a named human action is required; the exact ask is stored on the record), -> failed_retryable (automatic retry scheduled), -> failed_terminal (operator decision required).
- From live: -> suspended (client or UpSurge action), -> closed (agreement ended; all objects archived, none deleted).
- qa_gate is a deliberate stop: go live requires the UpSurge approver's recorded approval on the install record. It is the single approval gate in the pipeline.

Per step tracking:
- Each stage is a list of steps. Each step record holds: step key, status (pending, running, done, skipped with reason, failed), attempt count, last attempt timestamp, idempotency key, produced object reference, last error (code and message).
- Idempotency key format: <install_id>:<stage>:<step>:<natural_key>. Before executing, the orchestrator looks up the key and the natural key in the target system. If the object exists and matches the spec, the step is marked done with the existing reference and no create is issued.
- Concurrency: one runner per install (lock keyed by install_id in the state store). A second runner exits immediately. Stage steps run sequentially unless a step is explicitly marked parallel safe (app connections in Stage 2 are parallel safe per app, never within one app).
- Resume: on any crash or restart, the runner reloads the state record and resumes at the first step not marked done. No stage restarts from zero.
- Audit: every state transition appends a line to the install log in the repo (timestamp in the install timezone, actor, from state, to state, reason). The log is append only.
- Client visible status: a simplified projection of the state machine (Stage name, percent of steps done, current client action needed if any). Internal error detail never projects to the client view.

Retry policy (default, per step): attempts at 0s, 60s, 300s, 1800s for transient errors (timeouts, 5xx, tunnel failures). Provider 429: stop that provider for the run and reschedule per provider guidance. Auth and schema errors: no automatic retry, straight to paused_human or failed_terminal with the exact error recorded. After the final retry, the step is failed, the stage stops, and the ops channel receives one alert with install_id, stage, step, and error. Alerts do not repeat for the same failure.

## 11. Automation today vs needs a small build

Automatable today with the current stack (verified in production use as of 2026-11-04):
- Desk reads and writes (project create, status moves, brief field, blocker and next_step) through Lovable query_database, including INSERT and UPDATE.
- Repo memory structure creation, manifest writes, and install log appends through the GitHub connector (push_files for multi file commits; verify each push landed by reading back, because pushes can time out client side and still land).
- Slack channel messages, intake notices, and completion notices through the Slack connector. Note: the Slack connector cannot upload or read files; file delivery uses hosted download links.
- Connector authorization and verification for the connected set: Gmail, Google Calendar, Google Drive, Google Docs, Google Sheets, Slack, HighLevel (with the known limit that some locations need the browser for workflow internals because the workflow API is not enabled), Lovable, Vercel, GitHub, Meta Ads (reads gated on the advertiser granting professional consent; that tap is the client's or Austin's, not automatable).
- MAV style PM intake where the PM system is MAV: assignment detection from the fulfillment channel pattern plus the MAV helper for reads and completion only.
- Scheduled polling, sweeps, and watchers through Muse cron and hooks (the intake sweep and the waiting on Austin watcher are working patterns).
- Knowledge ingest drafting from Drive, Docs, and public web pages, and brief rewriting, as agent work under the orchestrator.

Needs a small build (none of these exist yet):
1. Install orchestrator service: the state store, step runner, locking, retry engine, and manifest writer as one small service (fits the existing app pattern: a worker plus a database table set). Today the steps can be run by an agent following this spec; that is supervised automation, not unattended automation.
2. Desk per client provisioning: a clone or template path for a client Desk instance, including passcode environment setup. Lovable has no verified project clone or GitHub sync API in our current toolset, so today this is a manual Lovable UI step or a shared Desk with per client rows. The spec assumes per client rows in one Desk until the clone path is built.
3. Roster and heartbeat data model: a roster table and a client_summary field on request_updates in the Desk schema, plus the heartbeat page itself in the Desk app (built GitHub first through the synced repo, per the Lovable GitHub first rule).
4. Intake webhook receiver: a small endpoint service that accepts PM system webhooks, verifies signatures, stores raw payloads, and runs the normalization pipeline. The SURGE form and direct modes work today without it; third party PM webhooks do not.
5. Cross platform seat bootstrap for Claude and Grok: there is no verified API in our current stack to push instructions or memory into a client owned Claude or Grok account programmatically. Today delivery is a guided manual paste plus the verification drill. A small build here is part product (a bootstrap package generator) and part platform limitation that may not fully close.
6. Connect wizard UI: a single client facing page that sequences connector authorizations and secure key captures with live checklist state. Today the flow runs through Maive in chat, one connector at a time.
7. Knowledge ingest connectors for non Google stacks (for example OneDrive or SharePoint exports): no connector exists today; ingest is manual export until one is built.

## 12. Go live (Stage 5 detail)

Trigger: Install state = seeded and the QA gate approval is recorded.

Automated actions, in order:
1. Final verification sweep: re-run one read check per required connector, confirm all three lanes answer a ping task, confirm the Desk test project pattern is Done, confirm the heartbeat page renders with live roster and project data.
2. Flip the install to live in the state record and the manifest; enable the intake adapters chosen in the agreement (webhook active, poll schedule active, SURGE form open, direct surface listening).
3. Publish the heartbeat page link to the sponsor with a short orientation message: how to submit work, what the team page shows, when the weekly digest arrives.
4. Create the first real project from the sponsor's first request through the normal intake pipeline (not a synthetic task), and staff it the same day per the same day completion directive.
5. Schedule the standing loops for the install: intake backstop sweep, waiting on client watcher equivalent for this Desk, weekly digest generation, and a monthly Pack update check (offer the new Team Pack version, apply on approval, re-run lane drills).

What the client sees: The live heartbeat page (org chart across the three lanes, every team member with role and strengths, live activity pulse from real Desk data, recent completed work), the orientation message, and their first project moving.

Human touchpoints (named):
- UpSurge Approver (Austin or his delegate): records the QA gate approval. This is the one approval that is never automated.
- Client Sponsor: submits the first real request. No other action required.

Failure handling: any failed check in the final sweep returns the install to the responsible stage with the failing step identified; go live does not proceed on partial checks. If the heartbeat page fails to render with live data, go live is blocked, because the page is part of the product promise, not decoration.

Definition of done: Install state = live; all intake adapters enabled and tested with one real or sponsor approved test submission each; heartbeat page live and verified against Desk data; standing loops scheduled; manifest final version committed; completion notice posted to #ai-command with install_id, client_slug, Pack version, and go live date 2026-11-04 format (absolute date recorded at actual go live).

## 13. Rollback and suspension

- Rollback of a stage: mark produced objects archived or superseded in place (repo files move to an archive path inside the client folder, Desk rows move to a closed status, channels are archived), reset the stage steps to pending, and set the install state back to the prior stage. Nothing is deleted, so a rollback is itself auditable.
- Suspension from live: intake adapters stop creating new projects (inbound payloads are still stored and acknowledged as received while suspended), lanes finish or hand back in flight work per the approver's instruction, and the heartbeat page shows the suspended state honestly.
- Data on close: the Client layer is exportable to the client on request (it is their facts). The Craft layer and internal logs are UpSurge property and are not exported.
