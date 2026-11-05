# The App Census: Finding Every App Before We Connect Anything

Status: v1, 2026-11-04
Owners: Owen (onboarding-orchestrator) with Diego (crm-architect), for Maive (delegator of record)
Companion documents: wiring-contract.md (the census section is Section 4.5; this document is the source of truth for census fields and step IDs), product/onboarding-simple-standard.md (every client facing word here follows it), platform-policy.md (which standard we set up for a client who has none, per function)

## 0. What the census is and why it exists

A setup is only complete when every app and platform the business uses, or needs, has been found and dealt with. A connection list written in advance from the agreement cannot promise that: the agreement names the stack we sold, not the full stack the business actually runs on. The business also runs on the booking widget a cousin installed, the invoicing app the bookkeeper chose, and the spreadsheet nobody mentioned.

The App Census is the completeness guarantee. During the Connect stage, before the verify steps run, the service builds one list of every app that matters to this business: from the client's own answers, from what their website and their already connected tools reveal, and from the standard the service sets up when a function is missing entirely. Every item on that list ends in a recorded decision. Nothing is quietly skipped, and nothing waits on a human at UpSurge: the census, the connections, and the decisions all run inside the self-serve flow the wiring contract defines.

The client never hears the word census. In the hub it is simply their list, under the heading "Your apps," in their words (wiring contract Section 4.5).

## 1. The census questions

One question per function, asked in the hub at the start of the Connect stage, one at a time, with what we already know filled in for a quick yes or a fix (the Simple Standard: no step asks for what the system can find itself). The whole list takes about 3 minutes. Each question names the function in the client's words; the business type pack may substitute the words that business uses (a brokerage hears "client list," a clinic hears "patient list") without changing the function underneath.

| # | Function (record value) | The one question we ask | Common answers and the tools they map to |
|---|---|---|---|
| 1 | `customer_system` | "Where do you keep the names of your customers, and how do you follow up with them?" | HighLevel, HubSpot, Salesforce, Zoho, Pipedrive, Keap, Follow Up Boss, Lofty, another named tool, a spreadsheet, on paper or in their head, none yet |
| 2 | `email` | "What do you use for email?" | Gmail or Google Workspace, Outlook or Microsoft 365, another named mail service |
| 3 | `calendar` | "What calendar runs your appointments?" | Google Calendar, Outlook Calendar, Calendly, Acuity Scheduling, the calendar inside their customer system, paper diary |
| 4 | `phones_texts` | "What do customers call or text to reach you?" | HighLevel phone, RingCentral, OpenPhone, Dialpad, Grasshopper, Vonage, a cell phone, a landline with a phone company |
| 5 | `files_photos` | "Where do your files and photos live?" | Google Drive, Dropbox, OneDrive, Box, iCloud, a computer folder only |
| 6 | `money_invoices` | "How do you send invoices and take payment?" | QuickBooks, Stripe, Square, Xero, FreshBooks, Wave, the invoicing inside their customer system, paper invoices |
| 7 | `ads_social` | "Where do you advertise, and where do you post?" | Meta ads (Facebook and Instagram), Google Ads, TikTok, LinkedIn, no ads yet; and the social accounts themselves: Facebook page, Instagram, LinkedIn, YouTube, TikTok |
| 8 | `website` | "Where does your website live?" | WordPress, Squarespace, Wix, Lovable, GoDaddy, a custom build, no website yet |
| 9 | `work_board` | "Where do you keep track of jobs and who is doing what?" | The answer is almost always their command center, which ships with this service and is set up in the Provision stage. Existing boards they name are recorded here too: Asana, Trello, Monday, ClickUp, Notion, a whiteboard |
| 10 | `weekly_other` | "What else do you open every week to run the business?" | Free words. Common answers: Slack, Zoom, Canva, DocuSign or another signing tool, and the trade specific tools their kind of business names (the type pack lists the usual ones for that business) |

Rules for the answers:

