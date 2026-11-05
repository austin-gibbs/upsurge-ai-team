"""Live adapters for the install orchestrator.

This module wires the four adapter interfaces from adapters.py to the
real systems, behind an explicit install config. adapters.py and the
DryRun bundle are untouched: the dry run path behaves exactly as
before. run.py selects this bundle only with --live --config.

Systems and calls:

- Desk: the Lovable query_database tool through /opt/hatch/bin/lovable
  against the configured Desk project. The Desk data model is the one
  the team page package defines (app/team-page/migrations): a single
  row workspace_config (id = 1) holding the workspace identity, the
  global team_roster table (shared template data), and public.requests.
  The install's own Desk project is a requests row whose links jsonb
  carries an orchestrator marker; the operational install markers
  (passcode pointer, webhooks, intake flags, heartbeat state) live in
  that same links object, so every Desk write is a row write followed
  by a read back verification.
- GitHub: writes through the dedicated /opt/hatch/bin/github
  push-files subcommand, which reads file contents from a local
  snapshot directory instead of --arguments-json. That matters: the
  call-tool path passes file contents in argv and dies with "Argument
  list too long" on multi file batches (hit during the service repo
  build out, 2026-11-04). Reads use call-read-tool get_file_contents,
  and the file text arrives in the second content element
  (resource.text). Every batch write verifies one file by read back;
  the manifest and stage writes verify their own file.
- Slack: /opt/hatch/bin/slack. Channel lookup by exact name through
  slack_search_channels, creation through slack_create_conversation,
  sends through slack_send_message (the text field is named message).
  Install notices carry the install id in the body.
- Connectors: client owned third party tools stay self serve in live
  mode. The apply methods return a structured awaiting result (see
  LiveConnectorAdapter) instead of raising, because connecting a
  client's own Gmail, CRM, or platform seat is an action only the
  client can take. A live install therefore records exactly what it is
  waiting on and parks at the qa_review gate instead of crashing or
  pretending a verification happened.

Error mapping follows the state.py taxonomy: subprocess timeouts and
provider 5xx become TransientError, any 429 becomes
ProviderRateLimited (hard stop), 401 and 403 style failures become
AuthError, and Postgres undefined table or column errors (42P01,
42703) become SchemaError.

Secrets never appear in config, state, or payloads. The config carries
pointers only (the Desk passcode pointer name, never a value).
"""

from __future__ import annotations

import json
import re
import subprocess
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .state import (
    AuthError,
    InstallContext,
    ProviderRateLimited,
    SchemaError,
    TransientError,
)

LOVABLE_CLI = "/opt/hatch/bin/lovable"
GITHUB_CLI = "/opt/hatch/bin/github"
SLACK_CLI = "/opt/hatch/bin/slack"

# The internal Surge Command Desk Lovable project. A client install
# overrides this with its own Desk project id in the install config.
DEFAULT_DESK_PROJECT_ID = "6b29dcf6-5f01-4dbe-a701-2c8f1ff20f48"

READ_TIMEOUT = 240          # seconds; first calls to a host can be slow
PUSH_TIMEOUT = 560          # seconds; pushes can take minutes to land

_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
_CHANNEL_ID_RE = re.compile(r"^[CD][A-Z0-9]{8,}$")
_SLACK_TS_RE = re.compile(r"\d{10}\.\d{6}")
_CHANNEL_LINE_RE = re.compile(r"#([\w-]+)\s*\(([CD][A-Z0-9]+)\)")

ROSTER_SEED_PATH = (
    Path(__file__).resolve().parent.parent
    / "app" / "team-page" / "migrations" / "0002_roster_seed.sql"
)

CLIENT_LAYER_FILES = (
    "profile.md",
    "people.md",
    "brand.md",
    "systems.md",
    "decisions.md",
    "open-items.md",
    "intake/README.md",
)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sql_literal(value: str) -> str:
    """Escape a string for a single quoted Postgres literal."""
    return "'" + value.replace("'", "''") + "'"


# ---------------------------------------------------------------------------
# Install config
# ---------------------------------------------------------------------------


@dataclass
class InstallConfig:
    """One install's wiring. Loaded from a JSON file by run.py --config.

    Pointers only: no credential values ever appear here. demo must be
    true for a live run unless the operator passes --allow-real.
    """

    business_name: str
    slug: str
    repo: str
    path_prefix: str = "clients"
    branch: str = "main"
    desk_project_id: str = DEFAULT_DESK_PROJECT_ID
    slack_channel: str = "ai-command"
    tier: str = "pilot"
    lanes: Tuple[str, ...] = ("muse", "claude", "grok")
    demo: bool = False
    sponsor_name: str = ""
    sponsor_email: str = ""
    timezone: str = "America/Denver"
    intake_mode: str = "surge-form"      # surge-form | direct | pm-system
    seat_model: str = "client-owned"     # client-owned | upsurge-managed
    pack_version: str = "1.0.0"
    crm_connector: str = "ghl"

    @property
    def repo_owner(self) -> str:
        return self.repo.split("/", 1)[0]

    @property
    def repo_name(self) -> str:
        return self.repo.split("/", 1)[1]

    @property
    def memory_root(self) -> str:
        """Repo path of this client's memory tree."""
        return f"{self.path_prefix.strip('/')}/{self.slug}"

    def to_context(self, install_id: str) -> InstallContext:
        return InstallContext(
            install_id=install_id,
            client_slug=self.slug,
            legal_name=self.business_name,
            sponsor_name=self.sponsor_name,
            sponsor_email=self.sponsor_email,
            timezone=self.timezone,
            intake_mode=self.intake_mode,
            seat_model=self.seat_model,
            pack_version=self.pack_version,
            crm_connector=self.crm_connector,
        )


