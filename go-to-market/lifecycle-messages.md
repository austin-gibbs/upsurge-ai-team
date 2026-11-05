# AI Team Lifecycle Messages

Purpose: the complete client message sequence for the AI Team journey, from first interest to a settled monthly rhythm. Copy is ready to load into automations. Replace the fields in double braces before activation.

Global rules for every message:

- Use the client first name, business name, team lead name, and the correct link for that client. Never send a message with an unfilled field.
- Stop a reminder the moment the client completes the step it points to.
- Keep the promise consistent: the client asks, the team handles the work, and the Surge Command app shows what is happening.
- Messages marked automated can send from the team lead name so the relationship stays human. Messages marked client lead personal are written, reviewed, and sent by the lead.

## 01. Landing Page Inquiry Acknowledgment

- Trigger: A visitor submits the landing page form and does not book a fit call in the same session.
- Timing: Within 15 minutes during business hours.
- Channel: Email.
- Subject: Thanks for reaching out to UpSurge
- Sender: Automated.
- Copy:

Hi {{first_name}},

Thanks for reaching out. You are in the right place if the work of running the business has started to crowd out the work of growing it.

The next step is a short fit call. We will look at the work you want off your plate, show you how your AI team would be set up inside your Surge Command app, and tell you plainly if we are not the right fit.

Book a time here: {{fit_call_booking_link}}

If you would rather start by replying to this email, send us the one task you most want to hand off. That is a very good place to begin.

Warmly,  
{{team_lead_name}}  
UpSurge AI Team

## 02. Fit Call Confirmation

- Trigger: Fit call is booked.
- Timing: Immediately after booking.
- Channel: Email.
- Subject: Your fit call is booked
- Sender: Automated.
- Copy:

Hi {{first_name}},

Your fit call is booked for {{fit_call_date}} at {{fit_call_time}} {{time_zone}}.

Here is what we will cover: the work you want to hand off, the tools your business already uses, and what your AI team would look like once it is installed. We will also show you the Surge Command app, where requests, status, and finished work live in one place.

Join here: {{fit_call_join_link}}

If you need to move the call, use this link: {{fit_call_reschedule_link}}

No preparation is needed. If one task keeps following you home at night, bring that one.

See you soon,  
{{team_lead_name}}  
UpSurge AI Team

## 03. Fit Call Reminder

- Trigger: Fit call is approaching and the client has not cancelled or rescheduled.
- Timing: One hour before the call.
- Channel: Short message, SMS.
- Sender: Automated.
- Copy:

Hi {{first_name}}, quick reminder from UpSurge: your fit call is in one hour. Join here when you are ready: {{fit_call_join_link}}. If something has come up, reply here and we will find a better time.

## 04. Fit Call No-Show Recovery

- Trigger: Fit call time passes and the client does not join.
- Timing: Within two hours after the missed call.
- Channel: Email.
- Subject: We missed you, and no harm done
- Sender: Client lead personal.
- Copy:

Hi {{first_name}},

We missed you on the fit call today, and no harm done. Business has a way of rearranging the calendar.

If you are still curious about handing off the work that keeps landing back on your desk, I am glad to find a calmer time. You can pick a new one here: {{fit_call_booking_link}}.

If the timing is simply not right, reply and tell me. I will close the loop on my side and leave you in peace.

Either way, thanks for considering us.

{{team_lead_name}}  
UpSurge AI Team

## 05. Application Received

- Trigger: Client submits the AI Team application.
- Timing: Immediately after submission.
- Channel: Email.
- Subject: We received your application
- Sender: Automated.
- Copy:

Hi {{first_name}},

We received your application for {{business_name}}. Thank you for trusting us with a close look at how your business runs.

We review each application personally. We are looking at the work you want to hand off, the tools you use, and whether an installed AI team can give you a clear win quickly.

You will hear from us after the review. If anything important changes in the meantime, just reply to this email.

With appreciation,  
{{team_lead_name}}  
UpSurge AI Team

## 06. Application Approved, Agreement and Start Payment

