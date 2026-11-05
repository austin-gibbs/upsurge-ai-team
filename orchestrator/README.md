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
- The live adapters are typed stubs. Every real adapter method raises
  NotImplementedError and names the exact call it will wrap. Wiring
  them, one system at a time, is the next build step. Until then the
  CLI refuses live mode and runs with `--dry-run`.
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
| `run.py` | The CLI. Walks an install, records QA approvals, prints status and the audit trail. |

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

## Wiring the real adapters

Each stub in `adapters.py` names its call in its docstring. In short:

- DeskAdapter: the Lovable query_database tool against the Surge
  Command Desk project (SELECT before INSERT, the same path production
  Desk writes use today). The passcode methods deal in pointers only;
  the value is generated server side and never enters the orchestrator.
- GitHubAdapter: `/opt/hatch/bin/github` call-tool push_files for
  writes, with every write verified by a get_file_contents read back,
  because a push can time out on the client side and still land.
- SlackAdapter: the Slack connector (channel list, channel create, send
  message). The connector cannot move files; downloads go out as
  hosted links in messages.
- ConnectorAdapter: the per-app connector docs (system connectors under
  /opt/hatch/connectors, custom ones under ~/workspace/custom-connectors).
  Verification is a status check plus one harmless read per app. API
  key apps stay on the one key at a time secure capture flow. Two known
  behaviors are baked into the docstrings: first calls to newly
  approved hosts can time out in the proxy tunnel (retry once), and
  Cloudflare protected APIs need a browser User Agent (error 1010 is
  not a bad key). The Claude and Grok seat delivery remains the guided
  paste plus verification drill from spec Section 11; no verified API
  exists for pushing into client owned accounts on those platforms.

## House rules carried into the code

No deletions anywhere (rollback archives, never deletes). Secrets are
pointers only in state records, manifests, and logs. Client facing
surfaces never see internal state detail; the audit log and state
records are internal. One alert per failure, never repeated.
