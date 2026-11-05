#!/usr/bin/env python3
"""Client setup package generator for the UpSurge AI Team service.

Takes a client profile JSON and produces a complete setup package:

  <output>/
    repo/                  The tree that becomes the client's own GitHub
                           repository (upsurge-client-<slug>) in UpSurge's
                           GitHub organization: root README, the filled
                           client memory layer, Team Pack delivery records
                           per lane, and positioning and rules summaries in
                           working form.
    pm-tool/               The setup files the PM tool (Surge Command)
                           workspace is built from: workspace config, board,
                           roster, starter projects, census, and the
                           hand-held onboarding checklist.
    provisioning-record.json
                           Payment status, repo target and creation status,
                           and the orchestrator step mapping. Honest by
                           construction: it never claims a repo was created
                           or a payment received when neither happened.
    verification-report.md The generator's own checks over the package.

Python standard library only. No network calls. No credential values are
read, written, or echoed anywhere in this script or its output.

Usage:
  python3 provisioning/client_setup.py PROFILE_JSON OUTPUT_DIR
  python3 provisioning/client_setup.py provisioning/profile-template.json \
      provisioning/examples/cedar-peak-dental
"""

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MEMORY_TEMPLATES = REPO_ROOT / "install-templates" / "client-memory"
PACKS_DIR = REPO_ROOT / "install-templates" / "business-types"

CENSUS_STATES = ("Connected", "Set up for them", "Coming next", "Not needed")
TIER_APP_COUNTS = {"launch": 5, "growth": 10, "full": 18, "pilot": None}

SECRET_PATTERNS = [
    r"sk-[A-Za-z0-9]{16,}",
    r"ghp_[A-Za-z0-9]{20,}",
    r"github_pat_[A-Za-z0-9_]{20,}",
    r"AKIA[0-9A-Z]{16}",
    r"xox[baprs]-[A-Za-z0-9-]{10,}",
    r"-----BEGIN (RSA |OPENSSH |EC )?PRIVATE KEY",
    r"Bearer [A-Za-z0-9._-]{20,}",
]

# The standard roster, from team-pack/team-pack-and-roster.md section 3.1.
# home_lane is the house lane the specialist works from (muse, claude, grok).
ROSTER = [
    ("Maive", "Team lead and client front door", "muse"),
    ("Marcus", "Grok lane lead", "grok"),
    ("Owen", "Onboarding orchestrator", "muse"),
    ("Lena", "Memory librarian", "muse"),
    ("Felix", "Fulfillment lead", "muse"),
    ("Diego", "CRM architect", "muse"),
    ("Dana", "CRM data operations", "muse"),
    ("Mira", "Marketing lead", "claude"),
    ("Milo", "Ad creative producer", "grok"),
    ("Remy", "Voice and dialer specialist", "muse"),
    ("Wes", "Web development lead", "claude"),
    ("Kai", "SEO and AEO lead", "claude"),
    ("Theo", "Meeting to action", "muse"),
    ("Quinn", "Call QA auditor", "muse"),
    ("Aria", "A2P compliance", "muse"),
    ("Hazel", "Client success lead", "muse"),
    ("Finn", "Finance controller", "muse"),
    ("Parker", "Performance analyst", "claude"),
    ("Greta", "Growth and sales lead", "claude"),
    ("Nova", "Service innovation", "claude"),
    ("Sage", "SOP and skill writer", "claude"),
    ("Dex", "Delivery QA", "muse"),
]

HOUSE_LANES = {
    "muse": {"name": "Operations Lane", "leader": "Maive"},
    "claude": {"name": "Strategy Lane", "leader": "Named in the install record"},
    "grok": {"name": "Speed Lane", "leader": "Marcus"},
}

