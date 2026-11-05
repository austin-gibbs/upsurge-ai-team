# Platform Policy

How the AI Team service connects to a client's tools, what it installs when a tool is missing, and how the team seats stay independent of any single platform or vendor.

Set by Maive on Austin's direction, 2026-11-04. This policy is part of the product contract: it governs every install, and anything client-facing quoted here uses the plain words of the Simple Standard.

## 1. The rule: connect what they have, install what they lack

Every business runs on the same nine functions, whatever the industry:

| Function | What it holds |
| --- | --- |
| Customer system | Customers, leads, pipelines, follow up history |
| Email | Sending and receiving mail |
| Calendar | Appointments, bookings, reminders |
| Phones and messages | Calls, texts, recorded conversations |
| Files | Documents, contracts, photos, shared folders |
| Money and invoices | Quotes, invoices, payments, bookkeeping |
| Ads | Paid campaigns and their results |
| Website | The public site and its forms |
| Work board | The client's command center, where work is tracked |

For each function, the install uses exactly one of three modes:

1. **Bring your own.** The client already has a tool that works. We connect it, learn it, and the team works inside it. Their logins, their data, their habits stay exactly where they are.
2. **Take the standard.** The client has no tool for that function, or the one they have is broken beyond light repair. We set up our standard for that function as part of the install, at no separate setup step for the client.
3. **Hybrid.** The normal case. Keep every tool that works, fill only the gaps with standards, and let the team bridge the two sides so the client sees one system.

During onboarding, each function gets one question in plain words: "Do you already have something that does this job? Show us, and we will connect it. If not, we will set up our standard for you, included in your install." The orchestrator records the chosen mode per function in the install record, and the connect stage walks the client through only the functions they actually have or are receiving. Nobody connects nine tools for the ceremony of it; each connection happens because the work needs it.

### The no rip and replace rule

Never rip and replace a working tool on day one. A migration is not an onboarding step. If a client's tool works but is not the tool we would have chosen, we connect it, the team goes live on it, and any move to a different tool becomes a separate project after the team is live, planned with the client, with its own timeline and its own confirmation. The install never holds go live hostage to a migration.

Light repair is in scope during install: reconnecting a broken sign in, fixing a pipeline stage list, restoring a disconnected calendar. Rebuilding a tool from scratch is not light repair; that is the "broken beyond light repair" case below, or a later project.

## 2. The customer system and phones standard: HighLevel

For the customer system function, and for phones and messages, the standard is HighLevel.

When a client has no customer system, or has one that is broken beyond light repair (data unusable, access lost, the tool no longer supported, or the cost of repair clearly exceeds the cost of starting clean), the install provisions a HighLevel sub-account under the UpSurge agency as part of the install:

- Provisioning is fulfilled by our team, not by the client clicking through agency settings. It is a catalog item in the Install Fulfillment Training program, with its own runbook and verification standard, under the same-day completion rule.
- The sub-account is set up in the client's business name, loaded with their pipeline stages in their words from their Business Type Pack, and connected to their phones and messages during the same connect stage as every other tool.
- Phones and messages ride the same sub-account: numbers, call recording, and texting live where the customer record lives, so the team never has to stitch a call to a contact by hand.

### The honest tradeoffs, stated plainly

Why we standardize here: it is a proven home we know deeply. Our automations, follow up sequences, and reporting are strongest on it, the team's playbooks are written against it, and a client with no system gets in one step what would otherwise take three tools and a month of stitching.

What the client gives up, and what we promise back: the sub-account lives under the UpSurge agency for as long as they are subscribed. That is real, and the agreement says so in plain words rather than hiding it. In exchange, the agreement carries this commitment, quoted as it appears to the client:

> "Your customer list and your records are yours. If you ever leave, we export your full contact list and your records from your account and hand them to you in a standard file you can take anywhere. Nothing about your business is held hostage."

Exit fairness is a selling point, not a concession: the export is complete (contacts, companies, pipeline records, notes, and conversation history where the tool allows export), delivered within ten business days of a written request, at no charge beyond any fee the agreement already names. Our team fulfills the export as a certified manual step, verified against a record count, never as an afterthought.

If a client arrives with a working customer system of their own, none of this applies on day one: bring your own wins, and HighLevel is simply the standard we offer when there is a gap or a break, or later if they ask for the migration project.

## 3. Standards for the other functions

Standards outside the customer system are recommendations, not requirements. If the client prefers the other named option, or already has an equivalent that works, bring your own applies and nothing changes about the install.

