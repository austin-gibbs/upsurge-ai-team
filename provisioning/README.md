# Client Provisioning: Website to Paid to Fully Set Up

How a new client flows from the website to a fully set up AI Team, and
how the generator in this folder powers the middle of that flow.
Internal document. Client facing words live in the onboarding hub and
in the generated `onboarding-checklist.md`, not here.

Companion documents: install-system/wiring-contract.md (the contract
this folder implements), install-system/app-census.md,
install-templates/client-memory/, product/platform-policy.md,
product/ip-and-stickiness.md, product/positioning-core.md,
orchestrator/README.md.

## The flow

| Step | What happens | Who acts |
|---|---|---|
| 1. Website and fit call | The prospect reads the homepage, books a fit call, and applies. Events and fields per wiring contract sections 1 and 2a | Client, then the sales automation |
| 2. Agreement | The agreement is generated from the proposal record and signed. This is T0. `install_id` is minted once, here | Client signs; the signature tool records it |
| 3. Payment (placeholder, deliberate) | Invoice 1 issues. A secure payment link is sent through the existing sales and accounting path, and the client pays through it. `payment_status` starts at `awaiting_payment_link` in every generated record and moves only on the accounting projection (`issued`, `paid`, `attention`) | Client pays; accounting is the only truth for money |
| 4. Provisioning trigger | `agreement_signed` plus `start_payment_received`, in either order, fire the trigger (wiring contract section 3.3, idempotency key `provision-trigger:{agreement_envelope_id}`) | The endpoint service, no human in the loop |
| 5. Setup package generated | The orchestrator's provision stage runs this generator against the client profile assembled from the application and agreement. Output: the repo tree, the PM tool setup files, and the verification report | The orchestrator (`provision.create_client_layer` and the manifest steps) |
| 6. Client repository created | See the repo creation section below. Honest status at every step; nothing is claimed before a read back proves it | Automation where permitted, else a certified team member |
| 7. PM tool workspace built | The Desk workspace is created from `pm-tool/`: workspace config, board in the client's words, roster, starter projects. The team page migration runs at template build, per the orchestrator README | The orchestrator Desk adapter |
| 8. Onboarding in the hub | The client walks the generated `onboarding-checklist.md` steps in the hub: census and connects (verified, never click counted), seat self-install with the drill, fact confirmation, go live checklist | Client, with automated recovery and the fulfillment path behind the curtain |
| 9. Live | The final sweep passes (including `census_completeness`), `install_live` fires invoice 2 and the standing loops, and the PM tool becomes the client's daily home base | The orchestrator |

## The payment step, stated plainly

Payment is a deliberate placeholder in this build. Stripe is
intentionally NOT integrated yet. There is no Stripe code, key, or
checkout session anywhere in this folder, and none may be added
without Austin's direction.

What exists instead:

- Every generated record carries `payment_status:
  awaiting_payment_link` at generation time.
- A secure payment link is sent to the client through the existing
  sales and accounting path (the same path invoice 1 already travels).
- Setup starts on the paid confirmation: the accounting event
  `start_payment_received`, combined with `agreement_signed`, fires
  the provisioning trigger in step 4 above.
- Amounts live only in the agreement and the accounting system, per
  wiring contract section 0. This package stores status words only,
  never an amount.

When Stripe (or another processor) is integrated later, it replaces
the link sending in this step only. The trigger, the generator, and
everything downstream do not change.

## The GitHub repo creation step, stated honestly

Each client gets their own repository:

- Target name: `upsurge-client-<slug>`.
- Target owner: UpSurge's GitHub organization. Per
  product/ip-and-stickiness.md, the repository is UpSurge owned and
  operated; the client receives application level access through the
  PM tool, never repo access. The client's data in it remains the
  client's property and fully exportable.
- Contents: exactly the `repo/` tree this generator produces, rooted
  in the UpSurgeAITeam pattern in sanitized form: the client memory
  layer from the templates, Team Pack delivery records in working
  form, and positioning and rules summaries. No internal brain
  content, no master source, no other client's data.

How creation works:

1. The provisioning run attempts to create the repository through
   the GitHub integration.
2. Where repo creation is not permitted to the automation, creation
   becomes a certified team fulfillment step under the Install
   Fulfillment Training model: a team member certified on that step
   creates the repo in the org, and the generated package is pushed
   the moment the repo exists. The package is complete and verified
   before the repo exists, so the fulfillment step is minutes of
   work, not a project.
