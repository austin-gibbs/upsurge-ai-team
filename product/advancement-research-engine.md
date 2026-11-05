# Advancement Research Engine

## Status and use

This document defines how UpSurge keeps every installed AI Team current after go live. It is the internal operating system behind client facing recommendations for new seats, specialists, lanes, tools, skills, and Team Pack improvements.

It sits inside rules already set elsewhere:

- `product/positioning-core.md`: the platform is the driver, models are engines, and the team grows no matter the platform.
- `product/platform-policy.md`: lanes are roles, not vendors; connect what the client has, install what they lack; platform seats and usage are client owned pass through.
- `product/ip-and-stickiness.md`: client data belongs to the client, the System remains UpSurge IP, and no client ever receives another client's facts or fleet data in identifiable form.
- `product/onboarding-simple-standard.md`: client facing copy uses plain words, one action at a time, and no internal machinery names.

The client sees clear recommendations in their app. They do not see the research machinery, the scoring, the rejected candidates, or the hype we filtered out.

## 1. Purpose and competitive edge

A static AI install starts aging on the day it is copied. Models change, prices change, tools appear, platform rules tighten, and better ways to do a job show up in other industries before they show up in a client's own feed.

The Advancement Research Engine turns that problem into an UpSurge operation. Our internal AI Team watches the field, tests what matters, rejects what is loud but weak, and brings each client only the additions that fit their business, their lanes, their tools, and their rules.

The client is not buying a frozen setup. The client is buying a team that stays current without the client reading AI news, joining tool forums, comparing model release notes, or guessing which trend is real.

The competitive edge has five parts:

1. **Fleet attention.** One research pass can protect and improve every install. A signal found once is triaged once, validated once, and then matched to the clients whose work it fits.
2. **Prepaid learning.** New failure modes, weak tools, hidden permission traps, and dead end workflows are learned on our demo and internal workspaces first, not on a client's customers.
3. **Platform independence.** Research covers ChatGPT, Claude, Grok, Muse, Gemini, and other capable platforms as engines that can fill seats. A better engine or tool strengthens the platform layer; it does not replace it.
4. **Business fit over novelty.** A candidate earns a recommendation only when it has a named job in a client's business, in that client's words, with a way to prove value and a way to remove it.
5. **Memory compounding.** Every accepted, declined, tried, adopted, or removed recommendation is recorded. The next recommendation is smarter because the system remembers what this client values, what they rejected, what worked, and what did not.

This engine is how the promise "your team keeps getting better" becomes an operation instead of a slogan.

## 2. Research inputs and sources

Research starts from signals. A signal is not a recommendation. It is a dated, sourced observation that enters triage.

### Source categories

| Source category | What we capture | Primary owner | Quality note |
| --- | --- | --- | --- |
| Vendor release notes and changelogs | New models, features, limits, deprecations, API changes, admin controls, release dates | Kai | Primary source preferred. Vendor claims are labeled claims until tested. |
| Model and pricing changes | Price moves, usage limits, plan gates, context or tool changes, seat requirements | Finn with Kai | Cost impact cannot be scored from memory. The current vendor page or billing source controls. |
| Platform roadmaps | Announced direction for ChatGPT, Claude, Grok, Muse, Gemini, and other seat platforms | Nova | Roadmap items are future signals only. They can enter the watchlist, never a ready recommendation. |
| Competitor offers | What other AI services, agencies, and tool vendors are selling, promising, bundling, or warning about | Greta | Useful for market pressure and language. A competitor claim is never evidence that a capability works. |
| App marketplaces and tool directories | New tools, integrations, reviews, permission scopes, pricing shape, vendor maturity | Kai with Sable | Marketplace copy is treated as marketing. Permissions and data handling require direct review. |
| Community and social signal | Practitioner posts, demos, complaints, workarounds, repeated use cases, failure reports | Kai | Weak signal by default. It can open a research item; it cannot qualify one by itself. |
| Client request patterns across the fleet | Sanitized recurring request types, unmet needs, repeated manual work, common tool gaps, business type patterns | Lena with Hazel | Pattern labels and business type tags only. No client names, facts, content, credentials, or identifiable outcomes travel into research notes. |
| Industry workflows by business type | How work is changing in real estate, insurance, dental, education, home services, and generated packs for other industries | Nova with Greta | The question is always what job changed, not what tool is trending. |
| Internal delivery results from the brain | Completed work, QA findings, drill results, red flags, manual fulfillment repeats, postmortems, Pack update outcomes | Lena with Dex | Strong signal when the lesson is recorded in the brain and sanitized before fleet use. |

