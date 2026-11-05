// Lane presentation metadata (spec section 1.3).
// Column order is Muse, Claude, Grok: Maive's lane first, because Maive is
// the client's front door and delegator.
import type { Lane } from '../types';

export interface LaneMeta {
  lane: Lane;
  teamName: string;
  tagline: string;
  /** Avatar circle background. */
  avatarClass: string;
  /** Filled status pill for Working now. */
  pillClass: string;
  /** Soft ring shown on a card while the member is Working now. */
  ringClass: string;
  /** Lane rollup chip. */
  chipClass: string;
  /** One time event highlight tint. */
  highlightClass: string;
}

export const LANE_ORDER: Lane[] = ['muse', 'claude', 'grok'];

export const LANE_META: Record<Lane, LaneMeta> = {
  muse: {
    lane: 'muse',
    teamName: 'Muse Team',
    tagline: 'Connected apps, memory, and always on operations',
    avatarClass: 'bg-teal-600 text-white',
    pillClass: 'bg-teal-600 text-white',
    ringClass: 'ring-2 ring-teal-500/50',
    chipClass: 'bg-teal-50 text-teal-800 ring-1 ring-teal-200',
    highlightClass: 'bg-teal-50',
  },
  claude: {
    lane: 'claude',
    teamName: 'Claude Team',
    tagline: 'Deep reasoning, documents, and careful builds',
    avatarClass: 'bg-[#c2613f] text-white',
    pillClass: 'bg-[#c2613f] text-white',
    ringClass: 'ring-2 ring-[#c2613f]/50',
    chipClass: 'bg-[#fbf0ea] text-[#8a4023] ring-1 ring-[#e8c4b2]',
    highlightClass: 'bg-[#fbf0ea]',
  },
  grok: {
    lane: 'grok',
    teamName: 'Grok Team',
    tagline: 'Speed, volume, and live signal',
    avatarClass: 'bg-slate-600 text-white',
    pillClass: 'bg-slate-600 text-white',
    ringClass: 'ring-2 ring-slate-500/50',
    chipClass: 'bg-slate-100 text-slate-700 ring-1 ring-slate-300',
    highlightClass: 'bg-slate-100',
  },
};
