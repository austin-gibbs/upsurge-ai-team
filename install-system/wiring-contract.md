# AI Team Wiring Contract: Front End to Live Service

Status: Contract v1, 2026-11-04
Owners: Owen (onboarding-orchestrator) with Finn (finance-controller), for Maive (delegator of record)
Scope: How every client facing surface (the marketing site, the fit call page, the pilot application, the onboarding hub, the client command home) connects to the systems that run a live install: the HighLevel sales pipeline, the install orchestrator, the Surge Command Desk, the Client layer memory, and accounting. This document is the agreement between the front end build and the service build. If a page and this contract disagree, this contract wins until it is amended here.
Companion documents: install-pipeline.md (stage and step detail, this repo), orchestrator/README.md and orchestrator/state.py (step IDs and engine behavior), go-to-market/sales-to-install-ops.md (pipeline stages, the T0 signature sequence, payment discipline), client-onboarding-pack.md (the words the client reads).

## 0. Contract conventions

- Event names are snake_case, past tense, and identical in the front end, the endpoint service, and the audit log: for example `application_submitted`, never three spellings of the same moment.
- Every event payload carries: `event` (string), `occurred_at` (ISO 8601, UTC), `application_id` (string, before signature) or `install_id` (string, from signature on), `client_slug` (string, once minted at provision), and `source_page` (one of `index`, `book`, `apply`, `onboard`, `home`, `system`).
- Step references use the orchestrator's real IDs in `stage.step` form from state.py: `provision`, `connect`, `seat`, `seed`, `go_live`. Fully qualified example: `connect.verify_crm`.
- Self-serve is the contract, not the aspiration (Austin, 2026-11-04): no onboarding step requires a human at UpSurge. Every recovery in this contract is automated: in-hub guidance, lifecycle nudges, and simplified retry paths (Section 5.3). Humans appear only as asynchronous internal oversight, reviewing flags after the fact; a client never waits on one. Roles own systems, not steps: Sales owns the pre-signature automation configuration, the Install Operator role owns the orchestrator and hub configuration, Finn's lane owns the accounting configuration, and the oversight function owns the flag queue. The change that retires the old human QA gate is specified in Section 5.1.
- Amounts appear in exactly two places: the signed agreement and the accounting system. No other system in this contract stores, displays, or logs an amount. Slack messages, Desk fields, front end payloads, and this contract carry payment status only.
- Secrets are pointers only, everywhere in this contract. No payload defined here may contain a credential value, a passcode value, or a signing secret.

## 1. The journey on one page

| # | Client moment | Page | Event | The service answers with |
|---|---|---|---|---|
| 1 | Prospect books a fit call | book.html | `fit_call_booked` | HighLevel opportunity advances, prep note posted internally |
| 2 | Prospect applies for the pilot | apply.html | `application_submitted` | Application record in HighLevel, internal review task, applicant acknowledgment |
| 3 | Agreement is signed | signature tool (Section 3) | `agreement_signed` | T0: invoice 1 issues, the hub unlocks, the welcome sequence fires; provisioning waits for the payment trigger (Section 3.3) |
| 4 | Start payment lands | accounting | `start_payment_received` | The provisioning trigger fires (Section 3.3): the orchestrator starts Stage 1 with no human in the loop; Desk `payment_status` projection updates |
| 5 | Client connects their tools | onboard.html | one `connector_verified` per tool | Orchestrator connect stage steps complete one by one |
| 6 | Client self-installs the seats and the drills verify | onboard.html | `seat_bootstrap_delivered`, `seat_lane_verified` per lane | Seat stage steps complete from hub delivery and drill returns (Section 5.2) |
| 7 | Client completes knowledge intake | onboard.html | `knowledge_form_submitted` | Seed stage gets its sponsor supplied facts and gap answers |
| 8 | Client reviews and confirms the seeded facts | onboard.html | `facts_self_confirmed` | Seed stage closes on the client's confirmation; unconfirmed facts ride as flagged assumptions (Section 5.1) |
| 9 | Client completes the go live checklist | onboard.html | `go_live_checklist_completed` | The retired QA gate's client side is complete (Section 5.1); the automated final sweep runs and go live proceeds |
| 10 | First real request submitted | home.html | `first_request_submitted` | `go_live.create_first_project` runs through normal intake |
| 11 | Install reaches live | system | `install_live` | Go live payment invoice fires, standing loops start, home.html becomes the client's daily surface |

## 2. Event wiring table

One row per event. "Satisfies" means the event is the evidence a step was waiting for; "triggers" means the event starts the step. Human touchpoints: none required, in any row. Every recovery below is executed by automation: in-hub guidance first, lifecycle nudges at 24 and 72 hours, a simplified retry path, and at the stage's outer timer an internal oversight flag that the client never sees and never waits on (the full ladder is Section 5.3). Where the ops bridge or the pipeline spec previously specified a human touch (a note from Finn's lane, an operator nudge, a same day page), this contract supersedes it: the touch becomes an automated message from the approved template, and the human surface becomes the oversight flag queue.

### 2a. Before signature

