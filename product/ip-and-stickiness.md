# Ownership, IP Protection, and Stickiness Model

## Why this document exists

The AI Team service runs inside a client's daily operations. That closeness is the value and the risk. A client who loves the work may ask, reasonably, what stops someone from copying the whole thing and running it without us. This document answers that question in full: what belongs to whom, what is never handed over, how the memory rule is enforced by design, and why clients stay because the service keeps getting better, not because any door is locked.

One principle runs through everything below. We protect the system. We never hold the client's business hostage. Those two lines never trade places.

## 1. The three estates

Everything involved in an install belongs to exactly one of three estates. The pilot agreement names all three.

### Estate one: Client Data

The client's business facts, contacts, records, customer lists, content, files, and anything their team created in their business's name. This is the client's property, fully and without qualification.

- Exportable at any time while subscribed. The client asks, we produce the export, no fee and no argument.
- On exit, for any reason, the client receives a full export of their Client Data.
- We never hold data hostage: not for payment disputes, not for notice periods, not for any reason. Amounts owed are settled as amounts owed. Data is never the lever.

### Estate two: the Client Memory Instance

The client's memory tree, their shaped business type pack, their work log, and their output ledger history. This estate is mixed by nature: the contents are about the client's business, and the structure that makes them useful is ours.

- Operated by UpSurge, in UpSurge-owned infrastructure, for the life of the subscription.
- Licensed to the client for use while subscribed. The client works in it every day through their app and their team; they do not administer the systems underneath it.
- On exit, the client receives a full export of the factual contents: their facts, their decisions, their work log, and their output ledger, in plain files they can open and keep. What does not transfer is the operating machinery around those contents: the memory system that keeps them current, the audit loops, and the templates in their master form. The client leaves with everything their business said and everything their team did. They do not leave with the factory.

### Estate three: the System

The Team Pack master source, the playbooks, the QA checklists and scoring, the drills, the routing rules, the install orchestrator, the PM app template, the business type pack generator, and the UpSurgeAITeam brain itself. This is UpSurge intellectual property.

- Licensed for use during the subscription. Never transferred. Never sold as a separate product.
- Never delivered in master-source form, to any client, at any tier, for any price. A client who wants to own the system outright is asking to buy the company, and the answer is the same at every level of the conversation: the service is the product.
- Client staff never receive seats, logins, or read access into System repositories or the brain.

## 2. Repo and infrastructure ownership

The mechanics that keep the three estates real, not just contractual:

- Every client's memory repo is created in, and owned by, UpSurge's GitHub organization. Every PM app instance is created from the app template under UpSurge's hosting accounts. There are no exceptions and no client-administered clones.
- The client receives application-level access only: their login to their own PM app, showing their workspace and nothing else. They never receive repo access, never receive admin rights to the underlying projects, and never see another client's instance.
- Memory updates, app updates, and Pack updates are pushed by UpSurge systems from UpSurge accounts. The client can watch their workspace improve; they cannot reach the machinery that improves it.
- The one deliberate exception: the client's AI platform accounts, the seats themselves, are client-owned. The approved pricing model treats platform seats and usage as client-owned pass-through, never inside the management fee. Section 7 addresses what that means honestly.

## 3. The brain-write rule

Their AI team must save everything to the memory brain. This is a rule with teeth, enforced by design at four points, not by asking nicely.

- **It is in the seat instructions.** Every lane's seat instructions, on every platform, carry the same standing instruction: work is not finished until it is recorded in the memory instance, in the client's memory tree, in the standard formats. A seat that cannot write to memory does not pass its installation drill.
- **The Output Ledger only counts recorded work.** The ledger is written only by the completion event in the memory instance. Work performed but not recorded does not appear in the ledger, does not count toward the monthly request totals, and does not appear in the owner report. Unrecorded work, for every reporting purpose, does not exist. This makes recording the rational move for every seat on every task.
- **The PM app reads its state from the memory.** Board state, work history, and the client-visible summaries are projections of the memory instance. A team that skipped memory would show the client an empty board. The memory is not a diary kept alongside the work; it is the work's system of record.
- **Oversight audits it weekly.** The oversight model runs a memory completeness audit: work visible in connected tools (sent messages, created records, published pages) that has no matching memory record is a named red flag, raised the same day. Memory health, the share of work properly recorded, is a scored line in the monthly owner report the client sees. The client watches the same number we do.

The result: saving to the brain is not a habit we hope the team forms. It is the only way work counts, the only way the client sees progress, and a graded behavior under oversight.

## 4. What is never delivered

The crown jewels, and where each one lives:

| Item | Where it lives | What the client side ever sees |
| --- | --- | --- |
| Team Pack master source | The UpSurge service repo only | Operational delivery per seat: each seat receives what it needs to do its work, in working form. Never the master files, never the versioning history, never the QA internals |
| Drill banks and scoring rubrics | UpSurge side only | The experience of being checked. A seat passes or fails a drill; it never sees the rubric it was scored against |
| The sanitization pipeline and brain consolidation process | Internal to UpSurge, in the brain | Nothing. Clients know generalized lessons flow both ways in sanitized form (section 5); the pipeline that does it is never described in operational detail |
| The install orchestrator source | UpSurge side only | Its results: a provisioned workspace, a connected tool list, a live team. The orchestrator operates their install; it never ships to them |
| Fleet-level data from other clients | UpSurge side only, aggregated internally | Never, in any form. No client ever sees another client's facts, volumes, results, or identity in any artifact of their install |
| The business type pack generator | UpSurge side only | Its output: their shaped pack, in their words. The generator that produced it stays home |

The pattern to notice: clients receive outputs and working capability. The sources, the scoring, and the machinery stay in UpSurge infrastructure. Copying what a client can touch produces a photograph of the service, not the service.

## 5. The generalized learning right

The agreement discloses, in plain language the client reads before signing, that sanitized and generalized lessons from their install may improve the Team Pack for all clients. The disclosure names
...[truncated 5525 chars]