| Function | Standard | Notes |
| --- | --- | --- |
| Email | Google Workspace or Microsoft 365, as the client prefers | Either is fully supported; the team connects to the mailboxes the work uses |
| Calendar | The calendar inside their email standard | Google Calendar with Google Workspace, Outlook calendar with Microsoft 365 |
| Files | Google Drive | The client's equivalent (Microsoft OneDrive, Dropbox, their existing shared folders) is equally acceptable |
| Money and invoices | The client's existing accounting tool | QuickBooks and equivalents connect as bring your own; if they have nothing, we recommend one during onboarding and connect it once chosen, the choice stays theirs |
| Ads | The client's existing ad accounts | Accounts are always client-owned; the team connects and works inside them, never holds them |
| Website | The client's existing site and host | Forms and lead capture get wired to the customer system during connect; a rebuild is a later project, never an install step |
| Work board | The Surge Command app, their own workspace | This one is ours by design: it is the product's home, shaped by their Business Type Pack, and their data in it exports with everything else |

## 4. Lane seats are platform-agnostic

A lane is a role, not a vendor. The three lanes (Muse, Grok, Claude in our own house naming) describe kinds of work and a way of working: who leads, how work is routed, how memory is kept, how quality is checked. Any capable AI platform the client owns can fill a seat in a lane.

The certified standard is the three lanes we run deepest: Muse, Grok, and Claude. A client may seat ChatGPT, Gemini, or another platform in a lane instead, or in an additional seat, and the service works the same way.

### The Pack and memory are platform-neutral

The Team Pack and the client's memory layer are stored as markdown and structured files. Nothing in them depends on one vendor's features. Delivery to a seat uses the best method that platform supports:

- Project or system instructions where the platform offers them, so the Pack loads as standing instruction.
- A paste-ready setup block where it does not, so the client (or our team, as a certified manual step) pastes the same content into the seat's instruction surface.
- API wiring where the platform offers an API, so delivery and memory updates happen without a human in the middle.

### The drill does not change

The seat verification drill is identical across platforms and scores the same named fields: `drill.facts_check`, `drill.format_check`, `drill.isolation_check`, `drill.language_check`, `drill.status`, `drill.attempts`, `drill.completed_at`. A seat counts as seated when its drill passes, whatever logo is on the platform. A seat that fails follows the same guided retry, and the same internal flag after three attempts, on every platform.

Oversight does not change either: QA sampling rates, the output ledger, escalation, and the monthly owner report are identical whatever platform fills a seat. Quality is platform-independent by construction, because the checks never lived inside the platform in the first place.

### Platform registry

| Platform | How the Pack is delivered | How memory updates reach it | Known seat limits | Drill notes |
| --- | --- | --- | --- | --- |
| Muse | Project instructions plus the memory tree in the project workspace | Re-sync of the client memory files on each Pack or memory release | Strongest fit for the lead seat and long running work | Standard drill, no adjustments |
| Grok | System instructions in the workspace, memory files attached per workspace setup | Memory files re-issued on each release; version stamp checked at drill time | Workspace instruction size caps the Pack summary layer; full Pack rides as files | Standard drill; format check watches for truncated instruction loads |
| Claude | Project instructions and project knowledge files | Project knowledge re-upload on each release | Project knowledge is a snapshot, so stale memory is the main risk | Standard drill; facts check includes a freshness probe against the current version stamp |
| ChatGPT (OpenAI) | Custom GPT instructions or project instructions, per the client's plan | Instruction block and files re-issued on each release | Instruction field length can require the condensed Pack layer; file support varies by plan | Standard drill; if the condensed layer is used, facts check runs the extended fact set |
| Gemini | System instructions in the workspace or shared instruction surface | Memory files re-issued on each release | Instruction persistence varies by surface; confirm which surface the client owns before seating | Standard drill; language check confirms the instruction surface actually retained the Pack |
| Any other platform | The fallback method: paste-ready setup block into whatever instruction surface exists, memory delivered as files | Manual re-issue by our team as a certified manual step on each release, until the platform offers something better | Unknown until seated; the drill is what tells us | Standard drill with no fields waived; a platform that cannot pass the isolation check does not get seated with client memory |

## 5. Vendor independence principles

These principles outrank any single platform decision in this document:

1. **The client's data and memory are exportable at all times.** Contacts, records, the full client memory layer, the Business Type Pack as applied to them, and their work history export in standard files on request, and automatically at exit. No export waits on our convenience.
2. **No client's operations depend on a single AI vendor being up.** If a platform is down, degraded, or unreachable, the lead re-routes the affected work to another seated platform or holds it visibly in the work board with the client informed in plain words. Work never silently stops because one vendor did.
3. **A seat can be re-filled without a re-install.** If a platform changes its terms, raises its price past the client's comfort, or drops in quality, the seat is re-filled by another platform using the same Team Pack, the same client memory, and the same drill. The change is a seating event, recorded in the install record, not a new onboarding.
4. **Client-owned accounts wherever a tool allows it.** Ad accounts, domains, websites, and sending accounts are the client's. Where a standard runs under our agency (the HighLevel sub-account), the export commitment in section 2 is the counterweight, and it is contractual.
5. **We recommend; the client decides.** Except for the two standards named as standards in this policy (HighLevel for a gap in the customer system and phones functions, and the Surge Command workspace as the work board), every standard here is an offer with a reason, and bring your own is always an acceptable answer.
