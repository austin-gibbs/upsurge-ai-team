"""Install states and step definitions for the AI Team install orchestrator.

This module is the shared contract: the install level state machine, the
per stage step lists, the idempotency key format, the install context,
and the error taxonomy the engine and the adapters both use. It holds no
execution logic.

State machine (install pipeline spec, Section 10):

    initiated -> provisioning -> provisioned -> connecting -> connected
    -> seating -> seated -> seeding -> seeded -> qa_review -> going_live
    -> live

Side states: paused_human, failed_retryable, failed_terminal (reachable
from any active state), suspended and closed (from live). qa_review is
the spec's qa_gate: the single human gate in the pipeline. Go live
cannot start until an approver is recorded on the install record.

Idempotency key format (spec, Section 10):

    <install_id>:<stage>:<step>:<natural_key>

Before a step creates anything, the engine looks the object up by its
natural key. If it exists, the step is marked done with the existing
reference and no create is issued. Re-running any stage converges to the
same end state.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Tuple


class InstallState(str, Enum):
    """Install level states. Values are the wire format in state files."""

    INITIATED = "initiated"
    PROVISIONING = "provisioning"
    PROVISIONED = "provisioned"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    SEATING = "seating"
    SEEDED = "seeded"
    SEATED = "seated"
    SEEDING = "seeding"
    QA_REVIEW = "qa_review"
    GOING_LIVE = "going_live"
    LIVE = "live"
    PAUSED_HUMAN = "paused_human"
    FAILED_RETRYABLE = "failed_retryable"
    FAILED_TERMINAL = "failed_terminal"
    SUSPENDED = "suspended"
    CLOSED = "closed"


# ---------------------------------------------------------------------------
# Error taxonomy (spec, Section 10 retry policy)
# ---------------------------------------------------------------------------


class OrchestratorError(Exception):
    """Base class for errors adapters raise and the engine understands."""


class TransientError(OrchestratorError):
    """Timeout, 5xx, or proxy tunnel failure. Retried on the backoff ladder."""


class ProviderRateLimited(OrchestratorError):
    """Provider answered 429. Hard stop for that provider in this run.

    The engine never retries a 429 in the same run, never switches to an
    alternate endpoint, and reschedules the install as failed_retryable.
    """

    def __init__(self, provider: str, message: str = "") -> None:
        self.provider = provider
        super().__init__(message or f"provider {provider} returned 429")


class AuthError(OrchestratorError):
    """Credential or account problem. No retry; install goes to paused_human."""


class SchemaError(OrchestratorError):
    """Target system shape does not match the spec. No retry; failed_terminal."""


class LockHeld(OrchestratorError):
    """Another runner already holds this install's lock."""


# Retry ladder from the spec: first attempt immediately, then retries
# after 60s, 300s, and 1800s for transient errors. Four attempts per run.
RETRY_WAITS: Tuple[int, ...] = (60, 300, 1800)
MAX_ATTEMPTS = len(RETRY_WAITS) + 1


# ---------------------------------------------------------------------------
# Install context
# ---------------------------------------------------------------------------


@dataclass
class InstallContext:
    """Everything a step needs to know about the install it belongs to.

    The identity fields are persisted in the install state record so a
    later process can rebuild the context and resume. The runtime fields
    (stage_key, step_key, idempotency_key) are set by the engine before
    each step runs.
    """

    install_id: str
    client_slug: str
    legal_name: str = ""
    sponsor_name: str = ""
    sponsor_email: str = ""
    timezone: str = "America/Denver"
    intake_mode: str = "surge-form"  # surge-form | direct | pm-system
    seat_model: str = "client-owned"  # client-owned | upsurge-managed
    pack_version: str = "1.0.0"
    crm_connector: str = "ghl"

    # Runtime fields, set by the engine per step.
    stage_key: str = ""
    step_key: str = ""
    idempotency_key: str = ""

    @property
    def slug_env(self) -> str:
        """Slug in env var form, for pointer names like SURGE_PASSCODE_X."""
        return self.client_slug.upper().replace("-", "_")

    def template_vars(self) -> Dict[str, str]:
        return {
            "install_id": self.install_id,
            "client_slug": self.client_slug,
            "pack_version": self.pack_version,
            "crm_connector": self.crm_connector,
            "slug_env": self.slug_env,
        }

    def params(self) -> Dict[str, str]:
        """The persistable identity fields."""
        return {
            "install_id": self.install_id,
            "client_slug": self.client_slug,
            "legal_name": self.legal_name,
            "sponsor_name": self.sponsor_name,
            "sponsor_email": self.sponsor_email,
            "timezone": self.timezone,
            "intake_mode": self.intake_mode,
            "seat_model": self.seat_model,
            "pack_version": self.pack_version,
            "crm_connector": self.crm_connector,
        }

    @classmethod
    def from_params(cls, params: Dict[str, str]) -> "InstallContext":
        return cls(**params)


