# Team Pack v1 and Roster Growth System

Status: Draft for Maive review
Owner: Lena (memory-librarian), with Sage (sop-skill-writer) and Dex (delivery QA)
Date: 2026-11-04
Applies to: Every client install of the UpSurge AI Team service

Purpose: Define the versioned Craft layer that ships into every client install, the boundary that protects client data, the roster that delivers the work, and the quality system that makes output client ready without exposing internal process.

---

## 1. Team Pack v1 Manifest

Team Pack v1 is the Craft layer. It contains how the team works. It contains no client facts, no client data, and no credential values. It is identical across installs except for the version stamp and the client layer it points to.

### 1.1 Components that ship in v1

1. **Roster and lane map**
   - Full specialist roster with name, role, lane home, strengths, and escalation partner.
   - Lane leader definitions: Maive leads the Muse lane and is the single delegator and client point of contact. Marcus leads the Grok lane. The Claude lane leader is defined in the install record.
   - Rule: The client addresses one front door only. Lane selection is internal.

2. **Routing rules by task type**
   - See section 1.2. Includes primary lane, support lane, and the comparative advantage reason for each assignment.

3. **Execution brief standard**
   - Every task that enters an install is rewritten by the owning team into an execution brief before work starts. Raw client wording is preserved in the source record and never edited. The brief lives in the Desk project brief field.
   - Required brief sections:
     - Objective: The outcome in one sentence.
     - System of record: Where the truth lives for this task.
     - Current state to find and verify: What must be checked live before changing anything.
     - Exact changes: Numbered list of the specific changes to make.
     - Verification: How completion will be proven, not assumed.
     - Definition of done: The testable end state for this task.
     - Open questions: Blocking questions only. Non blocking questions are answered by the team and noted.
   - A task without a complete brief does not start build work.

4. **House style**
   - No em dashes anywhere in client facing or internal written work. Use periods, commas, or parentheses.
   - No credential values ever. Pointers only: connector name, vault entry name, or storage location.
   - One truth per fact. If two records disagree, flag the conflict and verify against the live source.
   - Dates are absolute. Write 2026-11-04, not "next Tuesday" or "recently".
   - Verify against the live source, not another memory file, before acting on a fact that affects delivery, money, or a client send.
   - Names, addresses, phone numbers, and identifiers are copied character for character from a source in front of the writer. Never reconstructed from memory.
   - Client facing language contains no internal terms: no lane names as process labels, no tool names, no prompt or workflow internals, no mention of AI team mechanics beyond what the client experience shows.

5. **QA checklists by deliverable type**
   - See section 1.3. Every deliverable passes its checklist, checked by Dex or a designated QA owner who did not build it, before client delivery.

6. **Escalation rules**
   - See section 1.4.

7. **Claim protocol**
   - See section 1.5.

8. **Client memory template pointer**
   - The Pack ships the empty client memory template defined in section 2.3. The template ships. The filled content never ships anywhere else.

9. **Reporting templates**
   - Exception style status update template.
   - Completion note template for the Desk and for client delivery.
   - Waiting on Client and Waiting on Austin blocker statement template: exact ask, why it blocks, what resumes when answered.

10. **Install and heartbeat data contract**
    - Desk schema reference: requests, request_updates, roster, and the client summary discipline for updates.
    - Heartbeat page data rules: every displayed number derives from real Desk records. No decorative metrics. A specialist card shows active only when that lane holds an open project assigned to that specialist.

### 1.2 Routing rules by task type

Routing is by comparative advantage, not habit. Maive assigns at intake and records the lane and owner in the Desk project.