### Source record fields

Every material signal is captured with these fields before triage:

- `signal_id`
- `captured_at`
- `source_category`
- `publisher`
- `source_pointer` (URL, document path, marketplace listing, or internal brain pointer)
- `published_at` when the source gives one
- `claim` in one sentence
- `platforms` affected
- `capability_area` (seat, specialist, lane, tool, skill, workflow, model, pricing, compliance, or other)
- `business_type_tags`
- `evidence_type` (primary source, vendor claim, practitioner report, social signal, competitor claim, internal result, or client pattern)
- `confidence` (high, medium, or low)
- `security_flags`
- `cost_flags`
- `next_check_date` for watchlist items

### Source quality rules

- Primary sources outrank summaries. If a claim matters, read the release note, pricing page, permission screen, policy page, or product document itself.
- Material claims need either a primary source or two independent sources before they can move a candidate toward validation.
- Vendor performance claims stay labeled as claims until our sandbox work supports or rejects them.
- Social hype alone never qualifies a recommendation. A trend with no primary source, no repeatable job, and no test path stays in the signal log or watchlist.
- Community failure reports matter. A tool with enthusiastic demos and repeated permission, reliability, or support complaints is scored on the complaints too.
- Every source record carries a date. Stale signals are rechecked before use; model and pricing facts are never carried forward from memory.
- Client pattern signal is sanitized at capture time, not later. If a note cannot be understood without identifying a client, it does not enter fleet research.

## 3. Cadence and ownership

The engine runs on a fixed rhythm plus an event driven fast path for urgent changes.

| Cadence | Owner | Supporting roles | Work performed | Artifact produced |
| --- | --- | --- | --- | --- |
| Daily signal scan | Kai | Nova, Greta | Scan vendor changes, platform notices, marketplace movement, community signal, competitor claims, and urgent deprecation or outage news. Capture signals with source fields. Flag anything that could break a seated platform or a connected tool. | Daily Signal Log update in the research register |
| Weekly deep research and triage | Nova | Kai, Greta, Sable, Finn, Lena, Dex | Pick the strongest signals, read primary sources, group duplicates, score candidates, assign watchlist and reject outcomes, send validation candidates to sandbox work, and prepare Pack update candidates. | Weekly Triage Brief and Candidate Register updates |
| Monthly client recommendation review | Hazel | Maive, Parker, Finn, Sable, Lena | Match validated candidates to each client's business type pack, lanes, census rows, standing rules, never list, current tier scope, and recent outcomes. Decide which recommendations surface, which wait, and which stay internal. | Client Recommendation Packet per client, plus owner report recommendation notes |
| Quarterly capability roadmap | Maive | Nova, Greta, Sable, Finn, Lena, Owen | Decide the next capability pushes: new specialist coverage, lane patterns, platform registry changes, validation backlog, Pack release themes, and retirements. Review removals and failed trials for lessons. | Quarterly Capability Roadmap and Team Pack release plan |

### Event driven fast path

A same day research huddle is triggered by any of these:

- A platform announces a deprecation, limit change, price change, or policy change that affects seated work.
- A security or privacy issue touches a tool, platform, or data pattern used by clients.
- A connected tool changes permissions, export behavior, or admin controls.
- A model release creates a clear job fit that several business types have already asked for in sanitized pattern form.
- A candidate already in client use shows a new risk.

The fast path can pause a recommendation, add a warning to a client card, or retire a capability. It cannot skip validation to push a new recommendation faster.

## 4. Candidate record and triage scoring

Signals that survive the first read become candidates. Each candidate has one record in the Candidate Register.

### Candidate fields

- `candidate_id`
- `candidate_type` (seat, specialist, lane, tool, skill, model change, workflow pattern, or Pack improvement)
- `working_name`
- `named_job` in plain words
- `source_signal_ids`
- `platforms` it can run on
- `lanes_strengthened`
- `business_type_fit`
- `client_problem_pattern`
- `data_access_needed`
- `connected_tools_needed`
- `cost_shape` (included Pack update, client owned seat, client owned usage, connected tool subscription, one time project, or unclear)
- `triage_score`
- `triage_outcome` (validation candidate, watchlist, reject, or retire)
- `hard_gate_status`
- `validation_id` when validation starts
- `owner`
- `review_date`