# Delivery methods per platform, from product/platform-policy.md section 4.
PLATFORM_DELIVERY = {
    "Muse": {
        "method": "Project instructions plus the memory tree in the project workspace",
        "memory_updates": "Re-sync of the client memory files on each Pack or memory release",
        "drill_note": "Standard drill, no adjustments",
    },
    "Grok": {
        "method": "System instructions in the workspace, memory files attached per workspace setup",
        "memory_updates": "Memory files re-issued on each release; version stamp checked at drill time",
        "drill_note": "Standard drill; format check watches for truncated instruction loads",
    },
    "Claude": {
        "method": "Project instructions and project knowledge files",
        "memory_updates": "Project knowledge re-upload on each release",
        "drill_note": "Standard drill; facts check includes a freshness probe against the current version stamp",
    },
    "ChatGPT": {
        "method": "Custom GPT instructions or project instructions, per the client's plan",
        "memory_updates": "Instruction block and files re-issued on each release",
        "drill_note": "Standard drill; if the condensed Pack layer is used, facts check runs the extended fact set",
    },
    "Gemini": {
        "method": "System instructions in the workspace or shared instruction surface",
        "memory_updates": "Memory files re-issued on each release",
        "drill_note": "Standard drill; language check confirms the instruction surface actually retained the Pack",
    },
}
PLATFORM_FALLBACK = {
    "method": "Paste-ready setup block into whatever instruction surface exists, memory delivered as files",
    "memory_updates": "Manual re-issue by our team as a certified manual step on each release",
    "drill_note": "Standard drill with no fields waived; a platform that cannot pass the isolation check does not get seated with client memory",
}

DRILL_FIELDS = [
    "drill.facts_check",
    "drill.format_check",
    "drill.isolation_check",
    "drill.language_check",
    "drill.status",
    "drill.attempts",
    "drill.completed_at",
]

PACK_COMPONENTS = [
    "Roster and lane map",
    "Routing rules by task type",
    "Execution brief standard",
    "House style",
    "QA checklists by deliverable type",
    "Escalation rules",
    "Claim protocol",
    "Client memory template pointer",
    "Reporting templates",
    "Install and heartbeat data contract",
]

LANE_SPECIALIST_ORDER = {
    "muse": ["Diego", "Hazel", "Remy", "Owen", "Dana", "Theo"],
    "claude": ["Parker", "Mira", "Kai", "Sage", "Wes", "Greta"],
    "grok": ["Milo", "Greta", "Marcus"],
}


def slugify(name):
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or "client"


def pack_section(text, heading):
    """Return the body of a '## <heading>' section of a pack file."""
    pattern = re.compile(
        r"^## " + re.escape(heading) + r"\s*$(.*?)(?=^## |\Z)", re.M | re.S
    )
    match = pattern.search(text)
    return match.group(1) if match else ""


def parse_pack(pack_id):
    """Parse the board shape out of a Business Type Pack file."""
    path = PACKS_DIR / (pack_id + ".md")
    if not path.exists():
        path = PACKS_DIR / "general-services.md"
        pack_id = "general-services"
    text = path.read_text(encoding="utf-8")

    stages = []
    for line in pack_section(text, "Starter board stages").splitlines():
        m = re.match(r"\s*\d+\.\s+(.*\S)\s*$", line)
        if m:
            stages.append(m.group(1))

    categories = []
    for line in pack_section(text, "Task categories").splitlines():
        m = re.match(r"\s*-\s+(.*\S)\s*$", line)
        if m:
            categories.append(m.group(1))

    requests = []
    for line in pack_section(text, "Starter requests").splitlines():
        m = re.match(r"\s*-\s+(.*\S)\s*$", line)
        if m:
            requests.append(m.group(1).strip().strip('"'))

    item_word = "Job"
    customer_word = "Client"
    for line in pack_section(text, "Words this business uses").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 2:
            if cells[0] == "Main work item":
                item_word = cells[1]
            if cells[0] == "Customer":
                customer_word = cells[1]

    guardrails = []
    for line in pack_section(text, "Extra guardrails").splitlines():
        m = re.match(r"\s*-\s+(.*\S)\s*$", line)
        if m:
            guardrails.append(m.group(1))

    return {
        "pack_id": pack_id,
        "stages": stages,
        "categories": categories,
        "starter_requests": requests,
        "item_word": item_word,
        "customer_word": customer_word,
        "guardrails": guardrails,
    }