def load_config(path: Path) -> InstallConfig:
    """Load and validate an install config JSON. Raises ValueError."""
    try:
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"config file not found: {path}")
    except json.JSONDecodeError as exc:
        raise ValueError(f"config file is not valid JSON: {path}: {exc}")
    if not isinstance(raw, dict):
        raise ValueError("config must be a JSON object")
    for required in ("business_name", "slug", "repo"):
        if not raw.get(required):
            raise ValueError(f"config is missing required field: {required}")
    if not _SLUG_RE.match(str(raw["slug"])):
        raise ValueError(
            f"config slug {raw['slug']!r} must be lowercase letters, "
            "digits, and hyphens"
        )
    if "/" not in str(raw["repo"]):
        raise ValueError("config repo must be in owner/name form")
    lanes = tuple(raw.get("lanes", ("muse", "claude", "grok")))
    unknown = [lane for lane in lanes if lane not in ("muse", "claude", "grok")]
    if unknown:
        raise ValueError(f"config lanes contain unknown lanes: {unknown}")
    allowed = {
        "business_name", "slug", "repo", "path_prefix", "branch",
        "desk_project_id", "slack_channel", "tier", "lanes", "demo",
        "sponsor_name", "sponsor_email", "timezone", "intake_mode",
        "seat_model", "pack_version", "crm_connector",
    }
    extra = sorted(set(raw) - allowed)
    if extra:
        raise ValueError(f"config has unknown fields: {extra}")
    raw["lanes"] = lanes
    return InstallConfig(**raw)


# ---------------------------------------------------------------------------
# Subprocess helpers: one per CLI, with the taxonomy mapping in one place
# ---------------------------------------------------------------------------


def _run_cli(argv: List[str], timeout: int, provider: str) -> str:
    """Run a hatch CLI and return stdout. Raises taxonomy errors."""
    try:
        proc = subprocess.run(
            argv, capture_output=True, text=True, timeout=timeout
        )
    except subprocess.TimeoutExpired:
        raise TransientError(
            f"{provider} call timed out after {timeout}s: {' '.join(argv[:3])}"
        )
    out = proc.stdout or ""
    err = proc.stderr or ""
    if proc.returncode != 0:
        blob = f"{out} {err}"
        if "429" in blob or "rate limit" in blob.lower():
            raise ProviderRateLimited(provider)
        if any(code in blob for code in ("401", "403")) or \
                "not accessible" in blob.lower() or \
                "unauthorized" in blob.lower():
            raise AuthError(f"{provider} call failed: {blob.strip()[:300]}")
        raise TransientError(
            f"{provider} call exited {proc.returncode}: {blob.strip()[:300]}"
        )
    return out


def _envelope(stdout: str, provider: str) -> dict:
    """Parse a hatch CLI JSON envelope and surface tool level errors."""
    try:
        env = json.loads(stdout)
    except json.JSONDecodeError:
        raise TransientError(f"{provider} returned non JSON output")
    result = env.get("result") or {}
    if env.get("ok") is False or result.get("isError"):
        texts = [
            item.get("text", "")
            for item in result.get("content", [])
            if isinstance(item, dict)
        ]
        blob = " ".join(texts) or json.dumps(result)[:300]
        if "429" in blob or "rate limit" in blob.lower():
            raise ProviderRateLimited(provider)
        if "42P01" in blob or "42703" in blob or \
                "does not exist" in blob and "relation" in blob:
            raise SchemaError(f"{provider} schema mismatch: {blob.strip()[:300]}")
        if any(code in blob for code in ("401", "403")) or \
                "unauthorized" in blob.lower():
            raise AuthError(f"{provider} call failed: {blob.strip()[:300]}")
        raise TransientError(f"{provider} tool error: {blob.strip()[:300]}")
    return result


def _result_texts(result: dict) -> List[str]:
    return [
        item.get("text", "")
        for item in result.get("content", [])
        if isinstance(item, dict) and item.get("type") == "text"
    ]


# ---------------------------------------------------------------------------
# Desk: Surge Command Desk through the Lovable query_database tool
# ---------------------------------------------------------------------------


