# Install Orchestrator

The small service core that runs an AI Team install unattended through
the five stages from the install pipeline spec: Provision, Connect,
Seat platforms, Seed knowledge, Go live. Python standard library only,
no external dependencies.

## Status (honest)

- The core is built and verified: state machine, step runner,
  idempotency, locking, retry policy, resume, audit log, and the QA
  gate all pass an end to end dry run and failure injection tests
  (results below).
- The live adapters are wired (live_adapters.py, selected with
  `--live --config`): Desk through the Lovable query_database tool,
  GitHub through the file based push-files subcommand with read back
  verification, Slack through the Slack connector, and Connectors in
  self serve mode (client actions return a structured awaiting
  result; nothing is faked as verified). Read only live tests pass
  (results under Live wiring below).
- One prerequisite is outstanding on the internal Desk: the team
  page migration (app/team-page/migrations/0001) has not been
  applied there, so workspace_config and team_roster do not exist
  in that database yet. The Desk adapter maps that to a clean
  SchemaError. A client Desk instance runs the migration at
  template build, so this only affects pointing live mode at the
  internal Desk before the migration lands.
- No full live install has been run yet. Maive runs the first one.
  The stubs in adapters.py remain as the interface reference; the
  dry run path is unchanged.
- v0 limits: steps run sequentially (the spec marks Stage 2 app
  connections parallel safe per app; parallel execution is a later
  refinement). A paused_human install resumes when an operator reruns
  it after fixing the cause. A failed_terminal install needs an
  operator to edit or reset its state record; there is no reset
  command yet.

## Architecture

| File | Role |
|---|---|
| `state.py` | The contract: install states, the five stages with their step definitions, the idempotency key format, the install context, and the error taxonomy. No execution logic. |
| `engine.py` | The step runner: file lock, check-before-create, retry ladder, resume, append-only JSONL audit log, the QA gate, and one ops alert per failure. |
| `adapters.py` | The four adapter interfaces (Desk, GitHub, Slack, Connectors) as stubs naming their real calls, plus the DryRun adapter set that simulates every system and records what would happen. |
| `live_adapters.py` | The live bundle: install config loading and validation, the four adapters wired to the real CLIs, and the connector self serve awaiting results. |
| `run.py` | The CLI. Walks an install (dry run or live), records QA approvals, prints status and the audit trail. |

Runtime data lives in `orchestrator/.state/` (gitignored): one JSON
state record per install (the resume point), one append-only
`<install_id>.audit.jsonl`, one lock file per install, and in dry run
mode one `<install_id>.dryrun.json` registry of simulated objects.

### State machine

initiated, provisioning, provisioned, connecting, connected, seating,
seated, seeding, seeded, qa_review, going_live, live, plus the side
states paused_human, failed_retryable, failed_terminal, suspended, and
closed. qa_review is the spec's qa_gate: the single human gate in the
pipeline. Go live steps cannot run until `approve_qa` has recorded an
approver on the install record.

### Idempotency

Every step carries the key `<install_id>:<stage>:<step>:<natural_key>`.
Before creating anything, the engine calls the step's check method,
which looks the object up by natural key in the target system (Desk row
by slug, repo path, channel by name, manifest entry). An existing
object completes the step with its existing reference and no create is
issued. Step records persist status, attempt counts, the produced
object reference, and the last error.

### Retry policy

Transient errors (timeouts, 5xx, tunnel failures) retry on the spec
ladder: first attempt immediately, retries after 60s, 300s, and 1800s,
four attempts per run. After the final attempt the step is marked
failed, the stage stops, and one alert posts to the ops channel. A
provider 429 is a hard stop for that provider in the run: the step
returns to pending, the install moves to failed_retryable, and nothing
retries in band or through alternate endpoints. Auth errors move the
install to paused_human with the exact error recorded. Schema errors
move it to failed_terminal. Locks: one runner per install via an
flock file lock; a second runner exits immediately with code 3.

## The dry run

From the repo root:

