"""The install orchestrator engine.

Responsibilities, all from the install pipeline spec Section 10:

- One runner per install: a file lock keyed by install_id in the state
  directory. A second runner exits immediately.
- Check-before-create idempotency: every step looks its object up by
  natural key before creating it.
- Retry policy: transient errors retry on the ladder (immediate, then
  60s, 300s, 1800s); a provider 429 is a hard stop for that provider in
  this run; auth errors pause for a human; schema errors are terminal.
- Resume: the state record is the resume point. A run picks up at the
  first step not marked done; no stage restarts from zero.
- Audit: every transition and step outcome appends one JSON line to the
  install's audit log. The log is append only.
- The human gate: when every pre-live stage is done, the install stops
  at qa_review. Go live runs only after approve_qa records an approver
  on the install record.
"""

from __future__ import annotations

import fcntl
import json
import os
import time
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Dict, Iterator, Optional

from .state import (
    GATE_NAME,
    GATED_STAGE_KEY,
    MAX_ATTEMPTS,
    RETRY_WAITS,
    STAGES,
    AuthError,
    InstallContext,
    InstallState,
    LockHeld,
    ProviderRateLimited,
    SchemaError,
    Stage,
    Step,
)

# Run outcome statuses returned by Engine.run.
LIVE = "live"
GATE = "gate"
LOCKED = "locked"
RATE_LIMITED = "rate_limited"
PAUSED = "paused_human"
FAILED = "failed_retryable"
TERMINAL = "failed_terminal"
BLOCKED = "blocked_state"