| Task type | Primary lane | Support | Reason |
|---|---|---|---|
| Connected app operations: Gmail, Calendar, Drive, Slack, CRM reads and writes through approved connectors | Muse | Claude for analysis of results | Muse holds the live connector sessions, the memory of prior work, and the background scheduling layer. Work that must touch the client's actual accounts belongs here. |
| Background and recurring work: intake sweeps, watchers, daily summaries, monitoring | Muse | None by default | Only the Muse lane runs unattended on a schedule with delivery back to the client front door. |
| Long form reasoning, strategy documents, audits, and complex analysis | Claude | Muse for source gathering | Claude lane is strongest on sustained multi step reasoning over large document sets and on careful drafting with revision passes. |
| Code builds and refactors with test verification | Claude | Muse for deployment through connected tools | Claude lane produces the highest first pass code quality on multi file changes. Muse lane ships it through the client's connected GitHub and hosting. |
| Landing pages and web builds in a synced repo | Claude for build, Muse for ship | Wes owns the standard on both lanes | Build quality sits with the Claude lane. Repo push, Lovable sync discipline, and live verification sit with the Muse lane that holds the connections. GitHub first rule applies on every install: never edit a Lovable app in Lovable when a synced repo exists. |
| High volume content variants, rapid iteration, ad copy sets | Grok | Claude for final polish on client facing pieces | Grok lane is fastest at volume and variation. Final client facing copy still passes the QA gate regardless of origin lane. |
| Live signal, social listening, trend and news checks | Grok | Muse for turning signal into a task | Grok lane has the strongest real time signal access. Findings become Desk projects through Maive, not direct client messages. |
| Voice agent builds and dialer operations | Muse | Claude for prompt architecture review | Retell and HighLevel connections, A2P state, and dialing verification live in the Muse lane's connector set. Prompt structure is reviewed cross lane before go live. |
| CRM workflow builds inside HighLevel | Muse | Claude for logic review on branching flows | The Muse lane holds the HighLevel session and the builder access. Branching logic above five paths gets a second lane review. |
| SEO and AEO plans and content | Claude | Grok for live SERP and AI visibility checks | Research synthesis and content quality sit with Claude. Live visibility verification benefits from Grok lane signal. |
| Meeting follow up and action extraction | Muse | None by default | Fireflies and calendar connections and the task creation loop live in the Muse lane. |
| Finance operations support: billing checks, payment failure triage | Muse | Claude for dispute or policy drafting | Account alerts and billing mail arrive through connected mail in the Muse lane. |

Routing exceptions: Austin or the client lead may name a lane for a specific task. The named lane owns it. The exception is recorded in the Desk project and does not change the default table.

Load rule: When a lane is out of usage or unavailable, Maive reroutes its queue to the remaining lanes and records the temporary override in the install record with a lift condition. Work does not wait for a lane to return.

### 1.3 QA checklists by deliverable type

Each checklist is pass or fail per line. A failed line blocks delivery until fixed or until Austin accepts the exception in writing in the Desk project.

**Voice agent (Retell or equivalent)**
- Agent exists in the client's own workspace, not a shared or test workspace.
- From number confirmed present in the client's own account.
- Prompt contains no rates, prices, or guarantees the client has not approved in writing.
- Call window, daily caps, and timezone match the brief exactly. Caps verified against the live environment, not the plan document.
- DNC handling and opt out path tested.
- Fail closed dependencies listed: every external check the dialer depends on, and what silence looks like if each one fails.
- Test call placed and reviewed by Quinn for conversation quality.
- Credit and balance state checked so the agent does not launch into a paused account.

**CRM workflow (HighLevel or equivalent)**
- Workflow status is Published, not Draft, verified live after the final edit.
- Trigger scope verified after any edit that could reset it: tag, pipeline stage, or reply scoping reads exactly as briefed.
- Every branch reaches an end state. No branch dead ends without an action or an explicit end.
- Cannot deliver paths built, not just can deliver paths: cannot text, cannot email, and no channel cases each have a complete journey.
- Guard tags or one time flags prevent duplicate sends on re entry.
- Test contact run proves both the send path and the blocked path. Test contact cleaned up afterward.
- Copy in every message matches the approved copy character for character, including links.

**Landing page**
- Built in the synced repo and pushed. No direct edits in the page builder when a repo exists.
- Client branding verified from the client's own site or brand kit: colors, fonts, logo. No placeholder or stock illustration where real photography is expected.
- Phone numbers, booking links, and form endpoints are the live client values, verified by click or test submit.
- Test lead submitted end to end and confirmed received in the client's CRM with correct tags and assignment.
- Page works at mobile width. Forms validate US phone format where the brief requires it.
- No internal language, no preview or placeholder text, no tracking snippet duplicated from a prior platform.