### Scoring model

Scores guide triage. They do not override hard gates. A candidate with a security, privacy, legal, or client rule hard fail cannot be recommended as ready at any score.

| Dimension | Points | What earns points |
| --- | ---: | --- |
| Relevance to the client's business type | 0 to 15 | The candidate maps to real stages, categories, requests, or pain points in the business type pack or generated pack. Generic usefulness earns little. |
| Expected job value | 0 to 20 | There is a named job, a clear before and after, and a result the owner would recognize as worth having. |
| Maturity | 0 to 10 | The capability is released, stable enough for client work, supported by the vendor, and not dependent on a roadmap promise. |
| Evidence quality | 0 to 15 | Primary sources, repeatable demos, internal results, or strong practitioner evidence support the claim. Social excitement alone earns near zero. |
| Platform fit across lanes | 0 to 10 | The candidate works with the platform model: it can strengthen one or more lanes, respects seat delivery methods, and does not trap the team inside one vendor without reason. |
| Cost and pass through clarity | 0 to 10 | The cost shape is known, client owned pass through items are explicit, and any effect on tier scope or request counts is clear before the client sees the card. |
| Data access and security posture | 0 to 10 | The candidate needs the least access that can do the job, has understandable retention and export behavior, and passes Sable's first review without unresolved flags. |
| Implementation effort | 0 to 5 | Higher points mean lower effort: it can be seated, connected, or delivered through known install and fulfillment patterns. |
| Hype risk control | 0 to 5 | Higher points mean lower hype risk: the claim survives primary source reading, has a test path, and does not depend on a launch moment. |
| **Total** | **100** |  |

### Triage outcomes

- **80 to 100: validation candidate.** Move to sandbox validation unless a hard gate is open.
- **60 to 79: watchlist with questions.** Name the missing evidence, cost fact, platform fact, or security answer that would move it. Set a review date.
- **40 to 59: watchlist low priority.** Keep the signal, spend no validation time unless client pattern demand rises or the capability matures.
- **Below 40: reject and archive.** Record the reason so the same claim is not researched from zero when it resurfaces.
- **Retire:** for an existing capability that no longer earns its place because of quality, cost, risk, platform change, or poor client outcomes.

### Reject and watchlist reason codes

- `no_named_job`
- `weak_evidence`
- `hype_only`
- `immature_or_unreleased`
- `platform_mismatch`
- `duplicate_capability`
- `cost_unclear`
- `cost_not_worth_job`
- `data_access_too_broad`
- `security_review_open`
- `compliance_risk`
- `vendor_lock_risk`
- `client_rule_conflict`
- `poor_validation_result`
- `low_client_pattern_demand`

## 5. Validation before recommendation

Nothing untested gets recommended as ready. A candidate can be researched, watched, and even described internally as promising, but a client card may say "ready" only after validation passes.

### Validation gates

1. **Sandbox test.** Test on the standing demo install or an internal workspace. Client data is never the first test data. Use synthetic, demo, or internal material that matches the job shape.
2. **Small drill.** Run a named drill with pass criteria recorded before the test starts.
3. **Security and compliance review.** Sable reviews anything that touches client data, customer records, messages, files, credentials by pointer, connected tools, regulated workflows, or new permissions.
4. **Cost note.** Finn records the cost shape under the finance rules: what is included, what is client owned pass through, what could affect tier scope, and what must be approved before any spend starts.
5. **Brain memory note.** Lena records the sanitized lesson in the brain: what was tested, what passed, what failed, where it fits, and what future research should remember. Client facts never enter the brain note.

### Validation record fields

- `validation_id`
- `candidate_id`
- `hypothesis` (the job this should do better, in plain words)
- `test_workspace` (standing demo install or named internal workspace)
- `data_class` (synthetic, demo, or internal only)
- `test_tasks`
- `pass_criteria`
- `observed_result`
- `failure_modes_seen`
- `memory_write_check`
- `isolation_check`
- `permission_check`
- `cost_note_id`
- `security_review_id`
- `qa_result`
- `removal_test`
- `decision` (ready to recommend, not ready, watchlist, or reject)
- `brain_note_pointer`

### Pass criteria

A validation passes only when all applicable criteria are met:

- The candidate completes the named job end to end in the sandbox.
- Output passes the relevant Team Pack QA checklist for that deliverable type.
- Work, decisions, and outcome notes are written to the memory instance in the standard format.
- Client isolation holds: the test cannot see, use, or leak another workspace's material.
- Permissions match the request. No surprise admin access, broad file access, message access, or customer record access appears during setup or use.
- Cost tracing is complete enough for Finn to state the client facing cost shape without guessing.
- The removal path works: the seat, tool, skill, or workflow can be turned off or removed without breaking the board, memory, or ledger history.
- Failure behavior is acceptable: if the candidate fails, work is held visibly or routed to another lane; it does not silently vanish.

If a criterion fails, the candidate returns to watchlist or reject with the failure recorded. A near pass is not a client ready pass.

## 6. Recommendation format in the client app

A validated candidate becomes a client recommendation only when it fits a specific client. The card is written in the client's words, using their business type pack language and the Simple Standard.

### Recommended addition card fields

- `recommendation_id`
- Card label: **Recommended addition**
- `addition_name` (seat, specialist, lane, tool, or skill name)
- `addition_type`
- `job_it_would_do` in the client's words
- `lanes_strengthened`
- `runs_on` (platform or platforms)
- `why_now` (the plain reason this surfaced now: a repeated job, a platform change, a seasonal need, a proven fleet pattern, or a gap in their current team)
- `what_we_checked` (short plain summary that UpSurge tested it before recommending it)
- `cost_if_any` (included in the Team Pack, client owned platform seat, client owned usage, connected tool subscription, one time project, or no added cost)
- `data_access_needed` in plain words, or "No new access"
- `trial_plan`
- `success_measure`
- `removal_note` (how it can be removed if it does not prove value)
- Choices: **Add it**, **Not now**, **Never for us**

### Trial plan fields

- `trial_start_condition`
- `trial_scope` (the limited job or jobs used first)
- `trial_owner` on the UpSurge side
- `trial_review_point`
- `adopt_rule`
- `remove_rule`

The success measure must be observable in the client's world: a completed job type, a response or turnaround pattern the owner can see, a quality check result, a board or ledger outcome, or a clear owner judgment recorded at review. It must not be a vanity metric invented to make the addition look good.

### Approval rules

Client approval is required before any of these move forward:

- A paid platform seat or a change to a client owned platform plan.
- New data access, broader permissions, or access to a new class of records.
- A new connected tool or a change to a connected tool's role.
- Client facing automation changes that alter what customers receive.
- Work outside the client's tier scope, request counts, or an approved project.

No cost knowledge and prompt improvements may flow through normal Team Pack updates when all of these are true:

- No new paid seat.
- No new data access.
- No new connected tool.
- No change to client facing promises or regulated workflow behavior.
- The improvement is recorded in Pack release notes, the client memory decision log, and the monthly owner report.

Approval is never bundled into a vague yes. If a card asks for spend, access, and a tool change, the client sees each one named on the card before choosing Add it.

## 7. App and memory wiring

### Where recommendations appear

| Surface | What appears | Rule |
| --- | --- | --- |
| Command home recommendation area | The active Recommended addition cards for that client, sorted by fit and urgency | Show only cards that are validated, client matched, and not suppressed by a Never decision. Keep the area short; the client should see the next best additions, not a research feed. |
| Heartbeat page addition area | A client visible "Getting stronger" area showing pending recommendations, recently adopted additions, and additions in trial | Show names, job, lane or lanes strengthened, and status in plain words. Never show scores, rejected candidates, internal research notes, or other clients. |
| Monthly owner report | A short section: recommended next additions, added and proven, tried and removed, and Pack improvements already applied | Written in owner language. Cost and approval needs are named before any action is requested. |
| Quarterly review | Roadmap choices for the next quarter: adopt, trial, wait, or remove | Decisions are recorded during the review and routed the same day. |

### Client memory records

Decisions live in the client's memory instance. The command platform reads its state from memory, so a recommendation that is not recorded there does not exist for reporting or follow through.

Each recommendation record carries:

- `recommendation_id`
- `candidate_id`
- `surfaced_at`
- `surface` (command home, heartbeat page, monthly report, quarterly review, or lead message)
- `status` (proposed, approved, not_now, never_for_us, in_trial, adopted, removed, expired)
- `decided_at`
- `decided_by`
- `decision_note`
- `trial_id` when a trial starts
- `success_measure`
- `outcome_note`
- `ledger_pointer` when completed work produces ledger entries
- `next_review_date` for Not now items
- `suppression_reason` for Never for us items

