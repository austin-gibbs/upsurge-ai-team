# The Simple Standard

How every onboarding step in the AI Team service must be written and built, so a busy owner who is not technical can set up a full AI team and never feel lost.

This is a binding standard. If a step, a screen, or a message does not pass it, it does not ship.

---

## 1. The standard on one page

### The promise

Connecting a whole business is genuinely complex behind the curtain. Dozens of tools, accounts, checks, and settings have to line up before a team can work. None of that complexity belongs to the client.

The client's experience must feel like being walked through it by a patient person holding their hand: one small step at a time, each step plain, each step done before the next one starts, and a calm voice the whole way that says what is happening and what comes next.

We carry the complexity. They carry a finger to tap with.

### The test we design against

**Could a smart 10 year old follow this without asking a question?**

Every step, button, and message is tested against that question before it ships. If a step needs a second read, a guess, or a question, the step is wrong, not the reader. We rewrite the step, not the client.

Three quick checks that come from the test:

- Read it out loud. If you stumble, rewrite it.
- Cover everything except one step. If that step alone does not make sense, rewrite it.
- Ask what the reader does if it goes wrong. If the step does not say, rewrite it.

### The five rules

**Rule 1. One action per step.**
Each step asks for exactly one thing: tap one button, pick one choice, type one short answer. The moment a step holds two actions, split it into two steps. Small steps feel fast. Fast feels easy.

**Rule 2. Say exactly what to tap, in the words on the button.**
Never write "proceed with the connection." Write: "Tap the blue button that says Connect Gmail." The words on the screen and the words in our instruction must match, letter for letter, so the client never has to translate.

**Rule 3. Every step says how long it takes and what happens next.**
"Takes about 1 minute. Next, we will check it worked." A client who knows the size of a step and what follows it never feels trapped in a process. Unknown length feels long. Known length feels short.

**Rule 4. Never name the machinery.**
The client connects tools, turns on their team, and teaches us their business. They never meet words like integration, provision, seat, token, or webhook. If a thing cannot be said in plain words, we handle that part ourselves and say so: "We handle that part. Nothing for you to do."

**Rule 5. When something fails, say three things.**
What happened, in plain words. Whose it is to fix, and the answer is almost always us or the tool, never the client. And the one thing to try, a single next tap. No blame, no error codes, no dead ends. A failed step with a kind voice and one clear try is still a good experience.

---

## 2. The plain words dictionary

Words on the left never appear on a client screen, in a client message, or in a client call script. The words on the right are what we say instead.

