# Team Pack Delivery Manifest

The exact Team Pack components an install receives, where each one lands for each lane's seat, and how the Pack reaches and later updates a live install. Component definitions are in `team-pack/team-pack-and-roster.md` section 1.1. This manifest is the delivery record for that definition.

## Delivery rules

- Every component ships to every active lane's seat. Any lane must be able to pick up any work under the claim protocol, so no seat runs a partial Pack.
- The delegator of record is Maive (Muse lane). Lane emphasis below marks which seat works from a component daily. Emphasis is not exclusivity.
- Nothing in this manifest contains client facts. The Pack is identical across installs except for the version stamp and the client memory it points to.
- The Claude lane leader for the install is named in the install record at provisioning. Maive leads the Muse lane. Marcus leads the Grok lane.

## Components and landing spots

| # | Component | Form delivered | Muse seat (Maive) | Claude seat | Grok seat (Marcus) |
|---|---|---|---|---|---|
| 1 | Roster and lane map | Roster file in the seat bootstrap pack | Full roster. Maive assigns work from it at intake | Full roster. Consulted on handoffs | Full roster. Consulted on handoffs |
| 2 | Routing rules by task type | Routing table in the seat bootstrap pack | Held by Maive as routing authority at intake | Held in full. Governs what the lane accepts and supports | Held in full. Governs what the lane accepts and supports |
| 3 | Execution brief standard | Brief standard file plus the Desk brief field contract | Maive writes or approves briefs at intake | Lane works only from complete briefs | Lane works only from complete briefs |
| 4 | House style | Style file in the seat bootstrap pack | Applies to all output and to client facing review | Applies to all drafting | Applies to all drafting |
| 5 | QA checklists by deliverable type | Checklist set in the seat bootstrap pack | Dex gate runs from these on every deliverable | Builder self check runs from these before handoff | Builder self check runs from these before handoff |
| 6 | Escalation rules | Escalation file in the seat bootstrap pack | Maive is the escalation point and formats every escalation | Lane escalates to Maive, never directly to the client | Lane escalates to Maive, never directly to the client |
| 7 | Claim protocol | Protocol file plus Desk board discipline | Maive watches claims and the stale claim rule | Lane claims on the board before starting | Lane claims on the board before starting |
| 8 | Client memory template pointer | Pointer to this template pack (`install-templates/client-memory/`) | Orchestrator writes the filled Client layer from these templates at provisioning | Lane reads the filled client memory for the install it serves | Lane reads the filled client memory for the install it serves |
| 9 | Reporting templates | Template set in the seat bootstrap pack | Maive issues exception reports and completion notes from these | Lane supplies completions in template form | Lane supplies completions in template form |
| 10 | Install and heartbeat data contract | Schema reference and data rules file | Governs Desk writes and the heartbeat page for the install | Governs any Desk writes the lane makes | Governs any Desk writes the lane makes |

## Version stamp

- At provisioning, the orchestrator writes the delivered Pack version into `client-profile.md` in the Client layer, in the Team Pack version field of the engagement facts table.
- Format: Pack vMAJOR.MINOR, per Team Pack section 1.6. The first delivery under this manifest is Pack v1.0.
- The stamp is the single record of which Pack the install is running. If the stamp and a seat's bootstrap pack disagree, the seat is stale and is refreshed before it takes new work.

## How a Pack update reaches a live install

Per Team Pack section 1.6, in delivery terms:

1. Lena drafts the change in the master Pack with a changelog entry. Dex reviews for conflicts. Maive approves and sets the new version.
2. The update is pushed to every active install's seat bootstrap packs: roster file, routing rules, brief standard, checklists, and templates are replaced at the new version. All three lanes receive it.
3. The Client layer is never touched by a Pack push. No client memory file is opened, read for content, or modified by the update process. The push writes Craft layer files only.
4. The Team Pack version field in the install's `client-profile.md` is updated to the new stamp with the push date. This is the one Client layer field a Pack push may write, because it is the install record of the Craft layer's version, not a client fact.
5. In flight projects finish under the Pack version they started with. A compliance or safety fix applies immediately to all work and is noted in each affected project.
6. Superseded Pack versions are archived, never deleted, so the Pack any install was stamped with can be reconstructed exactly.