def fill_template(text, values):
    def repl(match):
        key = match.group(1)
        return values.get(key, match.group(0))

    return re.sub(r"\{\{([a-z_]+)\}\}", repl, text)


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_package(profile, out_dir):
    out = Path(out_dir)
    business_name = profile["business_name"]
    slug = profile.get("slug") or slugify(business_name)
    tier_key = profile.get("tier", "growth")
    pack = parse_pack(profile.get("business_type_pack", "general-services"))

    # Client words beat library words when the profile carries their own.
    shape = profile.get("custom_shape") or {}
    stages = shape.get("board_stages") or pack["stages"]
    categories = shape.get("categories") or pack["categories"]
    item_word = shape.get("item_word") or pack["item_word"]
    customer_word = shape.get("customer_word") or pack["customer_word"]

    lanes = []
    for entry in profile["lanes"]:
        house = entry["house_lane"]
        platform = entry["platform"]
        delivery = PLATFORM_DELIVERY.get(platform, PLATFORM_FALLBACK)
        lanes.append(
            {
                "house_lane": house,
                "name": entry.get("name") or HOUSE_LANES[house]["name"],
                "platform": platform,
                "leader": entry.get("leader") or HOUSE_LANES[house]["leader"],
                "delivery_method": delivery["method"],
                "memory_updates": delivery["memory_updates"],
                "drill_note": delivery["drill_note"],
                "drill_fields": DRILL_FIELDS,
            }
        )
    lanes_active = ", ".join(
        "{} on {}".format(lane["name"], lane["platform"]) for lane in lanes
    )

    systems = profile.get("systems", {})
    values = {
        "business_name": business_name,
        "legal_business_name": profile.get("legal_business_name", business_name),
        "slug": slug,
        "industry": profile.get("industry", ""),
        "website_url": profile.get("website_url", ""),
        "tier": profile.get("tier_label", tier_key),
        "pack_version": "Pack v" + profile.get("pack_version", "1.0"),
        "lanes_active": lanes_active,
        "intake_mode": profile.get(
            "intake_mode", "PM tool (Surge Command) submission"
        ),
        "install_date": profile.get("install_date", ""),
        "signer_name": profile.get("signer_name", ""),
        "champion_name": profile.get("champion_name", ""),
        "owner_name": profile.get("owner_name", ""),
        "desk_workspace_url": (
            "Recorded at provisioning: the PM tool workspace link is written "
            "here when the workspace is created."
        ),
        "team_page_url": (
            "Recorded at provisioning: the team page link is written here "
            "when the page goes live."
        ),
        "output_ledger_url": (
            "Recorded at provisioning: the output ledger link is written "
            "here when the workspace is created."
        ),
        "intake_channel": "The PM tool (Surge Command) request form",
        "notification_channel": profile.get(
            "notification_channel", "Email to the champion, plus the PM tool"
        ),
        "agreement_pointer": "Sales pipeline agreement record (pointer only)",
        "export_test_date": "Runs during install QA, before go live",
        "export_location_pointer": (
            "Recorded in access-manifest.md when the export test runs"
        ),
        "crm_name": systems.get("crm_name", "To be confirmed at the census"),
        "email_platform": systems.get("email_platform", "To be confirmed at the census"),
        "calendar_platform": systems.get(
            "calendar_platform", "To be confirmed at the census"
        ),
        "files_platform": systems.get("files_platform", "To be confirmed at the census"),
        "phone_platform": systems.get("phone_platform", "To be confirmed at the census"),
        "voice_platform": systems.get("voice_platform", "To be confirmed at the census"),
        "pm_platform": "Surge Command (the PM tool)",
        "billing_platform": systems.get(
            "billing_platform", "To be confirmed at the census"
        ),
        "ads_platform": systems.get("ads_platform", "To be confirmed at the census"),
        "web_platform": systems.get("web_platform", "To be confirmed at the census"),
    }

    repo_dir = out / "repo"
    pm_dir = out / "pm-tool"

    # ---- (a) The repo tree -------------------------------------------------
    write(repo_dir / "README.md", repo_readme(profile, slug, lanes_active))

    memory_out = repo_dir / "memory"
    for template in sorted(MEMORY_TEMPLATES.glob("*.md")):
        filled = fill_template(template.read_text(encoding="utf-8"), values)
        write(memory_out / template.name, filled)

    write(
        repo_dir / "team-pack" / "delivery-summary.md",
        delivery_summary(profile, lanes),
    )
    for lane in lanes:
        write(
            repo_dir / "team-pack" / ("lane-" + lane["house_lane"] + ".md"),
            lane_delivery_record(profile, lane),
        )
    write(
        repo_dir / "positioning-and-rules.md",
        positioning_and_rules(profile, pack),
    )

    # ---- (b) The PM tool setup files ---------------------------------------
    workspace_config = {
        "business_name": business_name,
        "client_slug": slug,
        "business_type": {
            "pack": pack["pack_id"],
            "display": profile.get("business_type_display", pack["pack_id"]),
            "custom_words": shape,
        },
        "timezone": profile.get("timezone", ""),
        "tier": tier_key,
        "tier_label": profile.get("tier_label", tier_key),
        "item_word": item_word,
        "customer_word": customer_word,
        "lanes": [
            {
                "house_lane": lane["house_lane"],
                "name": lane["name"],
                "platform": lane["platform"],
                "leader": lane["leader"],
            }
            for lane in lanes
        ],
        "payment_status": "awaiting_payment_link",
        "repository": {
            "name": "upsurge-client-" + slug,
            "owner": "UpSurge GitHub organization",
            "created_by_this_generator": False,
            "status": "package_ready_repo_creation_pending",
        },
        "pm_tool_rule": (
            "The PM tool is home base. Every lane adds every project here, "
            "and the client watches all work from here."
        ),
    }
    write(
        pm_dir / "workspace-config.json",
        json.dumps(workspace_config, indent=2) + "\n",
    )

    board = {
        "item_word": item_word,
        "customer_word": customer_word,
        "stages": stages,
        "categories": categories,
        "starter_requests": pack["starter_requests"],
        "source_pack": pack["pack_id"],
        "rename_rule": (
            "The client can rename any stage, category, or word at any "
            "time, in the PM tool or by asking their team lead."
        ),
    }
    write(pm_dir / "board.json", json.dumps(board, indent=2) + "\n")

    roster = {
        "front_door": "Maive (team lead and single point of contact)",
        "lanes": [],
        "specialists": [
            {"name": name, "role": role, "home_lane": home}
            for name, role, home in ROSTER
        ],
        "note": (
            "Lanes are roles, not vendors. The platform named on a lane is "
            "the seat filling it for this client and can be refilled by "
            "another platform without a re-install."
        ),
    }
    for lane in lanes:
        roster["lanes"].append(
            {
                "house_lane": lane["house_lane"],
                "name": lane["name"],
                "platform": lane["platform"],
                "leader": lane["leader"],
                "delivery_method": lane["delivery_method"],
                "specialists": [
                    name
                    for name, role, home in ROSTER
                    if home == lane["house_lane"]
                ],
            }
        )
    write(pm_dir / "roster.json", json.dumps(roster, indent=2) + "\n")

    starter_projects = build_starter_projects(profile, lanes, pack, categories, stages)
    write(
        pm_dir / "starter-projects.json",
        json.dumps(starter_projects, indent=2) + "\n",
    )

    census = build_census(profile, slug, tier_key)
    write(pm_dir / "census.json", json.dumps(census, indent=2) + "\n")

    write(
        pm_dir / "onboarding-checklist.md",
        onboarding_checklist(profile, slug, lanes),
    )

    # ---- Provisioning record ------------------------------------------------
    record = {
        "client_slug": slug,
        "business_name": business_name,
        "generated_from_profile": profile.get("_source_name", "profile"),
        "payment": {
            "payment_status": "awaiting_payment_link",
            "how_it_works": (
                "A secure payment link is sent through the existing sales "
                "and accounting path. Setup starts when the paid "
                "confirmation event (start_payment_received) is recorded, "
                "together with agreement_signed, per wiring contract "
                "section 3.3. No amounts are stored in this package."
            ),
            "stripe_integrated": False,
        },
        "repository": {
            "target_name": "upsurge-client-" + slug,
            "target_owner": "UpSurge GitHub organization",
            "created": False,
            "creation_path": (
                "The provisioning run attempts creation. Where repo "
                "creation is not permitted to the automation, creation "
                "becomes a certified team fulfillment step under the "
                "Install Fulfillment Training model, and this package is "
                "pushed the moment the repo exists. This record stays "
                "false until a creation is verified by read back."
            ),
        },
        "orchestrator_mapping": {
            "provision.create_client_layer": "repo/ tree in this package",
            "census.run_questions": "pm-tool/census.json rows",
            "census.resolve_rows": "pm-tool/census.json states",
            "seat.deliver_pack": "repo/team-pack/ delivery records",
            "go_live.create_first_project": "pm-tool/starter-projects.json",
        },
    }
    write(out / "provisioning-record.json", json.dumps(record, indent=2) + "\n")

    # ---- (c) Verification ---------------------------------------------------
    checks = run_checks(out, lanes, census, stages, categories)
    write(out / "verification-report.md", render_report(profile, slug, checks))
    return checks