- A named tool becomes a census row with that tool. "A spreadsheet," "on paper," or "none yet" becomes a census row for the function with no tool, which is exactly the row the policy in Section 3 resolves by setting up the standard.
- An answer we do not recognize is recorded in the client's own words as the tool name. It is never dropped for being unfamiliar, and no connection flow is invented for it: it follows the manual access pattern the wiring contract already defines for unrecognized tools (recorded, worked around, never faked).
- The application form's `tools_in_use` and `current_crm` (wiring contract Section 6.1) pre-fill questions 1 to 8. The census confirms them; it does not ask twice.

## 2. Detection signals: rows we add without asking

Answers miss things. Three signals add rows on their own, each recorded with its source in the row's `note` so the client can see why an app appeared on their list.

| Signal | What it finds | When it runs |
|---|---|---|
| Website scan | Booking widgets (a Calendly, Acuity, or customer system booking embed), chat widgets, and form handlers (the service a website form sends to) found on the client's website. Each one names a tool the business already depends on | During census seeding, against the `website_url` from the application; and again inside `seed.ingest_sources`, whose findings re-enter through `census.apply_detections` (Section 5) |
| Tools named in mail | **Phase two.** Tools named in the sponsor's email receipts, invoices from software vendors, and signature blocks would add rows for paid tools nobody listed. This needs the connected mailbox to be scanned, which is a later build; it is named here so the record format already has a place for it, and it is not part of the v1 completeness rule | Phase two, after `connect.verify_email`, behind the same consent as the connection itself |
| The shape of tools already connected | A connected tool that bundles a second function (a customer system that also runs the phones, an accounting tool that also sends the invoices) adds the bundled function as a row pointing at the same tool, so the function is counted once and the tool is connected once | Continuously during the Connect stage, as each verify step completes |

Detection never connects anything by itself. A detected row is a question the list asks on the client's behalf; it resolves the same way an answered row does.

## 3. The census record

### 3.1 One row per app

The census lives in the install manifest as the `census` array. One row per discovered app, with exactly these fields:

| Field | Type | Meaning |
|---|---|---|
| `function` | string | One of the Section 1 record values: `customer_system`, `email`, `calendar`, `phones_texts`, `files_photos`, `money_invoices`, `ads_social`, `website`, `work_board`, `weekly_other` |
| `tool_name` | string | The tool's own name as the client uses it ("HighLevel," "QuickBooks," "a spreadsheet"), or the standard's name when we set it up for them |
| `state` | string | Exactly one of the four states in Section 3.2. A row with no state yet is unresolved (Section 4) |
| `owner` | string | Who does the work on this row: `client` (their tap connects it) or `upsurge` (we set it up or connect it for them) |
| `note` | string | One short line: where the row came from ("you told us," "found on your website," "your QuickBooks also sends your invoices"), or, for a Coming next row, the week it is scheduled for |

The connection mechanics for a row (the tap, the check, the retries) live in the wiring contract Section 4.1 states on the manifest connected apps entry for the same tool. The census state is not a second connection state; it is the decision about the row. The two meet at one point only: a census row may not read Connected until the Section 4.1 verification for that tool has passed.

### 3.2 The four states

| State (stored value, exact) | What it means | Who gets there |
|---|---|---|
| `Connected` | The tool is connected and the orchestrator's verification passed (wiring contract Section 4: status check plus one harmless read, account label matching). A client's tap alone never produces this state | The orchestrator, only |
| `Set up for them` | The business had no tool for this function, or chose the standard, so we provision the standard for that function under platform-policy.md and connect it. For the `customer_system` function the standard is HighLevel. The row counts as resolved when the provisioned system is in place; its Connected standing still follows the same verification rule as every other row | UpSurge, by the policy, with the client's choice recorded in the row |
| `Coming next` | Deliberately scheduled after go live, with the week recorded in `note` (for example, "week 2 after go live"). A plan, not a gap: the row is resolved, dated, and resurfaces in the first monthly owner report until it lands | The census resolution step (Section 4), or the client deferring with one tap |
| `Not needed` | The client said skip this one. Recorded with their words in `note`, so a later "why is this not connected" always has its answer | The client, only |

### 3.3 What the client sees

In the hub, each row renders in the client's words: the function the way their business says it, the tool's own name, one plain state word (Connected, Set up for you, Coming next, Not needed), and the single action left if one exists. The full rendering rule is wiring contract Section 4.5.

## 4. Resolution and the completeness rule

