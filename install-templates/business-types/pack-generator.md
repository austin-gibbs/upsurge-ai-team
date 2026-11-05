# The Pack Generator

## Purpose

This is the standard way a Business Type Pack comes into existence. The generator is the default path for every client. It builds the pack from the client's own business, in the client's own words, for any industry, including industries with no library pack and businesses that fit no known category.

A library pack is an accelerator. When a library pack closely matches the business, generation starts from it and then corrects it against the client's materials. When nothing matches, generation starts from the universal core alone. Both paths end in the same place: a pack the client has seen, adjusted, and confirmed.

## Inputs, in strict priority order

Work the inputs in this order. A higher input always beats a lower one when they disagree.

### Input 1: The client's own website and materials (highest authority)

Gather first, before asking the client anything:

- their website, every page that describes offers, services, process, pricing shape, team, and locations
- their public listings and profiles (search, maps, directories, social profiles)
- documents they share during signup: brochures, menus, rate sheets, intake forms, proposals, contracts, email templates
- their own words for their offers, their customers, and their work, copied character for character where the words themselves matter

Rule: if a word, stage, or category cannot be traced to this input or to the client's own answers, it does not go in the pack.

### Input 2: The client's connected tools and their data shapes

Once tools connect during setup, read their shapes, not just their names:

- the CRM or client list tool: its pipeline stages, custom fields, and tags are the client's real workflow, written by the client over time
- the calendar: appointment types and durations show how work is actually scheduled
- the inbox: recurring senders, labels, and the shape of a normal week of messages
- the accounting tool: invoice categories and item names show what the business actually sells
- any industry tool they already run: its object names and statuses are vocabulary evidence

Rule: data shapes beat assumptions. If the CRM has six pipeline stages, the board starts from those six, renamed only if the client asks.

### Input 3: The universal questions

Ask the six universal intake questions from universal-core.md, plus the two gap follow ups when needed. The walk-through answer (question 3) is the primary source for board stages. The vocabulary answer (question 4) is the primary source for the words table where Input 1 was silent.

### Input 4: Brain craft knowledge (lowest authority, seasoning only)

The UpSurgeAITeam brain and the Team Pack contribute craft, never facts about this client:

- which specialists and starter skills usually matter for work of this shape
- guardrail patterns for businesses that handle money, health, legal, or personal data
- connection order lessons from past installs of similar shape
- QA checklist additions for deliverable types this business will request often

Rule: brain knowledge may suggest a question or a guardrail. It may never supply the client's words, facts, stages, or categories.

## Generation steps

Run these steps in order. Each step produces named pack fields from pack-format.md.

1. **Collect.** Pull Input 1 completely. List every source used, with the date read. Nothing is drafted yet.
2. **Map the offers.** From Input 1 and question 1, write the offer list in the client's words. This seeds the task categories and the memory profile.
3. **Map the journey.** From question 3 and the CRM shape in Input 2, draft the work journey as a stage list in the client's order and words. Trim or extend to 5 to 7 stages for the starter board, keeping the client's names even when two stages must merge.
4. **Build the words table.** Every row traces to a quote from Input 1, Input 2 field names, or the answer to question 4. Mark the source beside each word in the working draft (sources are removed from the client-facing pack, kept in the install record).
5. **Draft the categories and starter requests.** Categories from the offers and the recurring work (question 5). Starter requests from the pain list (question 6), written the way the client said them, lightly cleaned for clarity only.
6. **Order the connections.** Connect first list ordered by what unblocks the board and the memory fastest for this business shape: usually the client list tool, then email, then calendar, then the rest. Each entry states what the setup checks after sign in.
7. **Write the setup questions.** Only the gaps that Inputs 1 to 3 left open and that would change words, stages, first connections, or first work. Four to seven, in plain language.
8. **Write what we look for first.** The extraction list for seeding client memory from the gathered sources, with approval notes wherever a source needs client permission.
9. **Set team emphasis and guardrails.** From Input 4, matched to the work shapes found in steps 2 to 5. Guardrails are written in plain words and marked as pack additions on top of the core rules.
10. **Assemble and self-check.** Build the pack in the exact pack-format.md layout and run the quality checks below before the client sees it.

## The client confirmation loop

The pack does not lock on the team's word. It locks in the hub, with the client, like this:

1. **Show, do not describe.** The client sees their actual board in the hub, in their words, with their stage names, plus their words table and starter requests as simple lists. No internal pack file is ever shown.
2. **Ask three things only.** Does this sound like your business? What word is wrong? What is missing? Everything else is detail the lead can adjust later.
3. **Adjust live.** The lead (or the client, in the customize panel) renames, reorders, adds, and removes on the spot. Each change saves to the client's word list immediately.
4. **Confirm the start.** The client confirms the board and words are right enough to start. "Right enough" is the standard: the pack is a living draft, so perfection is not required and must not delay go live.
5. **Record the version.** The confirmed draft becomes pack version 0.1 for this client, stamped with the date and the sources used. The install record keeps the source list from step 4 of generation.

## Quality checks on a generated pack

Every generated pack passes these before the confirmation loop, and the lead re-checks them after any large reshape:

- **Traceability.** Every word, stage, and category traces to the client's materials, their tools' shapes, or their answers. Untraceable items are cut or asked about, never kept on a guess.
- **No invented jargon.** If the client does not say it, the pack does not say it. Software words, marketing words, and team words are all failures here.
- **Out loud test.** Stage names and starter requests read aloud sound like the owner talking, not like a brochure.
- **Journey completeness.** The stages cover first contact to paid, with a waiting state and a done state the client recognizes as theirs.
- **Counts.** Stages 5 to 7; categories 6 to 10; starter requests 5 to 8; setup questions 4 to 7, matching pack-format.md.
- **Rename readiness.** Nothing in the pack breaks if the client renames every word on day one. If something would break, it was code wearing a data costume; send it back.
- **Guardrail honesty.** Pack guardrails state what the team will not do without approval in plain words, and never promise a connected tool a capability it has not proven live.

## The living-draft rule

A generated pack is never finished. It is a living draft that the lead keeps reshaping as the business reveals itself:

- **Every correction is cheap.** When the client corrects a word, stage, or category in conversation, the lead applies it the same day and the pack version ticks up (0.1 to 0.2, and to 1.0 at the first monthly review if the client confirms it still fits).
- **Usage teaches.** Requests that do not fit any category, stages where work piles up, and words the client keeps retyping by hand are all signals. The lead reviews them in the weekly oversight pass and proposes pack adjustments.
- **The client can reshape at any time.** Through the customize panel or by telling their point of contact. There is no change window and no ticket.
- **Versions are kept, nothing is lost.** Each version is saved in the install record with its date and what changed. Rolling back to an earlier shape is always possible. Nothing is deleted.
- **General lessons flow up, details never do.** If a generated pack reveals a pattern useful for other businesses of similar shape, the generalized pattern may strengthen the library or the generator through the brain's sanitization path. The client's words, facts, and pack itself never travel.

## When generation runs

- At onboarding, after Input 1 collection and the first connections, before the board goes live.
- Again in light form at the first monthly review, when real usage replaces first impressions.
- Any time the client changes what they sell, who they serve, or how a job flows.