| Never say | Say this instead |
|---|---|
| integration | connect |
| integrate your CRM | connect your client list |
| provision | set up |
| provisioning is complete | your command center is ready |
| seat a lane | turn on your team |
| seat the Claude lane | turn on your writing and thinking team |
| verification | a quick check |
| verify the connection | check it worked |
| knowledge base | what your team knows |
| seed the knowledge base | teach your team about your business |
| PM tool | your command center |
| project management | your board, where you watch the work |
| workflow | the steps that happen on their own |
| automation | work that happens on its own |
| trigger | when this happens |
| API | we handle that part |
| token | we handle that part |
| webhook | we handle that part |
| OAuth | the sign in page from the tool itself |
| credentials | your sign in |
| subscription seat | your account |
| workspace | your command center |
| dashboard | your home screen |
| configuration | your settings |
| configure | set up |
| deploy | turn on |
| sync | keep up to date |
| two factor authentication | the code they text or email you |
| permissions | what your team is allowed to see |
| grant access | let your team in |
| revoke access | turn off your team's access |
| data migration | move your information over |
| import contacts | bring in your client list |
| CRM | your client list tool (or the tool's own name, like HubSpot) |
| pipeline | your list of jobs and where each one stands |
| onboarding | getting set up |
| instance | your copy, yours alone |
| environment | your live setup, the real one |

Two notes on using the dictionary:

- The tool's own name is always allowed and often best. "Connect Salesforce" is plainer than any description of Salesforce.
- When the honest plain word does not exist, use the Rule 4 sentence: "We handle that part. Nothing for you to do." Never invent a cute name for machinery.

---

## 3. Step scripts for every connection

Every connection in onboarding (email, calendar, client list tool, phone system, file storage, ads, accounting, project tool) follows one pattern of three beats. Write the pattern once, then fill it per tool.

### The pattern

**Beat 1. What you are about to do, and why, in one sentence.**
Name the tool, name the one thing the team gains, keep it human.
Template: "Next, connect [tool]. Once it is connected, your team can [one plain benefit]. Takes about [time]."

**Beat 2. The tap instruction.**
One action, in the exact words on the button, with where the button sits.
Template: "Tap the [color or place] button that says [exact words]. [If a sign in page opens: Sign in the way you always do. We never see your password.]"

**Beat 3. What success looks like, and what we do next.**
Describe the check mark or message they will see, then hand the work back to us.
Template: "You will see a green check and the words [tool] connected. That is it for this one. We will do a quick check that it worked, and then we will [next plain thing]."

If Beat 2 opens the tool's own sign in page, add one line before it: "This opens [tool]'s own page. That is on purpose, so your password stays between you and [tool]."

If a step fails, Rule 5 takes over inside the same panel: what happened, whose fix it is, one thing to try.

### Fully written example 1: email (Gmail)

**Beat 1.** "Next, connect your email. Once it is connected, your team can read new messages, sort them, and draft replies for you to approve. Takes about 2 minutes."

**Beat 2.** "Tap the blue button that says Connect Gmail. This opens Google's own page. That is on purpose, so your password stays between you and Google. Sign in the way you always do. We never see your password. When Google asks if UpSurge can connect, tap Allow."

**Beat 3.** "You will see a green check and the words Email connected. That is it for this one. We will do a quick check that it worked by finding your most recent message, and then we will set up your calendar."

**If it fails.** "The connection did not go through. That happens sometimes, and it is on the tool's side, not yours. One thing to try: tap Connect Gmail once more, and pick the account you use for work. Still stuck? Your team lead is one tap away, at the bottom of this page."

### Fully written example 2: phone system

**Beat 1.** "Next, connect your phone system. Once it is connected, your team can answer calls, take messages, and write down what each caller needed. Takes about 3 minutes."

**Beat 2.** "Tap the button that says Connect phone. This opens your phone provider's own page. That is on purpose, so your password stays between you and them. Sign in the way you always do. If it asks which number your team should answer, pick your main business number."

**Beat 3.** "You will see a green check and the words Phone connected, with your main number under it. That is it for this one. We will do a quick check by placing a short test call to ourselves, never to a customer, and then we will connect your files."

**If it fails.** "We could not reach your phone system. The fix is on our side or theirs, not yours. One thing to try: tap Connect phone once more and sign in again. Still stuck? Your team lead is one tap away, at the bottom of this page, and we will sort it out with the phone company so you do not have to."

### The remaining connections, same three beats

| Connection | Beat 1 benefit, in plain words | The one choice the client may meet |
|---|---|---|
| Calendar | your team can book, move, and guard your appointments | which calendar is the work one, if they have two |
| Client list tool (CRM) | your team can see every client and where each job stands | nothing, sign in only |
| File storage | your team can find and use your documents, photos, and files | which folder to start with, if they keep work in more than one |
| Ads | your team can run your ads and report what they bring in | which ad account is the business one, if they have more than one |
| Accounting | your team can send invoices and keep your books tidy | nothing, sign in only |
| Project tool | your team can work inside the board you already use | which board the team should work on |

Each one is written out in full, in the pattern, before it ships. No connection goes live on the table alone.

---

## 4. The hand-holding checklist

No new onboarding step ships until every line below is true of it. The reviewer checks the step itself, on a phone, the way a client meets it.

- [ ] **Progress is always visible.** The client can see where they are, how many steps are left, and that the end is close. "Step 3 of 6" or a simple bar, always on screen.
- [ ] **Back is always safe.** Going back never loses work, never starts anything over, and never punishes a second look.
- [ ] **Their place is always saved.** If they close the page, answer a call, or come back tomorrow, they land exactly where they left off, with what they did still done.
- [ ] **One primary button.** Each step has one obvious next tap. Other choices, if any, are quiet and secondary. The eye should never have to choose where to go.
- [ ] **Help lives on the step itself.** The answer to the question this step raises is written on this step, in one or two plain lines. Never "see the manual," never a help center link as the first answer.
- [ ] **A human promise line is on the step.** Every step carries it: "Stuck? Your team lead is one tap away." It goes to the lead, a person who knows their setup, never to a ticket queue, never to a form.
- [ ] **Milestones get a small celebration.** A finished connection, a team turned on, the last teaching question: mark it warmly and briefly ("That is your email done. Three to go.") so progress feels real.
- [ ] **No step asks for what the system can find itself.** If their website, their tools, or an earlier answer already holds it, we fill it in and show it for a quick yes or a fix. Asking again is a tax on trust.
- [ ] **One action only.** Rule 1, checked again at the door.
- [ ] **The failure path is written.** Rule 5, in the panel, before launch, not after the first client hits it.
- [ ] **The 10 year old test passed.** Someone who did not write the step followed it cold, on a phone, without asking a question.

---

## 5. How this standard works with business types

Onboarding adapts to the client's kind of business through business type packs: a real estate pack, an insurance pack, an education pack, a home services pack, and more as we grow. A pack changes the words, never the rules.

**What a pack changes:**

- **The names of things.** A real estate client's client list tool holds leads and listings. An insurance agency's holds policies and renewals. The pack uses the words the owner already uses at work, taken from the dictionary's spirit: plain first, theirs where theirs is plainer.
- **Which connections come first.** The pack orders the connections by what that business feels first. A brokerage connects the phone system early, because missed calls are missed listings. A school connects email and calendar early, because the term runs on them.
- **The examples.** Beat 1 benefits are written in the work of that business: "your team can answer calls about new listings," not "your team can answer calls."
- **The teaching questions.** What the team needs to know differs by business, so the questions do too, still one at a time, still with what we found already filled in.

**What a pack never changes:**

- The five rules.
- The three beats.
- The checklist.
- The 10 year old test.

Simplicity is the product's skeleton. The pack is the clothes. A client should feel the onboarding was written for their kind of business, and never feel that a different kind of business got an easier ride.

---

## The standard, in one line

If a step needs explaining, the step is not finished. When every step explains itself, onboarding stops feeling like setup and starts feeling like being looked after, which is the feeling this whole service is sold on.
