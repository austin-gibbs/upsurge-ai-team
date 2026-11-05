# Team Pack Delivery Record: Speed Lane (Cedar Peak Dental)

| Field | Value |
|---|---|
| Lane | Speed Lane (house lane: grok) |
| Platform filling the seat | Grok |
| Lane leader | Marcus |
| Team Pack version | Pack v1.0 |
| Delivery method | System instructions in the workspace, memory files attached per workspace setup |
| How memory updates reach the seat | Memory files re-issued on each release; version stamp checked at drill time |
| Drill note | Standard drill; format check watches for truncated instruction loads |

## What this seat receives

All ten Team Pack components in working form: roster and lane map, routing rules, the execution brief standard, house style, QA checklists, escalation rules, the claim protocol, the client memory pointer (the `memory/` tree in this repository), reporting templates, and the install and heartbeat data contract. Operational content only. The master source stays in the UpSurge service repo.

## The drill this seat must pass

The seat counts as seated only when its verification drill passes, scored on these fields:

- `drill.facts_check`
- `drill.format_check`
- `drill.isolation_check`
- `drill.language_check`
- `drill.status`
- `drill.attempts`
- `drill.completed_at`

## Standing rules for this seat

- Save everything to the memory layer in this repository. Work that is not recorded does not count.
- Add every project to the PM tool. The PM tool is home base for all lanes.
- Work only inside this client's layer. Nothing from any other client, ever.
- Escalate to the team lead, never directly around the front door.