def repo_readme(profile, slug, lanes_active):
    name = profile["business_name"]
    return f"""# {name}: AI Team Memory and Setup

Client slug: {slug}
Repository target: upsurge-client-{slug}, in UpSurge's GitHub organization

## What this repository is

This repository holds the working memory and setup for {name}'s installed
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

All work for {name} lives in the PM tool (Surge Command). Every lane
adds every project there, the client submits and watches work there, and
the Output Ledger the client reads is written from what completes
there. Nothing counts as done until it is recorded there and in the
memory work log.

## Lanes at install

{lanes_active}

## Hard rules for this repository

- Pointers only. No credential value is ever written here: no password,
  API key, token, or secret of any kind. Systems are reached through
  named connectors and vault entries.
- One truth per fact, every fact with a source, dates absolute.
- Client layer only. Nothing from another client, and nothing from the
  internal brain, is ever copied into this repository.
"""


def delivery_summary(profile, lanes):
    lines = [
        "# Team Pack Delivery Summary: " + profile["business_name"],
        "",
        "Team Pack version delivered: Pack v" + profile.get("pack_version", "1.0"),
        "",
        "Every active lane receives all ten components in working form, "
        "delivered from the master source held in the UpSurge service "
        "repo. The master source, its versioning history, the QA scoring "
        "rubrics, and the drill banks are never copied into this "
        "repository or into a seat.",
        "",
        "## Components delivered to every seat",
        "",
    ]
    for i, component in enumerate(PACK_COMPONENTS, 1):
        lines.append("{}. {}".format(i, component))
    lines += [
        "",
        "## Delivery records",
        "",
    ]
    for lane in lanes:
        lines.append(
            "- `lane-{}.md`: {} on {}, led by {}.".format(
                lane["house_lane"], lane["name"], lane["platform"], lane["leader"]
            )
        )
    lines += [
        "",
        "## The brain-write rule",
        "",
        "Work is not finished until it is recorded in the memory layer in "
        "this repository and in the PM tool. The Output Ledger counts "
        "only recorded work.",
        "",
    ]
    return "\n".join(lines)