# ---------------------------------------------------------------------------
# Step and stage definitions
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Step:
    """One idempotent step.

    adapter: which adapter bundle member runs it (github, desk, slack,
    connectors). check: adapter method returning an existing object
    reference or None. apply: adapter method creating the object and
    returning its reference. natural_key: format template resolved
    against InstallContext.template_vars().
    """

    key: str
    title: str
    adapter: str
    check: str
    apply: str
    natural_key: str


@dataclass(frozen=True)
class Stage:
    key: str
    title: str
    active_state: InstallState
    done_state: InstallState
    steps: Tuple[Step, ...]


PROVISION = Stage(
    key="provision",
    title="Provision",
    active_state=InstallState.PROVISIONING,
    done_state=InstallState.PROVISIONED,
    steps=(
        Step("create_client_layer", "Create Client layer memory structure",
             "github", "path_exists", "write_client_layer",
             "memory/muse/clients/{client_slug}"),
        Step("create_desk_workspace", "Create the client Desk workspace",
             "desk", "find_client_by_slug", "insert_client_workspace",
             "{client_slug}"),
        Step("desk_passcode_pointer", "Generate Desk passcode, record pointer only",
             "desk", "passcode_pointer_exists", "create_passcode_pointer",
             "SURGE_PASSCODE_{slug_env}"),
        Step("create_ops_channel", "Create the internal ops Slack channel",
             "slack", "find_channel_by_name", "create_channel",
             "ops-{client_slug}"),
        Step("create_roster_record", "Create the roster record from the Team Pack",
             "desk", "roster_exists", "insert_roster",
             "roster:{client_slug}"),
        Step("register_webhooks", "Register the install webhook endpoints",
             "desk", "webhooks_registered", "register_webhooks",
             "webhooks:{client_slug}"),
        Step("write_manifest_v1", "Write manifest v1 to the repo",
             "github", "manifest_exists", "write_manifest",
             "memory/muse/installs/{client_slug}/manifest.json"),
        Step("post_start_notice", "Post the internal start notice",
             "slack", "start_notice_posted", "post_start_notice",
             "start-notice:{install_id}"),
    ),
)

CONNECT = Stage(
    key="connect",
    title="Connect",
    active_state=InstallState.CONNECTING,
    done_state=InstallState.CONNECTED,
    steps=(
        Step("present_checklist", "Present the connect checklist in priority order",
             "connectors", "checklist_exists", "create_checklist",
             "checklist:{client_slug}"),
        Step("verify_email", "Connect and verify email",
             "connectors", "get_verification", "verify_connector", "gmail"),
        Step("verify_calendar", "Connect and verify calendar",
             "connectors", "get_verification", "verify_connector",
             "google_calendar"),
        Step("verify_file_storage", "Connect and verify file storage",
             "connectors", "get_verification", "verify_connector",
             "google_drive"),
        Step("verify_crm", "Connect and verify the primary CRM end to end",
             "connectors", "get_verification", "verify_connector",
             "{crm_connector}"),
        Step("record_connections", "Record verified connections in the manifest",
             "github", "stage_recorded", "record_stage",
             "manifest-stage:connect:{client_slug}"),
    ),
)