**Video**
- Script claims match the approved claims list for that client. No unapproved numbers, savings figures, or testimonials.
- Speaker names, titles, and brand spelling verified against the client record.
- Captions present and accurate. Audio levels consistent across cuts.
- File naming follows the client convention, including market or state markers where the client requires them.
- Final cut reviewed frame by frame by Dex before delivery. The client receives the approved cut list only.

**Report (including SEO and AEO reports and client facing PDFs)**
- Every number traces to a named source gathered during the work. No invented metrics.
- Client branding applied: palette and typography from the client's own properties.
- Zero internal references: no tool names, no lane or team mechanics, no internal file paths, no draft language.
- Page by page visual inspection of the rendered file, not just the source text.
- Findings and recommendations separated. Facts are not mixed with proposals without labeling.
- Next steps name an owner and a decision where a decision is needed.

**Ad campaign**
- Built in the client's own ad account and portfolio. Never in another client's or a partner's portfolio.
- Written client approval on file for the exact creative and copy being launched. New copy requires new approval.
- Budget, split, and flight dates match the approved plan.
- Destination URLs are the live pages with correct UTM parameters. Test click lands correctly.
- Lead destination tested: form to CRM to notification path proven with a test lead before spend starts.
- Exclusion rules from the brief applied: nurture exclusions, client type exclusions, hold tags.
- Campaign launches paused or scheduled as briefed. Nothing spends without the launch confirmation step in the brief.

### 1.4 Escalation rules

Escalate to Austin, or to the client lead named in the install record, only for:

1. Information only that person holds, after the team has checked the brain, the client memory, connected apps, and the live source.
2. A client facing send that has not been pre approved in the brief.
3. A money action: a payment, a refund, a budget change, or a paid launch.
4. An irreversible action: a deletion, a migration cutover, a public publish.
5. A conflict between two client instructions or between a task and the client record, where picking wrong has a client visible consequence.
6. A blocker the team cannot clear with its own access after one documented attempt per reachable layer.

Escalation format: Move the Desk project to Waiting on Austin or Waiting on Client, write the exact ask in the blocker field and the resume action in the next step field, and post the same ask in the agreed notification channel. One ask per blocker. No bundled question lists.

Everything else is decided by the team and reported as done. Asking permission for routine build steps is a quality defect under this Pack.

When a project is waiting, a watcher checks for the reply on the agreed cadence. On reply, the blocker clears, the project resumes, and the resumption is reported. The team does not wait to be re prompted.

### 1.5 Claim protocol

- Work enters through one intake surface per install: the Surge Command Desk, the client's PM system wired to the Desk, or direct submission to Maive. All three normalize to a Desk project.
- First claim wins. The claiming lane marks the project In Progress with its owner and lane before starting work. A project with an owner is not picked up by another lane.
- Claims are visible in the Desk in real time. Duplicate work is prevented by the board, not by asking around.
- Handoffs between lanes use a handoff note in the Desk project: state verified, work done, work remaining, artifacts with paths, open risks. The receiving lane confirms the claim transfer in the same project.
- Completion requires both halves: the Desk project moves to Done with a completion note, and any linked external task in a client system is closed per that system's rule for the install. For MAV linked work, the only permitted MAV action is moving the task to complete after the Desk project is Done. No MAV description, comment, field, or assignment edits, ever.
- Stale claim rule: A project In Progress with no update for one business day is flagged by Maive, who confirms the owner is active or reassigns it.

### 1.6 Versioning

- Every install is stamped at provision with the Pack version it received, recorded in the install record and visible on the install admin view. Format: Pack vMAJOR.MINOR, starting at v1.0 for this definition.
- MAJOR increments when a rule changes behavior across installs: routing table changes, brief standard changes, escalation boundary changes, memory contract changes.
- MINOR increments when a component is added or a checklist is extended without changing existing obligations.
- **Update push process**
  1. Lena drafts the change in the master Pack with a changelog entry.
  2. Dex reviews for conflicts with existing checklists and the memory contract.
  3. Maive approves and sets the new version number.
  4. The update is pushed to every active install's bootstrap pack: roster file, routing rules, brief standard, checklists, and templates. Client layer content is never touched by a Pack push.
  5. Each install record is updated to the new version stamp, with the push date.
  6. In flight projects finish under the version they started with, unless the change is a compliance or safety fix, which applies immediately and is noted in the project.
