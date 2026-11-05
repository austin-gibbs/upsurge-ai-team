# Cedar Peak Dental: AI Team Memory and Setup

Client slug: cedar-peak-dental
Repository target: upsurge-client-cedar-peak-dental, in UpSurge's GitHub organization

## What this repository is

This repository holds the working memory and setup for Cedar Peak Dental's installed
AI Team: what the team knows about this business, the rules it works
under, and the delivery records for its team seats. It is generated at
provisioning from the UpSurgeAITeam pattern in sanitized form. It carries
this client's layer only. It contains no internal brain content and no
other client's data.

## Ownership, stated plainly

- This repository and the systems around it are owned and operated by
  UpSurge. The client receives application level access through the PM
  tool, not repository access.
- The client's business data is the client's property. It is exportable
  at any time, and in full on exit, in plain files.
- The system that runs the team (the Team Pack master source, the
  routing and quality methods, the drills, the orchestrator) is UpSurge
  intellectual property, licensed while the service is active, and is
  never copied into this repository in master source form.

## What lives here

- `memory/`: the client memory layer. Facts, brand, systems, people,
  standing rules, work log, and open flags for this business only.
- `team-pack/`: one delivery record per lane, naming the platform that
  fills the seat, how the Pack reaches it, and the drill it must pass.
  Seats receive operational content in working form only.
- `positioning-and-rules.md`: the working summary of how the platform
  drives the team and the rules every lane works under.

## The PM tool is home base

All work for Cedar Peak Dental lives in the PM tool (Surge Command). Every lane
adds every project there, the client submits and watches work there, and
the Output Ledger the client reads is written from what completes
there. Nothing counts as done until it is recorded there and in the
memory work log.

## Lanes at install

Operations Lane on ChatGPT, Strategy Lane on Claude, Speed Lane on Grok

## Hard rules for this repository

- Pointers only. No credential value is ever written here: no password,
  API key, token, or secret of any kind. Systems are reached through
  named connectors and vault entries.
- One truth per fact, every fact with a source, dates absolute.
- Client layer only. Nothing from another client, and nothing from the
  internal brain, is ever copied into this repository.
