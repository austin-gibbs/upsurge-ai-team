# UpSurge AI Team: Site and Client Journey

The public site and the start of the client experience, as one connected flow. Every page shares one design system (`site.css`, extracted verbatim from `index.html`), one header, and one footer. Shared journey logic lives in `journey.js`.

## The journey map

```
index.html  ->  book.html  ->  apply.html  ->  onboard.html  ->  home.html
Overview        Fit call        Pilot            Zero-touch        Command
and pricing     scheduling      application      self-install      home

signin.html ->  home.html
Sign in         The client's own workspace, shaped for their business
```

- A prospect lands on the overview, books a 20 minute fit call, applies for the pilot, installs their own AI organization in the onboarding hub, and wakes up in the command home.
- The landing page CTAs all point at `book.html`. The nav carries a Client sign in item to `signin.html` on every page.
- `apply.html` ends in a success state whose button enters `onboard.html`. `onboard.html` ends at go live with a first request and a route to `home.html`.
- A returning client signs in at `signin.html` and lands in `home.html`, in their own version of the tool.

## The tool adapts to the business

The client never fits into our system. The system takes the shape of their business.

- `apply.html` asks early: **What kind of business is this?** The answer is saved into the journey state and shapes everything after it.
- `journey.js` holds a `TYPES` config per business type: the word used for work items, the board stages, the work categories, starter jobs in that business's own words, sample board items, ledger entries, the order tools are connected in, the setup questions and their wording, and the draft facts offered for confirmation.
- Three types are fully written: **real estate team** (work items are Listings; stages New, Preparing, Live, Under contract, Closed), **insurance agency** (Leads; New lead, Quoting, Bound, Renewal coming), **home services** (Jobs; New job, Estimate sent, Scheduled, In progress, Done and paid). Dental practice, school or education, and something else fall back to general wording until their pack exists.
- **There is no industry limit, and something else is a first-class path.** Picking it in `apply.html` opens a free-text field, "What kind of business is it?" The client's own words are stored on the journey as `customType` and name their workspace type wherever the general wording renders: the workspace line and industry fact in `onboard.html`, and the type line, board header, and switcher in `home.html`. Wherever the general wording renders, the shaped panels also carry one plain line: "Do not see your kind of business? We shape everything around yours as we learn it."
- Production note, also in the `journey.js` header: live type configs come from the Business Type Packs in `install-templates/business-types/` and are served to the workspace at setup time.
- `onboard.html` reads the type: the connect list is reordered to that business's priorities, the setup questions use its wording, and the draft facts are its facts.
- `home.html` reads the type: the board, the starter jobs, and the ledger all speak its language. A small switcher on `home.html` (See this workspace shaped for) re-renders the board live for another type, so the adaptation is visible in one click. Switching reloads the starter shape for the chosen type and keeps the business name. The switcher also carries a **Your kind of business** option, driven by the stored `customType` words: picking it shapes the workspace from the general wording and names its type in the client's own words (asking for the words first if none are stored yet). A type line under the switcher always names the workspace's current type, in their words when they gave us words.

## Page by page

### index.html: overview and pricing
The marketing landing page: hero, problem, the live team page rendering, how it works, what you can hand off, what comes with it, approved pricing (pilot plus Launch Team, Growth Team, Full AI Organization), FAQ, and the fit call call to action. All Book a fit call and Start with the pilot links go to `book.html`.

### book.html: the fit call
Explains the three things the call covers (see the team page live, map your first ten requests, an honest answer on fit), then a scheduling panel: a day picker (the next seven days, generated in the browser so it is always current) and a time slot picker. Confirming shows a confirmation state and routes to `apply.html`. The selection is kept in `localStorage` under `upsurgeFitCall` so later steps can reference the booked call.

### signin.html: sign in and workspace choice
One email field and one big button: Take me to my workspace. In this demonstration, signing in reveals a workspace choice: three fictional businesses of different types (Summit Ridge Realty Group, real estate; Harbor & Pine Insurance, insurance agency; BrightFlow Home Services, home services). Picking one seeds that workspace's config from its business type and lands in `home.html` shaped for that business. Demonstration labeling stays on the page. Production: the workspace comes from the signed-in account, and the choice step disappears.

