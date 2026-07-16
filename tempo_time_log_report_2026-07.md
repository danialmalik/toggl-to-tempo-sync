# Tempo Time Log Report — July 2026 (1–15)

**Status: DRAFT — for your review before syncing to Tempo.** This is a reconstruction, not a record of fact. See "Flags" below before logging anything.

## Scope

- Period: **2026-07-01 to 2026-07-15** (today, 2026-07-16, excluded as requested).
- Source of truth for total hours: Toggl (personal tracking, entries mostly undescribed).
- Sources used to reconstruct ticket attribution: `july_meetings.csv`, GitHub PRs (`gh search prs`, `roadpostinc/MyZoleo`), Jira REST API (issues updated since 2026-07-01, assignee = me, incl. story points via `customfield_10105`).

## Reconciliation summary

| | Hours |
|---|---|
| Raw Toggl total (Jul 1–15, exact) | 89.07h |
| Logged total after rounding to 15-min increments | **90.25h** |
| Rounding delta | +1.18h (≈1.3%) |

The rounding delta is expected: each day's total was ceiled to the nearest 15 minutes (per your instruction), and 11 working days of ceiling rounds the grand total up slightly. If you want exact-to-the-minute reconciliation instead of clean 15-min entries, tell me and I'll redo without the ceiling step.

Raw daily Toggl totals (before rounding), for reference:

| Date | Toggl total | Meeting hours (CSV) | Dev/other hours |
|---|---|---|---|
| 2026-07-01 | 6.20h | 0.00h | 6.20h |
| 2026-07-02 | 6.82h | 2.50h | 4.32h |
| 2026-07-03 | 10.77h | 3.50h | 7.27h |
| 2026-07-06 | 7.53h | 3.00h | 4.53h |
| 2026-07-07 | 8.50h | 1.50h | 7.00h |
| 2026-07-08 | 9.62h | 2.00h | 7.62h |
| 2026-07-09 | 7.73h | 0.83h | 6.90h |
| 2026-07-10 | 9.40h | 0.83h | 8.57h |
| 2026-07-13 | 4.70h | 2.33h | 2.37h |
| 2026-07-14 | 8.67h | 0.33h | 8.33h |
| 2026-07-15 | 9.13h | 0.33h | 8.80h |
| **Total** | **89.07h** | **17.17h** | **71.90h** |

## Methodology

1. **Meetings** (`july_meetings.csv`, restricted to Jul 2–15) were classified into three groups:
   - **New-cycle planning** (EPIC Walkthroughs ×2, Technical Design Walkthroughs ×2, Sprint Planning): these cover the whole batch of stories being planned, so hours were split across the 5 "new cycle" tickets proportional to story points (ZOL-6968:3, ZOL-7394:3, ZOL-7424:2, ZOL-6960:1, ZOL-6941:1 = 10 points). ZOL-5836 (a pre-existing carryover ticket, not part of the "new cycle") and ZOL-6961 (excluded per your instruction) were not included in this split.
   - **Generic/ceremony** (standups, 1-1s, Touchpoint, Team Lead Briefing): folded into whichever ticket(s) were the active dev allocation for that specific day, in the same ratio — logged as a **separate "Meeting" row** from the "Dev" row per your instruction, so you can see the meeting time and its rationale distinctly.
   - **Non-ZOLEO / org-wide** (Eng Initiatives Sync – FinOps+EngOps; Service Catalog review for Operation Excellence and FinOps): no matching ticket exists in any project on this Jira site (checked all: `ACSP, ISSM, ITHD, ITI, ITIS, NI, PAULAI, TP, ZMA, ZOL`). Logged as **`UNASSIGNED`** — 1.50h total. Needs a decision (see flags below).
   - **Topic-matched**: "MyZOLEO testing / launch plan" mapped to **ZOL-5836** ("[Track] WLT link forwarding for **Production release**") on keyword match.

