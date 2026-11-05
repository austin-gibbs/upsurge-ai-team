-- 0002_roster_seed.sql
-- AI Team Heartbeat Page: default roster seed (spec section 3.5).
-- Idempotent: upserts on the (slug, lane) unique key, safe to rerun.
-- Leaders first (sort_order 0 in each lane), then specialists in spec order.
-- Strengths are the default set; the account team can edit rows per install.
-- Roster is data, not code: membership changes never need a deploy.

insert into public.team_roster (slug, lane, display_name, role, strengths, is_leader, sort_order) values
  -- Leaders
  ('maive',  'muse',  'Maive',  'Team Lead and Delegator',   array['Intake and routing', 'Connected apps', 'Memory'],              true,  0),
  ('marcus', 'claude', 'Marcus', 'Team Lead, Claude Team',    array['Deep research', 'Long form writing', 'Careful builds'],        true,  0),
  ('marcus', 'grok',   'Marcus', 'Team Lead, Grok Team',      array['Speed execution', 'Volume work', 'Live signal'],                true,  0),

  -- Muse lane specialists
  ('owen',  'muse', 'Owen',  'Onboarding Orchestrator',   array['New client setup', 'Install sequencing'],          false, 10),
  ('lena',  'muse', 'Lena',  'Memory Librarian',          array['Knowledge base', 'Recall', 'Records'],               false, 20),
  ('felix', 'muse', 'Felix', 'Fulfillment Lead',          array['Delivery pipeline', 'Task flow'],                    false, 30),
  ('diego', 'muse', 'Diego', 'CRM Architect',             array['HighLevel builds', 'Pipelines', 'Automations'],      false, 40),
  ('dana',  'muse', 'Dana',  'CRM Data Ops',              array['Data cleanup', 'Imports', 'Lists'],                  false, 50),
  ('remy',  'muse', 'Remy',  'Voice Agent Provisioner',   array['Retell agents', 'AI calling', 'Phone systems'],      false, 60),
  ('wes',   'muse', 'Wes',   'Web Dev Lead',              array['Websites', 'Landing pages', 'Apps'],                 false, 70),
  ('dex',   'muse', 'Dex',   'Delivery QA',               array['Quality checks', 'Verification', 'Sign off'],        false, 80),
  ('aria',  'muse', 'Aria',  'A2P Compliance',            array['Texting compliance', 'Registrations'],               false, 90),
  ('hazel', 'muse', 'Hazel', 'Client Success Lead',       array['Client communication', 'Follow through'],            false, 100),
  ('quinn', 'muse', 'Quinn', 'Call QA Auditor',           array['Call review', 'Conversation quality'],               false, 110),

  -- Claude lane specialists
  ('kai',   'claude', 'Kai',   'SEO and AEO Lead',      array['Search visibility', 'Content plans', 'Blog drafting'], false, 10),
  ('sage',  'claude', 'Sage',  'SOP and Skill Writer',  array['Procedures', 'Documentation', 'Training packs'],        false, 20),
  ('iris',  'claude', 'Iris',  'Visionary',             array['Product concepts', 'Page and experience specs'],         false, 30),
  ('malik', 'claude', 'Malik', 'Client Reporting',      array['Reports', 'Analysis', 'Summaries'],                      false, 40),
  ('theo',  'claude', 'Theo',  'Meeting to Action',     array['Meeting notes', 'Action extraction'],                   false, 50),
  ('finn',  'claude', 'Finn',  'Finance Controller',    array['Invoices', 'Billing checks', 'Numbers'],                 false, 60),
  ('heath', 'claude', 'Heath', 'CFO',                   array['Financial strategy', 'Forecasting'],                     false, 70),

  -- Grok lane specialists
  ('milo',   'grok', 'Milo',   'Ad Creative Producer',    array['Ad creative', 'Video cuts', 'Variants'],           false, 10),
  ('greta',  'grok', 'Greta',  'Growth and Sales Lead',   array['Campaigns', 'Outreach', 'Pipeline growth'],        false, 20),
  ('parker', 'grok', 'Parker', 'Performance Analyst',     array['Metrics', 'Live monitoring', 'Trends'],            false, 30),
  ('nova',   'grok', 'Nova',   'Service Innovation',      array['New offers', 'Experiments'],                       false, 40),
  ('tara',   'grok', 'Tara',   'Talent Ops',              array['Roster growth', 'Specialist coverage'],            false, 50)
on conflict (slug, lane) do update set
  display_name = excluded.display_name,
  role = excluded.role,
  strengths = excluded.strengths,
  is_leader = excluded.is_leader,
  sort_order = excluded.sort_order,
  is_active = true,
  updated_at = now();