SEAT = Stage(
    key="seat",
    title="Seat platforms",
    active_state=InstallState.SEATING,
    done_state=InstallState.SEATED,
    steps=(
        Step("record_seat_model", "Record the seat model from the agreement",
             "github", "stage_recorded", "record_stage",
             "seat-model:{client_slug}"),
        Step("register_muse_seat", "Register the Muse seat as delegator of record",
             "connectors", "seat_registered", "register_seat", "seat:muse"),
        Step("deliver_pack_claude", "Deliver the Team Pack bootstrap to the Claude seat",
             "github", "pack_delivery_exists", "deliver_pack",
             "pack:claude:{pack_version}"),
        Step("deliver_pack_grok", "Deliver the Team Pack bootstrap to the Grok seat",
             "github", "pack_delivery_exists", "deliver_pack",
             "pack:grok:{pack_version}"),
        Step("drill_muse_lane", "Run the Muse lane seat verification drill",
             "connectors", "drill_passed", "run_drill", "drill:muse"),
        Step("drill_claude_lane", "Run the Claude lane seat verification drill",
             "connectors", "drill_passed", "run_drill", "drill:claude"),
        Step("drill_grok_lane", "Run the Grok lane seat verification drill",
             "connectors", "drill_passed", "run_drill", "drill:grok"),
        Step("publish_routing_table", "Publish the install routing table",
             "github", "routing_table_exists", "write_routing_table",
             "routing:{client_slug}"),
    ),
)

SEED = Stage(
    key="seed",
    title="Seed knowledge",
    active_state=InstallState.SEEDING,
    done_state=InstallState.SEEDED,
    steps=(
        Step("ingest_sources", "Ingest website, documents, and CRM structure",
             "connectors", "ingest_done", "ingest_sources",
             "ingest:{client_slug}"),
        Step("draft_client_layer_v1", "Draft Client layer v1 from ingested sources",
             "github", "client_layer_v1_exists", "draft_client_layer_v1",
             "client-layer-v1:{client_slug}"),
        Step("strip_and_quarantine", "Strip credentials and quarantine flagged facts",
             "github", "quarantine_done", "strip_and_quarantine",
             "quarantine:{client_slug}"),
        Step("cross_check_facts", "Cross check facts across at least two sources",
             "github", "cross_check_done", "cross_check_facts",
             "crosscheck:{client_slug}"),
        Step("generate_review_package", "Generate the knowledge review package",
             "github", "review_package_exists", "generate_review_package",
             "review-package:{client_slug}"),
        Step("knowledge_drills", "Refresh lane pointers and run knowledge drills",
             "connectors", "knowledge_drills_passed", "run_knowledge_drills",
             "knowledge-drills:{client_slug}"),
    ),
)

GO_LIVE = Stage(
    key="go_live",
    title="Go live",
    active_state=InstallState.GOING_LIVE,
    done_state=InstallState.LIVE,
    steps=(
        Step("final_verification_sweep", "Re-run one read check per required system",
             "connectors", "sweep_passed", "run_final_sweep",
             "final-sweep:{client_slug}"),
        Step("enable_intake_adapters", "Enable the intake adapters from the agreement",
             "desk", "intake_enabled", "enable_intake",
             "intake:{client_slug}"),
        Step("publish_heartbeat_page", "Publish the heartbeat page and orientation",
             "desk", "heartbeat_live", "publish_heartbeat",
             "heartbeat:{client_slug}"),
        Step("create_first_project", "Create the first real project from intake",
             "desk", "first_project_exists", "create_first_project",
             "first-project:{client_slug}"),
        Step("schedule_standing_loops", "Schedule intake sweep, watcher, and digests",
             "connectors", "loops_scheduled", "schedule_loops",
             "loops:{client_slug}"),
    ),
)

# Stage order is execution order. Go live is last and gated by qa_review.
STAGES: Tuple[Stage, ...] = (PROVISION, CONNECT, SEAT, SEED, GO_LIVE)

GATED_STAGE_KEY = "go_live"
GATE_NAME = "qa_review"


def all_step_keys() -> Tuple[str, ...]:
    """Fully qualified step keys (stage.step) in execution order."""
    return tuple(f"{stage.key}.{step.key}" for stage in STAGES for step in stage.steps)