```bash
python3 -m orchestrator.run --install-id demo --dry-run
```

Walks a new install from initiated through all four pre-live stages
(28 steps) and stops at qa_review with exit code 2. Then:

```bash
python3 -m orchestrator.run --install-id demo --dry-run \
    --approve-qa --approved-by "Your Name"
```

records the approval (the approver becomes the audit actor for that
entry) and continues through the five go live steps to live, exit
code 0. Read-only commands: `--status` (state, step counts, pending
steps) and `--show-audit` (the full audit trail). Every run prints its
audit trail before exiting. Dry run mode never sleeps on the retry
ladder; the intended waits are written to the audit log instead.

### Verification results (2026-11-04, this build)

- Full walk: initiated to qa_review in one run (exit 2), then the
  approve command carried it qa_review to going_live to live (exit 0).
  33 of 33 steps done, 47 audit entries, approval recorded.
- Idempotency: with the state record deleted but the simulated systems
  left in place, a rerun resolved 28 of 28 steps from existing objects
  and issued zero creates.
- Lock: a second runner against a held lock exited immediately, code 3.
- Transient failure injected twice on one step: retried after 60s and
  300s (recorded, not slept), succeeded on attempt 3.
- Transient failure on every attempt: 4 attempts, waits 60, 300, 1800,
  step failed, stage stopped, state failed_retryable.
- Provider 429 injected: single attempt, no retry entries in the
  audit, step returned to pending, state failed_retryable.
- Auth error injected: single attempt, state paused_human.
- Resume: after a mid-install failure and recovery, completed steps
  kept their original attempt counts and the run resumed at the failed
  step and reached the gate.

## Live wiring

Live mode runs the same engine against real systems:

```bash
python3 -m orchestrator.run --install-id demo1 --live \
    --config install-demo1.json
python3 -m orchestrator.run --install-id demo1 --live \
    --config install-demo1.json --approve-qa --approved-by "Maive"
```

Smoke guard: a live run refuses (exit 5) unless the config names
`demo: true` or the operator passes `--allow-real`. Read only
commands (`--status`, `--show-audit`) skip the guard. A config slug
that conflicts with `--client-slug` is refused; in live mode the
config is the identity source.

### Install config

One JSON file per install. Pointers only, never a credential value.

```json
{
  "business_name": "Demo Bakery",
  "slug": "demo-bakery",
  "repo": "austin-gibbs/upsurge-ai-team",
  "path_prefix": "clients",
  "branch": "main",
  "desk_project_id": "6b29dcf6-5f01-4dbe-a701-2c8f1ff20f48",
  "slack_channel": "ai-command",
  "tier": "pilot",
  "lanes": ["muse", "claude", "grok"],
  "demo": true,
  "sponsor_name": "Demo Sponsor",
  "sponsor_email": "",
  "timezone": "America/Denver",
  "intake_mode": "surge-form",
  "seat_model": "client-owned",
  "pack_version": "1.0.0",
  "crm_connector": "ghl"
}
```

Required: business_name, slug, repo. desk_project_id defaults to
the internal Surge Command Desk project; a client install names its
own Desk project. path_prefix plus slug gives the memory tree root
in the repo (here clients/demo-bakery).

### Desk adapter (Lovable query_database)

- Workspace identity is the single workspace_config row (id = 1).
  If that row already holds a different client name, the adapter
  raises SchemaError rather than overwrite another client's
  workspace.
- The install's own Desk project is a public.requests row (client
  set to the business name) whose links jsonb carries the marker
  {"orchestrator": {"install_id": ...}}. Check-before-create looks
  the row up by that marker. The passcode pointer, webhook
  registrations, intake flags, and heartbeat state live in the
  same links object; every update is read back and verified.
- team_roster is shared template data: the roster step inserts the
  seed from app/team-page/migrations/0002_roster_seed.sql only
  when the table is empty, then reads the count back.
