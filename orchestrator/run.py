"""Command line entry for the install orchestrator.

Usage (from the repo root):

    python3 -m orchestrator.run --install-id demo --dry-run
    python3 -m orchestrator.run --install-id demo --dry-run \\
        --approve-qa --approved-by "Austin"
    python3 -m orchestrator.run --install-id demo --status
    python3 -m orchestrator.run --install-id demo --show-audit

A run walks the install from initiated toward live and stops at the
qa_review gate. The approve command records the approval and continues
the same run through go live. Every invocation ends by printing the
audit trail.

Exit codes: 0 live (or a read only command), 2 paused at the QA gate,
3 another runner holds the lock, 4 the run ended in a failure or
blocked state, 5 live mode requested (real adapters are v0 stubs).

Dry run mode never sleeps on the retry ladder; the intended waits are
recorded in the audit log instead.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from .adapters import DryRunAdapters, RealAdapters
    from .engine import GATE, LIVE, LOCKED, Engine
    from .state import InstallContext
except ImportError:  # direct file execution fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from orchestrator.adapters import DryRunAdapters, RealAdapters
    from orchestrator.engine import GATE, LIVE, LOCKED, Engine
    from orchestrator.state import InstallContext

DEFAULT_STATE_DIR = Path(__file__).resolve().parent / ".state"


def _print_audit(engine: Engine, install_id: str) -> None:
    entries = engine.read_audit(install_id)
    print("--- audit trail ---")
    if not entries:
        print("(no audit entries yet)")
        return
    for entry in entries:
        parts = [entry["ts"], f"[{entry['actor']}]", entry["event"]]
        if entry["event"] == "transition":
            parts.append(f"{entry.get('from_state')} -> {entry.get('to_state')}")
            parts.append(f"({entry.get('reason', '')})")
        elif "step" in entry:
            parts.append(entry["step"])
            for field_name in ("via", "attempt", "wait_seconds", "provider", "error"):
                if field_name in entry:
                    parts.append(f"{field_name}={entry[field_name]}")
        elif "client_slug" in entry:
            parts.append(f"client={entry['client_slug']}")
        print(" ".join(str(part) for part in parts))
    print(f"--- {len(entries)} audit entries ---")


def _print_status(engine: Engine, install_id: str) -> int:
    record = engine.load_record(install_id)
    if record is None:
        print(f"no install record for {install_id}")
        return 0
    done = sum(1 for s in record["steps"].values() if s["status"] == "done")
    total = len(record["steps"])
    print(f"install {install_id}: state={record['state']} "
          f"steps done={done}/{total} approvals={list(record['approvals'])}")
    for key, step in record["steps"].items():
        if step["status"] != "done":
            print(f"  {key}: {step['status']}"
                  + (f" error={step['error']}" if step["error"] else ""))
    return 0


def main(argv: list | None = None) -> int:
    parser = argparse.ArgumentParser(prog="orchestrator.run",
                                     description="AI Team install orchestrator")
    parser.add_argument("--install-id", required=True)
    parser.add_argument("--client-slug", default=None,
                        help="defaults to <install-id>-client for a new install")
    parser.add_argument("--dry-run", action="store_true",
                        help="simulate every system with the DryRun adapters")
    parser.add_argument("--approve-qa", action="store_true",
                        help="record the QA gate approval, then continue the run")
    parser.add_argument("--approved-by", default="operator")
    parser.add_argument("--state-dir", default=str(DEFAULT_STATE_DIR))
    parser.add_argument("--status", action="store_true",
                        help="print the install state and exit")
    parser.add_argument("--show-audit", action="store_true",
                        help="print the audit trail and exit")
    args = parser.parse_args(argv)

    state_dir = Path(args.state_dir)
    install_id = args.install_id

    if args.dry_run:
        registry_path = state_dir / f"{install_id}.dryrun.json"
        adapters = DryRunAdapters(registry_path)
        sleeper = lambda seconds: None  # dry runs record waits, never sleep
    else:
        adapters = RealAdapters()
        sleeper = None  # engine default: real time.sleep

    engine_kwargs = {"state_dir": state_dir, "adapters": adapters, "log": print}
    if sleeper is not None:
        engine_kwargs["sleeper"] = sleeper
    engine = Engine(**engine_kwargs)

    if args.status:
        return _print_status(engine, install_id)
    if args.show_audit:
        _print_audit(engine, install_id)
        return 0

    if not args.dry_run and not args.approve_qa:
        print("live mode is not wired yet: the real adapters are v0 stubs. "
              "Use --dry-run.")
        return 5

    record = engine.load_record(install_id)
    if record is not None:
        ctx = InstallContext.from_params(record["params"])
    else:
        ctx = InstallContext(
            install_id=install_id,
            client_slug=args.client_slug or f"{install_id}-client",
        )

    if args.approve_qa:
        approved = engine.approve_qa(install_id, args.approved_by)
        if approved:
            print(f"QA approval recorded for {install_id} by {args.approved_by}")
        else:
            current = record["state"] if record else "missing"
            print(f"cannot approve: install {install_id} is not at the QA "
                  f"gate (state={current})")
            _print_audit(engine, install_id)
            return 4

    result = engine.run(ctx)
    print(f"result: {result.status} (state={result.state}) {result.message}")
    _print_audit(engine, install_id)

    if result.status == LIVE:
        return 0
    if result.status == GATE:
        print(f"approve with: python3 -m orchestrator.run --install-id "
              f"{install_id} --dry-run --approve-qa --approved-by \"<name>\"")
        return 2
    if result.status == LOCKED:
        return 3
    return 4


if __name__ == "__main__":
    raise SystemExit(main())
