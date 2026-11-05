# Client Memory: {{business_name}}

Client slug: {{slug}}
Team Pack version at install: {{pack_version}}

## What this is

This folder is the Client layer for {{business_name}}. It holds what the team knows about this one business: its facts, brand, systems, people, rules, and work history. It is created by the install orchestrator at provisioning from the templates in this pack, seeded during the install, and maintained by the team for the life of the install.

It is one of two memory layers. The other is the Craft layer, the Team Pack, which holds how the team works and is identical across installs. The two layers never mix. This folder never ships to another install, and nothing in it enters the Craft layer except a generalized pattern that has passed the sanitization checklist in the Team Pack memory contract and been approved by Maive.

This memory instance lives in a repository owned by UpSurge. For every install, that repository is created and held under UpSurge's GitHub organization. The client receives application-level access to their memory through the product, not ownership of the repository, and receives a full factual export of their Client layer on exit, per `product/ip-and-stickiness.md`.

## Files in this folder

- `client-profile.md`: Business basics, engagement facts, tier, lanes, intake mode, install record, links.
- `brand-kit.md`: Voice, visual identity, and the approved claims list.
- `systems-map.md`: Every connected system, its purpose, its connection state, and a credential pointer per system.
- `people.md`: Client side contacts, roles, and approval authority.
- `standing-rules.md`: Approval rules, hard rules, never-dos, holds, and escalation preferences.
- `work-log.md`: Index of Desk projects and deliverables, plus the decisions log.
- `open-flags.md`: Unresolved items, each with an owner and a next check date.

## Update discipline

1. One truth per fact. A fact lives in exactly one file, in exactly one place. Other files link to it instead of restating it. If two records disagree, neither is silently overwritten: the conflict goes to `open-flags.md` and is resolved against the live source.
2. Every fact carries a source. A fact without a source is not recorded. Sources are named concretely: the client website URL, the connected system and record, the hub confirmation, the meeting, or the person and date.
3. Facts carry a status. `draft` means auto-seeded or team gathered and not yet confirmed. `confirmed` means verified against the live source or confirmed by the client in the hub. Work that affects delivery, money, or a client send relies on confirmed facts only.
4. Edits are versioned, never silent. When a confirmed fact changes, the old value moves to the change note at the bottom of the same file with the date, the new source, and who made the change. See `seeding-protocol.md` in this template pack for the full protocol.
5. Dates are absolute. Write 2026-11-04, not "next Tuesday" or "recently".
6. No credential values ever. This folder holds pointers only: connector name and vault entry name. See `systems-map.md`.
7. Names, addresses, phone numbers, and identifiers are copied character for character from a source in front of the writer. Never reconstructed from memory.

## Who writes here

- The orchestrator writes the empty structure at provisioning and the seeded draft facts during the Seed stage.
- The client writes through the hub: confirmations and edits land here with the hub as their source.
- The team writes during delivery: work log entries on completion, flags when something is unresolved, rule changes when the client gives a new instruction.
- Oversight reads here on its sampling cadence and flags stale or contradicted facts in `open-flags.md`.