def lane_delivery_record(profile, lane):
    lines = [
        "# Team Pack Delivery Record: {} ({})".format(lane["name"], profile["business_name"]),
        "",
        "| Field | Value |",
        "|---|---|",
        "| Lane | {} (house lane: {}) |".format(lane["name"], lane["house_lane"]),
        "| Platform filling the seat | {} |".format(lane["platform"]),
        "| Lane leader | {} |".format(lane["leader"]),
        "| Team Pack version | Pack v{} |".format(profile.get("pack_version", "1.0")),
        "| Delivery method | {} |".format(lane["delivery_method"]),
        "| How memory updates reach the seat | {} |".format(lane["memory_updates"]),
        "| Drill note | {} |".format(lane["drill_note"]),
        "",
        "## What this seat receives",
        "",
        "All ten Team Pack components in working form: roster and lane "
        "map, routing rules, the execution brief standard, house style, "
        "QA checklists, escalation rules, the claim protocol, the client "
        "memory pointer (the `memory/` tree in this repository), "
        "reporting templates, and the install and heartbeat data "
        "contract. Operational content only. The master source stays in "
        "the UpSurge service repo.",
        "",
        "## The drill this seat must pass",
        "",
        "The seat counts as seated only when its verification drill "
        "passes, scored on these fields:",
        "",
    ]
    for field in DRILL_FIELDS:
        lines.append("- `{}`".format(field))
    lines += [
        "",
        "## Standing rules for this seat",
        "",
        "- Save everything to the memory layer in this repository. Work "
        "that is not recorded does not count.",
        "- Add every project to the PM tool. The PM tool is home base "
        "for all lanes.",
        "- Work only inside this client's layer. Nothing from any other "
        "client, ever.",
        "- Escalate to the team lead, never directly around the front "
        "door.",
        "",
    ]
    return "\n".join(lines)


