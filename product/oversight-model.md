# The UpSurge Oversight Model

Status: Service design v1.0, 2026-11-04
Owners: Hazel (client-success-lead) and Parker (performance-analyst), for Maive and UpSurge Pros
Applies to: Every live AI Team install, from go live through ongoing service

## The named service: UpSurge Oversight

UpSurge Oversight is the managed care layer that comes with an installed AI organization. It is a core part of the service, not an add-on and not a support queue.

The client promise is direct:

> Your AI organization is managed, not just installed. UpSurge watches the quality of the work, the health of what the team knows about your business, and the speed and reliability of delivery every week. If something needs attention, a person owns it. If something needs your decision, you receive one clear ask. If you ever need a human beyond your team lead, you have a direct path.

Installation creates the organization. Oversight keeps it accurate, useful, and improving as the client's business changes.

# 1. What oversight means in plain client language

An AI team can only do good work when four things stay true:

1. The work is checked by someone other than the person or specialist who produced it.
2. The business facts the team relies on stay current and properly sourced.
3. Slowdowns, repeated questions, and quality problems are spotted as patterns, not discovered by the client.
4. Improvements reach the client's team in an orderly way, with a plain explanation of what changed.

UpSurge Oversight covers those four responsibilities.

For the client, that means:

- **A senior owner is accountable.** The team lead of record reviews exceptions, delivery patterns, and open decisions for the account every week.
- **Quality is reviewed after delivery as well as before it.** The normal delivery gate still applies before work reaches the client. Oversight then samples completed work to test whether the gate is working and to catch patterns one project at a time would hide.
- **Memory is maintained like a business record.** Facts are checked for age, contradictions, and sources. A fact that cannot be supported is marked unverified and is not treated as settled truth.
- **Output is measured.** UpSurge watches how much work is delivered, how long it takes, where it waits, how often it passes review, and how often it needs escalation.
- **The team improves in public, within the client's own account.** Clients receive short change notes in ordinary language when an improvement affects how their team works. They do not receive internal process detail.
- **There is always a human path.** The client starts with their team lead. Quality concerns go to the quality lead. Unresolved or high impact matters reach Austin Gibbs, the owner escalation.

Oversight is not a promise that software never fails or that every low risk item receives a second full build review after delivery. It is a management system with named owners, defined checks, response standards, and a record of what was found and fixed.

# 2. Oversight services and how each one works

## 2.1 Deliverable QA sampling

### Purpose

Confirm that delivered work meets the brief, the client's standards, and the applicable Team Pack checklist, and detect repeat defects by deliverable type, specialist, or workflow.

### Method

Each week, the Quality Lead selects a stratified sample from deliverables completed in the prior week. The sample covers different deliverable types and owners rather than taking only the easiest or most recent items. The following always enter the audit pool regardless of the random sample:

- The first deliverable of a new type for that client.
- Any deliverable connected to a client correction, complaint, or red flag.
- Any public publish, paid launch, money related item, legal or compliance item, data migration, or external send that was not covered by a standing approval.
- Any deliverable produced after a material Team Pack update, until the updated process has a clean audit result.

The tier sample rates are defined in section 5. If weekly volume is lower than the stated minimum, the sample is all completed deliverables for that week.

### What the reviewer checks

- The delivered result matches the objective and definition of done in the execution brief.
- Names, numbers, dates, links, prices, claims, and offers match an approved source.
- Client branding, voice, spelling rules, and banned phrases were followed.
- The live destination works: the page loads, the form arrives, the workflow is published, the booking link opens, or the file renders correctly, as applicable.
- Required approvals were present before any client facing send, spend, publish, or irreversible step.
- The client summary says what was delivered and what remains open, without internal language.
- The project record is complete enough for another reviewer to reconstruct what happened.

### What happens when a sample fails

Findings are graded by impact:

