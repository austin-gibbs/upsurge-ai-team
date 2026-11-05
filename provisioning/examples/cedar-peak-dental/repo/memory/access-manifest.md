# Access Manifest: Go Live Checklist

What the client of Cedar Peak Dental holds in their hands at go live. Every item is a condition of the Go live stage: the install does not go live until each item is checked and evidenced. The orchestrator verifies what it can automatically; the lane lead verifies the rest against the live surfaces, not against a plan document.

## 1. PM app workspace (Surge Command Desk)

- [ ] Workspace exists for cedar-peak-dental and the client can sign in to it.
- [ ] Board is live with the install project visible and the project's status accurate.
- [ ] Team page (heartbeat) is live. Every number on it derives from real Desk records. No decorative metrics.
- [ ] Output ledger is live and shows only completed work with client summaries. An empty ledger at go live is correct if nothing has completed yet; a padded one is a defect.
- [ ] Client sees client summaries only. Internal notes, briefs, and blockers are not visible on any client surface. Verified by viewing the workspace as the client.

## 2. Seats on each active lane, verified by drill

For each lane in Operations Lane on ChatGPT, Strategy Lane on Claude, Speed Lane on Grok:

- [ ] Muse seat (Maive): seated with the current Team Pack version, matching the stamp in `client-profile.md`.
- [ ] Claude seat: seated with the current Team Pack version, lane leader for the install named in the install record.
- [ ] Grok seat (Marcus): seated with the current Team Pack version.
- [ ] Drill passed per active lane: the lane proves live that it can read the roster and lane map, state the routing rule for a sample task, and open this install's client memory. A seat that cannot pass the drill is not seated, and go live waits.
- [ ] Load rule noted: if a lane is unavailable at go live, its queue reroutes per the Pack routing rules and the override is recorded in the install record with its lift condition.

## 3. Intake channel live

- [ ] The intake mode in `client-profile.md` (PM tool (Surge Command) submission) is the mode actually wired: Desk submission, the client's PM system wired to the Desk, or direct submission to Maive.
- [ ] A test submission has traveled the full path and normalized into a Desk project with a complete execution brief.
- [ ] The client has submitted or witnessed the test submission, so their first real request is not their first time using the channel.
- [ ] Notification channel (Email to the champion, plus the PM tool) is live and has carried one real notification.

## 4. Digest and report rhythm scheduled

- [ ] Daily digest scheduled on business days at the client's local time, carrying completions, open blockers, and upcoming milestones.
- [ ] Weekly review scheduled: completions, flags past their check date, and memory drafts still unconfirmed.
- [ ] Monthly owner report scheduled under the oversight model.
- [ ] Schedules are verified as created in the scheduling system, not just planned.

## 5. Memory export path proven

- [ ] One full export of the Client layer has been generated during install QA: every file in this memory, in a portable format, with no Craft layer content included.
- [ ] The export was delivered to the client or placed where the client can retrieve it, and the delivery is recorded here: date Runs during install QA, before go live, location pointer Recorded in access-manifest.md when the export test runs.
- [ ] The client has been shown how to request an export at any time. Their memory is theirs; the export path is the proof.
- [ ] The export contains pointers only, no credential values, matching the source files.

## 6. Memory state at go live

- [ ] Seeded facts are in place with sources. Unconfirmed drafts are listed in the go live summary given to the client.
- [ ] Approved claims list state is stated plainly in the go live summary, including if it is still empty.
- [ ] `open-flags.md` holds every unresolved item from the install, each with an owner and a next check date.
- [ ] `systems-map.md` shows every in scope system at Connected or Verified, or carries the reason it is not.

## Sign off

Go live is declared by the lane lead when every box above is checked. The declaration, its date, and any box waived with Austin's written acceptance are recorded in `work-log.md` as the install's first entry.