def positioning_and_rules(profile, pack):
    guard = "\n".join("- " + g for g in pack["guardrails"]) or "- Standard client approval and privacy rules apply."
    return f"""# Positioning and Rules in Working Form: {profile['business_name']}

The working summary every seat on this team operates from. The full
product documents live on the UpSurge side; this is the form the team
works from day to day.

## The platform is the driver

AI platforms are engines. This platform is the driver: one command
platform, one point of contact, one board, one memory, and one quality
standard route the work across every lane. The client talks to the
team lead, not to a pile of separate AI accounts.

## Best of all platforms

A lane is a role, not a vendor. Seats can be filled by Muse, Grok,
Claude, ChatGPT, Gemini, or another capable platform. More lanes mean
more of the client's AI capacity gets used, work routes to the engine
that fits the job, important work can be cross checked by another
lane, and a seat can be refilled by another platform without starting
over, because the Team Pack and this memory stay with the platform.

## The rules

- Connect what they have, install what they lack. Never rip and
  replace a working tool on day one. When a function is missing, the
  standard for that function is set up for the client (HighLevel for
  the customer system plus phones and messages).
- The PM tool is home base. Every lane adds every project there.
- Everything is saved to the memory layer. The Output Ledger counts
  only recorded work.
- Client data is the client's property and exportable at any time.
  The system itself is UpSurge IP, licensed while subscribed.
- Plain words with the client, always. One clear action at a time.

## Guardrails from this business's pack

{guard}
"""


def build_starter_projects(profile, lanes, pack, categories, stages):
    requests = pack["starter_requests"] or [
        "Sort these new requests and tell me what detail is missing from each one."
    ]
    projects = []
    per_lane = {}
    for idx, request in enumerate(requests):
        lane = lanes[idx % len(lanes)]
        order = per_lane.get(lane["house_lane"], 0)
        per_lane[lane["house_lane"]] = order + 1
        specialists = LANE_SPECIALIST_ORDER.get(lane["house_lane"], ["Maive"])
        specialist = specialists[order % len(specialists)]
        category = categories[idx % len(categories)] if categories else "General"
        title = request[0].upper() + request[1:] if request else request
        projects.append(
            {
                "id": "starter-{:02d}".format(idx + 1),
                "title": title,
                "lane": lane["house_lane"],
                "lane_name": lane["name"],
                "platform": lane["platform"],
                "specialist": specialist,
                "category": category,
                "stage": stages[0] if stages else "New",
                "first_step": (
                    "Open this project in the PM tool, confirm the approved "
                    "source material for the work with the champion, and "
                    "begin with the first item on the list."
                ),
                "definition_of_done": (
                    "The finished work is checked against the source "
                    "material, recorded in the PM tool and in the memory "
                    "work log, and the result is visible to the client in "
                    "the PM tool."
                ),
                "source": "Business Type Pack starter request, in the client's words",
            }
        )
    return {
        "rule": (
            "The PM tool (Surge Command) is home base: it is the single "
            "location where all lanes add all projects, where the client "
            "submits and watches work, and where completed work enters "
            "the Output Ledger. No lane works off board."
        ),
        "projects": projects,
    }


def build_census(profile, slug, tier_key):
    rows = []
    for row in profile.get("census", []):
        rows.append(
            {
                "function": row["function"],
                "tool_name": row["tool_name"],
                "state": row["state"],
                "owner": row["owner"],
                "note": row["note"],
            }
        )
    counted = sum(
        1 for r in rows if r["state"] in ("Connected", "Set up for them")
    )
    return {
        "client_slug": slug,
        "source": (
            "App Census (install-system/app-census.md). States are the "
            "four recorded decisions. A row reads Connected only after "
            "the orchestrator verification passes during onboarding; "
            "until then the state in this file is the setup target the "
            "census resolved to."
        ),
        "tier_included_app_count": TIER_APP_COUNTS.get(tier_key),
        "counted_toward_included": counted,
        "rows": rows,
    }