- Prerequisite: the target Desk must have the team page schema
  (app/team-page/migrations/0001). Without it, workspace and
  roster calls fail with a SchemaError naming the missing table,
  which is the correct stop: applying migrations to a Desk is a
  template build step, not an install step.

### GitHub adapter (push-files subcommand)

Writes use `/opt/hatch/bin/github push-files` with a local snapshot
directory and a NUL delimited paths file. File contents never
travel in --arguments-json: the call-tool path passes contents in
argv and dies with "Argument list too long" on multi file batches
(hit during the service repo build out on 2026-11-04). Reads use
call-read-tool get_file_contents, with the file text in the second
content element (resource.text). Every write verifies by read
back: one file per batch, and the manifest, stage records, and
routing table verify their own file. A push that times out on the
client side may still have landed, so a timeout falls through to
the same read back before the step is allowed to fail.

Path mapping: the step natural keys carry the brain layout from
the spec; the live tree re-roots them under <path_prefix>/<slug>.
Layer files at the root, manifest.json, pack/<lane>.md delivery
records, review-package.md. Stage records live inside
manifest.json, which is read, updated, pushed, and read back.

### Slack adapter

Channel names resolve to ids by exact name search
(slack_search_channels); creation uses slack_create_conversation
and is verified by searching the name afterwards; sends use
slack_send_message (the text field is named message). Install
notices go to the configured channel and carry the install id in
the body; the start notice check reads the channel back and looks
for the install marker, so a re-run does not double post. The
connector cannot move files; downloads go out as hosted links in
messages. The engine's failure alerts post to #ai-command.

### Connector adapter (self serve)

Client owned third party tools cannot be connected by the
orchestrator: only the client can sign in to their own accounts,
and client owned Claude and Grok seats take the guided paste from
the self serve hub (no verified API exists for pushing into those
accounts). So in live mode every connector check returns None
(nothing verified yet) and every apply returns a structured
result instead of raising:

```json
{"status": "awaiting_client_action", "action": "connect:gmail",
 "natural_key": "gmail", "detail": "...", "recorded_at": "..."}
```

The engine records that dict as the step's object reference, so
the install record shows exactly which client action each step is
waiting on. Nothing is claimed as verified, the install parks at
the qa_review gate, and go live still needs a recorded QA
approval. When a connector's verification is wired for real, its
check method starts returning the verification reference and a
re-run converges without engine changes. Known behaviors from the
connector docs still apply when that wiring lands: first calls to
newly approved hosts can time out in the proxy tunnel (retry
once), Cloudflare protected APIs need a browser User Agent (error
1010 is not a bad key), and API key apps stay on the one key at a
time secure capture flow.

### Smoke test procedure (read only, no side effects)

1. Write a demo config (demo: true) for a throwaway slug.
2. Construct the live adapters and run only reads:
   Desk query of public.requests (row count proves the live read
   path), find_client_by_slug and roster_exists (SchemaError with
   the missing table named is the expected result against a Desk
   without the team page migration), GitHub read_file of the repo
   README (text returned) and of the demo manifest path (None),
   Slack find_channel_by_name for the configured channel (the id),
   and one connector apply (an awaiting dict) plus one check
   (None).
3. Guard checks: `--live` without `--config` exits 5; a config
   without demo: true and without `--allow-real` exits 5;
   `--live --config <demo> --status` exits 0.
4. Dry run regression: a fresh dry run still walks to the gate
   (exit 2) and the approve command still reaches live (exit 0).

Results on 2026-11-04: all of the above passed. Desk read of
public.requests returned 42 rows; the internal Desk returned
SchemaError for workspace_config and team_roster (migration not
applied there yet); GitHub read the service repo README and
returned None for the absent demo manifest; Slack resolved
ai-command to C0C2U7E3XAM; connector applies returned awaiting
dicts and checks returned None. No full live install was run.

## House rules carried into the code

No deletions anywhere (rollback archives, never deletes). Secrets are
pointers only in state records, manifests, and logs. Client facing
surfaces never see internal state detail; the audit log and state
records are internal. One alert per failure, never repeated.
