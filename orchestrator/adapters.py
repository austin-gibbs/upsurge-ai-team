"""Adapter interfaces for the install orchestrator, plus a DryRun set.

Every step in state.py names one check method and one apply method on one
adapter. Check returns an existing object reference or None; apply
creates the object and returns its reference. That split is what makes
check-before-create idempotency possible.

The real adapters (DeskAdapter, GitHubAdapter, SlackAdapter,
ConnectorAdapter) are typed stubs in v0: every method raises
NotImplementedError and its docstring names the real call it will wrap.
The DryRun adapters simulate every call succeeding, persist what they
"created" in a registry file next to the install state, and record an
action log, so a dry run exercises the full engine honestly: a second
run finds the objects the first run created and creates nothing twice.

Errors: adapters raise the taxonomy in state.py. TransientError for
timeouts and 5xx, ProviderRateLimited for a provider 429 (hard stop),
AuthError for credential or account problems, SchemaError when the
target system shape does not match the spec.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, List, Optional

from .state import InstallContext


def _stub(owner: str, method: str, real_call: str) -> NotImplementedError:
    return NotImplementedError(
        f"{owner}.{method} is a v0 stub. Wire it to: {real_call}"
    )


# ---------------------------------------------------------------------------
# Desk: Surge Command Desk through the Lovable database tool
# ---------------------------------------------------------------------------


class DeskAdapter:
    """Surge Command Desk data operations.

    Every method wraps the Lovable query_database tool against the Surge
    Command Desk project (the same path production Desk writes use
    today). query_database executes SELECT, INSERT, and UPDATE.
    """

    def find_client_by_slug(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        """Real call: query_database, SELECT id FROM clients WHERE slug = natural_key."""
        raise _stub("DeskAdapter", "find_client_by_slug",
                    "Lovable query_database SELECT on the Desk clients table")

    def insert_client_workspace(self, ctx: InstallContext, natural_key: str) -> str:
        """Real call: query_database, INSERT the client row plus the standard
        configuration (statuses New / In Progress / Waiting on Austin /
        Waiting on Client / Blocked / Done, priorities P0 to P3,
        assignees Maive / Marcus)."""
        raise _stub("DeskAdapter", "insert_client_workspace",
                    "Lovable query_database INSERT of client row and Desk config")

    def passcode_pointer_exists(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        """Real call: read the manifest's passcode pointer field and confirm
        the named server environment variable (natural_key) is set. The
        passcode value itself is never read into the orchestrator."""
        raise _stub("DeskAdapter", "passcode_pointer_exists",
                    "server environment lookup by pointer name, value never returned")

    def create_passcode_pointer(self, ctx: InstallContext, natural_key: str) -> str:
        """Real call: generate the passcode server side, set the environment
        variable named by natural_key, return the pointer name only."""
        raise _stub("DeskAdapter", "create_passcode_pointer",
                    "server side passcode generation and environment set, pointer only")

    def roster_exists(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        """Real call: query_database, SELECT on the Desk roster rows for this client."""
        raise _stub("DeskAdapter", "roster_exists",
                    "Lovable query_database SELECT on roster rows")

    def insert_roster(self, ctx: InstallContext, natural_key: str) -> str:
        """Real call: query_database, INSERT one roster row per team member
        per lane from the current Team Pack, with client safe bios."""
        raise _stub("DeskAdapter", "insert_roster",
                    "Lovable query_database INSERT of Team Pack roster rows")

    def webhooks_registered(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        """Real call: read the manifest webhook endpoint entries for this install."""
        raise _stub("DeskAdapter", "webhooks_registered",
                    "manifest webhook entry lookup")

    def register_webhooks(self, ctx: InstallContext, natural_key: str) -> str:
        """Real call: register the intake webhook, PM system webhook (when
        that intake mode is chosen), and status callback URLs with the
        intake webhook receiver service; store URLs in the manifest with
        signing secret pointers only."""
        raise _stub("DeskAdapter", "register_webhooks",
                    "intake webhook receiver registration, secret pointers only")

    def intake_enabled(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        """Real call: query_database, read the client row's intake mode flags."""
        raise _stub("DeskAdapter", "intake_enabled",
                    "Lovable query_database SELECT of intake flags")

    def enable_intake(self, ctx: InstallContext, natural_key: str) -> str:
        """Real call: query_database, UPDATE the client row to enable the
        intake adapters named in the agreement (SURGE form open, webhook
        active, poll schedule active, direct surface listening)."""
        raise _stub("DeskAdapter", "enable_intake",
                    "Lovable query_database UPDATE enabling intake adapters")

    def heartbeat_live(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        """Real call: fetch the heartbeat page URL and confirm it renders
        with live roster and project data (owner side read of the Desk)."""
        raise _stub("DeskAdapter", "heartbeat_live",
                    "heartbeat page render check against live Desk data")

    def publish_heartbeat(self, ctx: InstallContext, natural_key: str) -> str:
        """Real call: mark the heartbeat page published in the Desk config
        and record its URL in the manifest."""
        raise _stub("DeskAdapter", "publish_heartbeat",
                    "Lovable query_database UPDATE publishing the heartbeat page")

    def first_project_exists(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        """Real call: query_database, SELECT the first non-test project for this client."""
        raise _stub("DeskAdapter", "first_project_exists",
                    "Lovable query_database SELECT of first real project")

    def create_first_project(self, ctx: InstallContext, natural_key: str) -> str:
        """Real call: run the sponsor's first request through the standard
        intake pipeline (raw payload stored, brief rewritten, project
        created via query_database with lane routing)."""
        raise _stub("DeskAdapter", "create_first_project",
                    "intake pipeline project creation via Lovable query_database")


# ---------------------------------------------------------------------------
# GitHub: the client layer, the manifest, Pack delivery records
# ---------------------------------------------------------------------------


class GitHubAdapter:
    """Repo writes through the GitHub connector.

    Every write wraps /opt/hatch/bin/github call-tool push_files and is
    verified by reading the file back with call-read-tool
    get_file_contents, because a push can time out on the client side
    and still land.
    """

    def path_exists(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        """Real call: get_file_contents (or a tree listing) for natural_key
        in the ops repo. Returns the path as the reference when present."""
        raise _stub("GitHubAdapter", "path_exists",
                    "GitHub get_file_contents read on the ops repo")

    def write_client_layer(self, ctx: InstallContext, natural_key: str) -> str:
        """Real call: push_files creating the standard file set under
        natural_key (profile.md, people.md, brand.md, systems.md,
        decisions.md, open-items.md, intake/) seeded from the Team Pack
        client template with agreement facts only."""
        raise _stub("GitHubAdapter", "write_client_layer",
                    "GitHub push_files of the Client layer template file set")

    def manifest_exists(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        """Real call: get_file_contents for the manifest path (natural_key)."""
        raise _stub("GitHubAdapter", "manifest_exists",
                    "GitHub get_file_contents read of the manifest")

    def write_manifest(self, ctx: InstallContext, natural_key: str) -> str:
        """Real call: push_files writing manifest v1 (identity, Desk
        objects, channels, seats, webhooks, pointers only, no credential
        values), then read back to verify."""
        raise _stub("GitHubAdapter", "write_manifest",
                    "GitHub push_files of manifest.json plus read back verification")

    def stage_recorded(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        """Real call: get_file_contents for the manifest and check the
        stage marker named by natural_key is present."""
        raise _stub("GitHubAdapter", "stage_recorded",
                    "GitHub get_file_contents read of the manifest stage markers")

    def record_stage(self, ctx: InstallContext, natural_key: str) -> str:
        """Real call: push_files updating the manifest with the stage
        record named by natural_key (connections verified, seat model),
        then read back to verify."""
        raise _stub("GitHubAdapter", "record_stage",
                    "GitHub push_files manifest update plus read back verification")

    def pack_delivery_exists(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        """Real call: get_file_contents for the lane's Pack delivery record
        (natural_key carries lane and Pack version)."""
        raise _stub("GitHubAdapter", "pack_delivery_exists",
                    "GitHub get_file_contents read of the Pack delivery record")

    def deliver_pack(self, ctx: InstallContext, natural_key: str) -> str:
        """Real call: push_files writing the Team Pack bootstrap package
        for the lane (roster, routing rules, claim protocol, house
        style, brief standard, Client layer pointer) and the delivery
        record. Physical delivery into a client owned Claude or Grok
        account is the guided paste plus drill path from spec Section
        11 item 5; there is no verified API for it."""
        raise _stub("GitHubAdapter", "deliver_pack",
                    "GitHub push_files of the lane bootstrap package and delivery record")

    def routing_table_exists(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        """Real call: get_file_contents for the Client layer systems.md and
        check the routing table section is present."""
        raise _stub("GitHubAdapter", "routing_table_exists",
                    "GitHub get_file_contents read of systems.md")

    def write_routing_table(self, ctx: InstallContext, natural_key: str) -> str:
        """Real call: push_files updating systems.md with the task type to
        primary lane to fallback lane table from the Team Pack default."""
        raise _stub("GitHubAdapter", "write_routing_table",
                    "GitHub push_files of the routing table into systems.md")

    def client_layer_v1_exists(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        """Real call: read the Client layer files and check the v1 draft marker."""
        raise _stub("GitHubAdapter", "client_layer_v1_exists",
                    "GitHub get_file_contents read of the Client layer draft")

    def draft_client_layer_v1(self, ctx: InstallContext, natural_key: str) -> str:
        """Real call: push_files writing Client layer v1 (profile, people,
        brand, systems, open-items) drafted from ingested sources, each
        fact carrying its source."""
        raise _stub("GitHubAdapter", "draft_client_layer_v1",
                    "GitHub push_files of Client layer v1")

    def quarantine_done(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        """Real call: read open-items.md and check the quarantine section exists."""
        raise _stub("GitHubAdapter", "quarantine_done",
                    "GitHub get_file_contents read of open-items.md")

    def strip_and_quarantine(self, ctx: InstallContext, natural_key: str) -> str:
        """Real call: push_files rewriting the Client layer with every
        credential value, do-not-publish price, and unneeded personal
        identifier removed, and the quarantined categories listed in
        open-items (categories only, never the values)."""
        raise _stub("GitHubAdapter", "strip_and_quarantine",
                    "GitHub push_files of the stripped Client layer")

    def cross_check_done(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        """Real call: read open-items.md and check the cross check section exists."""
        raise _stub("GitHubAdapter", "cross_check_done",
                    "GitHub get_file_contents read of open-items.md")

    def cross_check_facts(self, ctx: InstallContext, natural_key: str) -> str:
        """Real call: push_files recording cross source conflicts in
        open-items with both values and their sources; the more recent
        dated source is used provisionally and flagged. Nothing is
        resolved by guessing."""
        raise _stub("GitHubAdapter", "cross_check_facts",
                    "GitHub push_files of cross check results into open-items")

    def review_package_exists(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        """Real call: get_file_contents for the knowledge review package document."""
        raise _stub("GitHubAdapter", "review_package_exists",
                    "GitHub get_file_contents read of the review package")

    def generate_review_package(self, ctx: InstallContext, natural_key: str) -> str:
        """Real call: push_files writing the single client readable review
        document (what the team knows, what it assumed, what it still
        needs) and recording its pointer for the review surface."""
        raise _stub("GitHubAdapter", "generate_review_package",
                    "GitHub push_files of the knowledge review package")


# ---------------------------------------------------------------------------
# Slack: the internal ops surface
# ---------------------------------------------------------------------------


class SlackAdapter:
    """UpSurge internal Slack operations via the Slack connector.

    Note: the Slack connector cannot upload or read files. Anything a
    human must download goes out as a hosted download link in a message.
    """

    def find_channel_by_name(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        """Real call: Slack connector channel list lookup by exact name
        (natural_key). On a name collision the create path appends a
        numeric suffix once and records the actual name."""
        raise _stub("SlackAdapter", "find_channel_by_name",
                    "Slack connector channel list lookup")

    def create_channel(self, ctx: InstallContext, natural_key: str) -> str:
        """Real call: Slack connector channel create with name natural_key
        (pattern ops-<client_slug>). Returns the channel id."""
        raise _stub("SlackAdapter", "create_channel",
                    "Slack connector channel create")

    def start_notice_posted(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        """Real call: read the manifest start notice field; the recorded
        message timestamp is the reference. Slack messages are not
        searchable by the orchestrator, so the manifest is the check."""
        raise _stub("SlackAdapter", "start_notice_posted",
                    "manifest start notice timestamp lookup")

    def post_start_notice(self, ctx: InstallContext, natural_key: str) -> str:
        """Real call: Slack connector send message to #ai-command with
        install_id and client_slug; the returned timestamp is recorded
        in the manifest by the engine's step record."""
        raise _stub("SlackAdapter", "post_start_notice",
                    "Slack connector send message to #ai-command")

    def post_message(self, channel: str, text: str) -> str:
        """Real call: Slack connector send message. Used by the engine for
        failure alerts (one alert per failure, never repeated)."""
        raise _stub("SlackAdapter", "post_message",
                    "Slack connector send message")


# ---------------------------------------------------------------------------
# Connectors: client app connections, seats, drills, ingest, loops
# ---------------------------------------------------------------------------


class ConnectorAdapter:
    """Muse connector operations and platform seat mechanics.

    Connection and verification follow the connector docs: system
    connectors under /opt/hatch/connectors/<name>/CONNECTOR.md and
    custom connectors under ~/workspace/custom-connectors/. Verification
    is always a status check plus one harmless read call. API key based
    apps go one key at a time through the secure capture form at the
    moment the app is reached; keys are never bulk collected and never
    pass through the orchestrator.
    """

    def checklist_exists(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        """Real call: read the manifest connect checklist for this install."""
        raise _stub("ConnectorAdapter", "checklist_exists",
                    "manifest connect checklist lookup")

    def create_checklist(self, ctx: InstallContext, natural_key: str) -> str:
        """Real call: build the checklist in the agreement's priority
        order (email, calendar, file storage, CRM, then client specific
        apps) and present it in the client's chosen surface."""
        raise _stub("ConnectorAdapter", "create_checklist",
                    "connect checklist creation in the client surface")

    def get_verification(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        """Real call: read the manifest entry for connector natural_key;
        a verified flag with a timestamp inside the stage window is the
        reference. Known behaviors: a first call to a newly approved
        host can time out in the proxy tunnel (retry once before
        treating it as a credential problem); Cloudflare protected APIs
        reject the default Python user agent with error 1010, so custom
        helpers send a browser User Agent; a 429 raises
        ProviderRateLimited and stops that provider for the run."""
        raise _stub("ConnectorAdapter", "get_verification",
                    "manifest connector verification lookup")

    def verify_connector(self, ctx: InstallContext, natural_key: str) -> str:
        """Real call: run the connector's status check plus one read only
        verification call for connector natural_key; for the CRM also
        confirm the write path the agreement requires and record
        location or account ids. Raises AuthError on a wrong account or
        dead credential, ProviderRateLimited on a 429."""
        raise _stub("ConnectorAdapter", "verify_connector",
                    "connector status check plus one verification read")

    def seat_registered(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        """Real call: read the manifest seat entry named by natural_key."""
        raise _stub("ConnectorAdapter", "seat_registered",
                    "manifest seat entry lookup")

    def register_seat(self, ctx: InstallContext, natural_key: str) -> str:
        """Real call: register the seat (for the Muse seat: connect the
        client's Muse environment to the Client layer, the Desk, and
        the Stage 2 connectors, with Maive as delegator of record)."""
        raise _stub("ConnectorAdapter", "register_seat",
                    "platform seat registration for the install")

    def drill_passed(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        """Real call: read the drill record named by natural_key from the
        Pack delivery records; a pass with timestamp is the reference."""
        raise _stub("ConnectorAdapter", "drill_passed",
                    "drill record lookup")

    def run_drill(self, ctx: InstallContext, natural_key: str) -> str:
        """Real call: route one synthetic, client safe test task to the
        lane named by natural_key. The lane must claim it, complete it
        from the Client layer only, and return it in the handoff packet
        format. Pass criteria: correct facts, correct format, no cross
        client data, no internal process language. A wrong result raises
        TransientError for the single automatic re-read and retry the
        spec allows, then the step fails for operator handling."""
        raise _stub("ConnectorAdapter", "run_drill",
                    "seat verification drill routed to the lane")

    def ingest_done(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        """Real call: read the manifest source log for this install."""
        raise _stub("ConnectorAdapter", "ingest_done",
                    "manifest ingest source log lookup")

    def ingest_sources(self, ctx: InstallContext, natural_key: str) -> str:
        """Real call: crawl the client website, read brand assets and
        documents from connected file storage, and read CRM structure
        (pipelines, stages, fields, locations) through its connector.
        Every source is logged with origin and timestamp. An unreachable
        source is recorded as a gap, never fabricated."""
        raise _stub("ConnectorAdapter", "ingest_sources",
                    "website crawl plus Drive, Docs, and CRM connector reads")

    def knowledge_drills_passed(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        """Real call: read the knowledge drill records for all three lanes."""
        raise _stub("ConnectorAdapter", "knowledge_drills_passed",
                    "knowledge drill record lookup")

    def run_knowledge_drills(self, ctx: InstallContext, natural_key: str) -> str:
        """Real call: refresh each seated lane's Client layer pointer,
        then ask each lane three factual questions from the seeded
        profile. Answers must match the Client layer exactly."""
        raise _stub("ConnectorAdapter", "run_knowledge_drills",
                    "lane pointer refresh plus knowledge drill per lane")

    def sweep_passed(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        """Real call: read the manifest final sweep record for this install."""
        raise _stub("ConnectorAdapter", "sweep_passed",
                    "manifest final sweep record lookup")

    def run_final_sweep(self, ctx: InstallContext, natural_key: str) -> str:
        """Real call: one read check per required connector, one ping
        task per lane, the Desk test project pattern confirmed Done,
        and the heartbeat render check. Any failed check raises and go
        live stops; go live never proceeds on partial checks."""
        raise _stub("ConnectorAdapter", "run_final_sweep",
                    "final verification sweep across connectors, lanes, and Desk")

    def loops_scheduled(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        """Real call: list the install's scheduled jobs and match the
        standing loop set."""
        raise _stub("ConnectorAdapter", "loops_scheduled",
                    "scheduled job listing for the install")

    def schedule_loops(self, ctx: InstallContext, natural_key: str) -> str:
        """Real call: create the standing loops for the install (intake
        backstop sweep, waiting watcher, weekly digest, monthly Pack
        update check) through the cron tooling, scoped to this client."""
        raise _stub("ConnectorAdapter", "schedule_loops",
                    "cron creation for the install standing loops")


# ---------------------------------------------------------------------------
# Adapter bundles
# ---------------------------------------------------------------------------


class RealAdapters:
    """The live bundle. Every method is a stub in v0 (see README)."""

    def __init__(self) -> None:
        self.github = GitHubAdapter()
        self.desk = DeskAdapter()
        self.slack = SlackAdapter()
        self.connectors = ConnectorAdapter()


# ---------------------------------------------------------------------------
# DryRun adapters
# ---------------------------------------------------------------------------


class DryRunRegistry:
    """What a dry run has 'created', persisted as JSON.

    Objects are keyed by idempotency key and by natural key, mirroring
    the check-before-create lookups the real adapters will perform
    against GitHub, the Desk, Slack, and the manifest. Actions is the
    human readable log of everything the dry run would have done.
    """

    def __init__(self, path: Path) -> None:
        self.path = path
        self.objects: Dict[str, str] = {}
        self.actions: List[str] = []
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            self.objects = data.get("objects", {})
            self.actions = data.get("actions", [])

    def get(self, key: str) -> Optional[str]:
        return self.objects.get(key)

    def put(self, idempotency_key: str, natural_key: str, ref: str, action: str) -> str:
        self.objects[idempotency_key] = ref
        self.objects[f"nk:{natural_key}"] = ref
        self.actions.append(action)
        self._save()
        return ref

    def record(self, action: str) -> None:
        self.actions.append(action)
        self._save()

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(
            json.dumps({"objects": self.objects, "actions": self.actions}, indent=2),
            encoding="utf-8",
        )
        os.replace(tmp, self.path)


class _DryRunBase:
    """Shared check and apply mechanics for the dry run adapters."""

    bundle = "dryrun"

    def __init__(self, registry: DryRunRegistry) -> None:
        self.registry = registry

    def _check(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        return self.registry.get(ctx.idempotency_key) or self.registry.get(
            f"nk:{natural_key}"
        )

    def _apply(self, ctx: InstallContext, natural_key: str, label: str) -> str:
        ref = f"dryrun://{self.bundle}/{natural_key}"
        action = f"{label} created {ref}"
        return self.registry.put(ctx.idempotency_key, natural_key, ref, action)


class DryRunDesk(_DryRunBase):
    bundle = "desk"

    def find_client_by_slug(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        return self._check(ctx, natural_key)

    def insert_client_workspace(self, ctx: InstallContext, natural_key: str) -> str:
        return self._apply(ctx, natural_key, "desk.insert_client_workspace")

    def passcode_pointer_exists(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        return self._check(ctx, natural_key)

    def create_passcode_pointer(self, ctx: InstallContext, natural_key: str) -> str:
        return self._apply(ctx, natural_key, "desk.create_passcode_pointer (pointer only)")

    def roster_exists(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        return self._check(ctx, natural_key)

    def insert_roster(self, ctx: InstallContext, natural_key: str) -> str:
        return self._apply(ctx, natural_key, "desk.insert_roster")

    def webhooks_registered(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        return self._check(ctx, natural_key)

    def register_webhooks(self, ctx: InstallContext, natural_key: str) -> str:
        return self._apply(ctx, natural_key, "desk.register_webhooks")

    def intake_enabled(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        return self._check(ctx, natural_key)

    def enable_intake(self, ctx: InstallContext, natural_key: str) -> str:
        return self._apply(ctx, natural_key, "desk.enable_intake")

    def heartbeat_live(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        return self._check(ctx, natural_key)

    def publish_heartbeat(self, ctx: InstallContext, natural_key: str) -> str:
        return self._apply(ctx, natural_key, "desk.publish_heartbeat")

    def first_project_exists(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        return self._check(ctx, natural_key)

    def create_first_project(self, ctx: InstallContext, natural_key: str) -> str:
        return self._apply(ctx, natural_key, "desk.create_first_project")


class DryRunGitHub(_DryRunBase):
    bundle = "github"

    def path_exists(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        return self._check(ctx, natural_key)

    def write_client_layer(self, ctx: InstallContext, natural_key: str) -> str:
        return self._apply(ctx, natural_key, "github.write_client_layer")

    def manifest_exists(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        return self._check(ctx, natural_key)

    def write_manifest(self, ctx: InstallContext, natural_key: str) -> str:
        return self._apply(ctx, natural_key, "github.write_manifest")

    def stage_recorded(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        return self._check(ctx, natural_key)

    def record_stage(self, ctx: InstallContext, natural_key: str) -> str:
        return self._apply(ctx, natural_key, "github.record_stage")

    def pack_delivery_exists(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        return self._check(ctx, natural_key)

    def deliver_pack(self, ctx: InstallContext, natural_key: str) -> str:
        return self._apply(ctx, natural_key, "github.deliver_pack")

    def routing_table_exists(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        return self._check(ctx, natural_key)

    def write_routing_table(self, ctx: InstallContext, natural_key: str) -> str:
        return self._apply(ctx, natural_key, "github.write_routing_table")

    def client_layer_v1_exists(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        return self._check(ctx, natural_key)

    def draft_client_layer_v1(self, ctx: InstallContext, natural_key: str) -> str:
        return self._apply(ctx, natural_key, "github.draft_client_layer_v1")

    def quarantine_done(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        return self._check(ctx, natural_key)

    def strip_and_quarantine(self, ctx: InstallContext, natural_key: str) -> str:
        return self._apply(ctx, natural_key, "github.strip_and_quarantine")

    def cross_check_done(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        return self._check(ctx, natural_key)

    def cross_check_facts(self, ctx: InstallContext, natural_key: str) -> str:
        return self._apply(ctx, natural_key, "github.cross_check_facts")

    def review_package_exists(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        return self._check(ctx, natural_key)

    def generate_review_package(self, ctx: InstallContext, natural_key: str) -> str:
        return self._apply(ctx, natural_key, "github.generate_review_package")


class DryRunSlack(_DryRunBase):
    bundle = "slack"

    def find_channel_by_name(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        return self._check(ctx, natural_key)

    def create_channel(self, ctx: InstallContext, natural_key: str) -> str:
        return self._apply(ctx, natural_key, "slack.create_channel")

    def start_notice_posted(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        return self._check(ctx, natural_key)

    def post_start_notice(self, ctx: InstallContext, natural_key: str) -> str:
        return self._apply(ctx, natural_key, "slack.post_start_notice (#ai-command)")

    def post_message(self, channel: str, text: str) -> str:
        self.registry.record(f"slack.post_message to {channel}: {text}")
        return f"dryrun://slack/message/{len(self.registry.actions)}"


class DryRunConnectors(_DryRunBase):
    bundle = "connectors"

    def checklist_exists(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        return self._check(ctx, natural_key)

    def create_checklist(self, ctx: InstallContext, natural_key: str) -> str:
        return self._apply(ctx, natural_key, "connectors.create_checklist")

    def get_verification(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        return self._check(ctx, natural_key)

    def verify_connector(self, ctx: InstallContext, natural_key: str) -> str:
        return self._apply(ctx, natural_key, f"connectors.verify_connector[{natural_key}]")

    def seat_registered(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        return self._check(ctx, natural_key)

    def register_seat(self, ctx: InstallContext, natural_key: str) -> str:
        return self._apply(ctx, natural_key, "connectors.register_seat")

    def drill_passed(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        return self._check(ctx, natural_key)

    def run_drill(self, ctx: InstallContext, natural_key: str) -> str:
        return self._apply(ctx, natural_key, f"connectors.run_drill[{natural_key}] PASS")

    def ingest_done(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        return self._check(ctx, natural_key)

    def ingest_sources(self, ctx: InstallContext, natural_key: str) -> str:
        return self._apply(ctx, natural_key, "connectors.ingest_sources")

    def knowledge_drills_passed(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        return self._check(ctx, natural_key)

    def run_knowledge_drills(self, ctx: InstallContext, natural_key: str) -> str:
        return self._apply(ctx, natural_key, "connectors.run_knowledge_drills PASS")

    def sweep_passed(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        return self._check(ctx, natural_key)

    def run_final_sweep(self, ctx: InstallContext, natural_key: str) -> str:
        return self._apply(ctx, natural_key, "connectors.run_final_sweep PASS")

    def loops_scheduled(self, ctx: InstallContext, natural_key: str) -> Optional[str]:
        return self._check(ctx, natural_key)

    def schedule_loops(self, ctx: InstallContext, natural_key: str) -> str:
        return self._apply(ctx, natural_key, "connectors.schedule_loops")


class DryRunAdapters:
    """The dry run bundle. Simulates every system, records everything."""

    def __init__(self, registry_path: Path) -> None:
        registry = DryRunRegistry(registry_path)
        self.github = DryRunGitHub(registry)
        self.desk = DryRunDesk(registry)
        self.slack = DryRunSlack(registry)
        self.connectors = DryRunConnectors(registry)
        self.registry = registry