def onboarding_checklist(profile, slug, lanes):
    lane_lines = "\n".join(
        "- {} on {}: copy the setup words, paste them where the hub "
        "shows you, then the quick check runs by itself.".format(
            lane["name"], lane["platform"]
        )
        for lane in lanes
    )
    return f"""# Your Setup, Step by Step: {profile['business_name']}

We hold your hand through every step. Each step says what you do, what
happens by itself, and what our trained team does for you if a step
needs a hand. Nothing is left for you to figure out alone.

One thing to know first: **the PM tool is home base.** It is the one
place where your whole team works. Every lane adds every project
there, you send requests and watch progress there, and finished work
lands in your Output Ledger there. If you ever wonder where something
is, the answer is the PM tool.

| Step | You do this | Happens by itself | If a hand is needed |
|---|---|---|---|
| 1. Agreement | Read and sign the agreement we send you. One link, no account to create. | Your welcome message and your setup hub link arrive, and your install record is created. | Our team answers any question about the words before you sign. |
| 2. Payment | Open the secure payment link we send and pay the start payment. | The moment the paid confirmation lands, setup starts on its own. Nothing waits on a person. | Our team resends the link or helps with a payment question the same day. |
| 3. Your workspace and memory | Nothing. Watch it appear in your hub. | Your PM tool workspace is set up in your business's words, your memory folder is created in your team's repository (upsurge-client-{slug}), and your team page is prepared. | If creating the repository needs a person on our side, a certified member of our team does it the same day, and your setup keeps moving either way. |
| 4. Your apps | Answer the short list of questions about the tools you use, then tap Connect next to each one and sign in on that tool's own page. | Each tool runs a quick check by itself. Only a tool that passes counts as connected. Anything you do not have, we set up the standard for. | A certified team member fulfills any connection that will not go through, and tells you the one thing left to do in plain words. |
| 5. Your team seats | For each lane below, follow the hub's three steps: copy, paste, done. | A quick check runs on each seat by itself, and the seat lights up when it passes. | Our team seats the lane with you, or for you, if the check does not pass after the guided retries. |
| 6. Your business facts | Read the draft facts we prepared from your website and tools, tap Confirm on each right one, and fix any that are off. | Your answers are saved into your memory, and your starter projects appear on your board. | Our team prepares the drafts and chases the few answers only you can give, one question at a time. |
| 7. Go live | Send your first request from the PM tool. | The final checks run by themselves, your team page goes live, and your team starts work the same day. | Our team completes any leftover setup step behind the scenes and reports it in your owner report. |

## Your lanes in step 5

{lane_lines}

## After go live

- Send every request in the PM tool, in your own words. Your team
  lead sorts it, the right lane picks it up, and you watch it move.
- Your monthly owner report shows finished work from the Output
  Ledger, what your team learned, and any recommended additions our
  research team has tested for you.
- Stuck at any point, at any step, forever: message your team lead
  from the PM tool. A person answers. That is the design, not a
  favor.
"""


