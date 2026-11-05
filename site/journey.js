/* UpSurge AI Team: shared journey and business type system.
 *
 * One config object per business type drives how the whole experience shapes
 * itself: the words on the board, the stages, the starter jobs, which tools
 * get connected first, and the questions asked during setup. The client never
 * fits into our system. The system takes the shape of their business.
 *
 * Production note: in the live product these type configs come from the
 * Business Type Packs in install-templates/business-types/ and are served to
 * the workspace at setup time. The three demo types below are fully written.
 * Dental, education, and anything else fall back to the general wording until
 * their pack is installed.
 */
(function () {
  var JOURNEY_KEY = 'upsurgeJourneyV1';
  var CONFIG_KEY = 'upsurgeWorkspaceConfigV1';

  var GENERAL = {
    label: 'Something else',
    itemWord: 'Work items',
    stages: ['New', 'In progress', 'In review', 'Done'],
    categories: ['Operations', 'Marketing', 'Reports'],
    items: [
      { title: 'Follow up with new enquiries', owner: 'Remy, Voice Agents', cat: 'Operations', stage: 0 },
      { title: 'Weekly summary for the owner', owner: 'Parker, Reporting', cat: 'Reports', stage: 1 },
      { title: 'Update the services page', owner: 'Wes, Web Builds', cat: 'Marketing', stage: 3 }
    ],
    templates: [
      'Answer every new enquiry the same day',
      'Write the weekly owner summary',
      'Tidy the customer list once a month',
      'Ask happy customers for a review'
    ],
    ledger: [
      { cat: 'Reports', title: 'Weekly owner summary', small: 'What moved, what is stuck, and what needs a decision.', turn: 'Same day', when: 'Completed today' },
      { cat: 'Operations', title: 'New enquiry follow up', small: 'Every enquiry from the week answered in the owner voice.', turn: 'Same day', when: 'Completed today' },
      { cat: 'Marketing', title: 'Services page update', small: 'New offer added and checked on phone and desktop.', turn: '1 day', when: 'Completed yesterday' }
    ],
    connectOrder: ['crm', 'email', 'calendar', 'phone', 'ads', 'files', 'accounting', 'project'],
    intake: {
      services: 'What you sell or do, in plain words.',
      serve: 'Who you do it for, and where.',
      season: 'Your busiest time of year'
    },
    facts: [
      { text: 'Business name: Your business, as you wrote it', src: 'From your application' },
      { text: 'Industry: Service business', src: 'From your application' },
      { text: 'Service area: Your local area', src: 'From your website' },
      { text: 'Core offer: Your main services', src: 'From your website' },
      { text: 'Main lead sources: Referrals and your website', src: 'Drafted from your application answers' },
      { text: 'Follow up today: Manual, owner-led', src: 'From your application answers' },
      { text: 'Team size: As you told us', src: 'From your application' },
      { text: 'Approval habit: Owner approves client-facing work', src: 'Default. Correct it below if a manager approves' }
    ]
  };

  var TYPES = {
    'real-estate': {
      label: 'Real estate team',
      itemWord: 'Listings',
      stages: ['New', 'Preparing', 'Live', 'Under contract', 'Closed'],
      categories: ['Listings', 'Buyers', 'Marketing', 'Reports'],
      items: [
        { title: 'New seller lead from the website', owner: 'Remy, Voice Agents', cat: 'Buyers', stage: 0 },
        { title: 'Maple Court listing, photos and launch', owner: 'Wes, Web Builds', cat: 'Listings', stage: 1 },
        { title: 'Foothills family home, on the market', owner: 'Mira, Marketing Strategy', cat: 'Listings', stage: 2 },
        { title: 'Elm Street buyer offer', owner: 'Diego, CRM Systems', cat: 'Buyers', stage: 3 },
        { title: 'Ridgeview closing, wrapped up', owner: 'Parker, Reporting', cat: 'Listings', stage: 4 }
      ],
      templates: [
        'Call every new lead back in five minutes',
        'Write the weekly market update',
        'Get a new listing ready to launch',
        'Check in with past clients once a month'
      ],
      ledger: [
        { cat: 'Reports', title: 'Weekly pipeline report', small: 'Week\u2019s movement, stalled stages flagged, summary in the owner\u2019s voice.', turn: 'Same day', when: 'Completed today' },
        { cat: 'Sales support', title: 'Open house follow-up sequence', small: 'Call and text sequence prepared for every unbooked attendee.', turn: 'Same day', when: 'Completed today' },
        { cat: 'Operations', title: 'CRM duplicate cleanup, spring list', small: 'Duplicate records merged and pipeline stages corrected.', turn: 'Same day', when: 'Completed today' },
        { cat: 'Marketing', title: 'Neighborhood guide, foothills edition', small: 'Search and AI visibility article drafted from the business memory.', turn: '1 day', when: 'Completed yesterday' }
      ],
      connectOrder: ['crm', 'email', 'phone', 'calendar', 'ads', 'files', 'accounting', 'project'],
      intake: {
        services: 'Listings, buyer representation, relocation, property management, and so on.',
        serve: 'First-time buyers, move-up families, investors, and the neighborhoods or areas you know best.',
        season: 'Spring listings, open enrollment, tax season'
      },
      facts: [
        { text: 'Business name: Summit Ridge Realty Group', src: 'From your website and application' },
        { text: 'Industry: Real estate, residential sales', src: 'From your website' },
        { text: 'Service area: Denver metro and the foothills', src: 'From your website service pages' },
        { text: 'Core offer: Listing representation and buyer representation', src: 'From your website' },
        { text: 'Main lead sources: Referrals, past clients, and open houses', src: 'Drafted from your connected CRM' },
        { text: 'Follow up today: Manual, owner-led, often next day', src: 'From your application answers' },
        { text: 'Team size: 6 to 15', src: 'From your application' },
        { text: 'Approval habit: Owner approves client-facing work', src: 'Default. Correct it below if a manager approves' }
      ]
    },
    'insurance': {
      label: 'Insurance agency',
      itemWord: 'Leads',
      stages: ['New lead', 'Quoting', 'Bound', 'Renewal coming'],
      categories: ['New leads', 'Renewals', 'Claims help', 'Marketing'],
      items: [
        { title: 'New car quote request, the Alvarez family', owner: 'Remy, Voice Agents', cat: 'New leads', stage: 0 },
        { title: 'Home and car bundle quote, the Chen family', owner: 'Diego, CRM Systems', cat: 'New leads', stage: 1 },
        { title: 'Coffee shop policy, bound and filed', owner: 'Parker, Reporting', cat: 'New leads', stage: 2 },
        { title: 'Garcia family renewal, due in 20 days', owner: 'Kai, Search and Visibility', cat: 'Renewals', stage: 3 }
      ],
      templates: [
        'Call every new quote request the same day',
        'Send renewal reminders 30 days early',
        'Ask happy clients for a review',
        'Send the monthly update to referral partners'
      ],
      ledger: [
        { cat: 'New leads', title: 'Same day quote callbacks', small: 'Every quote request from the website called back in the owner\u2019s voice.', turn: 'Same day', when: 'Completed today' },
        { cat: 'Renewals', title: 'Renewal reminders, next 30 days', small: 'Every renewal coming due got a friendly heads up and a booked review.', turn: 'Same day', when: 'Completed today' },
        { cat: 'Marketing', title: 'Review requests to recent clients', small: 'Polite asks sent to clients with a great recent experience.', turn: '1 day', when: 'Completed yesterday' }
      ],
      connectOrder: ['crm', 'phone', 'email', 'calendar', 'accounting', 'ads', 'files', 'project'],
      intake: {
        services: 'Car, home, life, and small business cover, and so on.',
        serve: 'Families, new homeowners, and small business owners in your town.',
        season: 'Renewal season, open enrollment'
      },
      facts: [
        { text: 'Business name: Harbor & Pine Insurance', src: 'From your website and application' },
        { text: 'Industry: Insurance agency', src: 'From your website' },
        { text: 'Service area: Portland and nearby suburbs', src: 'From your website service pages' },
        { text: 'Core offer: Car, home, life, and small business cover', src: 'From your website' },
        { text: 'Main lead sources: Referrals and quote requests from the website', src: 'Drafted from your connected CRM' },
        { text: 'Follow up today: Quotes often wait a day or two', src: 'From your application answers' },
        { text: 'Team size: 2 to 5', src: 'From your application' },
        { text: 'Approval habit: Owner approves client-facing work', src: 'Default. Correct it below if a manager approves' }
      ]
    },
    'home-services': {
      label: 'Home services',
      itemWord: 'Jobs',
      stages: ['New job', 'Estimate sent', 'Scheduled', 'In progress', 'Done and paid'],
      categories: ['Repairs', 'Installs', 'Maintenance plans', 'Reviews'],
      items: [
        { title: 'No hot water call, the Nguyen home', owner: 'Remy, Voice Agents', cat: 'Repairs', stage: 0 },
        { title: 'Water heater swap, estimate sent Tuesday', owner: 'Diego, CRM Systems', cat: 'Installs', stage: 1 },
        { title: 'Furnace tune up, booked for Friday', owner: 'Theo, Meeting Follow Through', cat: 'Maintenance plans', stage: 2 },
        { title: 'Kitchen repipe, day two on site', owner: 'Wes, Web Builds', cat: 'Repairs', stage: 3 },
        { title: 'AC install on Pine Street, paid in full', owner: 'Parker, Reporting', cat: 'Installs', stage: 4 }
      ],
      templates: [
        'Answer every new job call within minutes',
        'Chase the estimate on day two',
        'Ask for a review the day the job is done',
        'Fill slow days with maintenance plan offers'
      ],
      ledger: [
        { cat: 'Repairs', title: 'Same day call backs on new jobs', small: 'Every new job call answered or returned within the hour.', turn: 'Same day', when: 'Completed today' },
        { cat: 'Installs', title: 'Estimate follow ups, this week', small: 'Open estimates got a friendly nudge and a booked slot.', turn: 'Same day', when: 'Completed today' },
        { cat: 'Reviews', title: 'Review asks after finished jobs', small: 'Sent the day each job wrapped up, while it is fresh.', turn: '1 day', when: 'Completed yesterday' }
      ],
      connectOrder: ['phone', 'crm', 'calendar', 'email', 'accounting', 'ads', 'files', 'project'],
      intake: {
        services: 'Plumbing, heating, cooling, repairs and installs, and so on.',
        serve: 'Homeowners in your service area, landlords, and small property managers.',
        season: 'First heat wave, first cold snap'
      },
      facts: [
        { text: 'Business name: BrightFlow Home Services', src: 'From your website and application' },
        { text: 'Industry: Home services, plumbing, heating, and cooling', src: 'From your website' },
        { text: 'Service area: Austin and the north suburbs', src: 'From your website service pages' },
        { text: 'Core offer: Repairs, installs, and maintenance plans', src: 'From your website' },
        { text: 'Main lead sources: Phone calls, Google, and repeat customers', src: 'Drafted from your connected CRM' },
        { text: 'Follow up today: Estimates often wait two or three days', src: 'From your application answers' },
        { text: 'Team size: 6 to 15', src: 'From your application' },
        { text: 'Approval habit: Owner approves client-facing work', src: 'Default. Correct it below if a manager approves' }
      ]
    },
    'dental': null,
    'education': null,
    'other': null
  };
  TYPES['dental'] = GENERAL;
  TYPES['education'] = GENERAL;
  TYPES['other'] = GENERAL;

  var WORKSPACES = [
    { id: 'summit-ridge', name: 'Summit Ridge Realty Group', short: 'Summit Ridge', type: 'real-estate', line: 'Real estate team, Denver metro' },
    { id: 'harbor-pine', name: 'Harbor & Pine Insurance', short: 'Harbor & Pine', type: 'insurance', line: 'Insurance agency, Portland' },
    { id: 'brightflow', name: 'BrightFlow Home Services', short: 'BrightFlow', type: 'home-services', line: 'Plumbing, heating, and cooling, Austin' }
  ];

  function clone(o) { return JSON.parse(JSON.stringify(o)); }

  function getJourney() {
    var j = { businessType: 'real-estate', customType: '', workspaceId: 'summit-ridge', workspaceName: 'Summit Ridge Realty Group', shortName: 'Summit Ridge' };
    try {
      var raw = localStorage.getItem(JOURNEY_KEY);
      if (raw) { var p = JSON.parse(raw); for (var k in p) j[k] = p[k]; }
    } catch (e) { /* defaults */ }
    return j;
  }
  function setJourney(patch) {
    var j = getJourney();
    for (var k in patch) j[k] = patch[k];
    try { localStorage.setItem(JOURNEY_KEY, JSON.stringify(j)); } catch (e) { /* in memory only */ }
    return j;
  }
  function getType(key) { return TYPES[key] || GENERAL; }

  /* Dental, education, and something else render from the general wording
     until a pack exists for them. There is no industry limit: a business
     that picks something else tells us what it is in its own words
     (journey.customType), and those words name its workspace type wherever
     the general wording renders. */
  function isFallback(key) { return key === 'dental' || key === 'education' || key === 'other'; }
  function typeLabel(key, j) {
    j = j || getJourney();
    if (key === 'other' && j.customType) return j.customType;
    return getType(key).label;
  }

  function seedConfig(ws, typeKey) {
    var t = getType(typeKey || ws.type);
    var cfg = {
      workspaceId: ws.id,
      name: ws.name,
      shortName: ws.short,
      type: typeKey || ws.type,
      itemWord: t.itemWord,
      stages: clone(t.stages),
      categories: clone(t.categories),
      items: clone(t.items),
      templates: clone(t.templates),
      ledger: clone(t.ledger)
    };
    var j = getJourney();
    if ((typeKey || ws.type) === 'other' && j.customType) cfg.typeTerm = j.customType;
    return cfg;
  }
  function loadConfig() {
    try {
      var raw = localStorage.getItem(CONFIG_KEY);
      if (raw) return JSON.parse(raw);
    } catch (e) { /* seed below */ }
    var j = getJourney();
    var ws = WORKSPACES.filter(function (w) { return w.id === j.workspaceId; })[0] || WORKSPACES[0];
    var cfg = seedConfig(ws, j.businessType || ws.type);
    saveConfig(cfg);
    return cfg;
  }
  function saveConfig(cfg) {
    try { localStorage.setItem(CONFIG_KEY, JSON.stringify(cfg)); } catch (e) { /* in memory only */ }
  }
  function chooseWorkspace(ws) {
    setJourney({ workspaceId: ws.id, workspaceName: ws.name, shortName: ws.short, businessType: ws.type });
    var cfg = seedConfig(ws, ws.type);
    saveConfig(cfg);
    return cfg;
  }

  window.JOURNEY = {
    TYPES: TYPES,
    GENERAL: GENERAL,
    WORKSPACES: WORKSPACES,
    getJourney: getJourney,
    setJourney: setJourney,
    getType: getType,
    isFallback: isFallback,
    typeLabel: typeLabel,
    seedConfig: seedConfig,
    loadConfig: loadConfig,
    saveConfig: saveConfig,
    chooseWorkspace: chooseWorkspace,
    JOURNEY_KEY: JOURNEY_KEY,
    CONFIG_KEY: CONFIG_KEY
  };
})();
