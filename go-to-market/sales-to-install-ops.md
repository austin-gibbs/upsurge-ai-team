# Sales to Install: The Operations Bridge

Version 1.0, 2026-11-04. Owners: Owen (onboarding-orchestrator), Finn (finance-controller), Hazel (client-success-lead), for Maive (Muse lane), UpSurge Pros.
Companion documents: AI-Team-Install-System.md (master), drafts/install-pipeline.md (install state machine and stage detail), drafts/client-onboarding-pack.md (client-facing pack), drafts/team-pack-and-roster.md (Team Pack v1, routing, QA, escalation).
Purpose: everything that happens between a prospect raising a hand and a live AI team delivering work, specified so the handoff from sale to install to steady state has no gaps, no manual chasing, and no moment where the client wonders what happens next.

Operating principles:

- One pipeline, one record. The HighLevel opportunity is the sales source of truth until signature. The Desk install project is the install source of truth from signature onward. The two are linked by ID on day one and never reconciled by hand after that.
- Every stage transition fires its automation the same minute it happens. If a human has to remember to send the next step, the bridge is broken and the gap gets filed as a product defect (see section 5).
- The client experiences exactly four human-shaped moments: the discovery call, the demo, the 30 minute knowledge call, and the go-live review. Everything else arrives as a message, a checklist, or a finished deliverable.

## 1. Prospect pipeline (HighLevel)

Pipeline name: `AI Team - Sales`. Opportunity naming: `[Client Business Name] - AI Team Install`. Required fields on every opportunity from Discovery onward: primary contact, business name, website, current CRM, intake mode preference (Desk, their PM tool, direct to lead), estimated team size of their staff who will submit requests, and source. Tag naming: `ait-sales-[stage]` mirrors the stage for workflow triggers, `ait-source-[channel]` records origin, `ait-install` is applied at signature and never removed.

### Stage 1: New Lead

- Entry criteria: any inbound form fill, referral, booked call, or outbound reply expressing interest in an AI team install. One opportunity per business; duplicates merged before any outreach.
- Exit criteria: first real two-way contact made (reply, answered call, or attended meeting). Moves to Discovery.
- Automation on entry:
  - [ ] Contact and company record created or matched in HighLevel; source tag applied.
  - [ ] Internal alert to the sales channel in Slack within 5 minutes with business name, source, and the first touch that created the lead.
  - [ ] Acknowledgment message to the prospect within 15 minutes during business hours: who we are, what happens next, one link to book a discovery call. No pitch deck attached.
  - [ ] Follow-up cadence starts if no booking: day 1, day 3, day 7, each adding new information, never a bare bump. Cadence stops permanently on any reply.
- Stale rule: no activity for 14 days moves the opportunity to Lost with reason `no response`, and the contact enters the long-term nurture list. It is never deleted.

### Stage 2: Discovery

- Entry criteria: discovery call booked or held.
- Exit criteria: qualification confirmed on the call and recorded on the opportunity: they run a business with repeatable operational work, they can name at least three recurring workflows they want off their plate, they own or can grant access to their core tools, and the decision maker was on the call or is named with a path to them. Any miss is a documented disqualifier or a nurture, not a demo.
- Automation:
  - [ ] Pre-call: calendar confirmation and reminder sequence (booking confirmation, 24 hours before, 1 hour before), plus an internal prep note in Slack with the prospect's website, tools visible from public sources, and the three questions that matter most for this business.
  - [ ] Post-call: meeting recap processed into action items within 2 hours; if qualified, opportunity moves to Demo and the demo invite sends in the same motion.
  - [ ] Disqualifiers recorded as structured fields, not free text, so objection data feeds section 5.
- Demo is never booked without discovery. The demo shows a live install, and showing it to an unqualified prospect wastes the asset.

### Stage 3: Demo