def run_checks(out, lanes, census, stages, categories):
    checks = []

    required = [
        "repo/README.md",
        "repo/memory/README.md",
        "repo/memory/client-profile.md",
        "repo/memory/brand-kit.md",
        "repo/memory/systems-map.md",
        "repo/memory/people.md",
        "repo/memory/standing-rules.md",
        "repo/memory/work-log.md",
        "repo/memory/open-flags.md",
        "repo/memory/access-manifest.md",
        "repo/memory/seeding-protocol.md",
        "repo/memory/team-pack-delivery-manifest.md",
        "repo/team-pack/delivery-summary.md",
        "repo/positioning-and-rules.md",
        "pm-tool/workspace-config.json",
        "pm-tool/board.json",
        "pm-tool/roster.json",
        "pm-tool/starter-projects.json",
        "pm-tool/census.json",
        "pm-tool/onboarding-checklist.md",
        "provisioning-record.json",
    ]
    for lane in lanes:
        required.append("repo/team-pack/lane-{}.md".format(lane["house_lane"]))
    missing = [rel for rel in required if not (out / rel).exists()]
    checks.append(
        (
            "Required files present",
            not missing,
            "All {} required files exist.".format(len(required))
            if not missing
            else "Missing: " + ", ".join(missing),
        )
    )

    starter = json.loads((out / "pm-tool" / "starter-projects.json").read_text())
    covered = {p["lane"] for p in starter["projects"]}
    needed = {lane["house_lane"] for lane in lanes}
    checks.append(
        (
            "Starter projects cover every lane",
            needed.issubset(covered) and len(starter["projects"]) >= len(lanes),
            "{} starter projects across lanes: {}.".format(
                len(starter["projects"]), ", ".join(sorted(covered))
            ),
        )
    )
    fields_ok = all(
        p.get("title") and p.get("specialist") and p.get("first_step")
        and p.get("definition_of_done")
        for p in starter["projects"]
    )
    checks.append(
        (
            "Every starter project has title, specialist, first step, and definition of done",
            fields_ok,
            "Checked {} projects.".format(len(starter["projects"])),
        )
    )

    bad_states = [
        r["function"] for r in census["rows"] if r["state"] not in CENSUS_STATES
    ]
    checks.append(
        (
            "Census rows all resolved to one of the four states",
            not bad_states and len(census["rows"]) > 0,
            "{} rows, all in a recorded state.".format(len(census["rows"]))
            if not bad_states
            else "Unresolved or invalid: " + ", ".join(bad_states),
        )
    )

    texts = {}
    for path in sorted(out.rglob("*")):
        if path.is_file() and path.name != "verification-report.md":
            texts[path.relative_to(out).as_posix()] = path.read_text(
                encoding="utf-8", errors="replace"
            )
    leftovers = [rel for rel, body in texts.items() if "{{" in body or "}}" in body]
    checks.append(
        (
            "No template placeholder left unfilled",
            not leftovers,
            "No template placeholder tokens remain in any generated file. Named "
            "exceptions: none. Fields whose values only exist later "
            "(workspace links, the export test record) carry plain status "
            "text in the client's words instead of a placeholder.",
        )
        if not leftovers
        else "Placeholders remain in: " + ", ".join(leftovers),
    )

    hits = []
    for rel, body in texts.items():
        for pattern in SECRET_PATTERNS:
            if re.search(pattern, body):
                hits.append(rel)
                break
    checks.append(
        (
            "No credential values anywhere",
            not hits,
            "Scanned {} files against {} credential patterns. None found. "
            "The package holds pointers only.".format(
                len(texts), len(SECRET_PATTERNS)
            )
            if not hits
            else "Possible credential values in: " + ", ".join(sorted(set(hits))),
        )
    )

    json_ok = True
    json_count = 0
    for path in sorted(out.rglob("*.json")):
        json_count += 1
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            json_ok = False
    checks.append(
        (
            "Every JSON file parses",
            json_ok,
            "{} JSON files parsed.".format(json_count),
        )
    )

    checks.append(
        (
            "Board shape follows the pack format checks",
            5 <= len(stages) <= 7 and 6 <= len(categories) <= 10,
            "{} stages (pack format allows 5 to 7), {} categories "
            "(allows 6 to 10).".format(len(stages), len(categories)),
        )
    )

    record = json.loads((out / "provisioning-record.json").read_text())
    honest = (
        record["repository"]["created"] is False
        and record["payment"]["payment_status"] == "awaiting_payment_link"
        and record["payment"]["stripe_integrated"] is False
    )
    checks.append(
        (
            "Provisioning record is honest about payment and repo creation",
            honest,
            "payment_status is awaiting_payment_link, stripe_integrated "
            "is false, and repository.created is false. Nothing is "
            "claimed that has not happened.",
        )
    )
    return checks


def render_report(profile, slug, checks):
    passed = sum(1 for _, ok, _ in checks if ok)
    lines = [
        "# Verification Report: " + profile["business_name"],
        "",
        "Generated by provisioning/client_setup.py from the client "
        "profile for slug `{}`.".format(slug),
        "",
        "Result: {} of {} checks passed.".format(passed, len(checks)),
        "",
    ]
    for name, ok, detail in checks:
        lines.append(
            "- [{}] **{}**: {}".format("x" if ok else " ", name, detail)
        )
    lines += [
        "",
        "A failed check means the package is not ready to push or to "
        "build a workspace from. Fix the profile or the generator and "
        "run it again; the generator is safe to re-run over the same "
        "output folder.",
        "",
    ]
    return "\n".join(lines)


def main(argv):
    if len(argv) != 3:
        print(__doc__)
        return 2
    profile_path = Path(argv[1])
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    profile["_source_name"] = profile_path.name
    checks = build_package(profile, argv[2])
    failed = [name for name, ok, _ in checks if not ok]
    print(
        "Package written to {} : {} of {} checks passed.".format(
            argv[2], len(checks) - len(failed), len(checks)
        )
    )
    if failed:
        print("FAILED: " + ", ".join(failed))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