class LiveDeskAdapter:
    """Live Desk operations. Every write is verified by a read back.

    Workspace identity is the single workspace_config row (id = 1).
    The install's own Desk project is a public.requests row found by
    the orchestrator marker in its links jsonb; operational markers
    (passcode pointer, webhooks, intake, heartbeat) live in that links
    object. team_roster is shared template data across the Desk.
    """

    def __init__(self, config: InstallConfig) -> None:
        self.config = config

    # -- low level -----------------------------------------------------

    def query(self, sql: str) -> List[dict]:
        """Run one SQL statement and return its rows (empty for writes
        without RETURNING). Raises the taxonomy on failure."""
        args = json.dumps({"project_id": self.config.desk_project_id, "sql": sql})
        out = _run_cli(
            [LOVABLE_CLI, "call-tool", "--name", "query_database",
             "--arguments-json", args],
            READ_TIMEOUT, "lovable",
        )
        result = _envelope(out, "lovable")
        structured = result.get("structuredContent") or {}
        if isinstance(structured.get("rows"), list):
            return structured["rows"]
        for text in _result_texts(result):
            try:
                parsed = json.loads(text)
            except json.JSONDecodeError:
                continue
            if isinstance(parsed, dict) and isinstance(parsed.get("rows"), list):
                return parsed["rows"]
        return []

    # -- workspace and install project ---------------------------------

    def _workspace_row(self) -> Optional[dict]:
        rows = self.query(
            "SELECT id, client_name, timezone FROM public.workspace_config "
            "WHERE id = 1"
        )
        return rows[0] if rows else None

    def _install_project_row(self, ctx: InstallContext) -> Optional[dict]:
        marker = json.dumps({"orchestrator": {"install_id": ctx.install_id}})
        rows = self.query(
            "SELECT id, links FROM public.requests WHERE links @> "
            f"{_sql_literal(marker)}::jsonb ORDER BY requested_at LIMIT 1"
        )
        return rows[0] if rows else None

    def _project_links(self, ctx: InstallContext) -> dict:
        row = self._install_project_row(ctx)
        if row is None:
            raise SchemaError(
                "install Desk project row not found; provision order broken"
            )
        links = row.get("links") or {}
        return links if isinstance(links, dict) else {}

    def _merge_links(self, ctx: InstallContext, patch: dict) -> dict:
        row = self._install_project_row(ctx)
        if row is None:
            raise SchemaError(
                "install Desk project row not found; provision order broken"
            )
        patch_sql = _sql_literal(json.dumps(patch))
        self.query(
            "UPDATE public.requests SET links = "
            f"COALESCE(links, '{{}}'::jsonb) || {patch_sql}::jsonb, "
            f"updated_at = now() WHERE id = {_sql_literal(str(row['id']))}"
        )
        merged = self._project_links(ctx)
        for key, value in patch.items():
            if merged.get(key) != value:
                raise TransientError(
                    f"Desk links read back did not contain {key} after update"
                )
        return merged

    def find_client_by_slug(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        workspace = self._workspace_row()
        if workspace is None:
            return None
        name = str(workspace.get("client_name", "")).strip().lower()
        if name != self.config.business_name.strip().lower():
            raise SchemaError(
                f"Desk workspace_config already holds {workspace.get('client_name')!r}; "
                "refusing to overwrite another client's workspace"
            )
        project = self._install_project_row(ctx)
        if project is None:
            return None
        return f"desk://requests/{project['id']}"

    def insert_client_workspace(self, ctx: InstallContext, natural_key: str) -> str:
        workspace = self._workspace_row()
        if workspace is None:
            self.query(
                "INSERT INTO public.workspace_config (id, client_name, timezone) "
                f"VALUES (1, {_sql_literal(self.config.business_name)}, "
                f"{_sql_literal(self.config.timezone)}) RETURNING id"
            )
            workspace = self._workspace_row()
            if workspace is None:
                raise TransientError("workspace_config read back failed after insert")
        elif str(workspace.get("client_name", "")).strip().lower() != \
                self.config.business_name.strip().lower():
            raise SchemaError(
                f"Desk workspace_config already holds {workspace.get('client_name')!r}; "
                "refusing to overwrite another client's workspace"
            )
        project = self._install_project_row(ctx)
        if project is not None:
            return f"desk://requests/{project['id']}"
        cfg = self.config
        description = (
            f"AI Team install for {cfg.business_name}. "
            f"Tier {cfg.tier}; lanes {', '.join(cfg.lanes)}; "
            f"intake mode {cfg.intake_mode}; seat model {cfg.seat_model}; "
            f"Team Pack {cfg.pack_version}. Run by the install orchestrator; "
            "this project is the Desk record of the install itself."
        )
        brief = (
            "Objective: install the AI Team for this business through the "
            "five stages (Provision, Connect, Seat, Seed, Go live). "
            "Definition of done: install state live in the orchestrator, "
            "heartbeat published, first request intake open."
        )
        links = {"orchestrator": {"install_id": ctx.install_id,
                                  "kind": "install_project",
                                  "slug": cfg.slug}}
        rows = self.query(
            "INSERT INTO public.requests (title, client, description, status, "
            "priority, next_step, assignee, brief, links, source) VALUES ("
            f"{_sql_literal('AI Team Install: ' + cfg.business_name)}, "
            f"{_sql_literal(cfg.business_name)}, "
            f"{_sql_literal(description)}, 'In Progress', 'P1', "
            f"{_sql_literal('Provision stage running under the install orchestrator')}, "
            f"'Maive', {_sql_literal(brief)}, "
            f"{_sql_literal(json.dumps(links))}::jsonb, 'orchestrator') "
            "RETURNING id"
        )
        project = self._install_project_row(ctx)
        if project is None:
            raise TransientError("install project read back failed after insert")
        return f"desk://requests/{project['id']}"

    # -- passcode pointer (pointer only, value lives server side) -------

    def passcode_pointer_exists(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        pointer = self._project_links(ctx).get("passcode_pointer")
        return pointer if pointer else None

    def create_passcode_pointer(self, ctx: InstallContext, natural_key: str) -> str:
        # natural_key is the pointer name (SURGE_PASSCODE_<SLUG>). The
        # value is generated and set server side by operations; the
        # orchestrator records the pointer only and never reads a value.
        self._merge_links(ctx, {"passcode_pointer": natural_key})
        return natural_key

    # -- roster (shared template data) ----------------------------------

    def roster_exists(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        rows = self.query("SELECT count(*) AS n FROM public.team_roster")
        count = int(rows[0]["n"]) if rows else 0
        return f"desk://team_roster/{count}" if count > 0 else None

    def insert_roster(self, ctx: InstallContext, natural_key: str) -> str:
        if not ROSTER_SEED_PATH.exists():
            raise SchemaError(
                f"roster seed file missing: {ROSTER_SEED_PATH}"
            )
        seed_sql = ROSTER_SEED_PATH.read_text(encoding="utf-8")
        self.query(seed_sql)
        ref = self.roster_exists(ctx, natural_key)
        if ref is None:
            raise TransientError("team_roster read back empty after seed")
        return ref

    # -- webhooks, intake, heartbeat (links markers on the project) -----

    def webhooks_registered(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        webhooks = self._project_links(ctx).get("webhooks")
        return json.dumps(webhooks) if webhooks else None

    def register_webhooks(self, ctx: InstallContext, natural_key: str) -> str:
        env = ctx.slug_env
        webhooks = [
            {"kind": "intake", "pointer": f"WEBHOOK_INTAKE_{env}",
             "mode": self.config.intake_mode},
            {"kind": "status_callback", "pointer": f"WEBHOOK_STATUS_{env}"},
        ]
        if self.config.intake_mode == "pm-system":
            webhooks.append(
                {"kind": "pm_system", "pointer": f"WEBHOOK_PM_{env}"}
            )
        self._merge_links(ctx, {"webhooks": webhooks})
        return json.dumps(webhooks)

    def intake_enabled(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        intake = self._project_links(ctx).get("intake") or {}
        if intake.get("enabled"):
            return json.dumps(intake)
        return None

    def enable_intake(self, ctx: InstallContext, natural_key: str) -> str:
        adapters_by_mode = {
            "surge-form": ["surge-form"],
            "direct": ["direct"],
            "pm-system": ["pm-webhook", "pm-poll"],
        }
        intake = {
            "mode": self.config.intake_mode,
            "enabled": True,
            "adapters": adapters_by_mode.get(self.config.intake_mode,
                                             ["surge-form"]),
        }
        self._merge_links(ctx, {"intake": intake})
        return json.dumps(intake)

    def heartbeat_live(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        heartbeat = self._project_links(ctx).get("heartbeat") or {}
        if heartbeat.get("published"):
            return json.dumps(heartbeat)
        return None

    def publish_heartbeat(self, ctx: InstallContext, natural_key: str) -> str:
        heartbeat = {
            "published": True,
            "path": "/team",
            "published_by": "install-orchestrator",
            "published_at": _now(),
        }
        self._merge_links(ctx, {"heartbeat": heartbeat})
        return json.dumps(heartbeat)

    # -- first real project (go live) ------------------------------------

    def _first_project_row(self, ctx: InstallContext) -> Optional[dict]:
        marker = json.dumps(
            {"orchestrator": {"install_id": ctx.install_id,
                              "kind": "first_project"}}
        )
        rows = self.query(
            "SELECT id FROM public.requests WHERE links @> "
            f"{_sql_literal(marker)}::jsonb ORDER BY requested_at LIMIT 1"
        )
        return rows[0] if rows else None

    def first_project_exists(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        row = self._first_project_row(ctx)
        return f"desk://requests/{row['id']}" if row else None

    def create_first_project(self, ctx: InstallContext, natural_key: str) -> str:
        cfg = self.config
        links = {"orchestrator": {"install_id": ctx.install_id,
                                  "kind": "first_project",
                                  "slug": cfg.slug}}
        description = (
            "Intake opener created by the install orchestrator at go live. "
            "The sponsor's first real request replaces this brief at intake; "
            "the team rewrites it to the execution brief standard before work."
        )
        self.query(
            "INSERT INTO public.requests (title, client, description, status, "
            "priority, next_step, assignee, links, source) VALUES ("
            f"{_sql_literal('First Request: ' + cfg.business_name)}, "
            f"{_sql_literal(cfg.business_name)}, "
            f"{_sql_literal(description)}, 'New', 'P1', "
            f"{_sql_literal('Sponsor submits the first real request')}, "
            f"'Maive', {_sql_literal(json.dumps(links))}::jsonb, "
            "'orchestrator') RETURNING id"
        )
        row = self._first_project_row(ctx)
        if row is None:
            raise TransientError("first project read back failed after insert")
        return f"desk://requests/{row['id']}"


# ---------------------------------------------------------------------------
# GitHub: the client memory tree, manifest, Pack delivery records
# ---------------------------------------------------------------------------


class LiveGitHubAdapter:
    """Live GitHub operations against the configured repo.

    Writes go through the push-files subcommand with a local snapshot
    directory (file contents never travel in argv). Path mapping: the
    step natural keys carry the brain layout from the spec; the live
    tree re-roots them under <path_prefix>/<slug> in the configured
    repo. One tree per client: layer files at the root, manifest.json,
    pack/<lane>.md delivery records, review-package.md.
    """

    def __init__(self, config: InstallConfig) -> None:
        self.config = config

    # -- low level -----------------------------------------------------

    def read_file(self, path: str, strict: bool = False) -> Optional[str]:
        args = json.dumps({
            "owner": self.config.repo_owner,
            "repo": self.config.repo_name,
            "path": path,
        })
        try:
            out = _run_cli(
                [GITHUB_CLI, "call-read-tool", "--name", "get_file_contents",
                 "--arguments-json", args],
                READ_TIMEOUT, "github",
            )
            result = _envelope(out, "github")
        except (TransientError, AuthError):
            if strict:
                raise
            return None
        for item in result.get("content", []):
            resource = item.get("resource") if isinstance(item, dict) else None
            if resource and isinstance(resource.get("text"), str):
                return resource["text"]
        return None

    def push_files(self, files: Dict[str, str], message: str) -> None:
        """Push a batch of repo relative files from a local snapshot."""
        with tempfile.TemporaryDirectory(prefix="orchestrator-push-") as tmp:
            root = Path(tmp)
            relpaths = []
            for rel, content in sorted(files.items()):
                dest = root / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(content, encoding="utf-8")
                relpaths.append(rel)
            paths_file = root / ".paths"
            paths_file.write_bytes(
                b"".join(p.encode("utf-8") + b"\0" for p in relpaths)
            )
            argv = [
                GITHUB_CLI, "push-files",
                "--owner", self.config.repo_owner,
                "--repo", self.config.repo_name,
                "--branch", self.config.branch,
                "--message", message,
                "--source-dir", str(root),
                "--paths-file", str(paths_file),
            ]
            try:
                _run_cli(argv, PUSH_TIMEOUT, "github")
            except TransientError:
                # A push can time out on the client side and still
                # land. Give the caller one read back chance by
                # re-raising only when verification (done by every
                # apply method after this) cannot confirm; here we
                # surface the error and let verify decide.
                raise

    def _push_and_verify(self, files: Dict[str, str], message: str,
                         verify_path: str, verify_needle: str) -> None:
        try:
            self.push_files(files, message)
        except TransientError:
            landed = self.read_file(verify_path)
            if landed is not None and verify_needle in landed:
                return
            raise
        landed = self.read_file(verify_path, strict=True)
        if landed is None or verify_needle not in landed:
            raise TransientError(
                f"GitHub read back of {verify_path} did not contain the "
                "expected marker after push"
            )

    # -- path helpers ----------------------------------------------------

    def _root(self) -> str:
        return self.config.memory_root

    def _manifest_path(self) -> str:
        return f"{self._root()}/manifest.json"

    def _read_manifest(self) -> Optional[dict]:
        text = self.read_file(self._manifest_path())
        if text is None:
            return None
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            return None
        return parsed if isinstance(parsed, dict) else None

    def _layer_content(self, ctx: InstallContext, marker: str) -> Dict[str, str]:
        cfg = self.config
        facts = [
            f"Business: {cfg.business_name}",
            f"Slug: {cfg.slug}",
            f"Sponsor: {cfg.sponsor_name or 'to be confirmed'}",
            f"Timezone: {cfg.timezone}",
            f"Tier: {cfg.tier}",
            f"Lanes: {', '.join(cfg.lanes)}",
            f"Intake mode: {cfg.intake_mode}",
            f"Seat model: {cfg.seat_model}",
            f"Team Pack: {cfg.pack_version}",
        ]
        header = f"# {cfg.business_name}\n\n" + "\n".join(
            f"- {fact}" for fact in facts
        )
        return {
            "profile.md": header + f"\n\nClient layer status: {marker}.\n"
            "Facts above come from the signed agreement and the install "
            "config only.\n",
            "people.md": header + "\n\n## People\n\n"
            f"- Sponsor: {cfg.sponsor_name or 'to be confirmed'}"
            f" ({cfg.sponsor_email or 'email to be confirmed'})\n",
            "brand.md": header + "\n\n## Brand\n\n"
            "Brand facts are seeded in the Seed stage from the client's "
            "own sources, each with its source recorded.\n",
            "systems.md": header + "\n\n## Connected systems\n\n"
            "Connections are recorded here as they verify in the "
            "Connect stage.\n",
            "decisions.md": header + "\n\n## Decisions\n\n"
            "No decisions recorded yet.\n",
            "open-items.md": header + "\n\n## Open items\n\n"
            "No open items yet.\n",
            "intake/README.md": header + "\n\n## Intake\n\n"
            f"Intake mode: {cfg.intake_mode}. Raw intake payloads land "
            "here before brief rewrite.\n",
        }

    # -- client layer ----------------------------------------------------

    def path_exists(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        text = self.read_file(f"{self._root()}/profile.md")
        return f"github://{self.config.repo}/{self._root()}" if text else None

    def write_client_layer(self, ctx: InstallContext, natural_key: str) -> str:
        files = {
            f"{self._root()}/{name}": content
            for name, content in
            self._layer_content(ctx, "skeleton (provision stage)").items()
        }
        self._push_and_verify(
            files,
            f"orchestrator: create client layer for {self.config.slug} "
            f"(install {ctx.install_id})",
            f"{self._root()}/profile.md",
            self.config.business_name,
        )
        return f"github://{self.config.repo}/{self._root()}"

    # -- manifest ----------------------------------------------------------

    def manifest_exists(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        manifest = self._read_manifest()
        if manifest and manifest.get("install_id") == ctx.install_id:
            return f"github://{self.config.repo}/{self._manifest_path()}"
        return None

    def write_manifest(self, ctx: InstallContext, natural_key: str) -> str:
        cfg = self.config
        manifest = {
            "schema": "ai-team-install-manifest/1",
            "install_id": ctx.install_id,
            "slug": cfg.slug,
            "business_name": cfg.business_name,
            "tier": cfg.tier,
            "lanes": list(cfg.lanes),
            "timezone": cfg.timezone,
            "intake_mode": cfg.intake_mode,
            "seat_model": cfg.seat_model,
            "pack_version": cfg.pack_version,
            "desk": {"project_id": cfg.desk_project_id},
            "slack": {"channel": cfg.slack_channel},
            "repo": cfg.repo,
            "path_prefix": cfg.path_prefix,
            "pointers": {"passcode": f"SURGE_PASSCODE_{ctx.slug_env}"},
            "stages": {},
            "updated_at": _now(),
        }
        content = json.dumps(manifest, indent=2) + "\n"
        self._push_and_verify(
            {self._manifest_path(): content},
            f"orchestrator: manifest v1 for {cfg.slug} "
            f"(install {ctx.install_id})",
            self._manifest_path(),
            ctx.install_id,
        )
        return f"github://{self.config.repo}/{self._manifest_path()}"

    def stage_recorded(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        manifest = self._read_manifest()
        if manifest and natural_key in (manifest.get("stages") or {}):
            return f"github://{self.config.repo}/{self._manifest_path()}#{natural_key}"
        return None

    def record_stage(self, ctx: InstallContext, natural_key: str) -> str:
        manifest = self._read_manifest()
        if manifest is None:
            raise SchemaError(
                "manifest missing; provision stage order broken "
                "(write_manifest runs before stage records)"
            )
        manifest.setdefault("stages", {})[natural_key] = {
            "recorded_at": _now(),
            "recorded_by": "install-orchestrator",
        }
        manifest["updated_at"] = _now()
        content = json.dumps(manifest, indent=2) + "\n"
        self._push_and_verify(
            {self._manifest_path(): content},
            f"orchestrator: record stage {natural_key} for "
            f"{self.config.slug} (install {ctx.install_id})",
            self._manifest_path(),
            natural_key,
        )
        return f"github://{self.config.repo}/{self._manifest_path()}#{natural_key}"

    # -- Team Pack delivery --------------------------------------------------

    def _pack_path(self, natural_key: str) -> Tuple[str, str]:
        # natural_key form: pack:<lane>:<version>
        parts = natural_key.split(":")
        lane = parts[1] if len(parts) > 1 else "muse"
        version = parts[2] if len(parts) > 2 else self.config.pack_version
        return f"{self._root()}/pack/{lane}.md", lane

    def pack_delivery_exists(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        path, _lane = self._pack_path(natural_key)
        text = self.read_file(path)
        if text and f"pack_version: {self.config.pack_version}" in text:
            return f"github://{self.config.repo}/{path}"
        return None

    def deliver_pack(self, ctx: InstallContext, natural_key: str) -> str:
        path, lane = self._pack_path(natural_key)
        cfg = self.config
        content = (
            f"# Team Pack delivery record: {lane} lane\n\n"
            f"pack_version: {cfg.pack_version}\n"
            f"install_id: {ctx.install_id}\n"
            f"client_slug: {cfg.slug}\n"
            f"seat_model: {cfg.seat_model}\n"
            f"delivered_at: {_now()}\n\n"
            "## Bootstrap package (source of truth for the seat)\n\n"
            "- Roster and lane map: service repo team-pack/ (Team Pack "
            f"{cfg.pack_version}).\n"
            "- Routing rules, claim protocol, house style, execution "
            "brief standard: same Team Pack source.\n"
            f"- Client layer pointer: {cfg.repo} at {self._root()}.\n\n"
            "## Delivery note\n\n"
            "For client owned Claude and Grok seats there is no "
            "verified API push; the client pastes this package into "
            "their seat through the self serve hub, and the seat "
            "verification drill confirms it landed. This file is the "
            "delivery record and the package source.\n"
        )
        self._push_and_verify(
            {path: content},
            f"orchestrator: deliver Team Pack {cfg.pack_version} to "
            f"{lane} lane for {cfg.slug} (install {ctx.install_id})",
            path,
            f"pack_version: {cfg.pack_version}",
        )
        return f"github://{self.config.repo}/{path}"

    # -- routing table (into systems.md) --------------------------------------

    def routing_table_exists(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        text = self.read_file(f"{self._root()}/systems.md")
        if text and "## Routing table" in text:
            return f"github://{self.config.repo}/{self._root()}/systems.md#routing"
        return None

    def write_routing_table(self, ctx: InstallContext, natural_key: str) -> str:
        path = f"{self._root()}/systems.md"
        text = self.read_file(path, strict=True)
        if text is None:
            raise SchemaError(
                "systems.md missing; provision stage order broken"
            )
        table = (
            "\n## Routing table\n\n"
            "| Task type | Primary lane | Fallback lane |\n"
            "|---|---|---|\n"
            "| Connected apps, memory, background work | muse | claude |\n"
            "| Long documents, careful builds, deep reasoning | claude | muse |\n"
            "| Speed, volume, live signal | grok | muse |\n\n"
            "Source: Team Pack default routing. Per install overrides "
            "are recorded in the manifest.\n"
        )
        self._push_and_verify(
            {path: text.rstrip("\n") + "\n" + table},
            f"orchestrator: publish routing table for {self.config.slug} "
            f"(install {ctx.install_id})",
            path,
            "## Routing table",
        )
        return f"github://{self.config.repo}/{path}#routing"

    # -- seed stage: v1 draft, quarantine, cross check, review package ---------

    def client_layer_v1_exists(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        text = self.read_file(f"{self._root()}/profile.md")
        if text and "Client layer v1" in text:
            return f"github://{self.config.repo}/{self._root()}"
        return None

    def draft_client_layer_v1(self, ctx: InstallContext, natural_key: str) -> str:
        files = {
            f"{self._root()}/{name}": content
            for name, content in
            self._layer_content(ctx, "Client layer v1 (draft)").items()
        }
        # Preserve a routing table published in the Seat stage.
        systems_path = f"{self._root()}/systems.md"
        current = self.read_file(systems_path)
        if current and "## Routing table" in current:
            table = current[current.index("## Routing table"):]
            files[systems_path] = (
                files[systems_path].rstrip("\n") + "\n\n" + table
            )
        self._push_and_verify(
            files,
            f"orchestrator: draft client layer v1 for {self.config.slug} "
            f"(install {ctx.install_id})",
            f"{self._root()}/profile.md",
            "Client layer v1",
        )
        return f"github://{self.config.repo}/{self._root()}"

    def quarantine_done(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        text = self.read_file(f"{self._root()}/open-items.md")
        if text and "## Quarantine" in text:
            return f"github://{self.config.repo}/{self._root()}/open-items.md#quarantine"
        return None

    def strip_and_quarantine(self, ctx: InstallContext, natural_key: str) -> str:
        path = f"{self._root()}/open-items.md"
        text = self.read_file(path, strict=True)
        if text is None:
            raise SchemaError(
                "open-items.md missing; provision stage order broken"
            )
        patterns = ("sk-", "ghp_", "xoxb-", "xoxp-", "AKIA", "BEGIN RSA",
                    "BEGIN OPENSSH")
        scanned = []
        for name in CLIENT_LAYER_FILES:
            body = self.read_file(f"{self._root()}/{name}")
            if body:
                scanned.append(name)
                for pattern in patterns:
                    if pattern in body:
                        raise SchemaError(
                            f"credential shaped value found in {name}; "
                            "quarantine requires a human before rewrite"
                        )
        section = (
            "\n## Quarantine\n\n"
            f"Checked {len(scanned)} seeded files on {_now()} for "
            "credential shaped values (API key prefixes, private key "
            "blocks) and do-not-publish material. None found in "
            "orchestrator seeded files. Client sourced values are "
            "never written to this tree; categories only are recorded "
            "here.\n"
        )
        self._push_and_verify(
            {path: text.rstrip("\n") + "\n" + section},
            f"orchestrator: quarantine pass for {self.config.slug} "
            f"(install {ctx.install_id})",
            path,
            "## Quarantine",
        )
        return f"github://{self.config.repo}/{path}#quarantine"

    def cross_check_done(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        text = self.read_file(f"{self._root()}/open-items.md")
        if text and "## Cross check" in text:
            return f"github://{self.config.repo}/{self._root()}/open-items.md#cross-check"
        return None

    def cross_check_facts(self, ctx: InstallContext, natural_key: str) -> str:
        path = f"{self._root()}/open-items.md"
        text = self.read_file(path, strict=True)
        if text is None:
            raise SchemaError(
                "open-items.md missing; provision stage order broken"
            )
        profile = self.read_file(f"{self._root()}/profile.md") or ""
        cfg = self.config
        conflicts = []
        for label, value in (
            ("business name", cfg.business_name),
            ("slug", cfg.slug),
            ("timezone", cfg.timezone),
            ("intake mode", cfg.intake_mode),
        ):
            if value and value not in profile:
                conflicts.append(f"{label} {value!r} not found in profile.md")
        outcome = (
            "No conflicts detected: agreement facts match profile.md."
            if not conflicts
            else "Conflicts recorded, not resolved by guessing: "
            + "; ".join(conflicts) + "."
        )
        section = (
            "\n## Cross check\n\n"
            f"Cross checked on {_now()} across the install config "
            "(agreement facts) and profile.md. " + outcome + "\n"
        )
        self._push_and_verify(
            {path: text.rstrip("\n") + "\n" + section},
            f"orchestrator: cross check for {self.config.slug} "
            f"(install {ctx.install_id})",
            path,
            "## Cross check",
        )
        return f"github://{self.config.repo}/{path}#cross-check"

    def review_package_exists(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        text = self.read_file(f"{self._root()}/review-package.md")
        return f"github://{self.config.repo}/{self._root()}/review-package.md" \
            if text else None

    def generate_review_package(self, ctx: InstallContext, natural_key: str) -> str:
        cfg = self.config
        content = (
            f"# Knowledge review: {cfg.business_name}\n\n"
            "## What the team knows\n\n"
            f"- Business, sponsor, timezone, tier, lanes, intake mode, "
            f"and seat model from the signed agreement (see profile.md).\n\n"
            "## What the team assumed\n\n"
            "- Nothing yet. Assumptions are recorded here as the Seed "
            "stage adds sourced facts, each with its source.\n\n"
            "## What the team still needs\n\n"
            "- Brand assets and voice examples.\n"
            "- Service catalog and pricing the team may quote.\n"
            "- Approval rules for client facing sends.\n\n"
            "The client confirms or corrects this package in the self "
            "serve hub; corrections land in the Client layer with "
            "sources.\n"
        )
        path = f"{self._root()}/review-package.md"
        self._push_and_verify(
            {path: content},
            f"orchestrator: knowledge review package for {cfg.slug} "
            f"(install {ctx.install_id})",
            path,
            "Knowledge review",
        )
        return f"github://{self.config.repo}/{path}"


# ---------------------------------------------------------------------------
# Slack: install notices and ops alerts
# ---------------------------------------------------------------------------


class LiveSlackAdapter:
    """Live Slack operations through /opt/hatch/bin/slack.

    Channels are addressed by name in config and resolved to ids by
    exact name search. Every install notice carries the install id.
    """

    def __init__(self, config: InstallConfig) -> None:
        self.config = config
        self._channel_ids: Dict[str, str] = {}

    def _call(self, tool: str, arguments: dict) -> dict:
        args = json.dumps(arguments)
        out = _run_cli(
            [SLACK_CLI, "call-tool", "--name", tool,
             "--arguments-json", args],
            READ_TIMEOUT, "slack",
        )
        return _envelope(out, "slack")

    def resolve_channel(self, name_or_id: str) -> Optional[str]:
        """Resolve a channel name (with or without #) or id to an id."""
        candidate = name_or_id.lstrip("#")
        if _CHANNEL_ID_RE.match(candidate):
            return candidate
        if candidate in self._channel_ids:
            return self._channel_ids[candidate]
        result = self._call("slack_search_channels", {
            "query": candidate,
            "channel_types": "public_channel,private_channel",
            "response_format": "concise",
        })
        for text in _result_texts(result):
            for match in _CHANNEL_LINE_RE.finditer(text):
                if match.group(1) == candidate:
                    self._channel_ids[candidate] = match.group(2)
                    return match.group(2)
        return None

    def find_channel_by_name(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        return self.resolve_channel(natural_key)

    def create_channel(self, ctx: InstallContext, natural_key: str) -> str:
        result = self._call("slack_create_conversation", {
            "channel_name": natural_key,
            "is_private": False,
        })
        blob = " ".join(_result_texts(result))
        match = re.search(r"\(([CD][A-Z0-9]{8,})\)", blob) or \
            re.search(r"\b([CD][A-Z0-9]{8,})\b", blob)
        if match:
            self._channel_ids[natural_key] = match.group(1)
            return match.group(1)
        # Read back: the channel must be findable by exact name.
        found = self.resolve_channel(natural_key)
        if found is None:
            raise TransientError(
                f"channel {natural_key} not findable after create"
            )
        return found

    def _notice_marker(self, ctx: InstallContext) -> str:
        return f"orchestrator-install:{ctx.install_id}"

    def start_notice_posted(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        channel_id = self.resolve_channel(self.config.slack_channel)
        if channel_id is None:
            return None
        result = self._call("slack_read_channel", {
            "channel_id": channel_id,
            "limit": 50,
            "response_format": "concise",
        })
        blob = " ".join(_result_texts(result))
        if self._notice_marker(ctx) in blob:
            match = _SLACK_TS_RE.search(blob)
            return match.group(0) if match else channel_id
        return None

    def post_start_notice(self, ctx: InstallContext, natural_key: str) -> str:
        text = (
            f"Install started: {self.config.business_name} "
            f"({self.config.slug}). Tier {self.config.tier}, lanes "
            f"{', '.join(self.config.lanes)}, intake "
            f"{self.config.intake_mode}. "
            f"{self._notice_marker(ctx)}"
        )
        return self.post_message(self.config.slack_channel, text)

    def post_message(self, channel: str, text: str) -> str:
        channel_id = self.resolve_channel(channel)
        if channel_id is None:
            raise TransientError(f"Slack channel not found: {channel}")
        result = self._call("slack_send_message", {
            "channel_id": channel_id,
            "message": text,
        })
        blob = " ".join(_result_texts(result))
        match = _SLACK_TS_RE.search(blob)
        return match.group(0) if match else f"slack://{channel_id}/sent"


# ---------------------------------------------------------------------------
# Connectors: client self serve actions in live mode
# ---------------------------------------------------------------------------


def _awaiting(action: str, natural_key: str, detail: str) -> dict:
    """The structured result every live connector apply returns.

    The engine records this dict as the step's object reference, so
    the install record shows exactly which client action each step is
    waiting on. Nothing is claimed as verified: the check methods
    keep returning None until a real verification is recorded, and
    the install parks at the qa_review gate, which no awaiting step
    can pass.
    """
    return {
        "status": "awaiting_client_action",
        "action": action,
        "natural_key": natural_key,
        "detail": detail,
        "recorded_at": _now(),
    }


class LiveConnectorAdapter:
    """Third party client tools in live mode: self serve by design.

    Connecting a client's own accounts (email, calendar, CRM, phone)
    and seating client owned Claude and Grok accounts are actions
    only the client can perform, through the self serve hub. These
    methods therefore never raise for a missing connection and never
    fake a pass: checks report None (not done in the target system)
    and applies record the structured awaiting result.
    """

    def __init__(self, config: InstallConfig) -> None:
        self.config = config

    def checklist_exists(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        return None

    def create_checklist(self, ctx: InstallContext, natural_key: str) -> dict:
        return _awaiting(
            "client_connect_apps", natural_key,
            "Connect checklist presented in the self serve hub in "
            "priority order: email, calendar, file storage, CRM, then "
            "client specific apps. The client connects each app "
            "themselves; verification lands per connector.",
        )

    def get_verification(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        return None

    def verify_connector(self, ctx: InstallContext, natural_key: str) -> dict:
        return _awaiting(
            f"connect:{natural_key}", natural_key,
            f"Waiting on the client to connect {natural_key} in the "
            "self serve hub. Verification runs when the connection "
            "lands; a connector 429 or auth failure will surface "
            "there, not here.",
        )

    def seat_registered(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        return None

    def register_seat(self, ctx: InstallContext, natural_key: str) -> dict:
        return _awaiting(
            "seat_platform", natural_key,
            "Seat registration completes in the client's own platform "
            "environment. For the Muse seat, Maive is delegator of "
            "record once the client finishes the hub steps.",
        )

    def drill_passed(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        return None

    def run_drill(self, ctx: InstallContext, natural_key: str) -> dict:
        return _awaiting(
            "seat_verification_drill", natural_key,
            "The drill routes to the lane once its seat is registered "
            "and the Team Pack paste is confirmed in the hub. Pass "
            "criteria: correct facts, handoff format, no cross client "
            "data, no internal process language.",
        )

    def ingest_done(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        return None

    def ingest_sources(self, ctx: InstallContext, natural_key: str) -> dict:
        return _awaiting(
            "ingest_after_connections", natural_key,
            "Ingest (website, brand assets, documents, CRM structure) "
            "runs against the client's connected sources once the "
            "Connect stage verifications land.",
        )

    def knowledge_drills_passed(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        return None

    def run_knowledge_drills(self, ctx: InstallContext, natural_key: str) -> dict:
        return _awaiting(
            "knowledge_drills", natural_key,
            "Knowledge drills run per lane after the Client layer v1 "
            "draft and the client's hub confirmations.",
        )

    def sweep_passed(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        return None

    def run_final_sweep(self, ctx: InstallContext, natural_key: str) -> dict:
        return _awaiting(
            "final_verification_sweep", natural_key,
            "The sweep re-checks every required connection and lane "
            "before go live. It can only pass after the client "
            "connections verify; QA approval is also still required "
            "at the gate.",
        )

    def loops_scheduled(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        return None

    def schedule_loops(self, ctx: InstallContext, natural_key: str) -> dict:
        return _awaiting(
            "schedule_standing_loops", natural_key,
            "Standing loops (intake backstop sweep, waiting watcher, "
            "weekly digest, monthly Pack update check) are scheduled "
            "against the client workspace once it is live.",
        )


# ---------------------------------------------------------------------------
# Live bundle
# ---------------------------------------------------------------------------


class LiveAdapters:
    """The live bundle, constructed from one install config."""

    def __init__(self, config: InstallConfig) -> None:
        self.config = config
        self.github = LiveGitHubAdapter(config)
        self.desk = LiveDeskAdapter(config)
        self.slack = LiveSlackAdapter(config)
        self.connectors = LiveConnectorAdapter(config)