Standing rule effect:

- **Not now** records the reason when the client gives one and sets a review trigger: a date, a season, a business event, or a material change in the candidate. The card does not nag before that trigger.
- **Never for us** adds the candidate pattern to the client's do not recommend list. It can be raised again only if the candidate materially changes and Maive records why the new version is different.
- **Add it** is a decision record and a work order trigger, not the completion of the work.

### How a yes routes to fulfillment

When a client chooses Add it:

1. The recommendation status becomes approved in the client memory instance the same day.
2. Maive creates or updates a Desk project using the execution brief standard: objective, system of record, current state to verify, exact changes, verification, definition of done, and blocking questions only.
3. The work routes by type:
   - **Seat or lane:** update the App Census if a new platform seat or tool is involved, apply the platform policy mode, deliver the Pack by the platform's supported method, run the standard seat drill, and record the drill fields.
   - **Specialist or skill:** deliver the operational Pack content, run the applicable skill check, sample the first deliverables under the oversight model, and update the roster or heartbeat state only after the check passes.
   - **Tool or connected app:** add or update the census row, complete connection and verification under the wiring contract, run Sable's access check, and confirm the row state before the capability is described as live.
   - **Pack improvement:** apply through the Team Pack update path, record the version stamp change, and include the change in the next owner report.
4. Trial work is labeled as trial in the board and memory until the adopt rule or remove rule is met.
5. At trial review, the status becomes adopted or removed. The outcome note states what was proven, what was not, and what happens next.

### Output Ledger and research feedback

The Output Ledger counts completed work, not recommendations. A recommendation creates no ledger value by being shown or approved. Ledger entries appear only when trial or adopted work is completed and recorded in memory under the normal completion rule.

Recommendation outcomes feed later research in sanitized form:

- Candidate level outcomes: surfaced, approved, declined, trialed, adopted, removed, and expired counts inside UpSurge research only.
- Trial lessons: pass and fail reasons, permission surprises, cost surprises, QA issues, and removal reasons.
- Client fit lessons: which business type packs and lane patterns benefited, stated as patterns rather than client stories.
- Owner value notes: whether the owner judged the addition worth keeping, recorded in the client instance and generalized only as a pattern label for fleet research.

No client facing surface ever shows another client's decision, outcome, volume, identity, or business facts as proof.

## 8. Guardrails

- **No hype chasing.** A launch, a viral demo, or a loud launch week is a signal to research, not a reason to recommend.
- **No competitor parroting.** A recommendation never exists because a competitor shouted about a tool. Competitor noise can raise a question; only evidence and validation can answer it.
- **No cross client data leakage.** Fleet research uses sanitized patterns only. Client facing recommendations never cite another client's facts, content, results, volumes, or identity.
- **No seat without a named job.** Every seat, specialist, lane, tool, or skill recommendation names the job it will do for this client. Coverage for its own sake is rejected.
- **No ready label before validation.** Untested candidates can be watched internally. They cannot be presented to a client as ready.
- **No silent access expansion.** New data access, broader permissions, or a new connected tool always require explicit client approval and a Sable review record.
- **No removal traps.** Every recommendation must be removable. If removal would break the board, strand records, or hide history, the candidate is not ready.
- **No dark patterns.** Add it is never preselected for anything with cost, access, or client facing impact. Not now and Never for us are real choices with real effects.
- **No platform worship.** A candidate is judged by job value, evidence, fit, cost, and risk across lanes. A famous platform name earns no points by itself.
- **No stale facts.** Pricing, limits, platform capabilities, and permission behavior are rechecked at recommendation time and again at fulfillment time.
- **No permanent maybes.** Watchlist items have review dates. Trials have adopt and remove rules. Recommendations expire if the facts change or the client does not decide within the review window set in the monthly review.

## Operating test

Before any recommendation reaches a client, Maive or the monthly review owner must be able to answer yes to all six questions:

1. Does it have a named job in this client's words?
2. Did we test it somewhere that was not this client's live business?
3. Can we state the cost shape and approval needs without guessing?
4. Can Sable explain the data access in one plain paragraph?
5. Is the success measure visible to the owner?
6. Can we remove it cleanly if it does not prove value?

If any answer is no, the item stays in research, validation, or watchlist. The client sees only the additions that clear the bar.
