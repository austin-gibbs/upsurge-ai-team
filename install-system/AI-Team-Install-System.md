# The AI Team Install System

Version 1.0, 2026-11-04. Owner: Maive (Muse lane), for UpSurge Pros.
Status: designed and documented to buildable standard; pilot install ready to run concierge-style on this system while the two remaining code builds (install orchestrator, heartbeat page) are completed.

## What the client buys

A working AI organization, installed into their business: the Surge Command app with their full team visible on a live heartbeat page, one person to talk to (the team lead), and finished work delivered the way an established operations firm delivers it. The client sees capability, status, and results. They never see internal process, tooling, or how delegation works.

## The architecture in one page

- **One front door.** The client submits requests one way and talks to one lead. The lead routes each request to the lane that fits it: Muse, Grok, or Claude. The client never chooses a lane and never manages a specialist.
- **Three lanes, one team.** The same roster of specialists works across the three platforms, routed by comparative advantage (routing table in the Team Pack): Muse for connected apps, memory, and background work; Claude for sustained reasoning, long documents, and careful builds; Grok for speed, volume, and live signal. A lane outage reroutes, it never stalls work.
- **Two memory layers.** The Craft layer (Team Pack: roster, routing rules, brief standard, QA checklists, house style) is UpSurge intellectual property, versioned and pushed to every install like a software update. The Client layer (their facts, brand, people, decisions) is created at install, lives only in their install, and never moves. Generalized lessons may graduate from a client install into the Craft layer only after the sanitization checklist in the Team Pack, approved by Maive.
- **The Desk is the board of record.** Every request becomes a Desk project with an execution brief written by the team, a lane, a specialist, and a client-facing summary. Internal notes and client summaries are separate fields by design, so nothing internal can render on a client surface.

## The install: five stages

Full detail: drafts/install-pipeline.md. Summary:

1. **Provision.** Triggered by a signed agreement. Creates the Desk workspace, client memory structure, roster, passcode, ops channel, and the install's own tracking record. Client sees: nothing yet. Human touchpoints: none.
2. **Connect.** The client connects their tools one tap at a time from a guided checklist (client pack, section 3). They sign in on each tool's own page; the team never sees or stores a password; access is revocable by the client at any time. Human touchpoints: the client tapping sign-ins, about fifteen minutes total.
3. **Seat the platforms.** Each of the client's AI platform accounts (Muse, Grok, Claude) receives the Team Pack bootstrap and the pointer to client memory, then passes a verification drill (each lane proves it can read the roster, the routing rules, and the client memory before it counts as seated). Human touchpoint: a guided paste per platform where no API exists, verified by drill.
4. **Seed the knowledge.** Automated ingest of the client's website, brand assets, documents, and CRM into client memory v1, every fact carrying its source, unverified facts marked. One 30 minute call fills the gaps. Human touchpoints: that call, plus the team's QA pass over the seeded memory. This stage is deliberately not fully automated: a wrong fact in memory compounds into every deliverable.
5. **Go live.** The heartbeat page turns on, the welcome and go-live messages send (client pack, sections 1 and 5), and the client's first real request is run end to end the same day. One deliberate human gate sits here: QA approval of the assembled install before go live. It is the only approval gate in the pipeline.

Installs run on a state machine (initiated, provisioning, connecting, seating, seeding, qa_review, live, plus paused and failed states) with idempotent steps, a single runner lock per install, resume from the first unfinished step, and an append-only audit log. Full spec in the pipeline document.

## The client experience

Full text: drafts/client-onboarding-pack.md. The pack a client receives covers: welcome, the five stages in plain language with the tiny ask at each, the connect checklist and its security story, how to submit a request in any of the three intake modes with examples, what happens after they submit, the first week rhythm (one minute daily digest, weekly review, team page anytime), escalation to a human at UpSurge, and an FAQ that answers the data isolation question in plain words.

Intake modes are the only per-client variable: submit in the Surge Command app, submit in their own project management tool (connected by webhook or poll, with completion written back, nothing else edited there), or message the team lead directly. All three normalize through one pipeline: raw request stored, dedupe, brief rewrite, Desk project created, lane routed, client acknowledged.

## The heartbeat page

Full build spec: drafts/heartbeat-page-spec.md. A /team page inside the client's Desk, behind the same passcode: masthead with a real live clock, a pulse strip (in flight now, completed today, average turnaround, this week), three lane columns with the leader pinned and every specialist card below, a recent wins feed, and the board summary. Binding honesty rules: member status is computed from real open projects, never stored or faked; wins come only from completed projects that carry a client summary; the page never reads internal note, brief, or blocker fields. Schema additions are written SQL-ready (lane, specialist, completed_at, client visibility and summary fields, a team_roster table, a workspace_config row), realtime runs on Supabase subscriptions with a polling fallback, and the spec includes the per-client clone checklist and a 12 point QA acceptance list including a leak test.

## The Team Pack and the roster

Full detail: drafts/team-pack-and-roster.md. Team Pack v1 ships ten components: roster and lane map, routing rules, the execution brief standard, house style, QA checklists for six deliverable types (voice agent, CRM workflow, landing page, video, report, ad campaign), escalation rules (six triggers only; routine permission asks count as a quality defect), the claim protocol, the client memory template, reporting templates, and the heartbeat data contract. Versioning is semantic; pushes never touch Client layer content; in-flight projects finish on the version they started on except compliance fixes.

The roster today: 21 named specialists plus the two lane leaders, mapped in a coverage matrix. Six specialists are specced to build next, each with the skill file scope and the measurable quality bar that must be evidenced before they count as real: Vega (video editing), Pax (paid media), Bram (data and BI), Bea (bookkeeping ops), Sable (security and compliance review), Ivo (integrations). Unproven specialists are never shown on a client roster.

## What is automated today, and the three honest gaps

Automated today on the current stack: Desk data operations through the Lovable database tool, brain reads and writes through GitHub, Slack intake and notifications, and every Muse connector flow used in the stages above. The pipeline spec's section 11 has the full split. Three gaps stand between this system and hands-off automation:

1. **The install orchestrator.** Every step is individually automatable today; the small service that runs them unattended as one resumable pipeline (state store, step runner, locking, retries) is not built yet. Until it is, installs run agent-executed under this spec: supervised automation, honestly labeled.
2. **Per-client Desk provisioning.** Lovable exposes no verified project clone in our toolset and per-instance passcode setup is manual. The spec defaults to per-client workspaces in one Desk until a clone path is built.
3. **Claude and Grok seat bootstrap.** No verified API pushes the Team Pack into a client-owned Claude or Grok account. The durable control is guided paste plus the verification drill; this may remain partly manual by platform design.

## Build order from here

1. Run the pilot client through this system concierge-style, timing every stage. The install itself is a Desk project, and its completion becomes the first win on the client's heartbeat page.
2. Build the heartbeat page into the Desk template (GitHub first, per house rule), including the schema migration and roster seed.
3. Build the install orchestrator against the pipeline spec.
4. Recruit the six gap specialists against real client demand, in the order the pilot's work demands them.

## Decisions for Austin

- Seat model for the pilot: client-owned platform accounts with an UpSurge admin seat (recommended in the advice of 2026-11-04), or UpSurge-managed seats.
- The pilot client's intake mode: Surge Command app, their own PM tool, or direct to the lead.
- Ratify the operating charter as the Team Pack constitution, or send edits.