- Trigger: Application is approved and the agreement is ready for signature.
- Timing: Immediately after approval.
- Channel: Email.
- Subject: You are approved. Here is your agreement
- Sender: Automated.
- Copy:

Hi {{first_name}},

Good news. {{business_name}} is approved for an AI Team install.

Your agreement is ready here: {{agreement_link}}

The payment terms are simple and written the same way in the agreement. The install fee is split into two equal parts. The first half starts your install. The second half is due when your team goes live. Monthly management is paid in advance once your service begins, as set out in the agreement. Your founding rate lock is written into the agreement, so the rate promised for your selected tier is protected under the founding terms.

When you sign and complete the start payment, we begin right away: your command center is created, your connect checklist is prepared with your first tools marked, and your install is opened on our side.

Sign and start here: {{agreement_link}}  
Complete the start payment here: {{start_payment_link}}

If you have a question before signing, reply to this email and I will answer it directly.

Welcome to the front of the line,  
{{team_lead_name}}  
UpSurge AI Team

## 07. Agreement Signed Welcome

- Trigger: Agreement is signed and the start payment is confirmed.
- Timing: Immediately after confirmation.
- Channel: Email.
- Subject: Welcome aboard, {{business_name}}
- Sender: Automated.
- Copy:

Welcome aboard. Your AI team is officially on the job.

From today, you have a full team of specialists standing behind one simple promise: you ask, we deliver. Strategy, websites, automations, content, follow up, reporting. Whatever the request, it lands with the right expert, gets done to a professional standard, and comes back to you finished.

You will not need to manage tasks, chase updates, or wonder where something stands. Your Surge Command app will show you the work, and I will keep you posted before you ever have to ask.

Here is what happens next. We set up your command center, send your connect checklist, seat your team around your business, learn how you like things done, and take you live. Your part stays small: a few sign ins, one short knowledge call, and your first request.

Hundreds of moving parts just became someone else's problem. Ours. Gladly.

Welcome to the team.

{{team_lead_name}}  
The UpSurge AI Team

## 08. Your Command Center Is Ready

- Trigger: The client's Surge Command workspace is created and checked.
- Timing: During onboarding, as soon as the workspace is ready to view.
- Channel: Email.
- Subject: Your command center is ready to look at
- Sender: Automated.
- Copy:

Hi {{first_name}},

Your command center is ready.

Open it here: {{command_center_link}}

This is your private Surge Command app for {{business_name}}: your request board, your team page, and your activity view, all in one place. It will look quiet at first. That changes quickly once your tools are connected and your team starts moving work through it.

There is nothing you need to complete inside it yet. Have a look around, and watch for the next message from us. It contains your connect checklist, which is the one small task that puts your team to work.

Your team lead,  
{{team_lead_name}}

## 09. Connect Checklist Invitation

- Trigger: Command center is ready and the client's first tools have been marked on the checklist.
- Timing: Immediately after the command center message, or with it when the install is moving quickly.
- Channel: Email.
- Subject: Fifteen minutes connects your team
- Sender: Automated.
- Copy:

Hi {{first_name}},

It is time to give your team its hands.

Your connect checklist is ready here: {{connect_checklist_link}}

We have marked the first tools for {{business_name}} based on your application. You will connect one tool at a time, starting with the ones your team needs first.

The process is built to keep you in control. You sign in yourself on each tool's own secure page. We never see, receive, or store your passwords. Nothing connects without your tap. You can revoke access in the tool's own settings at any time, and the access simply stops.

Most clients finish the first pass in about fifteen minutes. If a tool does not apply to your business, skip it. You can add more later in seconds.

Start with the first item on the list. That is enough to get us moving.

{{team_lead_name}}  
UpSurge AI Team

## 10. Connect Nudge, 24 Hours

- Trigger: Connect checklist was sent and at least one priority connection is still unfinished.
- Timing: 24 hours after the checklist invitation.
- Channel: Email.
- Subject: One small tap gets your team moving
- Sender: Automated.
- Copy:

Hi {{first_name}},

A quick note on your install. Your command center is ready, and your team is waiting on the first connection before the real work can begin.

You do not need to finish the whole checklist today. Just complete the first item here: {{connect_checklist_link}}

It takes a few minutes, and you sign in on the tool's own page. Once that first connection is live, we can start setting up the work around it while you finish the rest at your pace.

If you get stuck, reply to this email and we will help you through the exact screen you are on.

{{team_lead_name}}  
UpSurge AI Team

## 11. Connect Nudge, 72 Hours

- Trigger: Priority connections are still unfinished 72 hours after the checklist invitation.
- Timing: 72 hours after the checklist invitation.
- Channel: Short message, SMS.
- Sender: Client lead personal.
- Copy:

Hi {{first_name}}, it is {{team_lead_name}} from UpSurge. No pressure at all on the connect checklist. If it helps, we can do the first tap together on a short call and I will walk you through it live. Want me to send a couple of times?

## 12. Your Team Is Seated

- Trigger: The client's specialists have been assigned and checked against the business profile.
- Timing: When the seating stage is complete, before the knowledge call.
- Channel: Email.
- Subject: Your team is seated
- Sender: Client lead personal.
- Copy:

Hi {{first_name}},

Your team is seated.

In plain terms, that means the right specialists for {{business_name}} have been assigned, briefed on your services and priorities, and arranged behind one point of contact: me. You will not need to choose who handles what or manage handoffs between people. You send a request, and I make sure it lands with the right expert.

You can see your team on your team page here: {{team_page_link}}

The next step is the knowledge call, where we make sure your team understands how you like things done, what great looks like, and what to avoid. After that, we take you live.

Thank you for trusting us with this. We are taking good care of it.

{{team_lead_name}}  
UpSurge AI Team

## 13. Knowledge Call Invitation

- Trigger: Team seating is complete and the knowledge stage begins.
- Timing: Immediately when the knowledge stage opens.
- Channel: Email.
- Subject: One short call teaches your team your business
- Sender: Automated.
- Copy:

Hi {{first_name}},

Your team has studied the basics of {{business_name}} from your website, materials, and systems. Now we need the part only you can teach us: how you like things done.

Please book your knowledge call here: {{knowledge_call_booking_link}}

If one of these times is easier, tell us and we will hold it for you: {{proposed_time_one}} or {{proposed_time_two}}.

The call takes about 30 minutes. We will confirm your services, your customers, your voice, your approval habits, and the standards you expect. We will also ask what your team should never do. Those answers become part of how your team works from day one.

Before the call, please complete the short intake form here: {{intake_form_link}}. It should take only a few minutes, and it helps us use the call for judgment instead of data entry.

Looking forward to it,  
{{team_lead_name}}  
UpSurge AI Team

## 14. Intake Form Reminder

- Trigger: Knowledge call is booked and the intake form is still incomplete.
- Timing: 24 hours before the knowledge call.
- Channel: Email.
- Subject: A few minutes before your knowledge call
- Sender: Automated.
- Copy:

Hi {{first_name}},

Your knowledge call is coming up on {{knowledge_call_date}} at {{knowledge_call_time}} {{time_zone}}.

Before we talk, please finish the short intake form here: {{intake_form_link}}

It covers the basics your team should know cold: your services, your customers, your tools, your approval preferences, and anything you never want automated without your eye on it. Short answers are perfect. We will go deeper together on the call.

If you would rather answer by replying to this email, do that instead. The goal is simply to make your team useful fast.

Thank you,  
{{team_lead_name}}  
UpSurge AI Team

## 15. Go Live

- Trigger: Install checks pass and the client's team is live.
- Timing: Immediately at go live.
- Channel: Email.
- Subject: You are live
- Sender: Client lead personal.
- Copy:

Hi {{first_name}},

You are live.

Your team is seated, your tools are connected, and your Surge Command app is open. Your board is ready, your team page is on, and your requests can start moving today.

Open your command center here: {{command_center_link}}