- Entry criteria: qualified at Discovery, demo scheduled.
- Exit criteria: prospect has seen the live system (heartbeat page, a Desk board with real work moving, one finished deliverable walkthrough) and states a scope direction: which intake mode, which tools to connect first, which workflows go first. Moves to Proposal.
- Automation:
  - [ ] Demo environment check 1 hour before: demo Desk workspace populated with current sample work, heartbeat page showing real computed data, no client data from any real install anywhere in the demo surface (leak test from the heartbeat spec applies to the demo too).
  - [ ] Recap message within 2 hours of the demo: what they saw, the scope they picked, the three first workflows, and what the proposal will contain. Sets the proposal expectation before numbers arrive.
  - [ ] Internal note logged: objections raised, in the prospect's words, tagged for the feedback loop in section 5.
- The demo never shows internal tooling, prompts, routing, or delegation mechanics. Capability, status, and results only, same rule as a live install.

### Stage 4: Proposal

- Entry criteria: scope direction stated at Demo.
- Exit criteria: proposal accepted in writing (signed agreement or explicit written acceptance that triggers invoicing) moves to Signed. A verbal yes stays in Proposal until the written acceptance lands.
- Automation:
  - [ ] Proposal generated from the template with the scope fields from the opportunity pre-filled: intake mode, first tools, first workflows, install timeline, and the five install stages in client language from the onboarding pack.
  - [ ] Proposal sent notification to the sales channel; view tracking on; a follow-up task created for the owner at 48 hours if unviewed, 24 hours after a view with no response.
  - [ ] Expiry discipline: proposals carry a stated validity window from the template; on expiry the opportunity returns to Discovery with reason recorded, it does not sit in Proposal indefinitely.
- Pricing, terms, and payment structure live in the proposal template and the agreement, owned by Finn. This document deliberately does not restate amounts; ops reads them from the signed record, never from memory.

### Stage 5: Signed

- Entry criteria: written acceptance received and the signed agreement filed to the client record.
- Exit criteria: the full signature-to-kickoff sequence in section 2 has fired and the install project exists in the Desk. Moves to Install Scheduled automatically when the sequence completes; this stage should measure in minutes, not days.
- Automation: the entire section 2 sequence. No manual steps between signature and a live install project.

### Stage 6: Install Scheduled