### apply.html: pilot application and start
A seven section form. Section 1 is the business type step above. Then business basics, the one job they want off their plate, current tools (checkbox grid), how they want to ask for work (three radio cards: Command App, their own project tool, direct to the team lead), where they want to start (tier cards, pilot preselected, approved price ranges), and the pilot terms in plain words with an agreement checkbox. Every section header carries a time estimate and a "We handle the rest" line. Client-side validation with friendly, field level errors and an error summary. Nothing is transmitted: the submit handler holds a commented wiring contract (POST the payload as JSON to `/api/pilot-applications`, which creates the prospect record and the install project), and writes the chosen business type into the journey state. A valid submit reveals the success state: what happens next in five steps with timing, and the button into the onboarding hub.

### onboard.html: the onboarding hub (zero-touch self-install)
The heart of the streamlined experience. The client installs themselves; no step waits on a human at UpSurge. A sticky progress header shows the five stages and keeps the client's place across visits.

1. **Set up your command center.** After application and start payment, setup runs as an automated sequence that ticks itself complete: command center created, workspace named for the business, team roster loaded, request board and output ledger opened, team page prepared.
2. **Connect your tools.** Eight tool rows (CRM, email, calendar, phone system, ads, file storage, accounting, project tool), ordered for the client's business type. Each Connect runs a launch and quick check loop in the UI: Opening sign-in, then Running a quick check, then Connected. The phone system row demonstrates the rescue path by design: its first quick check fails with a plain reason (an admin sign-in is required) and a Retry button, and the retry succeeds. A progress bar and counter track connections, and the security reassurance from the onboarding pack sits under the list (the client signs in on each tool's own page, UpSurge never sees a password, access can be turned off anytime, least access by default).
3. **Turn on your team.** A self-install per lane (Muse, Claude, Grok): copy the setup words, paste them into that app, tap I pasted it, and a quick check ticks itself (your team can see the team list, work rules checked, found what your team knows) and ends in Team is on. A lane counts only when every check passes.
4. **Tell us about your business.** Two parts. First, a draft facts review: facts drafted from the client's website, application, and connected tools, in their business type's set, each shown with its source, editable inline, confirmed one by one with a running counter. Second, the questions only the owner can answer, worded for their type: services, who they serve, voice (three choices plus free text), who approves client-facing work, hard rules and never-dos, busiest season, anything else.
5. **Go live.** Fires automatically the moment every stage passes its quick check: celebration state, the pack's go-live message, and a first request box right there. Until then, the panel lists exactly what remains, each item linking to its stage.

Every unfinished stage panel carries stall rescue microcopy: the next smallest step, and the promise that the client's place is kept. A Reset demo link in the progress header clears all state.

Honesty in the demo: a Guided preview badge states that connects and quick checks are pretend here. The demonstration business is Summit Ridge Realty Group, unless a workspace was picked at sign in.

### home.html: the command home
What a live client wakes up to, in their workspace's own shape:

- **Board.** Columns are the workspace's stages; cards are its work items with owners and category tags; the summary tiles count in its own words (for example Listings on the board). Category chips list its work categories.
- **Starter jobs, in your words.** Ready-made jobs from the business type, the first things the team can take on.
- **Team heartbeat strip.** The same UpSurge team for every business, in the lane and member language of the landing page.
- **Customize panel.** The client can rename any board stage inline, add a stage, remove a stage, add or rename a work category, and change the word used for work items. Every change saves to the workspace config and re-renders the board instantly. Next to it, a card for everyone who would rather not touch settings: "Do not want to touch settings? Just tell your team lead what you want changed and watch it happen," with a message box that goes to the team lead.
- **Output ledger.** Recent entries for that business type, written by completion, per the ledger rules in the product docs.
- **Next steps.** The short owner list: batched questions and the weekly review.
- **Type switcher.** In the hero: pick another business type and the whole board re-shapes live.

All home data is clearly fictional demonstration data, labeled as such.

## State model (localStorage)

Three keys, all written only inside the browser in this build:

- `upsurgeFitCall` (set by `book.html`): `{ day, slot }`, the booked fit call.
- `upsurgeJourneyV1` (set by `apply.html` and `signin.html`, read everywhere): `{ businessType, customType, workspaceId, workspaceName, shortName }`. The business type chosen in the application, the client's own words for their kind of business when they picked something else (`customType`, empty otherwise), and the workspace picked at sign in.
- `upsurgeWorkspaceConfigV1` (seeded by `signin.html` or first `home.html` load, edited by the Customize panel): the workspace's own shape: `{ workspaceId, name, shortName, type, itemWord, stages, categories, items, templates, ledger }`, plus `typeTerm` when the client's own words name the type (seeded for the something else path, and by the Your kind of business switcher option). Seeded from the business type config; Customize edits it in place; the type switcher reseeds it from the newly chosen type, keeping the business name.
- `upsurgeOnboardZeroTouchV1` (set by `onboard.html`): the install progress object:
  - `provSteps`: 0 to 5 setup steps completed. The sequence resumes or completes on return.
  - `tools`: per tool `{ s, tries }` where `s` is idle, opening, verifying, connected, or failed. Transient opening and verifying states restore as idle; connected and failed states persist, including the phone row's attempt count that drives its one designed failure.
  - `lanes`: per lane `{ pasted, drill, seated }` where `drill` is 0 to 3 checks passed. A pasted but not yet on lane resumes its quick check on return.
  - `facts`: the draft facts with their current text and confirmed flags. Editing a confirmed fact returns it to unconfirmed. Seeded from the business type's fact set on first visit.
  - `knowledge`: the answer form values, saved on input; `knowledgeSaved` records a valid save.
  - `live` and `firstRequestSent`: go live and first request state. Stage 5 completes only from the first four stages passing, never from a stored flag alone.

No data leaves the browser anywhere in this build.

## Simplicity rules for client copy

Applied across `apply.html`, `onboard.html`, `signin.html`, and `home.html`, and binding on future edits:

- **One action per step.** Each step asks for exactly one thing, and says what it is in its first line.
- **Verb-first buttons and instructions.** "Click Connect next to your email." "Copy the setup words." "I pasted it." Buttons say what happens when they are tapped.
- **Every stage header carries a time estimate and a "We handle the rest" line.** The client always knows what a step costs them and what it does not.
- **Plain words only.** The swap list is enforced in copy: connect, never integrate or integration; set up, never provision; turn on your team, never seat; a quick check, never verification; what your team knows, never knowledge base. If a word needs explaining, the word is wrong.
- **The test:** every step should be followable by someone who has never seen the product, with no help open in another tab.

## Zero-touch model: what is simulated, and where it wires for real

Simulated in this front-end build: the scheduling confirmation, the application submission, the setup sequence timing, the connect sign-in and quick check loop (including the phone failure), the lane quick check ticks, the draft facts content, the go-live trigger, the sign-in workspace choice, and the team lead change request from the Customize panel.

Production wiring points, each marked in code comments at the spot it belongs:

- `book.html`: POST the chosen day and slot to the scheduling endpoint, which creates the calendar event and sends the invitation.
- `signin.html`: the workspace comes from the signed-in account; the demo choice step is removed.
- `apply.html`: POST the application payload to `/api/pilot-applications`; the business type rides in the payload and selects the Business Type Pack for the install.
- `onboard.html` stage 1: setup steps map one to one to the install orchestrator's provision stage steps (see `../orchestrator/`); the ticks become real step completions from the orchestrator's audit log.
- Stage 2: each Connect launches the provider's own sign-in and checks with a live read against that connector before marking Connected; the failure state carries the provider's real reason. Row order comes from the type pack.
- Stage 3: the setup words are the current Team Pack bootstrap for that lane; the quick check becomes three real read checks against the turned-on platform.
- Stage 4: draft facts are generated from the client's real website crawl, application answers, and connected tool reads, using the type pack's fact set; confirmations write to the client memory.
- Stage 5: go live is the orchestrator's go-live transition, gated by the same all-stages-passed condition used here.
- `home.html`: the workspace config lives server side on the workspace. The client edits it here; the team lead writes the same config when the client asks in plain words; the type switcher is a sales and setup aid that applies the chosen type pack.

## Design rules for this folder

- One design system: `site.css` is the single source. Page-specific styles live in that page's own style block and use the shared variables.
- No em dashes in any copy. No invented statistics. No external images.
- Demo and preview data is always labeled (Guided preview, Demonstration) so simulated states are never mistaken for real integrations.