Send your first request whenever you are ready. Anything is a fair start, especially the task you have been putting off. We will acknowledge it, turn it into a plan, assign the right specialist, and bring it back finished.

This is the moment the busywork changes address. It lives with us now.

We are ready when you are.

{{team_lead_name}}  
UpSurge AI Team

## 16. First Request Invitation

- Trigger: Client has gone live and has not submitted a first request yet.
- Timing: The next business morning after go live, or sooner if the lead sees a natural opening.
- Channel: Email.
- Subject: Send us the first one
- Sender: Client lead personal.
- Copy:

Hi {{first_name}},

Your team is live and ready. If you are wondering what to send first, start small and annoying. The task that keeps resurfacing is usually the right one.

You can send it in your command center here: {{new_request_link}}, or simply reply to this email and I will log it for you.

Two examples of a good first request:

"Follow up with every lead from last week's open house who has not booked a tour yet. Friendly, short, and offer Thursday or Saturday times."

"Build a landing page for the spring listing package. Use the photos in the Spring folder, match the website, and have it ready to review by Friday."

You do not need to write a brief or work out the steps. Give us the outcome and the one or two facts that matter. We will handle the route.

Send the first one today, and let your team earn its keep.

{{team_lead_name}}

## 17. End of First Week Check-In

- Trigger: Seven days after go live.
- Timing: Morning of day seven, after the first weekly summary has been prepared.
- Channel: Email.
- Subject: Your first week with your team
- Sender: Client lead personal.
- Copy:

Hi {{first_name}},

Your first week is complete, so I want to check in properly.

Your team is set up, your tools are connected, and your board now shows the rhythm we want: requests coming in, work moving, and finished pieces coming back to you. Your daily digest keeps the short version in front of you, and your weekly review pulls the week together with what was delivered and what is next.

You can see the full picture anytime here: {{command_center_link}}

My question for you is simple: what else should we take off your plate? The best second wave usually comes from the work you still touch every day without thinking about it: follow up, scheduling, inbox cleanup, reporting, content, or the small fixes that wait too long.

Reply with one thing, or send it as a request in the app. Either way, we will pick it up.

Thank you for a strong first week.

{{team_lead_name}}  
UpSurge AI Team

## 18. Monthly Owner Report Cover Note

- Trigger: Monthly owner report is ready for the client.
- Timing: On the client's monthly reporting day.
- Channel: Email.
- Subject: Your {{report_month}} owner report
- Sender: Client lead personal.
- Copy:

Hi {{first_name}},

Your {{report_month}} owner report is ready.

Read it here: {{monthly_report_link}}

It covers what your team delivered, what is in motion now, the standards we are watching, and the decisions or opportunities that deserve your attention. Your output ledger sits behind it in your command center, so you can see the record of completed work whenever you want: {{output_ledger_link}}

If one item in the report deserves a conversation, reply and point to it. I will bring the context and a recommendation.

Thank you for letting us run this part of the business with you.

{{team_lead_name}}  
UpSurge AI Team

## 19. Quiet Client Re-Engagement, 30 Days of Low Usage

- Trigger: Client usage has been low for 30 days and no urgent support issue is open.
- Timing: On day 30 of the low usage period, during business hours.
- Channel: Email.
- Subject: Your team is ready when you are
- Sender: Client lead personal.
- Copy:

Hi {{first_name}},

I was looking at your output ledger, and it reminded me to check in. Your team and your command center are ready, and your ledger is the record we want to keep building with you: {{output_ledger_link}}

No concern and no pressure. Sometimes the business gets loud and the easiest work to postpone is the work of handing things off.

If it helps, send us one small thing this week. A follow up list, a page that needs fixing, an inbox pattern you are tired of, a report you keep rebuilding by hand. One request is enough to restart the rhythm.

Reply here and I will log it for you, or open your command center and tap New Request: {{new_request_link}}

If something about the setup is not working for you, tell me that instead. I would rather adjust the team around your habits than have it sit quietly.

Here when you are ready,  
{{team_lead_name}}  
UpSurge AI Team