| Event | System of record (exact field) | Orchestrator step | Automation that fires | Failure or abandonment recovery |
|---|---|---|---|---|
| `fit_call_booked` (book.html) | HighLevel pipeline `AI Team - Sales`: opportunity stage moves New Lead to Discovery on booking; calendar event id stored on the opportunity; contact fields `sponsor_name`, `sponsor_email` | None (pre-install). Recorded against the future install at `provision.write_manifest_v1` as source data | Booking confirmation to the prospect; reminder sequence at 24 hours and 1 hour before the call (ops bridge Stage 1); internal prep note to the sales channel with website, visible tools, and the three questions that matter | No-show: `fit_call_no_show` derived from the calendar at start time plus 10 minutes; automated rebook message within 1 hour, second touch at 48 hours, third touch at 5 days in the signer's name from the approved template; opportunity returns to New Lead with tag `ait-sales-noshow` if no rebook in 7 days |
| `application_started` (apply.html first field interaction or step 1 completion) | HighLevel: contact created or matched; application draft record with `application_id`, `application_state = started`, and the partial payload in `application_partial_json` | None | None on start. The draft exists so abandonment is recoverable, not visible | Not submitted within 4 hours: automated resume email with a signed resume link. 48 hours: second reminder. 5 days: a final automated note in the signer's name from the approved template, and an internal flag for the weekly sales review. 14 days: draft marked `application_state = dormant`; no further automated touches |
| `application_submitted` (apply.html) | HighLevel: `application_state = submitted`, full payload in the Section 5 fields on the contact and opportunity; opportunity stage = Proposal when the diagnostic is already done, else Discovery; tags `ait-source-[channel]` from the payload `source` field | None. The payload becomes the input record that `provision` reads at T0 (legal name, sponsor, timezone, intake mode, CRM) | Applicant acknowledgment within 15 minutes during business hours (ops bridge standard): what happens next, who reviews it, the expected decision window. Internal alert to the sales channel with business name, tier interest, intake mode, and bottleneck summary. Review task created for Maive's lane | Application incomplete on validation (missing required field): the page blocks submit and names the field; no partial record is promoted. Application submitted but no agreement sent within 1 business day: the agreement generation re-fires daily and an internal flag is raised at 2 business days. Declined applications get one written decision from the approved template, sent automatically, never silence |
| `agreement_sent` (signature tool) | Signature tool envelope record linked from the HighLevel opportunity field `agreement_envelope_id`; opportunity stage stays Proposal | None | Proposal follow-up discipline from the ops bridge applies: view tracking on, follow-up task at 48 hours if unviewed, 24 hours after a view with no response | Unsigned at 72 hours: automated reminder from the signature tool. 7 days: an automated note in the signer of record's name from the approved template. 14 days: opportunity parked with a dated reason per ops bridge discipline; the application stays on file |
| `agreement_signed` (signature tool webhook) | Signature tool: signed document filed to the HighLevel client record. HighLevel: stage = Signed, tag `ait-install` applied (never removed). This event is T0 | Records the install intent and mints `install_id`. The Desk install project is created here as the visible record. The orchestrator starts `provision.create_client_layer` only when the provisioning trigger fires (this event plus `start_payment_received`, in either order, Section 3.3) | The client visible T0 sequence (ops bridge Section 2, automation only under this contract): agreement filed and stage set by T0 + 5 min; invoice 1 issued by T0 + 15 min; welcome message and the hub link sent by T0 + 15 min; Desk install project created by T0 + 30 min; internal notice by T0 + 30 min. Memory skeleton and Desk workspace are provision stage outputs and follow the payment trigger, not the clock | Webhook missed or duplicated: the signature tool's envelope status is polled automatically once daily until `agreement_signed` is recorded; the event handler is idempotent on `agreement_envelope_id`, so a duplicate webhook is a no-op. Signed but a T0 item misses its target: an internal oversight flag is raised the same day; the client's hub simply shows the true state |

### 2b. Money events

| Event | System of record (exact field) | Orchestrator step | Automation that fires | Failure or abandonment recovery |
|---|---|---|---|---|
| `start_payment_received` (accounting: invoice 1 paid) | Accounting: invoice 1 record (id, amount, paid timestamp) is the only truth. Desk install project: `payment_status` moves to `paid` if no other due invoice is open, else stays `issued` | None. Payment never gates a step retroactively; install work starts at T0 per the ops bridge | Receipt confirmation to the client from accounting. Internal status only note to the install channel (status word only, no amount) | Not received at 24 hours: polite automated reminder (ops bridge step 9, automated under this contract). At 72 hours: a second automated reminder, the hub shows a billing banner, and Desk `payment_status` is set to `attention`. At 7 days: an internal oversight flag for the weekly review. No human sends anything and no step waits on one; provisioning has simply not triggered yet, which the hub states plainly (Section 3.3) |
| `go_live_payment_invoiced` (accounting, fired by `install_live`) | Accounting: invoice 2 created from the agreement's go live milestone. Desk: `payment_status` set to `issued` | Triggered by (not a step of) `go_live.schedule_standing_loops` completing and the install state reaching `live` | Invoice sent to the client from accounting with the go live confirmation message | Same ladder as invoice 1: automated reminders at 24 and 72 hours, `attention` at 72 hours, an internal oversight flag at 7 days. No human touch at any point |
| `payment_status_changed` (accounting projection) | Accounting computes it; Desk install project field `payment_status` is the only place the rest of the service reads it. Legal values, exactly three: `issued`, `paid`, `attention` | None | home.html renders the status word in the billing line only when it is `attention`, with the text "your account needs attention, your team lead has the details" and never an amount | Projection writer fails: the writer retries on its next cycle (Section 6); a stale `paid` during an open invoice is a defect surfaced in the weekly oversight report against accounting, because the Desk is a projection and accounting is the truth |

### 2c. Connect stage (onboard.html)

The full connect truth rule is Section 4. This table wires the events; the rule governs what the states mean.