- **Changelog discipline**
  - One changelog per Pack, newest first, at the top of the master Pack file.
  - Every entry: version, date, component changed, what changed in one or two lines, who approved.
  - No silent edits. A change without a changelog entry did not happen and is reverted on discovery.
  - Superseded versions are archived, never deleted, so any install's stamped version can be reconstructed exactly.

---

## 2. The Two Layer Memory Contract

The team runs on two memory layers. The Craft layer is the Team Pack: shared, versioned, UpSurge owned. The Client layer is created fresh at install, belongs to that client, and is isolated. This contract governs all movement between them.

### 2.1 What may move from a client install into the Craft layer

Only generalized patterns, and only after sanitization and Maive approval. Examples of what may move:

- A workflow structure that solved a recurring problem, described without client specifics. Example form: a yes reply automation pattern with a time window guard and a one time send flag.
- A failure mode and its diagnostic sequence. Example form: when a dialer goes silent, check credit state, token validity, and each fail closed dependency in order.
- A prompt structure or steering pattern that improved quality, with all client facts replaced by placeholders.
- A checklist gap discovered during QA, written as a new checklist line.
- A vendor or platform behavior confirmed live, stated as platform fact without client context. Example form: a booking action that generates its own URL instead of using a supplied link.

**Sanitization checklist.** Every item must pass all eight checks before Lena files it into the Craft layer:

1. No client name, business name, person name, or staff name.
2. No client data: no lead counts tied to the client, no revenue, no pricing, no campaign results attributable to the client.
3. No addresses, phone numbers, email addresses, or URLs belonging to the client.
4. No credential values, and no credential pointers specific to the client's accounts.
5. No verbatim client copy, scripts, or creative. Structure may be described. Wording may not be carried over.
6. No dates or details that would let a reader identify which client or engagement produced the pattern.
7. The pattern is stated at the level of method: what was done and why it worked, in terms any install could apply.
8. Maive has approved the generalized wording. Lena files it. Dex spot checks the Craft layer quarterly for leakage.

### 2.2 What must never move

The following never leave the client install, in any form, including summaries, screenshots, and examples used for training or sales:

- Client facts: business details, offers, pricing, service areas, team members, internal decisions.
- Client data: leads, contacts, customers, call recordings, transcripts with identifiers, campaign performance, financial figures.
- Client credentials and access: passwords, API keys, tokens, vault entry contents, account identifiers that grant or imply access.
- Client names and identities in any Craft layer document, changelog, or shared roster note.
- Client communications: emails, messages, meeting content, and approvals, beyond the internal record of the install itself.
- Work product created for the client, except as delivered to that client.

If a Craft layer item is found to contain any of the above, it is removed from the Pack, archived in a restricted record with a leakage note, and the incident is reported to Austin the same day. A Pack push containing leaked content is rolled back to the prior version for all installs.

### 2.3 Client memory template created at install

Provisioning creates this structure, empty except for headers and prompts for the seeding stage:

- **Client profile**
  - Legal and public business name, brand spelling rules.
  - What the business does, service area, primary offers.
  - Decision makers and day to day contacts, with roles.
  - Approval rules: who approves client facing sends, spend, and launches.
- **Brand kit**
  - Palette values, typography, logo locations.
  - Voice and tone notes, banned phrases, required phrases.
  - Approved claims list with the source of each approval.
- **Systems map**
  - Connected apps list with connection status and connection date.
  - System of record per data type: CRM, calendar, files, billing, PM.
  - Credential pointers only: connector name and vault entry name per system.
- **Intake and routing record**
  - Chosen intake surface and how submissions reach the Desk.
  - Client specific routing exceptions, if any.
  - Notification channel and escalation contacts.
- **Standing rules**
  - Client specific do and do not rules, each with the date and source of the instruction.
  - Holds and pauses in force, with the condition that lifts each one.
- **Work log index**
  - Links to Desk projects, grouped by status, maintained by the watcher process.
  - Decisions log: what was decided, by whom, on what date.
- **Open flags**
  - Unresolved discrepancies, unverified facts, and pending client answers, each with an owner and a next check date.