- **Critical fail:** A wrong recipient, a material factual error with external impact, a broken lead or booking path, a compliance problem, an unauthorized action, or any client information boundary issue. Related work is paused where necessary. A human owner is assigned the same day. The item is corrected or contained the same day whenever the underlying system allows it. The client is told promptly when the issue affected their customers, their public surfaces, their money, or a decision they need to make. Austin is escalated the same day.
- **Major fail:** The deliverable misses the brief or a material quality standard but has not created external harm. The item is corrected before more work of the same type is delivered. The Quality Lead records the root cause and the prevention step within two business days.
- **Minor fail:** A polish, formatting, naming, or record issue that does not change the result. The record or item is corrected, the pattern is counted, and repeated minor fails on the same checklist line become a major process finding.

A single fail is handled as an item problem. The same fail across two or more items becomes a process problem. The response then includes a checklist change, a routing change, a memory correction, or additional review for that deliverable type. Oversight reports the pattern and the fix, not just the corrected item.

### Measures kept

- First review QA pass rate: deliverables that pass the pre-delivery QA gate on first review, by install and type.
- Oversight audit pass rate: sampled delivered items with no critical or major finding.
- Repeat defect count by checklist line, deliverable type, and owner.
- Time from fail discovery to correction or containment.

The two pass rates are never combined. The first measures the delivery gate. The second measures whether oversight is finding problems after delivery.

## 2.2 Memory health pass

### Purpose

Keep the client's team working from current, consistent, sourced business knowledge. Memory health is treated as delivery quality because a wrong phone number, offer, service area, approval rule, or staff role can reproduce across many deliverables.

### Method

The Knowledge Manager runs a weekly targeted memory pass for every install and a deeper pass on the cadence in section 5. The pass reviews the client profile, brand kit, systems map, standing rules, decisions log, and open flags.

The pass has four checks:

1. **Stale fact sweep.** Facts in changeable categories are reviewed when their source changes, their stated review date arrives, or they pass the age limit set for that category. Changeable categories include offers, prices, service areas, hours, staff and roles, booking links, phone numbers, campaign settings, connected systems, and approval contacts. The reviewer checks the live source or the client's current record before refreshing the fact.
2. **Contradiction check.** The reviewer looks for two active versions of the same fact across memory sections, recent decisions, and live systems. The live source or latest client decision wins according to the system of record. The losing version is retired in place with a dated note. It is not silently left active.
3. **Source coverage check.** Each material fact is counted as sourced, client confirmed, or unverified. High impact facts require a source or client confirmation before a deliverable may rely on them. High impact facts include contact details, offers, claims, prices, service coverage, compliance statements, approval authority, and anything that will appear in a public or customer facing deliverable.
4. **Open flag aging.** Unverified facts, unresolved conflicts, and pending client answers are reviewed for owner and next check date. Oversight either resolves the item from an available source, keeps it clearly marked as unverified, or turns it into one exact client question when only the client can settle it.

### Output of the pass

- Confirmed facts added, corrected, or retired.
- Source coverage for the install, stated as counts rather than a vague health label.
- A short list of facts that remain unverified and what work they may or may not support.
- Any memory issue that caused or could cause a delivery defect, linked to the QA finding and the prevention step.

The client's monthly report shows memory growth in useful terms: new confirmed knowledge added, outdated items corrected, and decisions recorded. It does not expose the internal conflict log or every source record.

## 2.3 Output and turnaround monitoring

### Purpose

Show whether the organization is delivering at the standard the client was sold, where time is being lost, and whether quality problems are isolated or becoming a trend.

### Metrics watched

The measures are the fleet metrics defined in the sales-to-install operations bridge, computed from Desk and install records rather than estimated:

- **Time to first value:** Elapsed time from signature to the client's first delivered request. Target: the same business day as go live.
- **Install elapsed time:** Signature to live, broken down by install stage while the install is in progress.
- **Request turnaround:** Median and 90th percentile time from request intake to delivered, split by deliverable type and compared with the applicable definition of done.
- **QA pass rate:** First review pass rate by install and deliverable type, plus the separate oversight audit pass rate in section 2.1.
- **Escalation count:** Escalations per week and the trigger behind each one. A low count is not treated as good by itself. Zero escalations beside falling QA results is reviewed as a possible missed trigger.
- **Waiting time split:** Time spent waiting on the client compared with time waiting on UpSurge. Client waiting is shown to the client as the clearest lever they control. UpSurge waiting is treated as an internal defect.
- **Intake health:** Requests received per week and the share that contained enough information to brief without a follow-up question. A persistent problem leads to an intake adjustment proposal, not blame on the client.
- **Digest and review attention:** Opens and clicks on the daily digest and client review. This is an attention signal only. A client who ignores summaries but keeps submitting work is not marked unhealthy. The reporting format is adjusted before the client is escalated.