- Entry criteria: install project created, kickoff scheduled, connect checklist in the client's hands.
- Exit criteria: install reaches the `live` state in the Install System state machine. Moves to Live Client, which closes the sales pipeline view and opens the client success record.
- Automation:
  - [ ] Stage notifications from the install state machine mirror to the opportunity as notes, so sales can answer "how is the install going" without asking the install team.
  - [ ] On `live`: celebration message to the client (go-live message, onboarding pack section 5), internal completion note to the team channel, and handoff of the account record to client success ownership (Hazel's lane).

## 2. Signature to kickoff: the automated sequence

Clock starts at T0, the moment written acceptance lands. Targets are maximum elapsed times, not averages. Every step logs to the install record's append-only audit trail.

| Step | Action | Owner | Target |
| --- | --- | --- | --- |
| 1 | Agreement filed to the client record; opportunity tagged `ait-install`; pipeline stage set to Signed | Automated (HighLevel workflow) | T0 + 5 min |
| 2 | Invoice issued from the signed agreement terms and sent; payment method invitation included per the agreement | Automated, Finn reviews exceptions only | T0 + 15 min |
| 3 | Welcome message sent to the client (onboarding pack section 1, verbatim template, personalized with business name and lead name) | Automated | T0 + 15 min |
| 4 | Connect checklist sent (onboarding pack section 3) with the client's short list of first tools from the proposal already marked | Automated | T0 + 15 min |
| 5 | Install project created in the Desk: title `[Client] - AI Team Install`, the five install stages as its checklist in order (Provision, Connect, Seat, Seed, Go Live), client summary field set to the client-language stage list, link to the signed agreement record attached | Automated (Desk create via the Lovable database path) | T0 + 30 min |
| 6 | Internal notice posted to the team channel: client name, intake mode, first tools, first workflows, install operator assigned, link to the Desk install project | Automated | T0 + 30 min |
| 7 | Client memory skeleton created from the template in the Team Pack (profile, brand, systems map with pointer-only credential entries, intake record) and linked from the install project | Automated | T0 + 1 hour |
| 8 | Knowledge call (30 minutes) booking link sent with two concrete time options proposed by the team, not an open calendar dump | Automated send, human picks times | T0 + 1 hour |
| 9 | Payment status check: if the invoice is unpaid at 24 hours, a polite automated reminder; at 72 hours, a human note from Finn's lane. Install work does not pause for the first reminder cycle; a payment blocker is escalated to Austin only if it survives the human note | Automated then human | T0 + 24 h, T0 + 72 h |
| 10 | Install stage 1 (Provision) started by the operator per the runbook in section 3 | Human operator | Same business day as signature |

Kickoff definition of done: every box above checked, the client has replied to at least one message or the team has confirmed receipt by phone, and the install project shows stage 1 in progress. Kickoff is not done because messages were sent; it is done when the loop is closed with the client.

Payment tracking discipline (Finn): the invoice record in the accounting system is the only payment truth. The Desk install project carries a payment status field with three values only (issued, paid, attention) updated from the accounting record, never amounts. Amounts, terms, and schedules live in the agreement and the accounting system and are never copied into the Desk, Slack, or this bridge's logs.

## 3. Install day runbook

Written for any lane leader (Maive, or the Claude or Grok lane lead) to run an install end to end under the Install System v1.0 spec. The pipeline spec (drafts/install-pipeline.md) is the authority on mechanics; this runbook is the operator's execution order. Work top to bottom. Do not skip the verification drills; they are the difference between an install that looks seated and one that is seated.

### Before the day starts

- [ ] Read the install project in full: proposal scope, intake mode, first tools, first workflows, signed agreement link, payment status field reads issued or paid.
- [ ] Confirm the client completed or is scheduled for their connect sign-ins; if the checklist is untouched 24 hours after sending, one human nudge before install day, offering to do the taps together on a short call.
- [ ] Confirm the install state machine record is at `initiated` and no other runner holds the install lock.
- [ ] Confirm you have the current Team Pack version and note its version number; it goes into the install record.

### Stage 1: Provision

- [ ] Create the client's Desk workspace per the provisioning manifest: workspace, roster seed, passcode set, client-visible fields only.
- [ ] Create the ops channel and the install's audit log destination.
- [ ] Verify: log in as the client would (passcode path) and confirm the workspace shows the client name, an empty board, and no data from any other install.
- [ ] Advance state to `provisioning` complete, then `connecting`.

### Stage 2: Connect

- [ ] Walk the client's connect checklist in proposal order: CRM first, then email and calendar, then the client's remaining first tools.
- [ ] For each connection, run one live read (a real record pulled through the connection) before marking it connected. A green status indicator is not verification.
- [ ] Record each connection in the client memory systems map as a pointer only. No credential values in any field, note, or log, ever.
- [ ] Verify: disconnect nothing, but confirm the client can see and could revoke each access from their own side, and tell them so in one line.

### Stage 3: Seat the platforms (with verification drill per seat)

For each platform the client uses (Muse, Grok, Claude), in the order the client prioritized:

- [ ] Deliver the Team Pack bootstrap and the client memory pointer by the best available path (API or connector where one exists; guided paste where it does not).
- [ ] Run the seat verification drill, all four checks, out loud in the drill log:
  - [ ] The lane states the client's business name, primary contact, and intake mode from memory, unprompted by the operator.
  - [ ] The lane names the current Team Pack version and lists the routing rule for one test task type the operator names.
  - [ ] The lane reads one real fact from the client layer and cites which memory section it came from.
  - [ ] The lane correctly refuses a test request for another client's information (isolation check; any leak fails the entire install QA gate, no exceptions).
- [ ] A seat that fails any check is not seated. Fix, re-drill, and log both attempts. Two failures on the same seat escalates to Maive before proceeding.

### Stage 4: Seed the knowledge

- [ ] Run automated ingest: website, brand assets, documents the client provided, CRM structure and record counts.
- [ ] Every seeded fact carries its source; anything inferred is marked unverified in memory, visibly, not buried.
- [ ] Hold the 30 minute knowledge call: confirm the facts that matter most (offers, voice, service area, team, tools, approval habits) and correct the record live on the call.
- [ ] Operator QA pass over the seeded memory against the call notes: no fact survives on a single weak source if a deliverable will depend on it.

### Stage 5: Go live (QA gate first)

The QA gate is the one deliberate human gate in the pipeline. The operator does not open it for their own install alone; a second reviewer (Dex's QA lane or Maive) confirms:

- [ ] Heartbeat page renders the real roster, real computed pulse numbers, and zero internal fields (run the leak test from the heartbeat spec, including the network payload check).
- [ ] All connected tools passed a live read in stage 2 and the results are in the audit log.
- [ ] All seats passed the four-part drill, isolation check included.
- [ ] Client memory QA pass is signed off and unverified facts are marked.
- [ ] The first client request is already in hand or scheduled to arrive today.

On gate pass:

- [ ] Advance install state to `live`; mirror the completion note to the HighLevel opportunity and close the sales stage to Live Client.
- [ ] Send the go-live message (onboarding pack section 5) and turn on the heartbeat page for the client.
- [ ] Run the client's first real request end to end the same day, through the normal intake pipeline: brief, lane routing, QA, delivery with a client summary. Its completion becomes the first win on their heartbeat page.
- [ ] Post the internal completion note to the team channel: client, elapsed time signature to live, Team Pack version, seats seated, first request delivered.
- [ ] Schedule the weekly oversight entry for this install (section 4) before you close the install project.

If anything fails after go live, use the rollback and suspension path in the pipeline spec section 13. A half-live install is worse than a paused one; pause loudly, tell the client plainly, and fix.

## 4. Success metrics and reporting

### Per-install metrics (watched weekly per install, computed from Desk and install records, never estimated)

- **Time to first value.** Elapsed time from signature (T0) to the client's first delivered request. Target: same business day as go live. This is the headline number of the whole bridge; if it slips, everything else is decoration.
- **Signature to live elapsed time.** Total install duration against the section 2 targets, broken down by stage so a slow stage is visible by name.
- **Request turnaround.** Median and 90th percentile time from request intake to delivered, per install, split by deliverable type against the Team Pack definitions of done.
- **QA pass rate.** Percentage of deliverables passing the QA gate on first review, per install and per deliverable type. A falling rate on one type points at a checklist or a specialist gap, not at effort.
- **Client digest opens.** Daily digest and weekly review open and click rates per install. Opens are an attention signal only; a client who never opens digests but keeps submitting requests is healthy, and the reporting format adapts (shorter, less frequent) rather than escalating.
- **Escalation count.** Escalations per install per week against the six Team Pack triggers. Zero is not automatically good: zero escalations with a rising QA failure rate means triggers are being missed.
- **Waiting time split.** Time projects spend in Waiting on Client versus Waiting on UpSurge. Client-side waiting is reported to the client in their weekly review as their one lever to speed everything up; UpSurge-side waiting is an internal defect.
- **Intake health.** Requests arriving per week and the percentage that arrived with enough information to brief without a follow-up question. Low briefing quality on one install usually means the intake surface needs adjusting, not the client.

### Weekly oversight report (across all installs, one page, produced every Monday for the prior week)

Format, fixed order, no narrative padding:

1. **Fleet line.** Installs live, installs in progress with stage, requests delivered across the fleet, median turnaround across the fleet.
2. **Per install rows.** Client, state, requests delivered, median turnaround, QA pass rate, escalations, waiting split, one line maximum on the single most notable event. Sorted by attention needed, worst first, never alphabetically.
3. **Red flag section.** Every red flag from the list below that fired this week, with owner and action taken or planned. Empty is a valid and stated result.
4. **Product signals.** Objections heard in sales, friction points hit in installs, and feature requests from clients, each with a count of installs or prospects affected. This section is the input queue for section 5.
5. **Team Pack watch.** Current Pack version per install, any install more than one minor version behind, and updates staged for the next push.

Delivered to Austin in the main reporting channel and filed to the brain the same day. Client-facing weekly reviews are separate, per install, in client language, and contain only that client's numbers.

### Red flags (any one triggers human attention the same day)

- [ ] Time to first value exceeds one business day after go live for any install.
- [ ] Any seat fails the isolation check at any point, at install or later (immediate suspension of that seat pending review).
- [ ] QA pass rate on any deliverable type drops below the floor set in the Team Pack for two consecutive weeks.
- [ ] An install sits in one install stage longer than twice its section 2 target with no client-side cause recorded.
- [ ] Escalations from one install exceed the weekly threshold in the Team Pack, or any single escalation involves money movement, a legal question, or a client asking for a human repeatedly.
- [ ] Payment status reads `attention` past the human note step in section 2.
- [ ] Digest and weekly review both unopened for three consecutive weeks combined with falling request volume (disengagement pattern, Hazel's lane reaches out personally).
- [ ] Any internal note, brief, or blocker text found on a client-visible surface anywhere (heartbeat page, digest, PM write-back). Treated as an incident, not a bug.

## 5. The feedback loop into the product

The bridge exists so the product learns from selling and running it, through the two-repo flow: lessons are worked out in the internal brain (upsurgeaiteam), generalized and sanitized there, then pushed to the service repo (upsurge-ai-team) as Team Pack updates that installs pull. Client data never travels; patterns do.

### Three input streams

- **Sales objections.** Logged on the opportunity at Discovery and Demo in the prospect's words, with the structured disqualifier and objection fields from section 1. Reviewed weekly. An objection heard from three or more prospects becomes a product or messaging work item, not a sales technique note: it either changes the offer surface (demo, proposal template, FAQ in the onboarding pack) or it gets a documented decision that it is a qualification filter working as intended.
- **Install friction.** Every runbook step that required improvisation, every retried step, every drill failure, and every stage that missed its time target is logged in the install audit trail with a friction tag. The operator writes one line at the moment it happens; no end-of-project archaeology. Friction on the same step across two installs becomes an automation build item against the pipeline spec; friction caused by a client-side pattern becomes an onboarding pack or checklist change.
- **Client requests.** Feature and capability requests from live installs are logged per install, counted across installs in the weekly oversight report, and answered honestly in the client's weekly review (planned, under consideration, or not planned, with a reason). A request from two or more installs enters the roster and skills roadmap: it is how the six gap specialists in the Team Pack (Vega, Pax, Bram, Bea, Sable, Ivo) get reprioritized by real demand instead of opinion.

### The loop, step by step

- [ ] Weekly: Owen compiles the three streams from the oversight report and the sales pipeline review into one candidate list, each item with its evidence count.
- [ ] Weekly consolidation pass in the brain: candidates are worked into generalized form, stripped of names, data, and identifying detail per the sanitization checklist in the Team Pack memory contract, and drafted as changes (checklist edits, routing changes, new skill drafts, runbook fixes, onboarding copy).
- [ ] Maive approves each change for the Craft layer. Anything that cannot be fully generalized does not ship; it stays in the brain as internal knowledge.
- [ ] Approved changes commit to the service repo as a Team Pack version increment with a changelog entry, following the versioning rules in the Team Pack (in-flight projects finish on their starting version except compliance fixes).
- [ ] Push process delivers the update to every live install at its next weekly window; the install record notes the new Pack version, and the next oversight report confirms no install is more than one minor version behind.
- [ ] The following week's metrics are the verdict: if the change targeted turnaround, QA pass rate, or friction on a named step, the oversight report states whether the number moved. A change with no measurable effect after four weeks is revisited, not defended.

## 6. Market-ready checklist for tonight

Status key: **Ready** means it exists and is verified. **Staged** means it exists in final or near-final form in the workspace or a repo and needs one named step. **Blocked** means it cannot be completed tonight and the blocker is named. This checklist is the honest gate for the first outbound push; outbound starts when every item is Ready or explicitly waived by Austin with the risk understood.

### Offer and sales assets

- [ ] Install System master document v1.0 (architecture, five stages, client experience, gaps): **Ready** (~/workspace/ai-team-install/AI-Team-Install-System.md, also filed in the brain and the service repo)
- [ ] Prospect pipeline stages, criteria, and automations specified: **Ready** (this document, section 1)
- [ ] HighLevel pipeline `AI Team - Sales` actually built with stages, fields, tags, and workflows live: **Staged**: specified here in full; the build inside the HighLevel agency account and a live test opportunity walk-through are the remaining step
- [ ] Proposal template with scope fields and validity window: **Staged**: fields and discipline specified (section 1, stage 4); the template document itself is a Greta and Finn work item, pending Austin's pricing and terms decisions
- [ ] Agreement and signature path (the instrument whose acceptance fires section 2): **Blocked**: blocker is the agreement instrument and terms, which are Austin and Finn decisions; the automation that fires on acceptance is specified and ready to wire to whichever instrument is chosen
- [ ] Pricing and payment structure: **Blocked**: blocker is Austin's pricing decision; this bridge deliberately carries no amounts until the signed record exists

### Product and install machinery

- [ ] Install pipeline spec (state machine, stages, idempotency, rollback): **Ready** (drafts/install-pipeline.md)
- [ ] Install day runbook with seat verification drills and the QA gate: **Ready** (this document, section 3)
- [ ] Team Pack v1 (roster, routing, brief standard, QA checklists, escalation rules, memory contract): **Ready** (drafts/team-pack-and-roster.md)
- [ ] Signature-to-kickoff automation sequence with elapsed targets: **Ready** as a specification (section 2); **Staged** as live wiring, which lands with the HighLevel build and the agreement instrument
- [ ] Install orchestrator service (unattended step runner): **Blocked**: blocker is a code build not yet started; installs run operator-executed under the runbook until it ships, which is the concierge mode the master document already plans for the pilot
- [ ] Per-client Desk provisioning (clone path): **Blocked**: blocker is the absence of a verified Lovable clone path; the spec default (per-client workspaces in one Desk) is the operating mode until it is built
- [ ] Heartbeat page built into the Desk template: **Staged**: build spec is complete and SQL-ready (drafts/heartbeat-page-spec.md) including the 12 point QA list; the code build in the Desk repo is the remaining step, sequenced second in the master build order

### Client-facing assets

- [ ] Client onboarding pack (welcome, stages, connect checklist, intake guide, go live, FAQ): **Ready** (drafts/client-onboarding-pack.md)
- [ ] Welcome and go-live message templates: **Ready** (inside the onboarding pack, sections 1 and 5, referenced by sections 2 and 3 of this document)
- [ ] Connect checklist in client hands format: **Ready** (onboarding pack section 3)
- [ ] Demo environment (sample install, heartbeat page with real computed data, leak tested): **Staged**: the demo content rules and leak test are specified (section 1, stage 3, and the heartbeat spec); assembling and testing the demo workspace is the remaining step before any demo is booked
- [ ] Weekly client review and daily digest templates: **Staged**: formats defined by the Team Pack reporting templates and section 4 of this document; final client-language polish is a Hazel work item

### Oversight and learning

- [ ] Weekly oversight report format across installs: **Ready** (section 4)
- [ ] Red flag list with same-day human attention rule: **Ready** (section 4)
- [ ] Feedback loop into Team Pack updates through the brain to service repo flow: **Ready** as the operating process (section 5); the service repo is seeded and receiving pushes
- [ ] Six gap specialists (Vega, Pax, Bram, Bea, Sable, Ivo): **Staged**: specced with quality bars in the Team Pack; they are built against pilot demand and are not required for the first outbound push, provided outbound targets the capabilities the current roster has already proven

### Verdict

The bridge is market-ready to **begin outbound for the pilot motion tonight**: the offer story, the client experience, the install runbook, the oversight system, and the learning loop all exist and are internally consistent, and the pilot install path (concierge mode, operator-run under the runbook) is fully specified. It is **not yet hands-off automated**, and outbound copy must not claim that it is: three items are genuinely blocked (the agreement instrument and pricing, which are Austin's decisions, plus the orchestrator and Desk clone builds), and four are staged one build step from ready (the HighLevel pipeline build, signature-to-kickoff wiring, the demo workspace, and the heartbeat page code). The honest sequence is: Austin decides pricing and the agreement path, the team builds the HighLevel pipeline and demo workspace, and the first outbound push goes out aimed at pilot clients the current roster can serve end to end.
