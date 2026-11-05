// The one shared map from internal Desk statuses to client facing labels
// (spec section 2.5). Raw Desk status strings must never render on the page.
import type { ClientStatusLabel, DeskStatus } from '../types';

export const CLIENT_STATUS_LABELS: Record<DeskStatus, ClientStatusLabel> = {
  New: 'Received',
  'In Progress': 'In progress',
  'Waiting on Austin': 'Waiting on UpSurge',
  'Waiting on Client': 'Waiting on you',
  Blocked: 'Needs attention',
  Done: 'Completed',
};

/** Display order for the board summary status counts row. */
export const STATUS_DISPLAY_ORDER: DeskStatus[] = [
  'New',
  'In Progress',
  'Waiting on Austin',
  'Waiting on Client',
  'Blocked',
  'Done',
];
