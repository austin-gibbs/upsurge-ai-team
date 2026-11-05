# UpSurge AI Team: Service Repo

This repo is the product. It holds everything that ships to a client when UpSurge installs an AI Team into their business: the install system, the Team Pack, the client-facing materials, and the templates each install is cloned from.

It is deliberately separate from the internal `upsurgeaiteam` repo. That repo is UpSurge's internal brain: client work, internal process, raw memory, experiments. Nothing in this repo may ever contain client data, client names from real engagements, internal process notes, or credential material of any kind.

## The two-repo model

- **upsurgeaiteam (the brain)** is where the team works and learns. Every engagement, build, failure, and fix lands there first, in full internal detail.
- **upsurge-ai-team (this repo, the product)** is what clients receive. It contains only generalized, sanitized, client-safe knowledge: systems, processes, checklists, templates, and the roster, with placeholders where a real install inserts the client's own facts.

## The strengthening loop (how this repo gets better)

1. Real work happens in the brain. The team builds, fixes, and learns on live engagements.
2. On the weekly consolidation pass, generalized lessons are extracted: a process that worked, a failure mode to guard against, a checklist gap, a better build pattern.
3. Each candidate passes the sanitization checklist in `team-pack/team-pack-and-roster.md` (no names, no data, no identifiers, no verbatim client material, no credentials).
4. Approved lessons are committed here as Team Pack updates with a version increment and a changelog entry.
5. Installs pull Pack updates on the push process defined in the Team Pack document. Every installed team gets stronger because the whole team learned, and no client's information ever travels with the lesson.

Flow is one way for knowledge and never for data: brain to product to installs. Nothing flows from a client install back into this repo except through the same sanitized path, reviewed by Maive.

## Build doctrine (Austin, 2026-11-04)

GitHub is the source of truth for everything in this product. Code is built and tested locally first, then pushed to GitHub, and deployments sync from GitHub. Lovable credits are never spent on this product: no editing or generating inside Lovable. The scalable shape is one template codebase with per-client configuration and data, never per-client hand builds.

## Contents

- `install-system/AI-Team-Install-System.md`: the master system document. Architecture, the five install stages, the client experience, the heartbeat page, automation status and gaps, build order.
- `install-system/install-pipeline.md`: the install pipeline spec. Stages, state machine, idempotency, failure handling, provisioning manifest, intake adapters.
- `install-system/client-onboarding-pack.md`: everything the client receives. Welcome, timeline, connect checklist, how to work with the team, go live, FAQ.
- `install-system/heartbeat-page-spec.md`: the client-facing team page build spec, with the Desk schema additions and the data honesty rules.
- `team-pack/team-pack-and-roster.md`: Team Pack v1. Components, routing rules, QA checklists, the two-layer memory contract, the roster coverage matrix, and the quality system.

## Rules for this repo

- No deletions. Superseded material moves to an `archive/` path.
- No credential values, ever. Pointers only, and client installs hold their own pointers in their own layer.
- House style: no em dashes, dates absolute, one truth per fact.
- Every change states which install version it affects and lands with a changelog note in the Team Pack document.
