# Seeding Protocol: Client Memory

How the client memory for an install gets its first facts, how the client confirms and corrects them, and how wrong or aging facts are handled afterward. This protocol governs the Seed stage of every install and the confirmation flow in the client hub.

## Principle

A seeded fact is a draft until it is confirmed. The team would rather ship an install with honest drafts clearly marked than with confident facts nobody checked. A wrong fact in memory compounds into every deliverable built on it, so the protocol protects confirmation over speed.

## 1. Drafting auto-seeded facts

Sources, in the order they are worked at install:

1. The client's public website (https://cedarpeakdental.example.com at install): business basics, offers, service area, voice, published claims, palette, typography, logo locations.
2. The client's connected tools, once Verified in `systems-map.md`: CRM structure and pipeline names, calendar and booking setup, file storage layout, existing automations.
3. The structured client interview at install: approval rules, hard rules, never-dos, escalation preferences, facts no public source carries.
4. The agreement: signer, champion, tier, lanes, intake mode.

Drafting rules:

- Every drafted fact lands in its template file with status `draft` and its source named concretely in the Source column. "Website" is not a source. The URL and the page are the source.
- Facts are copied character for character from the source: names, phone numbers, addresses, prices, and claims are never paraphrased into memory.
- Branding is taken from the client's own live properties only. Nothing is borrowed from another client or from a template example.
- Anything the sources do not establish is left blank. A blank field is an honest state. It becomes a question in the interview or a flag in `open-flags.md`, never a guess.
- Published claims from the client's own properties may be drafted into the approved claims list in `brand-kit.md` with the property named as source. Claims found anywhere else stay off the list until the client approves them.

## 2. Client confirmation and edits in the hub

The hub presents the client with their drafted memory during the install, grouped by file, and the client works through it once.

- **Confirm**: The client confirms a fact as correct. The fact's status changes from `draft` to `confirmed`, and the source gains the hub confirmation with its date. The draft marker is removed. Nothing else about the fact changes.
- **Edit**: The client corrects a fact. The corrected value replaces the draft, status becomes `confirmed`, and the change is recorded in that file's Change notes with the date, the old draft value, the new value, and the hub as source. Draft values are not silently overwritten; the record shows what the seed said and what the client corrected it to.
- **Reject**: The client marks a fact wrong without supplying a correction. The fact is cleared to blank, status stays `draft`, and a flag opens in `open-flags.md` owned by the champion, so the gap is visible instead of filled with a guess.
- **Skip**: The client leaves a fact unreviewed. It stays `draft`. Seeded drafts the client never reviewed are listed in the go live summary, so the client knows exactly what is still unconfirmed when their team starts work.
- Facts the team verifies against a live source during the install (for example, a connection state proven by a live read) are confirmed by the team with that source named, without waiting for the client.

After go live, the same flow applies to later edits: a client correction in the hub or in a meeting changes the fact, keeps the old confirmed value in the Change notes, and cites the new source. Confirmed facts are versioned, never silently overwritten.

## 3. Contradictions

A contradiction is any case where two records state different values for the same fact: memory against a connected system, memory against the client's website, or two memory files against each other.

1. Neither value is edited away. A flag opens in `open-flags.md` naming both values and both sources.
2. The fact is checked against the live source. The live source wins over any memory file, including this one.
3. The losing value is corrected with a Change note citing the live source and the flag.
4. If picking wrong would have a client visible consequence (wrong price, wrong phone number, wrong approver) and the live source cannot settle it, the flag escalates to the client lead under the Team Pack escalation rules before any work relies on the fact.
5. Work that depends on a contradicted fact uses neither value until the flag resolves, or proceeds only on the parts the contradiction does not touch.

## 4. Stale facts

Facts age. The protocol assumes it and plans for it.

- Facts with a natural lifespan (offers, prices, team members, connection states, holds) are rechecked on the install's oversight cadence and whenever a task is about to rely on them.
- Rechecking means verifying against the live source, not rereading the memory file. A fact that verifies keeps its status and gains the recheck date in its source. A fact that fails becomes a contradiction and follows section 3.
- Oversight samples seeded and confirmed facts on its review rhythm: a rotating sample per cycle, weighted toward facts that delivery relies on most (contact details, approval authority, hard rules, claims). Sample failures are reported to the lane lead the day they are found.
- A seeded fact still at `draft` 30 days after go live is raised at the weekly review: confirm it, correct it, or clear it. Drafts do not age in place quietly.
- Client side changes the team can see in connected systems (a new team member in the CRM, a changed booking page) trigger a memory update with the system named as source, so memory tracks the business instead of freezing at install.
