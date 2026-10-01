# Ajaia Technical Project Manager Assessment – Charles Kyalo Mulinga

**Video walkthrough:** [PASTE VIDEO LINK]
**Build (GitHub):** https://github.com/Mulinga/ajaia-tpm-assessment
**Resume:** https://drive.google.com/file/d/1ZFOpTKlKHwwY-SyHn-z534K7x1OthwP7/view?usp=drive_link
**Other work:** https://github.com/Mulinga
**Prepared for:** Ajaia – https://ajaia.ai

---

## Task 1 – Triage

| Rank | Item | This week | Why |
|---|---|---|---|
| 1 | **B. Priya: duplicate routing on retry / overlapping polls** | **Worked – fix before merge** | Real risk. If the queue push succeeds but the "routed" update fails, or two poll cycles overlap under load, a dispatcher gets the same exception twice – the exact noise this tool exists to remove. Launch-day load makes it more likely, so it's a now problem. Fix: make routing idempotent on `exception_id` and prevent overlapping poll cycles. |
| 2 | **C. DET-121: Terminal 3 null urgency scores** | **Worked – escalate to Dana today** | Real risk, unowned since 8/6. Unscored Terminal 3 exceptions won't be routed. Blocked on Corrigan Peak's IT contact, then ~2 days of work. I ask Dana for the contact today and set Friday as the decision point for the date. |
| 3 | **D. DET-118: terminal leads routing-rules review** | **Worked – I contact all three leads today** | Marked "no blocker", but it's on the critical path: routing rules can't go live without the people who own them signing off. Scheduling it is my job. |
| 4 | **A. Dana: auto-reassign to backup carrier** | **Declined for Sept 8 – offered as first post-launch enhancement** | Looks urgent because it comes from the COO, but it turns the tool from flagging into acting on its own. That needs carrier rules, safeguards and testing that can't be done in three weeks without risking the date. |
| 5 | **E. Queue UI blue shade** | **Deferred – post-launch backlog** | **This is the noise.** Cosmetic, mentioned in passing, no launch impact. Logged so it isn't lost. |

**Correcting the record:** last Friday's update said Green with no blockers while DET-121 was open and unassigned. The update in Task 3 corrects this.

**Protecting the date:** nothing is assumed to go faster. Scope added before launch: none. Scope cut: auto-reassignment and the colour change move to after launch. Fallback if Terminal 3 isn't unblocked by Friday: launch Terminals 1 and 2 on Sept 8, and Terminal 3 once the fix lands.

---

## Task 2 – Build

**Files:** `clean_exceptions.py` (the cleaner), `test_clean_exceptions.py` (correctness checks), `exceptions_raw.csv` (input), `exceptions_clean.csv` and `exceptions_flagged.csv` (output).

**Run it:**
```
python clean_exceptions.py exceptions_raw.csv
python test_clean_exceptions.py
```

**Output:**
```
Records in: 5   Cleaned: 5   Flagged: 2

Exceptions by event type
  missed_pickup         2
  doc_mismatch          2
  carrier_substitution  1
  TOTAL                 5

Records not confidently cleaned
  CPX-88215: timestamp is UTC ('Z') while others have no timezone; kept as written, needs FreightWorks to confirm source timezone
  CPX-88216: missing carrier code
```

**What it does and how I checked it worked:** [EDIT INTO YOUR OWN WORDS] The script normalises terminal names ("T3" becomes "Terminal 3"), carrier codes ("swft", "SWFT" and "Swft" become "SWFT") and three timestamp formats into one, then counts exceptions by event type. It flags rather than guesses: CPX-88216 has no carrier code, and CPX-88215 is the only UTC timestamp while the rest have no timezone, so it can't be safely compared until FreightWorks confirms the source timezone – a question for the same IT contact blocking DET-121. To prove it worked rather than just ran, `test_clean_exceptions.py` asserts the exact expected value for every record, confirms no rows are dropped, and checks that unknown values (an unknown terminal, an invalid carrier, a day-first date) are flagged instead of guessed. All 11 checks pass.

---

## Task 3 – Status update to Dana

**Subject: Dispatch Exception Triage – status update and a correction to last week's report**

Hi Dana,

I need to start with a correction. Last Friday's update reported Green with no blockers. That understated where we are, and I'm sorry for that. **Our honest status is Amber.** The September 8 date is still achievable, but it depends on two things in the next few days, and I want you to have the full picture before your next update to the board.

**1. Terminal 3 data issue (needs your help this week).** Terminal 3 sends some exception fields in a different format from the other terminals, and as a result a portion of Terminal 3's exceptions are currently getting no urgency score, which means they would not be routed. This is more than the "minor validation task" we described. We need 30 minutes with your FreightWorks IT contact to confirm which fields Terminal 3 sends and which timezone its timestamps use. Once we have that, the fix takes about two days. **If we can speak to them by Friday, September 8 is safe. If not, I'll come back to you immediately with options,** such as launching Terminals 1 and 2 on the 8th and Terminal 3 shortly after.

**2. Routing-rules review with your terminal leads.** We should have scheduled this sooner. I'm contacting all three terminal leads today to book the review for next week; their sign-off on who receives which exceptions is needed before go-live.

**3. A fix we caught in our own work.** In code review, our engineer found a case where, under heavy load, the same exception could be sent to a dispatcher twice. It's being fixed and tested now, well before launch, and doesn't affect the date. I'm mentioning it because I'd rather you hear about issues from us early.

**4. Your COO's request: automatic reassignment to a backup carrier.** It's a strong idea and a natural next step, but not one we can responsibly add before the 8th. It moves the tool from flagging exceptions to taking action on its own, which needs agreed carrier rules, safeguards and proper testing. My recommendation: launch on the 8th as planned, then scope auto-reassignment as the first post-launch enhancement, using real data from the first weeks to decide which missed pickups are safe to automate. I'm happy to join you when you take this to your COO.

**5. Queue colour change.** Noted and added to the post-launch list.

**What I need from you:** the name of your FreightWorks IT contact, ideally today, so we can meet by Friday.

I'll send the next update on [DAY], and I'll contact you sooner if anything changes on Terminal 3.

Best regards,
Charles Kyalo Mulinga
Technical Project Manager, Ajaia

---

## Task 4 – AI workflow note

[WRITE IN YOUR OWN WORDS – 3 to 4 sentences]
- **Used AI for:** 
- **Kept human:** 
- **One thing AI got wrong, or I checked or chose not to use:** 