| Event | System of record (exact field) | Orchestrator step | Automation that fires | Failure or abandonment recovery |
|---|---|---|---|---|
| `connect_checklist_opened` (onboard.html first authenticated view) | Desk install project: checklist item `connect` marked started; manifest entry `checklist_presented_at` | Satisfies the display half of `connect.present_checklist` (the step completes when the checklist exists in the manifest and this view is recorded) | None beyond rendering. The page renders the projection defined in Section 4 | Checklist live but never opened within 24 hours: first lifecycle nudge with the link. At 72 hours: second nudge, and the hub switches the connect section into guided mode, one tool at a time with the exact tap named on screen. Untouched at 5 business days: an internal oversight flag is raised and the install record moves to `paused_human` (read: paused awaiting client, Section 5.1). The client's experience does not change; the checklist simply waits with its state preserved |
| `connector_authorized` (per tool: the client completed the OAuth tap or secure key entry and the callback returned) | Manifest connected apps entry: `status = authorizing`, `authorized_at` timestamp, account label as returned. This event never sets Connected | Starts the verification half of the matching step: `connect.verify_email` (gmail), `connect.verify_calendar` (google_calendar), `connect.verify_file_storage` (google_drive), `connect.verify_crm` (the agreement's `crm_connector`), or a per app verify under the same step family for agreement named apps | The orchestrator runs the connector's status check plus one harmless read (Section 4). The page shows "verifying" for that row, nothing else changes | Callback never arrives (client closed the tab mid flow): the row returns to `awaiting_client` after 15 minutes with its action link live again; no error is shown to the client. Wrong account connected (account label mismatch with the agreement): row set to `needs_human`, the sponsor gets one exact message naming the account that was expected, and the app does not proceed (pipeline spec Stage 2 rule) |
| `connector_verified` (per tool: orchestrator verification passed; this is the only event that makes a row Connected) | Manifest connected apps entry: `verified = true`, `verified_at`, scopes granted, account or location ids, credential pointer (name only). Desk install project: the connect checklist row for that tool marked done | Completes the matching `connect.verify_*` step. When every required app has an entry, `connect.record_connections` completes and the install state moves to `connected` | The row flips to Connected on the next projection push (Section 4). When the stage completes: the client gets the plain language line from the onboarding pack ("your tools are connected and verified") and the internal completion notice posts to the ops channel | Verification fails: first failure retries once before it is treated as a credential problem (proxy tunnel behavior, pipeline spec). A 429 is a hard stop for that provider in the run; the row shows `pending` with a retry scheduled, never an error code. Three failed verifications: row set to `failed` with a reason code in the manifest, operator alerted with the account label (never the credential); a required app failing moves the install to `paused_human` with the exact sponsor ask; an optional app failing is listed as pending and does not block (spec Stage 2) |
| `connector_key_requested` (per API key app: the checklist reaches an app with no OAuth path) | Manifest connected apps entry: `status = awaiting_key`, credential pointer name reserved | Part of the matching `connect.verify_*` step's evidence chain | One secure capture form sent for that one key at that moment (never a bulk request, per the standing Retell key rule). The page row shows "secure form sent" | Key not entered in 24 hours: first nudge naming the app and why it is needed. 72 hours: second nudge with the secure form re-sent. 5 business days: an internal oversight flag is raised; the app is treated as optional pending unless the agreement names it required, in which case the install record moves to `paused_human` (paused awaiting client) with the ask shown in the hub, not in a message a human must send |

### 2d. Seat stage (self-install in onboard.html; the full contract is Section 5.2)

| Event | System of record (exact field) | Orchestrator step | Automation that fires | Failure or abandonment recovery |
|---|---|---|---|---|
| `seat_bootstrap_delivered` (per lane: Claude and Grok; the Muse seat needs no client paste) | Hub: the per lane bootstrap package is generated from the current Team Pack and shown in the Seat section (copy block plus numbered paste path, Section 5.2). Manifest platform seats entry: `bootstrap_delivered_at`, `pack_version`, seat account label once known | Satisfies `seat.deliver_pack_claude` / `seat.deliver_pack_grok` on delivery plus the client's paste confirmation in the hub. The Muse seat is registered by `seat.register_muse_seat` directly | The hub Seat section unlocks per lane. No message leaves the hub; the client works at their own pace, and the drill is packaged with the bootstrap so verification starts the moment the paste lands | Package never opened: lifecycle nudges at 24 and 72 hours (Section 5.3). Opened but no drill return in 7 days: an internal oversight flag; the lane shows as still setting up on the page and the install continues on the verified lanes. Only the Muse lane is mandatory for go live, and it needs no client action |
| `seat_lane_verified` (per lane: the automated verification drill passed on a returned drill) | Manifest platform seats entry: the drill record from Section 5.2 (`drill.status = passed`, the four `drill.*_check` fields, `drill.attempts`, `drill.completed_at`, `pack_version`) | Completes `seat.drill_muse_lane`, `seat.drill_claude_lane`, or `seat.drill_grok_lane`. When all lanes are recorded on the same Pack version, `seat.publish_routing_table` completes and the state moves to `seated` | The hub seat card for that lane flips to Verified on the next projection push. When the stage completes, the hub shows the team seated confirmation in plain language (onboarding pack: three lanes named, what each is strongest at) | Drill fails on any named check (Section 5.2): the hub opens the guided retry loop, naming the failed check in plain language with the exact bootstrap section to re-paste; the client retries in the hub, attempts 1 to 3 fully self-serve. After 3 failed attempts: an internal oversight flag (`seat_drill_unresolved`) is raised, the lane is marked limited internally and receives no client work, and the install continues on the remaining lanes. The client sees "still setting up" with the retry path always open; nothing blocks visibly |

### 2e. Seed stage (onboard.html)

| Event | System of record (exact field) | Orchestrator step | Automation that fires | Failure or abandonment recovery |
|---|---|---|---|---|
| `knowledge_form_submitted` (onboard.html knowledge intake form) | The form payload is stored raw first (install intake log, same discipline as request intake), then mapped to the Client layer: `profile.md`, `people.md`, `brand.md`, and the quarantine list in `open-items.md` per the Section 5 field map. HighLevel contact notes are not a memory store and never receive this payload | Supplies the sponsor source for `seed.ingest_sources` and the facts that `seed.draft_client_layer_v1` must agree with; anything the client marks not publishable is evidence for `seed.strip_and_quarantine` | Sponsor acknowledgment on the page and by message: received, what the team does with it, when the review package arrives. Internal notice to the ops channel (form received, field count, no content) | Form not started 24 hours after the seat stage completes: first nudge. 72 hours: second nudge. Started and abandoned: the draft autosaves per section, and the 72 hour nudge deep links to the first incomplete section. Contradictions with ingested sources are not resolved by the form or by guessing: both values go to `open-items.md` with sources, per `seed.cross_check_facts` |
| `knowledge_review_ready` (system: the review package exists) | Client layer: review package path recorded in the manifest; Desk install project: client visible note carries the review link and `knowledge.review_state = awaiting_review` | Completes `seed.generate_review_package` | Sponsor message with the review package and the short open items list, in client language (onboarding pack). onboard.html knowledge card flips to "review ready" | Package cannot be generated because a source was unreachable: the gap is recorded in open items, the package ships with the gap stated, and affected roster capabilities are marked limited until the source is provided (spec Stage 4). A missing fact is never fabricated |
| `facts_self_confirmed` (onboard.html: the sponsor reviews the auto-seeded facts, corrects inline, answers open items, and confirms. This event replaces the old `knowledge_review_returned` event and the human review it fed) | Client layer: corrections applied to the v1 files; `open-items.md` updated (answered items closed with the sponsor's words, unanswered stay open with `confirmation_state` per item); manifest `knowledge.review_state = confirmed`, or `assumptions_flagged` on the outer timer path | Satisfies the sponsor half of the seed stage definition of done and the client side of the retired gate (Section 5.1); `seed.knowledge_drills` then runs per lane against the confirmed layer | Sponsor confirmation on the page: what their team now knows, in one short list. Internal notice: facts confirmed, correction count | Not confirmed on the Section 5.3 ladder (nudges at 24 and 72 hours, guided review mode in the hub): at the seed stage outer timer of 3 business days the install proceeds with unconfirmed facts carried as flagged assumptions. Client facing critical facts (names, prices, service claims) are never blocked on and never published either: the team does not use an unconfirmed claim in client facing work, the affected capability shows as limited on the team page, and the items appear in the first monthly owner report until confirmed. The page keeps showing "confirmation waiting" honestly until one of those outcomes lands. This replaces the blocking rule in pipeline spec Stage 4; see Section 5.1 |

### 2f. Go live and first value

| Event | System of record (exact field) | Orchestrator step | Automation that fires | Failure or abandonment recovery |
|---|---|---|---|---|
| `go_live_checklist_completed` (onboard.html: every client side item done, including the first request drafted and the heartbeat orientation viewed) | Desk install project: go live checklist items all marked done; manifest `sponsor_preconditions_met = true` with timestamp | Satisfies the sponsor preconditions for go live. Combined with `facts_self_confirmed` (or the flagged assumption path) it completes the client side of the retired gate (Section 5.1); no human approves anything | The hub advances to its final checks state; when the gate condition in Section 5.1 evaluates true, the orchestrator runs `go_live.final_verification_sweep`. The client sees "your team is doing its final checks" on the page, which is the true state | Checklist incomplete: nudges at 24 and 72 hours naming the exact remaining items in the hub; at 5 business days an internal oversight flag is raised. Unconfirmed critical facts constrain publishing, never progress (Section 5.1) |
| `go_live_gate_satisfied` (system event, no human actor: the Section 5.1 condition evaluates true) | Install state record: the legacy `qa_review` checkpoint is recorded automatically with actor `system:client-self-confirmation`, the confirmation event id (or the flagged assumption marker), and a timestamp. Audit log line appended | Opens the whole `go_live` stage: `go_live.final_verification_sweep` runs first | The go live stage executes in order. The client is not messaged at the gate; the next client visible event is `install_live` | Any final sweep check fails: the install returns to the responsible stage with the failing step identified; go live does not proceed on partial checks (spec Section 12). A failed heartbeat render holds go live on the retry ladder, because the page is part of the product promise; the client sees "final checks still running", never an error |
| `first_request_submitted` (home.html, or the go live checklist's first request item) | Raw payload stored in the install intake log first; then a Desk project created by the normal intake pipeline (status New, brief in the brief field, assignee by routing, source = the install's intake mode) | Triggers `go_live.create_first_project`; the project's Desk id is recorded as the step's produced object reference | Acknowledgment to the sponsor in their surface with the project reference (intake pipeline step 7). Internal notice to the ops channel. The same day completion directive applies from this moment | Malformed submission (empty description): held in New with a blocker note and one clarification request; never discarded (intake Adapter C rule). If the sponsor never submits a first request within 2 business days of live: one invitation message with two example requests from their own bottleneck answer on the application |
| `install_live` (system: install state reaches `live`) | Install state record and manifest final version (committed and read back). Desk install project: stage checklist complete, `client_summary` set to the live announcement | Completes `go_live.schedule_standing_loops`; the stage and the install are done | Fires, in order: heartbeat orientation message to the sponsor (`go_live.publish_heartbeat_page` evidence), go live invoice event to accounting (Section 2b), standing loops scheduled (intake sweep, watcher, weekly digest, monthly Pack update check), completion notice to the internal command channel with install_id, client_slug, Pack version, and the absolute go live date. home.html switches from onboarding mode to command mode | Any post-live loop fails to schedule: the install stays live (the client has a working team) but the failed loop raises an internal oversight flag the same day and is fixed under the oversight model, because a silent loop is how work gets lost |

## 3. Agreement and payment wiring

### 3.1 The agreement: generation and signature

The agreement is generated from the proposal record, never drafted by hand per client. The instrument is a mainstream electronic signature service with an API, envelope status webhooks, and a downloadable signed document with an audit certificate. The vendor is not yet selected; this contract binds to the capabilities (API generation, completion webhook, envelope status polling), not to a brand, so the wiring does not change when the vendor is chosen.

| Element | Contract |
|---|---|
| Generation trigger | The opportunity reaching Proposal exit in `AI Team - Sales` with all scope fields present (ops bridge required fields). Generation is automatic; a missing field blocks generation and names the field internally, it never produces a partial agreement |
| Template owner | Finn's lane owns the agreement template and its clauses; Sales owns the proposal data that fills it |
| Data in | Legal name, display name, signer name and email (from the application, Section 6.1), tier and scope, intake mode, seat model, first tools, install timeline wording from the onboarding pack |
| Terms carried | Install fee with the 50 percent start and 50 percent go live milestone structure; management fee and the initial term (three months after install, then month to month); the founding pilot rate lock clause where it applies; platform seats and usage as client owned pass through, never inside the management fee; the request overage block rule from the approved pricing |
| Amounts | Amounts exist in the agreement and in accounting only (Section 0). The envelope id, never an amount, is what other systems store: HighLevel field `agreement_envelope_id` |
| Signing | The signer signs by email link in the signature tool. No account creation is required of the client. Reminders run on the Section 2a ladder inside the tool |
| On completion | The tool's webhook fires `agreement_signed` (T0). The signed document is filed to the HighLevel client record automatically; once the Desk install project exists (T0 + 30 min) its link field points at that record. After provisioning, the manifest records the filed copy's pointer |

### 3.2 Invoices and payment tracking

| Invoice | Issued by | Trigger | Due | Tracked fields (accounting only) |
|---|---|---|---|---|
| Invoice 1: install start, 50 percent | Accounting system, automatically | T0 + 15 min (ops bridge step 2) | Per the agreement's payment terms | `invoice_id`, `milestone = install_start`, `status` (open, paid, overdue, void), `due_at`, `paid_at` |
| Invoice 2: install go live, 50 percent | Accounting system, automatically | The `install_live` event | Per the agreement's payment terms | `invoice_id`, `milestone = install_go_live`, `status`, `due_at`, `paid_at` |
| Management, monthly in advance | Accounting system, recurring schedule created at signature | The schedule in the agreement (first management period per the pilot or tier terms) | Monthly in advance | `invoice_id`, `milestone = management`, `period_start`, `status`, `due_at`, `paid_at` |

The Desk projection rule, exactly as the ops bridge sets it and this contract enforces it everywhere:

| Desk field | Legal values | Set by | Meaning |
|---|---|---|---|
| Install project `payment_status` | `paid` | The projection writer only | No due invoice is open |
| Install project `payment_status` | `issued` | The projection writer only | A due invoice is open and inside its reminder ladder |
| Install project `payment_status` | `attention` | The projection writer only | An invoice is overdue, or unpaid 72 hours after issue |

The projection writer is a single small component: it consumes accounting webhooks where the accounting tool offers them, and otherwise polls invoice status every 6 hours, and it is the only writer of the Desk field. Nobody edits `payment_status` by hand, and no process reads amounts from the Desk because none are there. The front end receives the same three values in the projection (Section 4) and renders `attention` only, with words and no numbers.

### 3.3 Provisioning on payment (the trigger contract)

Added 2026-11-04 with the self-serve direction. This section supersedes one ops bridge rule: the bridge said install work starts at T0 and does not pause for the first payment cycle. Under the self-serve contract, the client visible kickoff starts at T0 (agreement filed, invoice issued, welcome sent, hub unlocked, Desk install project created as the visible record), and the orchestrator's provision stage starts on payment. The reason is mechanical, not punitive: a zero touch system cannot have a human judging payment exceptions at the gate, so the gate is an event pair, not a judgment.

| Element | Contract |
|---|---|
| Trigger condition | Both events recorded, in either order: `agreement_signed` (envelope id known) and `start_payment_received` (invoice 1 paid). The later of the two fires the trigger. In the wired path the order is signature then payment, because invoice 1 only issues after signature; the trigger is defined order independently so a replayed or out of order webhook cannot break it |
| Trigger handler | A single idempotent handler in the endpoint service (Section 7, build item 3). On firing, it invokes the orchestrator run for the install |
| Trigger idempotency key | `provision-trigger:{agreement_envelope_id}`. The handler records this key on the HighLevel opportunity and in the install state record before minting anything. A second delivery of either event finds the key and is a no-op |
| Install id minting | `install_id` is minted once, at `agreement_signed`, and recorded against the trigger key. If the handler runs again it recovers the same `install_id`; it never mints a second one |
| First step key (engine format, from state.py) | `<install_id>:provision:create_client_layer:memory/muse/clients/<client_slug>`. Every later step carries its own key in the same format, so a trigger replay converges on the engine's check before create discipline and can never duplicate a Desk workspace, channel, or roster |
| Client visible state before the trigger | The hub shows one honest line: agreement signed, start payment pending, and what happens the moment it lands. The connect checklist is visible but locked, because its rows write into a Desk workspace that does not exist yet |
| Payment never lands | The Section 2b ladder runs (reminders at 24 and 72 hours, `attention` at 72 hours, oversight flag at 7 days). The install intent record stays; nothing is provisioned, nothing is owed beyond the agreement, and if the payment lands at any later date the trigger fires then. No human chases, decides, or provisions by hand |

## 4. The connect-state truth rule

This rule is absolute and the front end build must treat it as such: **a tool counts as Connected only when the orchestrator's verification for that connector passes. A client click is never evidence of connection.**

### 4.1 Per row states

Each connect row (one per tool) carries exactly one state at a time, stored on the manifest connected apps entry and projected to the hub:

| State | Set by | Meaning |
|---|---|---|
| `not_started` | System | The row exists; the client has not begun it |
| `awaiting_client` | System | The row's action (OAuth tap or secure form) is the next step and the client has not completed it |
| `authorizing` | The callback arriving | The client completed the tap or the key entry; verification has not run yet. This is the highest state a client action can produce |
| `verifying` | The orchestrator | The status check and the harmless read are running |
| `connected` | The orchestrator, only | Verification passed. The manifest entry holds `verified = true` and `verified_at`. See 4.2 |
| `pending_retry` | The orchestrator | Verification hit a transient failure or a provider 429. A retry is scheduled on the spec ladder. The client sees "we will check again automatically" |
| `failed` | The orchestrator | Verification failed three times, or the connector answered with a hard error. A reason code lives in the manifest; the client sees plain words and the retry action |
| `needs_human` | The orchestrator | The connected account label does not match the agreement. The client sees the expected account named and a reconnect action. The name is historical: no UpSurge human is involved; it means the row needs the client's correction (see Section 5.1 on legacy state names) |
| `awaiting_key` | System | API key apps only: the secure capture form is the next step |
| `deferred` | The client | The client used the simplified path to defer an optional app to post-live (Section 5.3). The manifest lists it as pending with the client as owner |
| `not_applicable` | System | The agreement does not include this tool |

### 4.2 What verification is

For each connector, verification is the pair the pipeline spec Stage 2 defines, executed by the orchestrator's connector adapter: (1) the connector's own status check passes against the account the client just authorized, and (2) one harmless read (a list or a single record read, named per connector in its connector doc) returns successfully against that account. Both must pass, the account label must match the agreement, and the result is recorded with a timestamp before the row may show Connected. The primary CRM has the additional end to end check from the spec (read one pipeline or list; confirm the write path exists where the agreement requires it; record the location or account ids, which are identifiers, not credentials).

Truth is continuous, not a one time badge: the standing loops re-run a light health check per required connector after go live. A connector that later fails degrades its row to `pending_retry` and, if it stays failed, to `failed` with a reconnect action in home.html. The hub never displays a Connected state that the manifest does not currently hold.

### 4.3 How the front end learns the true state

The front end never writes connect state, seat state, or install state. It renders one object, the client projection, which the service owns:

| Channel | Contract |
|---|---|
| Pull | `GET /api/installs/{install_id}/projection` on the endpoint service returns the projection below. onboard.html and home.html poll it every 30 seconds while open and any section is non terminal, and stop polling when everything is terminal (live, or every row in a resting state) |
| Push | The status callback endpoint registered by `provision.register_webhooks` POSTs the full projection, plus `changed_keys` (the list of projection paths that changed), to the front end host on every state change. Push is an optimization; pull alone is always sufficient and always correct |
| Versioning | The projection carries `state_version`, a monotonically increasing integer from the install state record. A response whose `state_version` is not newer than the one on screen is discarded without rendering |
| Demo mode | onboard.html's localStorage demo state lives under the key `ait_demo_projection_v1` and holds exactly this shape. The demo driver mutates the stored object on timers; the components cannot tell demo data from live data, which is the point: one rendering path, two sources |

### 4.4 The projection shape (field names are contractual)

```json
{
  "install_id": "string",
  "client_slug": "string",
  "state_version": 0,
  "updated_at": "ISO 8601",
  "stage": {
    "key": "provision | connect | seat | seed | go_live | live",
    "label": "string, client language",
    "steps_done": 0,
    "steps_total": 0,
    "percent": 0
  },
  "client_action_needed": "string or null, one exact next action in plain words",
  "payment_status": "issued | paid | attention",
  "connect": [
    {
      "key": "gmail | google_calendar | google_drive | ghl | string per connector",
      "label": "string, business language (Email, Calendar, Files, CRM)",
      "state": "one of the Section 4.1 states",
      "verified_at": "ISO 8601 or null",
      "action": { "type": "oauth | secure_form | reconnect | none", "label": "string", "url": "string or null" }
    }
  ],
  "seats": [
    {
      "lane": "muse | claude | grok",
      "leader": "Maive | Marcus",
      "state": "not_started | bootstrap_ready | awaiting_drill | verifying | verified | retry_guided | still_setting_up",
      "pack_version": "string"
    }
  ],
  "knowledge": {
    "form_state": "not_started | in_progress | submitted",
    "review_state": "not_ready | awaiting_confirmation | confirmed | assumptions_flagged",
    "open_items_count": 0
  },
  "go_live": {
    "checklist": [ { "key": "string", "label": "string", "done": false } ],
    "final_checks_state": "not_started | running | passed | retrying",
    "live_at": "ISO 8601 or null"
  }
}
```

Internal detail never enters the projection: no error codes, no step keys, no manifest paths, no amounts, no flag data. The projection is a client surface and follows the spec's rule that client visible status is a simplified, honest projection of the state machine.

## 5. The self-serve contract

Austin's direction, 2026-11-04: onboarding is fully self-serve with a zero touch target for UpSurge. This section is where that direction becomes mechanics. It supersedes the pipeline spec and the ops bridge wherever they conflict, and the conflicts are named, not hidden.

### 5.1 The gate change: from blocking human review to client confirmation plus sampling

**The change, named.** The install pipeline spec (Sections 10 and 12) placed a single human gate before go live: an UpSurge approver (Austin or his delegate) records a QA approval on the install record, and go live cannot start without it. That gate is retired for client installs. In its place:

1. **The client's own self-confirmation of the auto-seeded facts in the hub** (`facts_self_confirmed`, Section 2e). The facts only the client can judge (are these our services, our people, our claims) are confirmed by the only party who actually knows them.
2. **The automated final verification sweep** (`go_live.final_verification_sweep`): one read check per required system, a ping task per lane, the Desk test pattern verified, the heartbeat page rendered against live data. The mechanics only systems can judge are judged by systems, on every install, identically.
3. **Post-live QA sampling under the oversight model** (product/oversight-model.md): deliverables are sampled after delivery at the tier rate (10, 20, and 35 percent) with graded fail responses. Judgment QA still happens; it just stops being a tollbooth in front of every install.

**The rationale.** A blocking human gate makes every install wait on UpSurge's calendar, which breaks the self-serve promise on day one and does not scale past a handful of installs. It also misassigns the verification: a human approver at UpSurge cannot confirm a client's facts better than the client, and a human cannot re-check every connector more reliably than the sweep that actually calls them. Confirmation by the owner of the facts, verification by the systems themselves, and sampling for judgment is the stronger control, not the weaker one.

**How the engine records it.** state.py keeps the checkpoint name `qa_review`; this contract does not fork the state machine. Under this contract the checkpoint is satisfied automatically when all three hold: the go live checklist is complete, and `facts_self_confirmed` is recorded (or the flagged assumption path in 5.1.1 has run), and the final sweep passes. The orchestrator records the checkpoint with actor `system:client-self-confirmation` and the confirmation event id, and the `go_live` stage opens. No human runs an approve command for a client install. (The manual approve path still exists in the CLI for UpSurge's own internal installs and testing, and is never part of a client journey.)

**Legacy state name.** The state machine's `paused_human` state predates this contract. For client installs it is read as **paused awaiting client**: the install is waiting on a client act that only the client can perform (an OAuth tap, a key entry, a confirmation). It never means an UpSurge person is working on it, and the client projection never uses the word human for it; it shows the exact action needed.

#### 5.1.1 Flagged assumptions (the no-block path for unconfirmed facts)

If the confirmation does not arrive by the seed stage outer timer (Section 5.3), the install proceeds and the unconfirmed facts are carried with `confirmation_state = assumed` in `open-items.md`:

- Assumed facts are usable for internal work (routing, drafting, preparation).
- An assumed client facing claim (a name spelling, a price, a service claim) is **not usable** in anything the client's customers would see. The team works around it or leaves the gap visible; it never publishes an unconfirmed claim.
- Capabilities that depend on assumed facts show as limited on the team page until confirmation lands.
- The facts card persists in home.html after go live. The client can confirm or correct at any time; confirmation clears the limitation on the next projection and closes the items.
- The assumed items appear in the first monthly owner report (oversight model) until they are confirmed, so nothing rides as an assumption forever in silence.

### 5.2 The seat self-install contract

No API exists to push instructions into a client owned Claude or Grok account (pipeline spec Section 11). The old answer was a guided paste performed with an operator nearby. The self-serve answer is that the hub itself is the guide, the drill is the proof, and the loop is closed without a human on either side of the glass.

**Delivery (what the hub hands the client), per lane (Claude and Grok):**

| Package element | Contents |
|---|---|
| The copy block | One single block per lane, generated from the current Team Pack version: the roster and lane identity, routing rules and claim protocol, house style, the execution brief standard, the pointer to this client's Client layer, and the drill instructions. Generated, never hand edited per client, so every install drills against the same Pack |
| The paste path | Numbered steps written for a non technical owner: open the platform, open its project or instructions surface (named per platform in the package), paste the block, save. Three to five steps, each one line |
| The drill task | A synthetic, client safe task embedded at the end of the copy block: summarize the client profile back to the delegator, in the handoff packet format, using the Client layer facts only |
| The return path | Named inside the package. Where the seat's platform has a connected surface back to the service, the drill answer returns through it. The universal fallback, always offered, is the hub's paste back field for that lane, labeled in client language ("paste your team's reply here") |

The Muse seat needs none of this: it is registered by the orchestrator against the connected Muse environment (`seat.register_muse_seat`) and drilled by the system directly.

**Return handling.** A drill return is stored raw in the install record before any scoring (the same raw first discipline as request intake). The scorer then runs four automated checks against the Client layer and the Pack. The results are recorded per lane, in the manifest seats entry and mirrored in the install state record, under these exact field names:

| Field | Type | Values |
|---|---|---|
| `drill.status` | string | `not_started`, `awaiting_return`, `passed`, `retrying`, `unresolved_flagged` |
| `drill.facts_check` | string | `pass` or `fail`: every fact in the return matches the Client layer; nothing invented |
| `drill.format_check` | string | `pass` or `fail`: the return follows the handoff packet format |
| `drill.isolation_check` | string | `pass` or `fail`: nothing in the return comes from any other client or from outside this install's facts |
| `drill.language_check` | string | `pass` or `fail`: no internal process language; house style held |
| `drill.attempts` | integer | Count of scored returns for this lane |
| `drill.last_error` | string | Client safe summary of the failed checks on the latest attempt (for example "quoted a fact that is not in your business profile") |
| `drill.completed_at` | timestamp or null | When `drill.status` became `passed` |
| `pack_version` | string | The Pack version the lane drilled against |

**Pass.** All four checks pass: `seat_lane_verified` fires, the step (`seat.drill_claude_lane` or `seat.drill_grok_lane`) completes with the drill record as its produced reference, and the hub card flips to Verified.

**Fail: the guided retry loop.** On any failed check, the hub responds in the same session, in plain language: which check failed, what that means in one sentence, and the exact bootstrap section to re-paste (the package is sectioned for this: facts, format, isolation, style). The client re-pastes that section in their seat and returns a fresh drill, or uses the paste back field again. Attempts 1 to 3 are fully self-serve with no lockout and no penalty; the client can also retry later from the same card, which keeps its state.

**After 3 failed attempts.** An internal oversight flag is raised: `seat_drill_unresolved`, carrying the lane, the drill record, and the attempt history. The lane is marked limited internally and receives no client work. **Nothing blocks visibly.** The hub card reads "still setting up" with the retry path open, the other lanes proceed, and go live is not held by a Claude or Grok lane. The flag is worked asynchronously under the oversight model; if it is ever resolved by a Pack improvement, the improvement ships to every install as a Pack update, which is how one client's drill trouble makes the fleet better.

### 5.3 Stall detection and automated rescue

**Detection.** The orchestrator's state record timestamps every stage opening and every step completion. A stall scanner (a standing loop on the same pattern as the intake sweep and watcher already in production) evaluates open installs hourly and applies the timers below. A stall is a stage open past its first timer with required progress missing. System stalls (a step failing inside a stage with no client action involved, for example in Provision) skip the client ladder entirely: the retry policy runs, and exhaustion raises an internal flag immediately.

**Timers per stage** (measured from the event that opened the stage):

| Stage | First nudge | Second nudge | Oversight flag | Notes |
|---|---|---|---|---|
| Provision | none (no client action exists) | none | On retry exhaustion of any step | System stall path only |
| Connect | 24 hours from checklist live | 72 hours | 5 business days | Required rows only; optional rows never stall a stage |
| Seat | 24 hours from bootstrap delivery, per unfinished lane | 72 hours | 7 days, per lane | A verified lane stops its own timers |
| Seed (form) | 24 hours from seat completion | 72 hours | 5 business days | Draft autosave means a started form is never lost progress |
| Seed (confirmation) | 24 hours from review ready | 72 hours | At 3 business days the flagged assumption path runs instead (5.1.1); the flag is informational | Confirmation is the one timer that resolves by proceeding, not by waiting longer |
| Go live checklist | 24 hours from `seeded` | 72 hours | 5 business days | Names the exact remaining items |
| Start payment (pre-provision) | 24 hours from invoice issue | 72 hours | 7 days | Governed by Section 3.3; the hub state line is the guidance |

**The rescue ladder** (in order, all automated, per stalled item):

1. **In-hub guidance.** The stalled section becomes the hub's top card: the single next action named, one line on why it matters, and the exact tap, field, or paste that completes it. Nothing else on the page competes with it. Most stalls are a client who could not see the next step, and this rung exists for them.
2. **Lifecycle nudges at 24 and 72 hours.** Sent in the client's chosen surface and by email, from the approved templates, deep linked by signed resume link to the exact section and item. One message per timer per item, never more frequent, never a sequence beyond the second nudge. The nudge names the action and the payoff, never the delay.
3. **Simplified retry path.** Every stalled item offers a reduced way through: connect one tool now and defer the optional rest to post-live with one tap (manifest records them pending, client owned, and they appear in the first monthly owner report); confirm the seeded facts in bulk with only the exceptions listed for editing; return the drill by paste back instead of re-running any setup; complete the go live checklist's first request later from home.html. A deferred item is a recorded decision, not a failure.

**The oversight flag point.** A flag is raised when the second nudge has fired and the stage's outer timer expires, or immediately for system stalls and the drill unresolved case. A flag carries: `install_id`, `client_slug`, stage, stall type, the timers fired, and the client visible state at flag time. Flags land in the internal oversight queue and are worked under the oversight model (weekly fleet review; the red flag list for the urgent classes). The flag changes nothing for the client: the hub keeps its state, the retry paths stay open, and if the client acts a week later the install resumes from exactly where it waited, because resume is a property of the state record, not of anyone's memory.

## 6. Data contracts: the forms

The front end and the service agree on these fields exactly. A field name here is the wire name in the POST payload, the stored name in the receiving system, and the name in any error message. Types are validated twice: the page validates presence and format for the client's sake, and the endpoint validates everything again, because the page is never trusted.

Shared rules for both forms:

- The raw payload is stored unchanged before any mapping runs (apply: the HighLevel application record; knowledge: the install intake log). Mapping reads the raw record, never the live request.
- Unknown fields are preserved in the raw record and ignored by mapping. Missing optional fields are stored as null, never as empty guesses.
- Every submission returns the same response shape: `{ "ok": true or false, "reference_id": "application_id or install_id", "next_step": "string, client language", "next_url": "string or null", "field_errors": { "field_name": "plain language problem" } }`.
- Timestamps the client generates are advisory; the server stamps receipt time and that is the time of record.

### 6.1 The apply form (apply.html) delivers

| Field | Type | Required | Lands in |
|---|---|---|---|
| `business_legal_name` | string | yes | InstallContext `legal_name`; agreement data in; manifest identity |
| `business_display_name` | string | yes | Desk client record label; hub and heartbeat display name |
| `website_url` | string (URL) | yes | HighLevel opportunity `website`; seed source list for `seed.ingest_sources` |
| `sponsor_name` | string | yes | InstallContext `sponsor_name`; HighLevel primary contact |
| `sponsor_email` | string (email) | yes | InstallContext `sponsor_email`; HighLevel primary contact; signer email for the agreement |
| `sponsor_phone` | string | no | HighLevel contact only |
| `timezone` | string (IANA name, page pre-fills from the browser) | yes | InstallContext `timezone`; all install timestamps and nudge timing |
| `industry` | enum: `real_estate`, `insurance`, `education`, `home_services`, `professional_services`, `other` | yes | HighLevel opportunity; qualification scorecard input |
| `current_crm` | enum: `highlevel`, `hubspot`, `salesforce`, `zoho`, `pipedrive`, `other`, `none` | yes | Resolves InstallContext `crm_connector` where a connector exists; `other` or `none` produces a manual access entry in the manifest instead (no connection flow is invented, per spec Stage 2) |
| `tools_in_use` | array of enum: `gmail`, `google_calendar`, `google_drive`, `google_docs`, `google_sheets`, `slack`, `meta_ads`, `vercel`, `phone_system`, `other` | yes (may be empty array only if `current_crm` is also `none`, otherwise at least one) | The connect checklist composition for `connect.present_checklist`: required rows from the agreement stack first, these as the expected set |
| `intake_mode` | enum: `surge-form`, `direct`, `pm-system` (the state.py values) | yes | InstallContext `intake_mode`; decides which intake adapter `go_live.enable_intake_adapters` turns on |
| `pm_system_name` | string | required when `intake_mode` is `pm-system` | Manifest intake adapter record; webhook or poll pattern chosen from it |
| `tier_interest` | enum: `pilot`, `launch`, `growth`, `full` | yes | HighLevel opportunity; the proposal and agreement scope |
| `seat_preference` | enum: `client-owned`, `upsurge-managed`, `undecided` | yes | Input to `seat.record_seat_model`; the agreement records the final model and the step records that, not the preference |
| `submitter_count_estimate` | integer (1 or more) | yes | HighLevel opportunity required field; Desk workspace expectations |
| `monthly_request_volume_estimate` | integer | no | HighLevel opportunity; tier fit check against the tier's included requests |
| `biggest_bottleneck` | string (long text) | yes | The diagnostic wedge: Desk install project context, and the seed for the first project suggestions at go live |
| `source` | string (the page sets it from the entry channel) | yes | HighLevel tag `ait-source-[channel]` |
| `utm_source`, `utm_medium`, `utm_campaign` | string | no | HighLevel contact and opportunity attribution fields |
| `terms_acknowledged` | boolean (must be `true` to submit) | yes | Application record with `terms_acknowledged_at` (server stamp). This acknowledges the pilot terms summary shown on the page; it is not the agreement and does not replace signature |
| `privacy_acknowledged` | boolean (must be `true` to submit) | yes | Application record with its server stamp |

Agreement with the service: on signature, the install's identity is built from `business_legal_name`, `sponsor_name`, `sponsor_email`, `timezone`, `intake_mode`, the resolved `crm_connector`, and the agreement's seat model. If the agreement and the application disagree (a term negotiated between), the agreement wins and the difference is recorded in the manifest identity notes.

### 6.2 The knowledge form (onboard.html) delivers

Submitted once, editable per section until `facts_self_confirmed`; the seed stage reads the latest stored version. The form's job is to hand `seed.ingest_sources` and `seed.draft_client_layer_v1` the facts that crawling cannot know, and to mark what must never be published so `seed.strip_and_quarantine` has the client's own word for it.

| Field | Type | Required | Feeds (Client layer target) |
|---|---|---|---|
| `business_summary` | string (long text) | yes | `profile.md`: what the business does, in the owner's words |
| `offers` | array of objects: `name` (string), `description` (string), `publishable` (boolean) | yes (at least one) | `profile.md` offers; any offer with `publishable = false` also lands on the quarantine list in `open-items.md` and is never used in client facing work |
| `service_area` | string | yes | `profile.md` |
| `operating_hours` | string (day ranges with times, format shown on the page) | yes | `profile.md` |
| `decision_makers` | array of objects: `name` (string), `role` (string), `email` (string) | yes (at least one) | `people.md` |
| `key_contacts` | array of objects: `name` (string), `role` (string), `contact` (string) | no | `people.md` |
| `brand_assets_url` | string (URL) | no | Ingest source for `seed.ingest_sources` (brand files) |
| `brand_voice_notes` | string (long text) | no | `brand.md` voice rules |
| `banned_phrases` | array of strings | no | `brand.md` banned phrases |
| `approved_claims` | array of strings | no | `brand.md` approved claims list. The rule the seed stage applies: a claim not on this list and not confirmed elsewhere is not publishable |
| `do_not_publish` | string (long text) | no | The quarantine list in `open-items.md` verbatim (rates, internal terms, anything the client names). Quarantined content is listed by category in memory, never copied into memory content (spec Stage 4) |
| `existing_sops_url` | string (URL) | no | Ingest source for `seed.ingest_sources` (documents) |
| `open_items_answers` | object: map of open item id (string) to answer (string) | no | Closes the matching items in `open-items.md` with the sponsor's words; unanswered ids stay open |

The confirmation itself is not a form field. It is the `facts_self_confirmed` event (Section 2e), fired by the hub's confirm action after the review package renders, and recorded with the package version it confirms, so a later package version does not silently inherit an earlier confirmation.

## 7. What is live today, what is stubbed, and the build order

Honest as of 2026-11-04. Nothing in outbound copy may claim a stubbed item is live; the sales bridge's rule stands until this section says otherwise.

### 7.1 Live today

| Capability | State |
|---|---|
| Desk reads and writes through the Lovable database path (install project create, checklist and status updates, `payment_status` writes, brief and client summary fields) | Live, in production use |
| GitHub writes for the Client layer and the manifest, with read back verification of every push | Live |
| Slack internal notices and channel creation | Live |
| Connector verification for the connected set (Gmail, Google Calendar, Google Drive, Google Docs, Google Sheets, Slack, HighLevel, Lovable, Vercel, GitHub; Meta Ads reads gated on the advertiser's consent tap) | Live: status check plus a harmless read per app |
| Scheduled sweeps and watchers on the cron and hook patterns (the stall scanner in Section 5.3 is this same pattern) | Live as a pattern |
| The orchestrator core: state machine, the 33 steps in state.py, idempotency, runner lock, retry ladder, resume, append only audit log | Built and dry run verified end to end (initiated to the gate, approval, live; 47 audit entries) |
| The heartbeat team page package (migrations, roster seed, components, realtime hook) | Built as code in this repo (app/team-page/); not yet dropped into the Command App template |
| The marketing site (index.html) with approved pricing | Built in this repo (site/) |

### 7.2 Stubbed or not built

| Item | State |
|---|---|
| The orchestrator's live adapters (Desk, GitHub, Slack, Connectors in adapters.py) | Typed stubs that name the exact real call each method wraps. The CLI refuses live mode until they land |
| book.html, apply.html, onboard.html, home.html | In build now; index.html exists. onboard.html currently demonstrates state in localStorage; the live projection wiring is Section 4 and build item 6 below |
| Form endpoints (apply POST, knowledge POST) and the projection endpoint | Not built. Today the forms would have nowhere to send |
| The provisioning trigger handler (agreement plus payment, Section 3.3) | Not built |
| The HighLevel `AI Team - Sales` pipeline, its stage workflows, and the lifecycle nudge workflows | Specified in the ops bridge; not yet built in the account |
| The agreement instrument | Vendor not selected; the template is Finn's to finalize. This is the one decision shaped blocker left in the chain |
| Accounting wiring (invoice triggers, the `payment_status` projection writer) | Not built. Today invoicing and the Desk field are runbook steps, done by hand |
| The drill scorer (Section 5.2 checks) and the bootstrap package generator | Not built. Today a drill would be scored by an agent reading the return, which is concierge mode, not the contract |
| The automated gate recording (actor `system:client-self-confirmation`, Section 5.1) | Not built; the engine's manual approve path is what exists |
| The stall scanner loop and the oversight flag queue surface | Not built; the patterns they copy are live |
| The intake webhook receiver for `pm-system` mode | Not built (spec Section 11, item 4). `surge-form` and `direct` modes do not need it |
| Per client Desk clone path | Not built; installs use per client rows in one Desk until it is (spec Section 11, item 2) |
| Claude and Grok seat bootstrap API | Does not exist on those platforms. The self-install contract in Section 5.2 is the durable answer, not a stopgap |

### 7.3 Build order to wire it

Ordered so each step unblocks the next, and the pilot can run concierge style on the finished parts while the rest lands:

1. **HighLevel pipeline build.** The `AI Team - Sales` stages, required fields, tags, and the workflows behind Sections 2a and 5.3 (acknowledgments, reminders, nudge ladders, signature filing). Everything downstream keys off opportunity and stage data; build it first.
2. **Agreement instrument and template.** Select the signature vendor against Section 3.1's capability list, finalize Finn's template, and wire the completion webhook to the event bus the trigger handler will read.
3. **Endpoint service.** The form POSTs (Section 6), the provisioning trigger handler (Section 3.3), and the projection endpoint with the status callback push (Section 4). This is the intake receiver pattern from the spec, grown to serve the front end.
4. **Accounting wiring.** Invoice triggers at T0 and at `install_live`, the recurring management schedule, and the `payment_status` projection writer (webhook if offered, 6 hour poll otherwise).
5. **Orchestrator live adapters.** Desk first, then GitHub, Slack, Connectors, each verified against a real pilot install's manifest. In the same step: the automated gate recording (Section 5.1) and the stall scanner loop with its flag queue (Section 5.3).
6. **Hub completion.** onboard.html driven by the live projection instead of the demo driver (same shape, Section 4.4); the bootstrap package generator and drill scorer (Section 5.2); the facts self-confirmation surface with the flagged assumption mechanics (Section 5.1.1); home.html command mode with the persistent facts card.
7. **Desk checklist sync.** Orchestrator stage transitions write the Desk install project's checklist items and `client_summary` automatically (rides the Desk adapter from step 5), so the internal board and the client's hub can never quietly disagree about where an install stands.

Until items 1 to 5 land, installs run in concierge mode: an operator executes this same contract by hand and by agent, the client experience is the hub in demo driven form plus human sent messages that follow the same templates, and the honest label for that mode, anywhere it is described, is supervised automation. The self-serve contract above is the target the builds are wiring to, in this order, and the pilot is the install that proves each item as it lands.