`census.resolve_rows` (Section 5) walks the list and brings every row to one of the four states:

1. Rows the client connects in this stage verify and read `Connected`.
2. Rows with no tool, or where the client picks the standard, resolve to `Set up for them` under platform-policy.md.
3. Rows the client defers, and rows past the tier's included count (below), resolve to `Coming next` with a week.
4. Rows the client declines resolve to `Not needed`.

**The included app count.** Rows in `Connected` and `Set up for them` count toward the tier's included app count: Launch Team 5, Growth Team 10, Full AI Organization 18 (founding pilot installs use the count written in their agreement). Rows are counted in census order, which is the order that matters to the business: customer system first, then email, calendar, phones and texts, and the rest in the Section 1 order. When the count is reached, any further row that would connect in this stage defaults to `Coming next` rather than being dropped, so the plan stays complete even when the connections phase in. The client can swap a Coming next row into the count by moving another row out; the census records the swap, never an argument about it.

**The go live rule.** The install may not go live with an unresolved row. `go_live.final_verification_sweep` gains a named check, `census_completeness`: every census row holds exactly one of the four states, and every `Connected` row's tool currently verifies. A row discovered late (a detection landing during the Seed stage, for example) re-opens `census.resolve_rows` and must resolve before the sweep can pass. If the sweep runs while a row is unresolved, the sweep fails on `census_completeness` by name, the install returns to the Connect stage, and the hub shows the row as the one thing left, in the client's words. Resolved is not the same as connected, and that is the point: go live requires a complete plan for every app the business runs on, with every deferral dated and every skip recorded as the client's own decision.

## 5. Orchestrator wiring

The census lives inside the Connect stage, as three new steps in state.py's CONNECT stage, in this order, immediately after `connect.present_checklist` and before `connect.verify_email`. They follow the existing step pattern exactly (adapter, check before create, idempotency key in the house format `<install_id>:connect:<step>:<natural_key>`):

| Step ID | Adapter | Check (before create) | Apply | Natural key | Idempotency key |
|---|---|---|---|---|---|
| `census.run_questions` | connectors | `census_exists` | `run_census_questions` | `census:{client_slug}` | `<install_id>:connect:census.run_questions:census:{client_slug}` |
| `census.apply_detections` | connectors | `census_detections_applied` | `apply_census_detections` | `census-detections:{client_slug}` | `<install_id>:connect:census.apply_detections:census-detections:{client_slug}` |
| `census.resolve_rows` | github | `census_resolved` | `resolve_census_rows` | `census-resolution:{client_slug}` | `<install_id>:connect:census.resolve_rows:census-resolution:{client_slug}` |

Step behavior:

- `census.run_questions` presents the Section 1 questions in the hub (pre-filled from the application and from `connect.present_checklist`'s expected set) and writes the first `census` array to the manifest. It completes when the array exists with one row per answered function. Unanswered functions stall on the Connect stage ladder (wiring contract Section 5.3), never on a person.
- `census.apply_detections` runs the available Section 2 signals and appends any new rows, each with its source in `note`. It is safe to re-run: a re-run after `seed.ingest_sources` adds only rows not already present (same function and tool name), which is how late detections enter without disturbing resolved rows.
- `census.resolve_rows` completes when every row holds one of the four states and the count rule in Section 4 has been applied. A row that later loses its state (a Connected tool removed by the client) re-opens this step on the engine's check before create discipline, and the row resolves again before the final sweep.

**The verify steps consume the census.** `connect.verify_email`, `connect.verify_calendar`, `connect.verify_file_storage`, and `connect.verify_crm` remain the standard four. Every further census row the client connects gets its own verify step in the same step family, `connect.verify_<tool_key>`, generated from the census rows at `census.resolve_rows` time, so the set of verify steps for an install is exactly its census, not a fixed list written in advance. `connect.record_connections` records the verified set from the census rows, and the manifest connected apps entries it writes are the Section 4.1 records the census `Connected` state points at.

**The final sweep.** `go_live.final_verification_sweep` runs its existing read check per required system plus `census_completeness` (Section 4). The sweep's failure record names `census_completeness` when that check is the one that failed, so an oversight flag or a retry never has to guess which part of completeness broke.