### Review method

- The daily exception watch looks for severe breaches and stalled work.
- The weekly fleet review looks for movement, not just totals. Any important metric moving the wrong way for two consecutive weeks receives a named owner and a corrective action.
- A single severe event does not wait for a trend. It enters the red flag process in section 2.6.
- Results are compared only within the client's own history in client facing reports. Clients never see another install's numbers.

## 2.4 Team Pack update application

### Purpose

Give every install the benefit of improvements learned across the service, without changing the client's facts, approvals, or in flight work unexpectedly.

### Method

1. The Knowledge Manager confirms the install's current Team Pack version and lists any install more than one minor version behind.
2. The team lead reviews the proposed update for client impact, current deadlines, and any client specific exception.
3. Updates are applied in the weekly oversight window unless the change is a safety or compliance fix, which is applied immediately.
4. In flight projects normally finish under the version they started on. Safety and compliance fixes apply immediately and are noted in the affected project record.
5. The Quality Lead samples the first deliverables produced under a material process change.
6. If the audit shows a regression, the change is paused for that install, the prior process is restored where possible, and the issue enters the weekly fleet review.

### What the client receives

The client receives a short change note in ordinary language, normally inside the weekly review or monthly owner report. The note answers three questions:

- What improved?
- What may the client notice?
- Does the client need to do anything?

Example:

> Your team now checks every new landing page form against your CRM before the page is marked complete. You do not need to do anything. The change is intended to prevent a page from looking finished while its leads are going to the wrong place.

The client does not receive internal version mechanics, internal prompts, routing tables, or the source engagement that produced the lesson. No client information from another install is included in an update or a change note.

## 2.5 Capability watch

### Purpose

Notice when the client's business has outgrown the current shape of its AI organization and recommend the next useful capability before the gap becomes a bottleneck.

### What UpSurge watches

- Repeated requests that are being handled as one off work and should become a standing capability.
- Work that waits because the current roster lacks a proven specialist.
- Connected systems that are present but underused.
- Seasonal work, campaigns, launches, reporting needs, and service lines visible in the client's requests.
- New specialists or capabilities that have met the Team Pack quality bar and are relevant to the client's business.
- Repeated manual work on the client's side that has not yet been handed off.

### How a recommendation is made

A capability is proposed, never imposed. The proposal states:

- The business problem or opportunity.
- The work the new capability would take over.
- The expected operational benefit, stated without promising revenue or business results.
- The setup required and any new access needed.
- Whether the capability is fully proven, available as a supervised pilot, or not yet available.
- Any tier, scope, or cost decision the client needs to make.

The client may approve, defer, or decline. A declined proposal is recorded and is not repeatedly resubmitted unless the underlying pattern materially changes. No new specialist is shown as part of the client's team, no new system access is requested, and no scope or price change takes effect without the client's approval.

Possible recommendations include video editing, paid media management, business reporting, bookkeeping operations support, security and compliance review, and integrations for systems that do not yet connect cleanly. A capability is recommended as a rostered service only after its skill standard and quality bar have been met. Earlier access, if offered at all, is labeled as a supervised pilot.

## 2.6 Red flag response

### Standard

Any red flag receives human attention the same day it is detected. The response has six steps:

1. Assign one named human owner.
2. Contain the risk before investigating the full cause.
3. Check whether the client, their customers, their money, or a public surface is affected.
4. Tell the client promptly when there is impact, a decision is needed, or a delivery date changes.
5. Correct the item and record the root cause and prevention step.
6. Confirm the fix in the next oversight cycle and include material incidents in the monthly owner report.

### The eight red flags