@dataclass
class RunResult:
    status: str
    state: str
    message: str


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class Engine:
    def __init__(
        self,
        state_dir: Path,
        adapters: object,
        sleeper: Callable[[float], None] = time.sleep,
        actor: str = "orchestrator",
        log: Callable[[str], None] = lambda msg: None,
    ) -> None:
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.adapters = adapters
        self.sleeper = sleeper
        self.actor = actor
        self.log = log

    # -- paths ------------------------------------------------------------

    def _state_path(self, install_id: str) -> Path:
        return self.state_dir / f"{install_id}.json"

    def _audit_path(self, install_id: str) -> Path:
        return self.state_dir / f"{install_id}.audit.jsonl"

    def _lock_path(self, install_id: str) -> Path:
        return self.state_dir / f"{install_id}.lock"

    # -- locking ----------------------------------------------------------

    @contextmanager
    def _locked(self, install_id: str) -> Iterator[None]:
        fd = os.open(self._lock_path(install_id), os.O_CREAT | os.O_RDWR, 0o644)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            os.close(fd)
            raise LockHeld(f"another runner holds the lock for install {install_id}")
        try:
            yield
        finally:
            fcntl.flock(fd, fcntl.LOCK_UN)
            os.close(fd)

    # -- state record -----------------------------------------------------

    def load_record(self, install_id: str) -> Optional[dict]:
        path = self._state_path(install_id)
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def _save(self, record: dict) -> None:
        record["updated_at"] = _now()
        path = self._state_path(record["install_id"])
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(record, indent=2), encoding="utf-8")
        os.replace(tmp, path)

    def _new_record(self, ctx: InstallContext) -> dict:
        steps: Dict[str, dict] = {}
        for stage in STAGES:
            for step in stage.steps:
                steps[f"{stage.key}.{step.key}"] = {
                    "status": "pending",
                    "attempts": 0,
                    "last_attempt_at": None,
                    "idempotency_key": None,
                    "natural_key": None,
                    "object_ref": None,
                    "error": None,
                }
        return {
            "install_id": ctx.install_id,
            "params": ctx.params(),
            "state": InstallState.INITIATED.value,
            "steps": steps,
            "approvals": {},
            "created_at": _now(),
            "updated_at": _now(),
        }

    # -- audit ------------------------------------------------------------

    def _audit(self, install_id: str, actor: str, event: str, **fields: object) -> None:
        entry = {"ts": _now(), "actor": actor, "event": event}
        entry.update(fields)
        with open(self._audit_path(install_id), "a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry) + "\n")
            fh.flush()
            os.fsync(fh.fileno())

    def read_audit(self, install_id: str) -> list:
        path = self._audit_path(install_id)
        if not path.exists():
            return []
        return [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    def _transition(self, record: dict, to_state: InstallState, reason: str) -> None:
        from_state = record["state"]
        if from_state == to_state.value:
            return
        record["state"] = to_state.value
        self._audit(
            record["install_id"],
            self.actor,
            "transition",
            from_state=from_state,
            to_state=to_state.value,
            reason=reason,
        )
        self.log(f"[state] {from_state} -> {to_state.value} ({reason})")

    def _alert(self, record: dict, text: str) -> None:
        """One alert per failure to the ops channel. Never masks the failure."""
        try:
            self.adapters.slack.post_message("#ai-command", text)
        except Exception:
            pass

    # -- the QA gate ------------------------------------------------------

    def approve_qa(self, install_id: str, approved_by: str) -> bool:
        """Record the QA approval. Returns False when not at the gate."""
        with self._locked(install_id):
            record = self.load_record(install_id)
            if record is None or record["state"] != InstallState.QA_REVIEW.value:
                return False
            record["approvals"][GATE_NAME] = {
                "approved_by": approved_by,
                "approved_at": _now(),
            }
            self._audit(
                install_id, approved_by, "gate_approved", gate=GATE_NAME
            )
            self._save(record)
            return True

    # -- running ----------------------------------------------------------

    def run(self, ctx: InstallContext) -> RunResult:
        install_id = ctx.install_id
        try:
            with self._locked(install_id):
                return self._run_locked(ctx)
        except LockHeld:
            return RunResult(
                LOCKED,
                "unknown",
                f"install {install_id} already has a runner; exiting immediately",
            )

    def _run_locked(self, ctx: InstallContext) -> RunResult:
        install_id = ctx.install_id
        record = self.load_record(install_id)
        if record is None:
            record = self._new_record(ctx)
            self._save(record)
            self._audit(install_id, self.actor, "install_created",
                        client_slug=ctx.client_slug)
            self.log(f"[install] {install_id} created for client {ctx.client_slug}")
        else:
            # Resume with the persisted identity, not the caller's args.
            ctx = InstallContext.from_params(record["params"])

        state = record["state"]
        if state == InstallState.LIVE.value:
            return RunResult(LIVE, state, "install is already live; nothing to do")
        if state in (
            InstallState.SUSPENDED.value,
            InstallState.CLOSED.value,
            InstallState.FAILED_TERMINAL.value,
        ):
            return RunResult(
                BLOCKED, state,
                f"install is {state}; an operator must act before it can run",
            )

        for stage in STAGES:
            if self._stage_done(record, stage):
                # Crash recovery: steps finished but the state never moved.
                if record["state"] == stage.active_state.value:
                    self._transition(record, stage.done_state,
                                     f"stage {stage.key} complete")
                    self._save(record)
                continue

            if stage.key == GATED_STAGE_KEY:
                gate_result = self._pass_gate(record)
                if gate_result is not None:
                    return gate_result
            elif record["state"] != stage.active_state.value:
                self._transition(record, stage.active_state,
                                 f"stage {stage.key} started")
                self._save(record)

            for step in stage.steps:
                failure = self._run_step(record, ctx, stage, step)
                if failure is not None:
                    return failure

            self._transition(record, stage.done_state,
                             f"stage {stage.key} complete")
            self._save(record)

        return RunResult(LIVE, record["state"], "install is live")

    def _pass_gate(self, record: dict) -> Optional[RunResult]:
        """Returns a RunResult when the run must stop at the gate."""
        approval = record["approvals"].get(GATE_NAME)
        if approval is None:
            if record["state"] != InstallState.QA_REVIEW.value:
                self._transition(
                    record, InstallState.QA_REVIEW,
                    "all pre-live stages complete; awaiting QA approval",
                )
                self._save(record)
            self._audit(record["install_id"], self.actor, "gate_waiting",
                        gate=GATE_NAME)
            self._save(record)
            return RunResult(
                GATE, InstallState.QA_REVIEW.value,
                "paused at qa_review: go live requires a recorded QA approval",
            )
        if record["state"] == InstallState.QA_REVIEW.value:
            self._transition(
                record, InstallState.GOING_LIVE,
                f"QA approved by {approval['approved_by']}",
            )
            self._save(record)
        return None

    @staticmethod
    def _stage_done(record: dict, stage: Stage) -> bool:
        return all(
            record["steps"][f"{stage.key}.{step.key}"]["status"] == "done"
            for step in stage.steps
        )

    def _run_step(
        self, record: dict, ctx: InstallContext, stage: Stage, step: Step
    ) -> Optional[RunResult]:
        """Returns None on success, or the RunResult that ends the run."""
        install_id = record["install_id"]
        key = f"{stage.key}.{step.key}"
        rec = record["steps"][key]
        if rec["status"] == "done":
            return None

        natural_key = step.natural_key.format(**ctx.template_vars())
        idem_key = f"{install_id}:{stage.key}:{step.key}:{natural_key}"
        rec["natural_key"] = natural_key
        rec["idempotency_key"] = idem_key
        ctx.stage_key = stage.key
        ctx.step_key = step.key
        ctx.idempotency_key = idem_key

        adapter = getattr(self.adapters, step.adapter)
        check = getattr(adapter, step.check)
        apply = getattr(adapter, step.apply)

        # Check before create: an existing object completes the step
        # without any create being issued.
        existing = check(ctx, natural_key)
        if existing is not None:
            rec.update(status="done", object_ref=existing, error=None)
            self._audit(install_id, self.actor, "step_done", step=key,
                        idempotency_key=idem_key, object_ref=existing,
                        via="existing")
            self._save(record)
            self.log(f"[step] {key} already exists, marked done ({existing})")
            return None

        rec["status"] = "running"
        self._save(record)

        for attempt in range(1, MAX_ATTEMPTS + 1):
            rec["attempts"] += 1
            rec["last_attempt_at"] = _now()
            self._save(record)
            try:
                ref = apply(ctx, natural_key)
            except ProviderRateLimited as exc:
                # Hard stop for this provider in this run. The step goes
                # back to pending, not failed; nothing retries in band.
                rec["status"] = "pending"
                rec["error"] = {"code": "provider_429",
                                "message": str(exc), "provider": exc.provider}
                self._transition(
                    record, InstallState.FAILED_RETRYABLE,
                    f"provider {exc.provider} rate limited at step {key}; "
                    "stopped for this run",
                )
                self._audit(install_id, self.actor, "provider_rate_limited",
                            step=key, provider=exc.provider)
                self._save(record)
                self._alert(record, f"Install {install_id} paused: provider "
                                    f"{exc.provider} returned 429 at {key}. "
                                    "Rescheduled, no in-band retry.")
                return RunResult(RATE_LIMITED, record["state"],
                                 f"provider {exc.provider} returned 429 at "
                                 f"{key}; hard stop for this run")
            except AuthError as exc:
                rec["status"] = "failed"
                rec["error"] = {"code": "auth", "message": str(exc)}
                self._transition(record, InstallState.PAUSED_HUMAN,
                                 f"auth error at step {key}: {exc}")
                self._audit(install_id, self.actor, "step_failed", step=key,
                            idempotency_key=idem_key, error="auth")
                self._save(record)
                self._alert(record, f"Install {install_id} needs a human: "
                                    f"auth error at {key}: {exc}")
                return RunResult(PAUSED, record["state"],
                                 f"auth error at {key}; paused for a human")
            except SchemaError as exc:
                rec["status"] = "failed"
                rec["error"] = {"code": "schema", "message": str(exc)}
                self._transition(record, InstallState.FAILED_TERMINAL,
                                 f"schema error at step {key}: {exc}")
                self._audit(install_id, self.actor, "step_failed", step=key,
                            idempotency_key=idem_key, error="schema")
                self._save(record)
                self._alert(record, f"Install {install_id} failed terminal: "
                                    f"schema error at {key}: {exc}")
                return RunResult(TERMINAL, record["state"],
                                 f"schema error at {key}; terminal, operator required")
            except Exception as exc:  # TransientError and unexpected failures
                if attempt <= len(RETRY_WAITS):
                    wait = RETRY_WAITS[attempt - 1]
                    rec["error"] = {"code": "transient", "message": str(exc)}
                    self._audit(install_id, self.actor, "step_retry", step=key,
                                idempotency_key=idem_key, attempt=attempt,
                                wait_seconds=wait, error=str(exc))
                    self._save(record)
                    self.log(f"[step] {key} attempt {attempt} failed "
                             f"({exc}); retrying in {wait}s")
                    self.sleeper(wait)
                    continue
                rec["status"] = "failed"
                rec["error"] = {"code": "transient_exhausted",
                                "message": str(exc)}
                self._transition(record, InstallState.FAILED_RETRYABLE,
                                 f"retries exhausted at step {key}")
                self._audit(install_id, self.actor, "step_failed", step=key,
                            idempotency_key=idem_key, error="transient_exhausted")
                self._save(record)
                self._alert(record, f"Install {install_id} failed at {key} "
                                    f"after {attempt} attempts: {exc}")
                return RunResult(FAILED, record["state"],
                                 f"step {key} failed after {attempt} attempts")
            rec.update(status="done", object_ref=ref, error=None)
            self._audit(install_id, self.actor, "step_done", step=key,
                        idempotency_key=idem_key, object_ref=ref, via="created")
            self._save(record)
            self.log(f"[step] {key} done ({ref})")
            return None

        return None  # unreachable; the loop always returns