2. **Dev/other hours** (day total minus meetings) were allocated per your explicit direction:
   - **ZOL-7424**: 1 full day (2026-07-09, matching PR #831 opened that day).
   - **ZOL-6968**: half a day (half of 2026-07-15, matching PR #855 opened that day).
   - **ZOL-6961**: 0 hours (excluded per your instruction).
   - **ZOL-5836**: absorbed all dev time on days with no other ticket evidence (2026-07-01, 02, 03, 06, 07, plus the other half of 07-15) — this exceeds "at least 2 days" by a wide margin (see flag below).
   - Remaining days (07-08, 10, 13, 14) had no specific ticket evidence, so were split by story points across the 3 **Done** tickets only (ZOL-7394:3, ZOL-6941:1, ZOL-6960:1 = 5 points), per your instruction to use story points on done tickets.

3. **Rounding**: every entry rounded up to the nearest 15 minutes; each day's entries were adjusted (drift absorbed into the largest entry that day) so the day's total lands exactly on its own ceiled 15-minute total.

4. **2026-07-16 revision** (post-review): ZOL-5836 was capped at **8h total** (was 35.25h) per your instruction. The freed 27.25h was redistributed across the other 5 active tickets (ZOL-7394, ZOL-7424, ZOL-6968, ZOL-6960, ZOL-6941), proportional to story points, on the same days it was originally on (2026-07-01, 02, 03, 06, 07, and half of 07-15) — this is my best-judgement placeholder, not evidence-backed, and is called out per-row below. ZOL-6961 still gets 0h. The FinOps/EngOps sync and Service Catalog review meetings stay **UNASSIGNED** — per your note, these are engineering-initiative meetings with no dedicated ticket yet.

## Per-ticket summary

| Ticket | Type / Status | Points | Summary | Dev hrs | Meeting hrs | Total hrs |
|---|---|---|---|---|---|---|
| **ZOL-7394** | Task / Done | 3 | Add workflows to auto-assign PR reviews (+ Slack digest) | 22.50h | 5.00h | **27.50h** |
| **ZOL-7424** | Story / To Do | 2 | [MyZ][EIP-Cache-01] EIP read cache: Redis client factory refactor + eipCacheClient | 12.25h | 3.50h | **15.75h** |
| **ZOL-6968** | Story / To Do | 3 | [CS][BE-4b] Lazy-upsert auto-provision + GET /cs/me [P1] | 12.00h | 3.50h | **15.50h** |
| **ZOL-6960** | Story / Done | 1 | [MyZ][SPIKE-3] Billing Performance: EIP read caching strategy | 8.75h | 2.50h | **11.25h** |
| **ZOL-6941** | Story / Done | 1 | [MyZ][FE-2] Account Balance: build header from GET /users/eip-details | 8.25h | 2.50h | **10.75h** |
| **ZOL-5836** | Story / In Progress | 1 | [Track] WLT link forwarding for Production release | 7.00h | 1.00h | **8.00h** |
| **ZOL-6961** | Story / To Do | 2 | [MyZ][SPIKE-4] Billing Performance: EIS/EngageIP database indexing | 0.00h | 0.00h | **0.00h** |
| **UNASSIGNED / eng-initiative overhead** | — | — | FinOps/EngOps sync, Service Catalog review — no ticket yet | 0.00h | 1.50h | **1.50h** |
| **TOTAL** | | | | **70.75h** | **19.50h** | **90.25h** |

## Day-by-day detail (ready for Tempo entry, pending your sign-off)

| Date | Ticket | Type | Hours | Notes |
|---|---|---|---|---|
| 2026-07-01 | ZOL-5836 | Dev | 1.50h | Capped per your 8h instruction (was 6.25h) |
| 2026-07-01 | ZOL-6941 | Dev | 0.50h | Redistributed share of the ZOL-5836 reduction (story-point split, best-judgement placeholder) |
| 2026-07-01 | ZOL-6960 | Dev | 0.50h | Redistributed share of the ZOL-5836 reduction (story-point split, best-judgement placeholder) |
| 2026-07-01 | ZOL-6968 | Dev | 1.50h | Redistributed share of the ZOL-5836 reduction (story-point split, best-judgement placeholder) |
| 2026-07-01 | ZOL-7394 | Dev | 1.25h | Redistributed share of the ZOL-5836 reduction (story-point split, best-judgement placeholder) |
| 2026-07-01 | ZOL-7424 | Dev | 1.00h | Redistributed share of the ZOL-5836 reduction (story-point split, best-judgement placeholder) |
| 2026-07-02 | ZOL-5836 | Dev | 0.75h | Capped per your 8h instruction (was 4.50h) |
| 2026-07-02 | ZOL-6941 | Dev | 0.50h | Redistributed share of the ZOL-5836 reduction (story-point split, best-judgement placeholder) |
| 2026-07-02 | ZOL-6941 | Meeting | 0.25h | ZOLEO Detailed EPIC Walkthrough (New Cycle) — share by story points 1/10 |
| 2026-07-02 | ZOL-6960 | Dev | 0.50h | Redistributed share of the ZOL-5836 reduction (story-point split, best-judgement placeholder) |
| 2026-07-02 | ZOL-6960 | Meeting | 0.25h | ZOLEO Detailed EPIC Walkthrough (New Cycle) — share by story points 1/10 |
| 2026-07-02 | ZOL-6968 | Dev | 1.00h | Redistributed share of the ZOL-5836 reduction (story-point split, best-judgement placeholder) |
| 2026-07-02 | ZOL-6968 | Meeting | 0.75h | ZOLEO Detailed EPIC Walkthrough (New Cycle) — share by story points 3/10 |
| 2026-07-02 | ZOL-7394 | Dev | 1.00h | Redistributed share of the ZOL-5836 reduction (story-point split, best-judgement placeholder) |
| 2026-07-02 | ZOL-7394 | Meeting | 0.75h | ZOLEO Detailed EPIC Walkthrough (New Cycle) — share by story points 3/10 |
| 2026-07-02 | ZOL-7424 | Dev | 0.75h | Redistributed share of the ZOL-5836 reduction (story-point split, best-judgement placeholder) |
| 2026-07-02 | ZOL-7424 | Meeting | 0.50h | ZOLEO Detailed EPIC Walkthrough (New Cycle) — share by story points 2/10 |
| 2026-07-03 | UNASSIGNED | Meeting | 1.00h | Eng Initiatives Sync - FinOps + EngOps — engineering-initiative meeting, left open, needs a dedicated ticket |
| 2026-07-03 | ZOL-5836 | Dev | 1.75h | Capped per your 8h instruction (was 7.50h) |
| 2026-07-03 | ZOL-6941 | Dev | 0.75h | Redistributed share of the ZOL-5836 reduction (story-point split, best-judgement placeholder) |
| 2026-07-03 | ZOL-6941 | Meeting | 0.25h | ZOLEO Detailed EPIC Walkthrough (New Cycle) — share by story points 1/10 |
| 2026-07-03 | ZOL-6960 | Dev | 0.75h | Redistributed share of the ZOL-5836 reduction (story-point split, best-judgement placeholder) |
| 2026-07-03 | ZOL-6960 | Meeting | 0.25h | ZOLEO Detailed EPIC Walkthrough (New Cycle) — share by story points 1/10 |
| 2026-07-03 | ZOL-6968 | Dev | 1.75h | Redistributed share of the ZOL-5836 reduction (story-point split, best-judgement placeholder) |
| 2026-07-03 | ZOL-6968 | Meeting | 0.75h | ZOLEO Detailed EPIC Walkthrough (New Cycle) — share by story points 3/10 |
| 2026-07-03 | ZOL-7394 | Dev | 1.25h | Redistributed share of the ZOL-5836 reduction (story-point split, best-judgement placeholder) |
| 2026-07-03 | ZOL-7394 | Meeting | 0.75h | ZOLEO Detailed EPIC Walkthrough (New Cycle) — share by story points 3/10 |
| 2026-07-03 | ZOL-7424 | Dev | 1.25h | Redistributed share of the ZOL-5836 reduction (story-point split, best-judgement placeholder) |
| 2026-07-03 | ZOL-7424 | Meeting | 0.50h | ZOLEO Detailed EPIC Walkthrough (New Cycle) — share by story points 2/10 |
| 2026-07-06 | ZOL-5836 | Dev | 1.00h | Capped per your 8h instruction (was 4.75h) |
| 2026-07-06 | ZOL-5836 | Meeting | 0.50h | Andrew/Danial 1-1 — generic, folded pro-rata into day's active ticket |
| 2026-07-06 | ZOL-6941 | Dev | 0.50h | Redistributed share of the ZOL-5836 reduction (story-point split, best-judgement placeholder) |
| 2026-07-06 | ZOL-6941 | Meeting | 0.25h | ZOLEO EPIC's Technical Design's Walkthrough — share by story points 1/10 |
| 2026-07-06 | ZOL-6960 | Dev | 0.50h | Redistributed share of the ZOL-5836 reduction (story-point split, best-judgement placeholder) |
| 2026-07-06 | ZOL-6960 | Meeting | 0.25h | ZOLEO EPIC's Technical Design's Walkthrough — share by story points 1/10 |
| 2026-07-06 | ZOL-6968 | Dev | 1.00h | Redistributed share of the ZOL-5836 reduction (story-point split, best-judgement placeholder) |
| 2026-07-06 | ZOL-6968 | Meeting | 0.75h | ZOLEO EPIC's Technical Design's Walkthrough — share by story points 3/10 |
| 2026-07-06 | ZOL-7394 | Dev | 1.00h | Redistributed share of the ZOL-5836 reduction (story-point split, best-judgement placeholder) |
| 2026-07-06 | ZOL-7394 | Meeting | 0.75h | ZOLEO EPIC's Technical Design's Walkthrough — share by story points 3/10 |
| 2026-07-06 | ZOL-7424 | Dev | 0.75h | Redistributed share of the ZOL-5836 reduction (story-point split, best-judgement placeholder) |
| 2026-07-06 | ZOL-7424 | Meeting | 0.50h | ZOLEO EPIC's Technical Design's Walkthrough — share by story points 2/10 |
| 2026-07-07 | ZOL-5836 | Dev | 1.25h | Capped per your 8h instruction (was 6.75h) |
| 2026-07-07 | ZOL-6941 | Dev | 0.75h | Redistributed share of the ZOL-5836 reduction (story-point split, best-judgement placeholder) |
| 2026-07-07 | ZOL-6941 | Meeting | 0.25h | ZOLEO EPIC's Technical Design's Walkthrough — share by story points 1/10 |
| 2026-07-07 | ZOL-6960 | Dev | 0.50h | Redistributed share of the ZOL-5836 reduction (story-point split, best-judgement placeholder) |
| 2026-07-07 | ZOL-6960 | Meeting | 0.25h | ZOLEO EPIC's Technical Design's Walkthrough — share by story points 1/10 |
| 2026-07-07 | ZOL-6968 | Dev | 1.50h | Redistributed share of the ZOL-5836 reduction (story-point split, best-judgement placeholder) |
| 2026-07-07 | ZOL-6968 | Meeting | 0.50h | ZOLEO EPIC's Technical Design's Walkthrough — share by story points 3/10 |
| 2026-07-07 | ZOL-7394 | Dev | 1.50h | Redistributed share of the ZOL-5836 reduction (story-point split, best-judgement placeholder) |
| 2026-07-07 | ZOL-7394 | Meeting | 0.50h | ZOLEO EPIC's Technical Design's Walkthrough — share by story points 3/10 |
| 2026-07-07 | ZOL-7424 | Dev | 1.00h | Redistributed share of the ZOL-5836 reduction (story-point split, best-judgement placeholder) |
| 2026-07-07 | ZOL-7424 | Meeting | 0.50h | ZOLEO EPIC's Technical Design's Walkthrough — share by story points 2/10 |
| 2026-07-08 | ZOL-6941 | Dev | 1.50h | Done; story-point share of unattributed dev pool |
| 2026-07-08 | ZOL-6941 | Meeting | 0.25h | ZOLEO Story and Sprint Planning Session — share by story points 1/10 |
| 2026-07-08 | ZOL-6960 | Dev | 1.50h | Done; story-point share of unattributed dev pool |
| 2026-07-08 | ZOL-6960 | Meeting | 0.25h | ZOLEO Story and Sprint Planning Session — share by story points 1/10 |
| 2026-07-08 | ZOL-6968 | Meeting | 0.50h | ZOLEO Story and Sprint Planning Session — share by story points 3/10 |
| 2026-07-08 | ZOL-7394 | Dev | 4.50h | Done; story-point share of unattributed dev pool |
| 2026-07-08 | ZOL-7394 | Meeting | 0.75h | ZOLEO Story and Sprint Planning Session — share by story points 3/10 |
| 2026-07-08 | ZOL-7424 | Meeting | 0.50h | ZOLEO Story and Sprint Planning Session — share by story points 2/10 |
| 2026-07-09 | ZOL-7424 | Dev | 6.75h | PR #831 opened this day; user-directed 1 full day |
| 2026-07-09 | ZOL-7424 | Meeting | 1.00h | Touchpoint; MyZoleo Team Standup |
| 2026-07-10 | UNASSIGNED | Meeting | 0.50h | Follow up - Service Catalog review for Operation Excellence and FinOps — engineering-initiative meeting, left open, needs a dedicated ticket |
| 2026-07-10 | ZOL-6941 | Dev | 1.50h | Done; story-point share of unattributed dev pool |
| 2026-07-10 | ZOL-6941 | Meeting | 0.25h | MyZoleo Team Standup — generic, folded pro-rata |
| 2026-07-10 | ZOL-6960 | Dev | 1.75h | Done; story-point share of unattributed dev pool |
| 2026-07-10 | ZOL-6960 | Meeting | 0.25h | MyZoleo Team Standup — generic, folded pro-rata |
| 2026-07-10 | ZOL-7394 | Dev | 5.00h | Done; story-point share of unattributed dev pool |
| 2026-07-10 | ZOL-7394 | Meeting | 0.25h | MyZoleo Team Standup — generic, folded pro-rata |
| 2026-07-13 | ZOL-5836 | Meeting | 0.25h | MyZOLEO testing / launch plan — topic matches ZOL-5836 production-release tracking |
| 2026-07-13 | ZOL-6941 | Dev | 0.25h | Done; story-point share of unattributed dev pool |
| 2026-07-13 | ZOL-6941 | Meeting | 0.75h | Andrew/Danial 1-1; MyZoleo Team Standup; Team Lead Briefing |
| 2026-07-13 | ZOL-6960 | Dev | 0.50h | Done; story-point share of unattributed dev pool |
| 2026-07-13 | ZOL-6960 | Meeting | 0.75h | Andrew/Danial 1-1; MyZoleo Team Standup; Team Lead Briefing |
| 2026-07-13 | ZOL-7394 | Dev | 1.25h | Done; story-point share of unattributed dev pool |
| 2026-07-13 | ZOL-7394 | Meeting | 1.00h | Andrew/Danial 1-1; MyZoleo Team Standup; Team Lead Briefing |
| 2026-07-14 | ZOL-6941 | Dev | 1.50h | Done; story-point share of unattributed dev pool |
| 2026-07-14 | ZOL-6941 | Meeting | 0.25h | MyZoleo Team Standup — generic, folded pro-rata |
| 2026-07-14 | ZOL-6960 | Dev | 1.75h | Done; story-point share of unattributed dev pool |
| 2026-07-14 | ZOL-6960 | Meeting | 0.25h | MyZoleo Team Standup — generic, folded pro-rata |
| 2026-07-14 | ZOL-7394 | Dev | 4.75h | Done; story-point share of unattributed dev pool |
| 2026-07-14 | ZOL-7394 | Meeting | 0.25h | MyZoleo Team Standup — generic, folded pro-rata |
| 2026-07-15 | ZOL-5836 | Dev | 0.75h | Capped per your 8h instruction (was 4.50h) |
| 2026-07-15 | ZOL-5836 | Meeting | 0.25h | MyZoleo Team Standup — generic, folded pro-rata |
| 2026-07-15 | ZOL-6941 | Dev | 0.50h | Redistributed share of the ZOL-5836 reduction (story-point split, best-judgement placeholder) |
| 2026-07-15 | ZOL-6960 | Dev | 0.50h | Redistributed share of the ZOL-5836 reduction (story-point split, best-judgement placeholder) |
| 2026-07-15 | ZOL-6968 | Dev | 5.25h | PR #855 opened this day (half-day, user-directed) + redistributed share of the ZOL-5836 reduction |
| 2026-07-15 | ZOL-6968 | Meeting | 0.25h | MyZoleo Team Standup — generic, folded pro-rata |
| 2026-07-15 | ZOL-7394 | Dev | 1.00h | Redistributed share of the ZOL-5836 reduction (story-point split, best-judgement placeholder) |
| 2026-07-15 | ZOL-7424 | Dev | 0.75h | Redistributed share of the ZOL-5836 reduction (story-point split, best-judgement placeholder) |
| 2026-07-XX | ZOL-6961 | — | 0.00h | Explicitly excluded per your instruction — no hours logged this batch |

## Flags — please review before syncing to Tempo

1. **ZOL-5836 capped at 8h** (down from 35.25h), per your instruction. The freed 27.25h was spread across the other 5 active tickets (story-point proportional, same days), which is my best judgement, not evidence — there's still no PR/Jira trail for 2026-07-01, 02, 03, 06, 07, or the first half of 07-15, so treat these "Redistributed share..." rows as soft placeholders, not fact. If you recall which ticket that time actually went to, tell me and I'll move it directly instead of spreading it by points.
2. **FinOps/EngOps Sync (07-03, 1.0h) and Service Catalog review (07-10, 0.5h) are intentionally left `UNASSIGNED`** — per your note, these are engineering-initiative meetings, not ZOLEO-project work, and there's no dedicated ticket for them yet. Once you create one (or decide on an existing eng-initiative ticket), these 1.5h can be moved there.
3. **Meeting → ticket mapping is a best-effort guess**, not verified against meeting content/attendees. If you get dedicated tickets later for recurring ceremonies (standups, 1-1s, TL briefings), we can swap this logic out per your note.
4. **PR search only covered `roadpostinc/MyZoleo`** via global `gh search prs --author=@me`. If you also contribute to `ZMA` (ZOLEO Mobile Apps) or another repo under a different account/org, that work wouldn't be captured here.
5. **90.25h vs 89.07h raw** — the 1.18h gap is purely from ceiling each day to the nearest 15 minutes, not double-counting. Flag if you want it tightened.

## Next step

Once you confirm/adjust the flags above, this table can drive the actual Tempo worklog creation (via `JiraTempoAPI.add_worklog`, the same client this repo already uses) — happy to write that sync script next, but nothing has been logged to Tempo yet.