1. **Late first value.** Time to first value exceeds one business day after go live.
2. **Information boundary failure.** A team seat fails the isolation check at install or later, or client information appears where it does not belong.
3. **Falling QA floor.** The QA pass rate for a deliverable type falls below the Team Pack floor for two consecutive weeks.
4. **Stalled install.** An install stays in one stage longer than twice its target time with no client side cause recorded.
5. **Escalation surge or serious escalation.** Escalations exceed the weekly threshold, or one escalation involves money movement, a legal question, or a client repeatedly asking for a human.
6. **Payment attention overdue.** Payment status remains at attention after the human follow up step in the signature to kickoff sequence.
7. **Disengagement pattern.** The digest and weekly review are both unopened for three consecutive weeks while request volume is falling.
8. **Internal material on a client surface.** Internal notes, briefs, blockers, or process language are found on the heartbeat page, a digest, a report, a client board view, or any other client visible surface.

An information boundary failure or internal material on a client surface is treated as an incident, not an ordinary defect. The affected seat, page, or reporting path is paused until the Quality Lead and team lead confirm containment. Austin is escalated the same day.

# 3. Cadence calendar

## Daily: exception watch

**Owner:** Team lead of record, supported by the Quality Lead and Knowledge Manager.

**Visibility:** Internal only, unless a client action or notice is required.

The daily watch reviews:

- Red flags and newly stalled work.
- Projects waiting on UpSurge beyond their expected next step.
- Critical QA findings.
- Failed connections or delivery paths that could affect active work.
- Escalations that arrived since the prior watch.

The output is an owner and a next action for each exception. Clients are not sent a daily list of internal exceptions. They receive a prompt notice only when an exception affects their work, timing, money, public presence, or decision.

## Weekly: internal fleet review

**Owner:** Maive, with Hazel for client health, Parker for metrics, Dex for QA, and Lena for memory and Team Pack currency.

**Visibility:** Internal only. No client is compared with another client in any client facing document.

The fixed agenda is:

1. Fleet line: live installs, installs in progress, requests delivered, and median turnaround.
2. Per install attention list: QA findings, memory risks, waiting time, escalations, and red flags, ordered by attention needed.
3. QA sample results and repeat defects.
4. Memory health exceptions and source coverage risks.
5. Team Pack versions, pending updates, and any update regression.
6. Capability watch proposals that are ready for a client decision.
7. Decisions that must go to a client, stated as one exact ask per item.
8. Product signals for the brain to service repo improvement loop.

The output is an action list with owners and dates. The review also schedules the client specific oversight work for the coming week.

## Monthly: owner report

**Owner:** Hazel, using metrics prepared by Parker and QA and memory results supplied by Dex and Lena.

**Delivery:** Within the first five business days of the month for the prior month.

**Format:** One page. Links may point to the client's own board or deliverables, but the report itself must be readable without opening them.

### Required format

**Your AI Organization: Monthly Owner Report**

- **What your team delivered:** Completed requests by category, major deliverables by name, and the count of items still in progress at month end.
- **Ledger highlights:** The most valuable completed work, any corrected items the client should know about, open commitments carried forward, and time spent waiting on the client compared with waiting on UpSurge.
- **Turnaround:** Median turnaround, the slowest category by 90th percentile, and whether speed improved or slipped against the prior month.
- **Quality and memory:** Oversight audit result in plain language, any material correction already made, confirmed knowledge added, outdated facts corrected, and facts still awaiting client confirmation.
- **Team improvements applied:** Short change notes for updates that affected this client's team and anything the client needs to do, which will usually be nothing.
- **Next month's proposed focus:** The work UpSurge recommends prioritizing, including any capability watch proposal and the reason for it.
- **Decisions needed from you:** Each decision stated in one sentence, with the effect of waiting. If no decision is needed, the section says so.

The monthly report contains only that client's facts and numbers. It does not contain fleet averages unless they are clearly labeled as a service standard rather than another client's result.

## Quarterly: organization review

**Owner:** Team lead of record and Hazel, with Austin available for strategic or commercial decisions.

**Format:** A live review for Growth Team and Full AI Organization clients. Launch Team clients receive the same review in written form, with a live meeting on request or when a material decision is pending.

The review answers five questions:

1. What work has the organization taken off the client's plate, and what still returns to the owner too often?
2. What should the client hand off next?
3. Which specialist or capability would remove the largest recurring bottleneck for this business?
4. Which system should be connected next, and what work would that unlock?
5. Which approval rule, intake habit, or memory gap most limits speed or quality?

The output is a one page next quarter plan with:

- Priority handoffs.
- Proposed specialists or capabilities, each marked proven, supervised pilot, or future.
- Proposed system connections.
- Approval or access decisions needed.
- Memory topics to confirm.
- The measures UpSurge will watch to judge whether the plan worked.

No quarterly recommendation changes scope, access, team composition, or price by itself. The client approves changes before they are made.

# 4. What the client sees and what stays internal

## The client sees

- Their Surge Command board with client safe project titles, statuses, summaries, and completed deliverables.
- Their team page with the roster, real work in progress, real completed work, and real turnaround measures.
- The daily digest and weekly review for their own account.
- The monthly owner report and quarterly organization review.
- Team improvement change notes that affect their install.
- A prompt notice when a red flag affects their work, customers, timing, money, or public surfaces.
- Corrections to their own deliverables and a plain explanation of what changed.
- Capability proposals and the decision required to approve, defer, or decline them.
- The exact question or approval UpSurge needs, presented once with the relevant context.

## UpSurge keeps internal

- Execution briefs, internal notes, blocker analysis, and next step working notes.
- Routing decisions, internal assignments, and handoff notes.
- QA sampling worksheets, reviewer comments, and defect scoring before a finding is ready to communicate.
- Memory contradiction logs, source working records, and unverified research that has not been settled.
- Fleet metrics, cross client comparisons, and internal attention rankings.
- Team Pack mechanics, internal instructions, tool details, and update source material.
- Sales, payment, staffing, and escalation deliberations that do not require a client decision.
- Every other client's name, facts, work, metrics, and existence as a comparison point.

The separation is functional as well as contractual. Client visible fields are written for the client from the start. Internal notes are not copied into a client summary and then edited down.

# 5. Oversight by tier

Safety and honesty do not scale down by tier. Red flags receive same day human attention at every tier, high risk work receives the required approval and QA gate at every tier, and information boundary rules are identical. What scales is sampling depth, analysis depth, planning time, and routine response speed.

| Oversight element | Launch Team | Growth Team | Full AI Organization |
|---|---|---|---|
| **Deliverable QA audit sample** | 10 percent of completed deliverables each week, minimum 3 when volume allows. If fewer than 3 are completed, sample all. | 20 percent each week, minimum 5 when volume allows. If fewer than 5 are completed, sample all. | 35 percent each week, minimum 10 when volume allows. If fewer than 10 are completed, sample all. |
| **Targeted audit** | First of type, client corrected, and high risk items always included. | Launch Team coverage plus all items after a material process change until one clean audit cycle. | Growth Team coverage plus all major launches and all deliverables tied to a quarterly priority. |
| **Memory health** | Weekly targeted stale and contradiction queue. Full source coverage pass monthly. | Human memory health pass weekly. Deep source coverage audit monthly. | Human memory health pass weekly, plus source verification before major campaigns or initiatives. Deep audit monthly. |
| **Output monitoring** | Daily exception watch and weekly trend review. Monthly figures in the owner report. | Daily exception watch, weekly trend review, and category level turnaround and QA analysis. | Daily exception watch, weekly senior review, and initiative level analysis for priorities named in the quarterly plan. |
| **Owner report** | One page monthly report in the standard format. | One page monthly report with trend comparison and fuller ledger analysis. | One page executive report with initiative progress, risk notes, and a direct link to supporting detail in the client's own board. |
| **Organization review** | Quarterly written review. Live meeting on request or when a decision requires one. | Quarterly live review with a next quarter handoff plan. | Monthly strategy check in plus quarterly live organization review and next quarter plan. |
| **Capability watch** | Included when a clear repeat pattern appears in the monthly review. | Reviewed monthly and presented in the owner report when relevant. | Reviewed weekly and tied to the client's named initiatives. |
| **Routine oversight response** | Within two business days. | Within one business day. | Same business day. |
| **Red flag response** | Human owner assigned the same day. Client notice the same day when there is impact or a decision is needed. | Same standard as Launch Team. | Same standard as Launch Team, with Austin notified the same day on every red flag, not only critical incidents. |