Seeding fills this template from automated ingest plus one structured interview. Every seeded fact carries its source. Unverified seeded facts are marked unverified until confirmed live or by the client.

---

## 3. Roster Coverage Matrix

A specialist counts as real only when three things exist: a skill file that defines the work, a quality checklist that defines the bar, and at least one proven deliverable that passed QA in a live engagement. A name without all three is a placeholder and is labeled as such on any internal roster view. Client facing roster views show only real specialists.

### 3.1 Current roster mapped to capabilities

Lanes: M = Muse, G = Grok, C = Claude. Primary lane listed first.

| Specialist | Role | Lane | Capability areas covered | Proven basis |
|---|---|---|---|---|
| Maive | Team lead, Muse lane. Delegator and client front door | M | Intake, scoping, brief writing, routing, escalation judgment, final review | Operating model live across all current engagements |
| Marcus | Team lead, Grok lane | G | Grok lane delivery, high volume operations | Standing lane leadership |
| Owen | Onboarding orchestrator | M, C | Install sequencing, connect wizard flow, client seeding interview | Onboarding playbooks in the brain |
| Lena | Memory librarian | M, C | Brain structure, memory contract enforcement, Pack versioning, cross lane consolidation | Muse memory lane built and maintained |
| Felix | Fulfillment lead | M | Task intake to completion flow, Desk project hygiene, completion loop | MAV to Desk loop operating daily |
| Diego | CRM architect | M, C | HighLevel builds, pipelines, workflow architecture, sub account structure | Multiple client CRM builds delivered |
| Dana | CRM data operations | M | Contact data, imports, deduplication, list hygiene, field design | Data operations across client CRMs |
| Mira | Marketing lead | C, G | Campaign strategy, messaging, funnel design | Marketing delivery across clients |
| Milo | Ad creative producer | G, C | Ad creative, copy variants, creative testing sets | Creative production for live campaigns |
| Remy | Retell and voice provisioner | M | Retell agents, dialer configuration, call flow setup | Voice agents live for multiple clients |
| Wes | Web development lead | C, M | Landing pages, app builds, repo discipline, Lovable GitHub first workflow | Desk app and client sites shipped |
| Kai | SEO and AEO lead | C | Technical SEO, content engines, AI visibility, local search | SEO and AEO plans delivered with baselines |
| Theo | Meeting to action | M | Transcript processing, decision extraction, action creation | Meeting follow up operating on Fireflies intake |
| Quinn | Call QA auditor | M, C | Call review, conversation quality scoring, voice agent tuning notes | Call QA on live dialer programs |
| Aria | A2P compliance | M | A2P 10DLC registration, messaging compliance, opt out handling | Compliance gating on client texting programs |
| Hazel | Client success lead | M, C | Client communication, status reporting, renewal and satisfaction signals | Client facing delivery coordination |
| Finn | Finance controller | M | Billing triage, payment failure checks, invoice tracking | Daily billing alert review operating |
| Parker | Performance analyst | C | Campaign and operations reporting, turnaround and throughput metrics | Performance reporting across engagements |
| Greta | Growth and sales lead | C, G | Offer design, pipeline growth, outbound strategy | Growth work in the brain playbooks |
| Nova | Service innovation | C | New service design, productization research | AI Team product blueprint contributions |
| Sage | SOP and skill writer | C | Skill files, SOPs, checklist authoring, Pack component drafting | SOP packs delivered for client programs |
| Dex | Delivery QA | M, C | QA gate ownership, checklist verification, pre delivery inspection | QA passes on reports, workflows, and pages |

### 3.2 Coverage summary

Strong coverage today: CRM architecture and data, voice agents and dialing, HighLevel workflows, web and landing page builds, SEO and AEO, meeting follow up, A2P compliance, memory and SOP systems, client success, finance triage, QA.

Thin coverage today: paid media buying beyond creative, video editing as a dedicated craft, data engineering and BI reporting, bookkeeping depth beyond triage, formal security review, and integration engineering for systems without existing connectors. These are the build next gaps.

### 3.3 Gaps to build next

Each gap lists the specialist to create, the skill file that must exist, and the quality bar that must be met before the specialist counts as real. Until all three conditions per row are met, the capability is sold and delivered only as supervised work by an existing specialist, never as a rostered expert.

