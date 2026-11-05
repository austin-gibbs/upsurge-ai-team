# Business Type Pack Format

## Purpose

A Business Type Pack gives the setup team a strong starting point for one kind of business. It fills the client's PM tool with words, board stages, work groups, starter requests, setup questions, and first connections that already fit the way that business talks and works.

The goal is simple: the system bends toward the business. The business does not have to learn a new language to use it.

## Rules that apply to every pack

1. A pack is data, never code. It may set words, lists, order, questions, and starting choices. It may not add scripts, formulas, hidden steps, or program logic.
2. The client can rename anything the pack sets. That includes the name for a project, a customer, a work item, every board stage, every work group, and every starter request.
3. The client can add, remove, or reorder board stages and work groups during setup and at any later time.
4. The client's AI point of contact can apply those choices, save them in the client's own word list, and use the client's words from then on.
5. A pack is a starting point, not a mold. If a business works in two ways, choose the closest pack first, then copy in only the useful parts from another pack.
6. The General Services pack is the fallback when no named pack fits, when the business is hard to classify, or when the owner prefers to start plain and shape everything themselves.
7. The words shown to the client must be plain words the owner already uses. Do not use company-only terms, software terms, or team-only terms in client-facing text.
8. Starter requests are examples, not limits. The owner can change the words, save new favorites, and ask for help in any normal wording.
9. Connection order is a recommendation. The owner may connect a different tool first if that tool matters more to their business.
10. Packs move with the Team Pack. Every pack lists the Team Pack version it works with. When the Team Pack gets a new version, each pack is checked, updated if needed, and released with that same update.
11. A pack never overrides the client's safety, privacy, legal, or approval rules. Pack guardrails add protection. Client rules and the law come first.
12. Nothing in a pack promises that a connected tool can do something until that tool has been checked live during setup.

## No matching pack is the normal case

Most businesses will not match a library pack exactly, and many will match none at all. That is the normal case, not an exception. The packs in this library are accelerators: they save time when a business happens to resemble one. The default path for anything new, mixed, or unclassifiable is the generator (see pack-generator.md), which builds the pack from the client's own materials and answers, on the universal core (see universal-core.md). A client is never squeezed into the closest library pack when the fit is poor, and no industry is out of scope.

## Required pack layout

Copy this layout exactly. Keep the headings in this order.

### 1. Pack facts

Include these fields:

| Field | What it means |
| --- | --- |
| Pack ID | A short, stable ID in lowercase words joined by hyphens. It never changes after release. |
| Display name | The name people see when choosing the pack. |
| Pack version | The version of this pack. |
| Team Pack version | The Team Pack version this pack was checked against. |
| Use this pack when | A plain description of the businesses this pack fits. |
| Main promise | One sentence that says how the setup will feel for this kind of business. |

### 2. Words this business uses

Use a three column table:

| General idea | Words to use | What it means here |
| --- | --- | --- |

The table must define at least these ideas:

| General idea | Required meaning |
| --- | --- |
| Project | The larger piece of work that holds the steps, messages, files, and dates together. |
| Customer | The person or business being served. Use the word this business uses every day. |
| Main work item | The central job, case, listing, appointment, enrollment, or other unit of work. |
| New person | Someone who has asked for help but is not yet a customer. |
| Done | The clear end point for the main work item, in plain words. |

A pack may add more words when the business has common terms that would confuse a new user if translated poorly.

### 3. Starter board stages

List 5 to 7 stages in order. Stage names must sound like the business, not like office software. The stages should cover first contact, work in progress, waiting or next action, delivery, and the finished state.

The setup may rename, add, remove, or reorder stages before the board goes live.

### 4. Task categories

List 6 to 10 work groups. Use short names an owner would say out loud. A category is a helpful sorting label. It does not limit what the client can ask for.

### 5. Starter requests

List 5 to 8 requests. Each request must be one line and written the way the owner would naturally say it. A starter request should be useful on day one and should not need special codes or fixed wording.

### 6. Connect first

List the first tools in order. For each tool, say:

- what kind of tool it is
- why it comes at that point in the order
- what the setup team checks after the client signs in

Use tool types, not required brand names, unless the pack truly depends on a named kind of system.

### 7. Questions we ask during setup

List 4 to 7 questions that are special to this kind of business. Ask only what will change the setup, the words, the board, the first connections, or the first work. Write each question in plain language.

### 8. What we look for first

List the useful facts to gather from the client's website, public pages, and connected tools. For each source, say what to look for and where it helps. Do not list private records as a website or public source. If a source needs client approval or special access, say so plainly.

### 9. Team help that matters most

Name the specialists and starter work skills that matter most for this kind of business. Keep the focus on useful help, such as sorting requests, writing follow ups, checking dates, building reports, or reviewing work. Other specialists remain available when the client needs them.

### 10. Extra guardrails

List any safety, privacy, money, health, legal, or promise related limits that are special to this kind of business. Write them in plain words. If there are no special limits, say that the standard client approval and privacy rules apply.

### 11. Client choices

Close every pack with the choices the client controls. At minimum, remind the owner that they can:

- rename the pack's words
- change board stages
- add or remove work groups
- save their own starter requests
- choose a different first tool to connect
- tell the team to stop using any word that does not fit

## Writing checks before a pack is released

Before a pack ships with a Team Pack update, check all of these:

- The pack ID matches the file name.
- The headings match this format and stay in order.
- The board has 5 to 7 stages.
- There are 6 to 10 task categories.
- There are 5 to 8 starter requests.
- There are 4 to 7 setup questions.
- The connection list is in a clear order and gives a reason for each step.
- All client-facing words sound natural when read out loud.
- No client-facing text depends on team-only language.
- The client rename rule is stated in the pack.
- Safety and privacy limits are plain and visible.
- The pack version and Team Pack version are filled in.