3. The provisioning record tells the truth throughout:
   `repository.created` stays `false`, and the workspace config
   status stays `package_ready_repo_creation_pending`, until a
   creation is verified by read back. No step, report, or client
   surface may claim a repo was created when it was not. (Known
   state at this build: the current GitHub integration cannot create
   repositories, returning 403, verified 2026-11-04. The fulfillment
   path in step 2 is therefore the expected path today.)

## The generator

```bash
python3 provisioning/client_setup.py PROFILE_JSON OUTPUT_DIR
```

- Input: one client profile JSON (see the field guide below).
- Output: the package described in the script header, plus
  `verification-report.md` written by the script's own checks.
- The script is Python standard library only, makes no network
  calls, and reads or writes no credential values.
- It is safe to re-run over the same output folder. The
  orchestrator's check before create discipline applies one level
  up: existing objects are found by natural key and not duplicated.

What the checks verify: every required file exists; starter projects
cover every lane in the profile, each with title, specialist, first
step, and definition of done; every census row holds one of the four
states from app-census.md; no `{{placeholder}}` token survives in any
generated file (fields whose values only exist later carry plain
status text instead); no credential value pattern appears anywhere;
every JSON file parses; the board shape passes the pack format
writing checks (5 to 7 stages, 6 to 10 categories); and the
provisioning record is honest about payment and repo creation.

## Profile field guide

`profile-template.json` in this folder is a complete fictional
example (Cedar Peak Dental) and doubles as the template. Fields:

| Field | Meaning |
|---|---|
| `business_name` | The public name the client uses. Fills most `{{business_name}}` slots |
| `legal_business_name` | The legal name from the agreement |
| `slug` | The client slug. Optional; derived from the business name when absent |
| `industry` | Plain words for what the business is |
| `business_type_pack` | The pack file id in install-templates/business-types/ (for example `dental-practice`). Unknown or absent falls back to `general-services` |
| `business_type_display` | The words the client sees for their kind of business |
| `custom_shape` | Optional client words that beat the pack: `board_stages`, `categories`, `item_word`, `customer_word` |
| `website_url` | The client's public website |
| `timezone` | The client's timezone, IANA name |
| `tier` | `launch`, `growth`, `full`, or `pilot`. Drives the census included app count (5, 10, 18; pilot reads its agreement) |
| `tier_label` | The tier name the client sees |
| `pack_version` | The Team Pack version delivered, for example `1.0` |
| `install_date` | Absolute date the install record is created |
| `signer_name`, `champion_name`, `owner_name` | Client side people, copied character for character from the agreement |
| `intake_mode` | How requests reach the team. Default: PM tool submission |
| `notification_channel` | Where the client hears from the team |
| `lanes` | One entry per active lane: `house_lane` (`muse`, `claude`, or `grok`), `platform` (the seat filling it: Muse, Grok, Claude, ChatGPT, Gemini, or another platform), optional `name` and `leader`. Lanes are roles; platforms are interchangeable seats |
| `systems` | The platform names for the systems map: `crm_name`, `email_platform`, `calendar_platform`, `files_platform`, `phone_platform`, `voice_platform`, `billing_platform`, `ads_platform`, `web_platform`. The PM tool is always Surge Command |
| `census` | The resolved census rows: `function` (a record value from app-census.md section 1), `tool_name`, `state` (exactly one of Connected, Set up for them, Coming next, Not needed), `owner` (`client` or `upsurge`), `note` |

## The PM tool is home base

Every artifact in this folder points at one fact the client must
never have to wonder about: the PM tool (Surge Command) is the single
location where all lanes add all projects, where the client submits
and watches work, and where completed work enters the Output Ledger.
The generated repo README says it, every lane delivery record says
it, `starter-projects.json` carries it as its rule, and the
onboarding checklist teaches it in step order. The generated board,
roster, and starter projects are placed there at provisioning, so
the client's first sign in already shows their business's words,
their team, and real starter work from every lane.

## The example

`examples/cedar-peak-dental/` is the generator run over
`profile-template.json`: a fictional dental practice on the Growth
tier whose three lanes run on ChatGPT, Claude, and Grok, proving the
platform mix works in one package. Its `verification-report.md` is
the run's own report. The example is a demonstration artifact, kept
compact; it is not a client record.