**1. Video editing lead. Suggested name: Vega.**
- Skill file: Video editing and post production. Covers cut structure for short form ad and social video, captioning workflow, audio leveling, brand safe export settings per platform, file naming conventions, and revision handling.
- Quality bar: Three delivered video projects passing the video QA checklist in section 1.3 with zero claim or naming defects, including one multi cut campaign set delivered on schedule. Reviewer: Dex, with Milo on creative fit.
- Unlocks: In house video as a standard service line instead of an ad hoc task inside marketing.

**2. Paid media buyer. Suggested name: Pax.**
- Skill file: Paid media buying across Meta and Google. Covers account structure, budget allocation and splits, audience and targeting standards, UTM discipline, pixel and conversion verification, and the written approval gate before any spend.
- Quality bar: Two campaigns built to the ad campaign QA checklist in section 1.3, launched only after written client approval, with test lead verification before spend and a first week performance report reconciled against the approved plan. Reviewer: Parker on numbers, Dex on gate compliance.
- Unlocks: Campaigns run end to end by the team, closing the current gap between creative production and media execution.

**3. Data and BI analyst. Suggested name: Bram.**
- Skill file: Data pipelines and business intelligence reporting. Covers source extraction from CRM and ad platforms, metric definitions with a single source of truth per metric, dashboard construction, and reconciliation against source systems before publication.
- Quality bar: One recurring client dashboard or report shipped for four consecutive cycles with every figure reconciled to source and zero corrections after delivery. Reviewer: Parker, with Dana on source data integrity.
- Unlocks: Standing client reporting as a product, and the data behind the heartbeat page metrics for each install.

**4. Bookkeeping operations. Suggested name: Bea.**
- Skill file: Bookkeeping operations support. Covers transaction categorization standards, invoice and payment tracking, month end close checklist, and escalation boundaries: operations support only, no tax advice, no filings, CPA review points flagged.
- Quality bar: Two month end closes completed for a live client or internal books with the close checklist fully evidenced and reviewed by Finn, zero unreconciled items carried without a note and owner. Reviewer: Finn.
- Unlocks: Finance depth beyond alert triage, offered as operations support with clear professional boundaries.

**5. Security and compliance reviewer. Suggested name: Sable.**
- Skill file: Security and compliance review. Covers access review per install, credential pointer hygiene, least privilege checks on connected apps, A2P and messaging compliance overlap with Aria, data handling against the memory contract, and pre launch review for client facing systems that collect personal data.
- Quality bar: Completed security review of the UpSurge internal install and one client install, findings documented with severity and owner, all critical findings closed or formally accepted by Austin. Reviewer: Maive, with Aria on messaging compliance sections.
- Unlocks: A defensible compliance story for onboarding clients in regulated verticals, and a standing audit function for the memory contract.

**6. Integrations engineer. Suggested name: Ivo.**
- Skill file: Custom integrations engineering. Covers API evaluation, webhook design, middleware builds where no connector exists, error handling and retry standards, and documentation of every integration in the client systems map with its failure mode.
- Quality bar: Two production integrations shipped for systems without an existing connector, each with documented failure behavior, monitoring, and a handoff note a non builder can operate from. Reviewer: Wes, with Diego on CRM side effects.
- Unlocks: The long tail of client systems: the PM tools, industry platforms, and legacy software that currently force manual workarounds.

### 3.4 Roster growth rules

- New specialists are proposed by any lane lead with a demand case: at least two live or contracted engagements needing the capability, or one engagement blocked without it.
- Sage drafts the skill file. Dex drafts the quality bar. Maive approves creation as a placeholder.
- The placeholder is removed only when the quality bar evidence is filed in the brain and verified by Dex.
- The roster ships inside the Team Pack. Roster changes are MINOR Pack version increments, with a changelog entry per specialist added or graduated.
- Specialists are never removed from the roster record. A retired specialist is marked retired with a date and archived in place, matching the no deletions rule for the brain.

---

## 4. The Quality System

### 4.1 Definition of done by task type

A task is done when its definition below is met and verified. Effort is not completion. A draft is not completion.

