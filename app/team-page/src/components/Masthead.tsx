// Masthead (spec 1.1): logo or wordmark, title, live clock in the
// workspace timezone, and the connection indicator. The connection pulse
// is the only looping animation on the page, and it runs only while the
// realtime channel is subscribed.
import { useEffect, useState } from 'react';
import type { ConnectionState, WorkspaceConfig } from '../types';

interface MastheadProps {
  config: WorkspaceConfig;
  connection: ConnectionState;
}

function useClock(timeZone: string): { time: string; tzAbbrev: string } {
  const [now, setNow] = useState(() => new Date());
  useEffect(() => {
    const id = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(id);
  }, []);
  const parts = new Intl.DateTimeFormat('en-US', {
    timeZone,
    hour: 'numeric',
    minute: '2-digit',
    second: '2-digit',
    hour12: true,
    timeZoneName: 'short',
  }).formatToParts(now);
  const get = (type: string) =>
    parts.find((p) => p.type === type)?.value ?? '';
  return {
    time: `${get('hour')}:${get('minute')}:${get('second')} ${get('dayPeriod')}`,
    tzAbbrev: get('timeZoneName'),
  };
}

export function Masthead({ config, connection }: MastheadProps) {
  const { time, tzAbbrev } = useClock(config.timezone);
  const live = connection === 'live';
  const brand = config.brand_color ?? undefined;

  return (
    <header className="w-full">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div className="flex min-w-0 items-center gap-4">
          {config.logo_url ? (
            <img
              src={config.logo_url}
              alt={config.client_name}
              className="h-12 w-auto max-w-[180px] object-contain"
            />
          ) : (
            <span
              className="text-2xl font-bold tracking-tight text-slate-900"
              style={brand ? { color: brand } : undefined}
            >
              {config.client_name}
            </span>
          )}
          <div className="min-w-0">
            <h1 className="truncate text-xl font-semibold text-slate-900 sm:text-2xl">
              {config.client_name} AI Team
            </h1>
            <p className="text-sm text-slate-500">Your team, live</p>
          </div>
        </div>

        <div className="flex items-center gap-5">
          <div className="text-right">
            <div className="font-mono text-lg leading-none text-slate-900 tabular-nums">
              {time}
            </div>
            <div className="mt-1 text-xs text-slate-500">{tzAbbrev}</div>
          </div>
          <div className="flex items-center gap-2" role="status">
            <span
              className={
                live
                  ? 'h-2.5 w-2.5 rounded-full bg-emerald-500 animate-pulse motion-reduce:animate-none'
                  : 'h-2.5 w-2.5 rounded-full bg-amber-500'
              }
            />
            <span
              className={
                live
                  ? 'text-sm font-medium text-emerald-700'
                  : 'text-sm font-medium text-amber-700'
              }
            >
              {live ? 'Live' : 'Reconnecting'}
            </span>
          </div>
        </div>
      </div>
      <div
        className="mt-4 h-0.5 w-full bg-slate-200"
        style={brand ? { backgroundColor: brand } : undefined}
      />
    </header>
  );
}