Tier changes do not apply retroactively to work already delivered. A move to a higher tier starts with the next weekly oversight cycle unless the client and UpSurge agree on an immediate catch up review.

# 6. Oversight roles on the UpSurge side

Client facing names describe the responsibility without exposing internal systems or team mechanics.

| Responsibility | Client facing name | Accountable for |
|---|---|---|
| Lane leader of record | **Team Lead** | Account ownership, request intake, routing judgment, status accuracy, weekly exception review, client decisions, and escalation acknowledgement. This is the client's first contact. |
| Independent quality function | **Quality Lead** | Pre-delivery QA standards, post-delivery sampling, fail grading, correction tracking, repeat defect analysis, and incident review for client surface problems. |
| Memory librarian function | **Knowledge Manager** | Client memory structure, stale fact sweeps, contradiction checks, source coverage, decision records, and Team Pack update application records. |
| Performance analysis function | **Operations Reviewer** | Turnaround, throughput, waiting time, QA trends, escalation patterns, and the figures used in the monthly owner report. |
| Final owner escalation | **Austin Gibbs, UpSurge Owner** | Unresolved client concerns, high impact incidents, money or legal gates, irreversible actions, repeated requests for a human, and any matter the Team Lead and Quality Lead cannot settle. |

The client does not need to manage these people separately. The Team Lead brings in the Quality Lead or Knowledge Manager when needed and remains accountable for the answer. Austin is not positioned as routine support. His involvement means the matter has crossed a defined escalation threshold or the client has asked for the owner.

Internally, role ownership is recorded per install. A person may hold more than one function on a small install, but the QA reviewer for a sampled deliverable may not be the person who built that deliverable.

# 7. Honest limits and client approval gates

## What oversight can and cannot do

Oversight is a review, measurement, correction, and direction service. It improves the odds that work is accurate, timely, consistent, and aligned with the client's record. It does not guarantee business outcomes.

UpSurge does not promise that oversight will produce a specific amount of revenue, profit, traffic, search ranking, advertising return, booked appointments, enrollment, or cost savings. Those outcomes also depend on the client's market, offer, pricing, sales process, staff, customers, third party platforms, and decisions.

Sampling is a risk control, not proof that every low risk item was independently rebuilt or rechecked after delivery. The pre-delivery QA gate applies to deliverables under the Team Pack. Oversight sampling then audits a defined share of completed work and all targeted high risk categories. Clients who need a higher audit rate can move to a higher tier or request a specific review.

Oversight can only review information and systems the team is authorized to access. Delayed source material, unavailable systems, unclear client records, and late approvals can limit what can be verified. When that happens, the limitation is recorded and the affected fact or deliverable is not presented as fully verified.

Professional and regulated decisions remain with qualified humans chosen by the client. Oversight may identify a question for legal, tax, financial, medical, insurance, real estate, or other regulated review. It does not replace that review.

## Decisions that remain the client's

The client's approval remains the gate for:

- A client facing send that is not already covered by a written standing approval.
- Any spend, paid launch, budget change, refund, or other money action.
- A public publish or an irreversible action, including a deletion, migration cutover, or change that cannot be cleanly undone.
- A legal, compliance, pricing, offer, or public claim decision.
- A change to the client's services, team access, connected systems, or approval rules.
- A new capability, specialist, scope expansion, tier change, or cost change proposed through capability watch.
- Any use of client information beyond the work and systems the client has authorized.

When approval is needed, UpSurge sends one exact ask with the recommendation, the risk of waiting, and what will resume when the client answers. Routine work inside an approved brief does not stop for repeated permission requests.

## The oversight commitment

UpSurge Oversight gives the client a managed organization, not a black box. The client can see what was delivered, how long it took, what was corrected, what the team learned about the business, what is proposed next, and what decision is needed. UpSurge keeps the machinery internal, watches the work every week, and puts a named human behind the result.