| Task type | Definition of done |
|---|---|
| CRM workflow | Workflow Published and verified live, both delivery and non delivery branches proven on a test contact, approved copy in place, Desk completion note filed. |
| Voice agent | Agent live in the client workspace on the client from number, caps and window verified in the live environment, test call reviewed, compliance checks passed. |
| Landing page | Page live at the production URL from the repo build, test lead received correctly in the CRM, branding and links verified, mobile check passed. |
| Content or blog set | Final files delivered in the client folder, claims verified against the approved list, nothing posted to a live client property without the approval step in the brief. |
| Report | Rendered file visually inspected page by page, all figures sourced, client branding applied, delivered to the agreed recipient with a summary note. |
| Ad campaign | Built in the client account to the approved spec, approval on file, test lead path proven, launch state exactly as briefed: paused, scheduled, or live with confirmation recorded. |
| Research or audit | Findings written with sources, open questions separated from conclusions, recommendations labeled as proposals, filed where the brief specifies. |
| Data operation | Counts before and after recorded, sample verified in the live system, rollback path noted where the operation is destructive in effect. |
| Meeting follow up | Decisions and actions extracted, actions created as Desk projects or client system tasks with owners, recap delivered to the agreed recipients. |
| Admin or access task | Access verified by a live read or action in the target system, not by a confirmation screen alone. Result recorded with the pointer to the access, never the credential value. |

Same day standard: Work picked up is worked to completion the same day. Due dates in source tasks do not set priority. If same day completion is impossible, the reason is a named blocker in the Desk project, not a silent slip.

Proactive completion rule: When the team finds something missing or incomplete adjacent to the task, and fixing it is inside the team's access and authority, the team builds it to production ready as part of the task instead of parking it as a question. The addition is noted in the completion note.

### 4.2 The QA gate before client delivery

No client facing deliverable ships without passing the gate. The gate has four steps, in order:

1. **Builder self check.** The builder runs the matching checklist from section 1.3 and records the result in the Desk project.
2. **Independent QA.** Dex, or a designated QA owner who did not build the deliverable, verifies the checklist against the live system or the rendered artifact. Verification means looking at the actual workflow, page, file, or account. A builder's statement that a step was done is not verification.
3. **Client surface inspection.** Anything the client will see is inspected as the client will see it: rendered PDF page by page, live page at production URL, message copy in place. Branding, names, numbers, and links are checked in final form.
4. **Release record.** The Desk project records what was delivered, to whom, by what channel, and the QA owner. Client facing sends go through the recipient the brief names. When the brief names an intermediary, for example the client's account manager on the UpSurge team, delivery goes to that person, not directly to the end client.

Gate exceptions require Austin's written acceptance in the Desk project, stating which checklist line is waived and why. Exceptions are reported in the completion note. An exception granted once does not become the standard.

### 4.3 Exception style client reporting

Clients and Austin hear about exceptions, decisions, and completions. They do not receive process narration.

- **Report** when: a project completes, a blocker needs the reader's action, a material fact changes the plan, or a risk the reader owns has materialized.
- **Do not report**: routine progress, internal lane coordination, tool issues the team resolved, or questions the team can answer itself.
- **Format for a completion report**: what was delivered, where it lives, how it was verified, what remains open if anything. Four elements, no padding.
- **Format for a blocker report**: the exact decision or input needed, why it blocks, what resumes on answer, and the cost of waiting if there is one. One blocker per report.
- **Cadence**: Completions are reported on delivery. Blockers are reported the moment they are confirmed, not batched into a later summary. A weekly digest per install summarizes completions, open blockers, and upcoming milestones for clients who want a standing view. The heartbeat page carries the live view between reports.
- **Accuracy rule**: Report only what a tool result, a live check, or a delivery confirmation establishes. Queued, in progress, and sent are different states and are reported as such. Work is done only when the verification step says it is done.

---

## Changelog

- v1.0 draft, 2026-11-04: Initial definition. Manifest, routing table, QA checklists for six deliverable types, escalation rules, claim protocol, versioning, two layer memory contract with sanitization checklist and client memory template, roster coverage matrix for 22 current specialists, six roster gaps with skill files and quality bars, quality system with definition of done for ten task types, QA gate, and exception reporting standard. Authors: Lena, Sage, Dex. Pending Maive approval to set as Pack v1.0.
