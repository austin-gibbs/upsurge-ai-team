# Systems Map: {{business_name}}

One row per connected system. This file is the record of what the team can reach for this client, and how.

## Hard rule: pointers only

The credential pointer column holds a connector name and a vault entry name, nothing else. It must never hold a password, API key, token, or any credential value. If a value is ever found in this file, it is removed the moment it is spotted, the credential is treated as exposed and rotated by its owner, and the incident is recorded in `open-flags.md`.

## Connection states

- `Not connected`: Named as in scope, no connection attempted yet.
- `Connecting`: Connection in progress or awaiting the client's sign in step.
- `Connected`: Connection established.
- `Verified`: Connection proven by a live read or action in the system. Only Verified systems are relied on for delivery.

## Systems

| System | Purpose for {{business_name}} | System of record for | State | Connected date | Credential pointer (never a value) |
|---|---|---|---|---|---|
| CRM: {{crm_name}} | | | Not connected | | Connector: / Vault entry: |
| Email: {{email_platform}} | | | Not connected | | Connector: / Vault entry: |
| Calendar: {{calendar_platform}} | | | Not connected | | Connector: / Vault entry: |
| File storage: {{files_platform}} | | | Not connected | | Connector: / Vault entry: |
| Phone and messaging: {{phone_platform}} | | | Not connected | | Connector: / Vault entry: |
| Voice agents: {{voice_platform}} | | | Not connected | | Connector: / Vault entry: |
| Project management: {{pm_platform}} | | | Not connected | | Connector: / Vault entry: |
| Billing and accounting: {{billing_platform}} | | | Not connected | | Connector: / Vault entry: |
| Ads: {{ads_platform}} | | | Not connected | | Connector: / Vault entry: |
| Website and hosting: {{web_platform}} | | | Not connected | | Connector: / Vault entry: |

Rows are added as systems connect during the install and removed from scope only by a client instruction recorded in `standing-rules.md`. A system the client uses that the team cannot connect is still listed, with state `Not connected` and the reason in the purpose column, so nobody assumes access that does not exist.

## System of record summary

| Data type | System of record |
|---|---|
| Contacts and pipeline | |
| Calendar and bookings | |
| Files and documents | |
| Billing state | |
| Project tracking | Surge Command Desk (the PM app) |

## Change notes

Versioned record of state and pointer changes. Newest first. Format: date, system, old state or pointer, new state or pointer, source, changed by.

- (none yet)
