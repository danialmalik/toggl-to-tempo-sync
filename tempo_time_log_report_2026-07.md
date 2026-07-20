# Tempo Time Log Report — July 2026 (1–17)

**Status: DRAFT — for your review before syncing to Tempo.** This is a reconstruction, not a record of fact. See "Flags" below before logging anything.

**Revision history:**
- v1: Initial reconstruction, Jul 1–15, 15-min ceiling rounding, `UNASSIGNED` bucket for org meetings.
- v2: ZOL-5836 capped at 8h per your instruction, freed time redistributed by story points.
- v3: incorporated the [Time Tracking Process (July 2026)](https://roadpost.atlassian.net/wiki/spaces/WOW/pages/2889908247/Time+Tracking+Process+July+2026#Non-project-Time) guide — rounding changed to **nearest 30 minutes** (was 15-min ceiling), non-project/misc time logged to **ZOL-4295**, and **2026-07-16** added.
- v4: the two engineering-initiative meetings (Eng Initiatives Sync – FinOps+EngOps; Service Catalog review) are **not** ZOL-4295 — per your correction, these are not general non-project time, and you'll create a dedicated ticket for engineering-initiative work. Pulled back out into a separate **`PENDING-ENG-TICKET`** placeholder (1.5h) until that ticket exists.
- v5: ZOL-7394, ZOL-6968 and ZOL-7424 had too much placeholder (story-point-redistributed) dev time — trimmed each back to a small baseline and moved the excess to their real parent epics (**ZOL-6930** for ZOL-7394/ZOL-7424, **ZOL-6775** for ZOL-6968) and into ZOL-6960/ZOL-6941 (both capped at 25h) instead of the epic, per your instruction. Evidenced hours (actual PRs, explicit Toggl labels) were left untouched — only the unevidenced redistribution pool was moved. Grand total and every day's total are unchanged (96.00h); only the ticket split changed.
- **v6 (current)**: added **2026-07-17** (9.37h raw / 9.50h rounded). Entries with explicit ticket numbers logged as-is (`ZOL-6968`, `ZOL-6971`, `ZOL-7534`, `ZOL-4295`). The FinOps meeting stays unassigned — held in `PENDING-ENG-TICKET` per your instruction, you'll create the ticket. One catch-all entry ("Zoleo Track work + RBAC Epic + EIS Cache Epic + Team Leading work", 4.03h across 3 separate Toggl entries) was split evenly 4 ways across ZOL-5836 / ZOL-6775 / ZOL-6930 / ZOL-4295 — see flag below, no weighting was specified. New grand total: **105.50h**.

## Scope

- Period: **2026-07-01 to 2026-07-17**.
- Source of truth for total hours: Toggl (personal tracking).
- Sources used to reconstruct ticket attribution: `july_meetings.csv`, GitHub PRs (`gh search prs`, `roadpostinc/MyZoleo`), Jira REST API (issues updated since 2026-07-01, assignee = me, incl. story points via `customfield_10105`), and the Confluence Time Tracking Process guide.

## What changed based on the new policy guide

1. **Rounding**: nearest half-hour per day (per your instruction and the guide's explicit "Round to the nearest half-hour" rule), replacing the previous 15-min-ceiling approach. This means the grand total can now land **below** raw Toggl hours on days that round down, not just above.
2. **Non-project time → ZOL-4295**: the guide defines a per-space "miscellaneous time reporting epic" for non-project time — vacation, team/company meetings, general admin. For ZOLEO that's **ZOL-4295** ("ZOL misc time reporting"), confirmed live in Jira (Epic, To Do). This **absorbs the generic ceremonies** I'd previously been folding pro-rata into whichever dev ticket was active (standups, 1-1s, Touchpoint, Team Lead Briefing) — those are explicitly "team meetings" under the guide's Non-project definition, not project work.
   - **Not included**: Eng Initiatives Sync (FinOps+EngOps) and the Service Catalog review — per your correction, these are engineering-initiative work, not generic non-project time. They're held in a separate **`PENDING-ENG-TICKET`** placeholder (1.5h total) until you create the dedicated ticket.
3. **Kept as project time**: EPIC/Technical-Design walkthroughs and Sprint Planning stay split across the relevant stories by story points — the guide's Project-related Time section says planning/design work for an Epic should be logged against tasks under that Epic, so this is the closest available proxy (see flag below — ideally these move to dedicated Epic-level planning tasks if you have them).
4. **Rebalanced ZOL-7394/ZOL-6968/ZOL-7424 (2026-07-17 correction)**: these three had absorbed most of the unattributed "story-point pool" dev hours (25.0h, 11.5h and 4.5h of pure guesswork respectively), inflating their totals. Trimmed each to a small baseline (6.0h / 4.0h / 2.0h of that placeholder pool) and moved the freed 19.0h / 3.0h / 2.5h to: **ZOL-6775** (ZOL-6968's real parent epic, gets 100% of its freed time), and for ZOL-7394+ZOL-7424's combined 21.5h — **ZOL-6930** (their parent epic, ~40%) and **ZOL-6960/ZOL-6941** (~30% each, both capped at 25h, per your instruction to prefer those over the epic). PR-evidenced hours (ZOL-7424's PR #831 day, ZOL-6968's PR #855 day) and explicit Toggl labels were left untouched — only the unevidenced pool moved. Done per-day so daily Toggl reconciliation still holds exactly.
5. **2026-07-17**: 10 Toggl entries, mostly with explicit ticket numbers this time — used as-is per your instruction: `ZOL-6968` (dev), `ZOL-6971` "Track Launch Epic" (logged directly against the epic), `ZOL-7534` (meeting), `ZOL-4295` (non-project standup). The two `FinOps meeting` entries stay unassigned in **`PENDING-ENG-TICKET`**, per your instruction. One catch-all entry recurring 3 times ("Zoleo Track work + RBAC Epic + EIS Cache Epic + Team Leading work", 4.03h combined) was split evenly across its 4 named buckets: **ZOL-5836** (Zoleo Track work), **ZOL-6775** (RBAC Epic), **ZOL-6930** (EIS Cache Epic — there's no ticket literally named this; ZOL-6930 is the real epic housing both the EIP-cache work and the EIS/EngageIP-indexing spike, so I mapped it there), **ZOL-4295** (Team Leading work). No weighting was given for this split — flagged below. The standalone "Track discussion meeting" (45min) was classified like other Track-topic meetings earlier in this report → ZOL-5836.

## Reconciliation summary

| | Hours |
|---|---|
| Raw Toggl total (Jul 1–17, exact) | 106.05h |
| Logged total after rounding to nearest 30 min (per day) | **105.50h** |
| Rounding delta | −0.55h (≈0.5%) |

Raw daily Toggl totals, for reference:

| Date | Toggl total | Meeting/CSV hours | Dev/other hours |
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
| 2026-07-16 | 7.62h | 1.33h (CSV) — actual entries used directly, see below | 6.28h |
| 2026-07-17 | 9.37h | — actual entries used directly, see below | 9.37h |
| **Total** | **106.05h** | | |

## Methodology

1. **Meetings, Jul 2–15** (`july_meetings.csv`), classified per the new policy:
   - **Epic/Sprint planning** (EPIC Walkthroughs ×2, Technical Design Walkthroughs ×2, Sprint Planning): project time, split across the 5 "new cycle" tickets by story points (ZOL-6968:3, ZOL-7394:3, ZOL-7424:2, ZOL-6960:1, ZOL-6941:1 = 10 points).
   - **Generic ceremonies** (standups, 1-1s, Touchpoint, Team Lead Briefing) → **ZOL-4295** (non-project, per the guide).
   - **Non-ZOLEO/org, engineering-initiative meetings** (Eng Initiatives Sync – FinOps+EngOps; Service Catalog review) → **`PENDING-ENG-TICKET`** placeholder, **not** ZOL-4295 — per your correction, you'll create a dedicated ticket for these.
   - **Topic-matched**: "MyZOLEO testing / launch plan" → **ZOL-5836** (production-release ticket, topic match).

2. **2026-07-16**: you'd added descriptions to most Toggl entries, so these were used directly instead of inference:
   - `ZOL-6968: Zoleo Track URL updates` (47min) → ZOL-6968, dev.
   - `Team lead stuff. reviewing tickets etc` (120min), `Standup` (30min), `KT Meeting with product` (30min) → ZOL-4295, non-project.
   - `meeting: Pricing plan and track deployment walkthrough` (30min) + `track - launch go or no go meeting` (30min) → ZOL-5836 (both explicitly about the Track/production-release deployment).
   - **3 undescribed entries (170min total)**: split 50/50 between "team leading activities" (→ ZOL-4295) and "currently in-progress tickets" (→ ZOL-5836 and ZOL-7424, the two tickets in "In Progress" status as of today, weighted by story points 1:2). This 50/50 split is my judgement call, not specified by you — flagged below.

3. **Dev/other hours, Jul 1–15**, per your explicit direction (unchanged from v2):
   - ZOL-7424: 1 full day (2026-07-09, PR #831).
   - ZOL-6968: half a day (half of 2026-07-15, PR #855).
   - ZOL-6961: 0 hours.
   - ZOL-5836: capped at 8h total; the days with zero PR/Jira evidence (07-01, 02, 03, 06, 07, half of 07-15) had their dev pool redistributed across the other 5 active tickets by story points once ZOL-5836's share was capped.
   - Remaining days (07-08, 10, 13, 14): split by story points across the 3 **Done** tickets (ZOL-7394:3, ZOL-6941:1, ZOL-6960:1).

4. **Rounding**: each day's entries rounded to the nearest 30 minutes, with drift absorbed into that day's largest entry so the day's total matches its own nearest-half-hour target exactly.

## Per-ticket summary

| Ticket | Type / Status | Points | Summary | Dev hrs | Meeting hrs | Non-project hrs | Total hrs |
|---|---|---|---|---|---|---|---|
| **ZOL-6968** | Story / To Do | 3 | [CS][BE-4b] Lazy-upsert auto-provision + GET /cs/me [P1] | 11.0h | 4.0h | 0.0h | **15.0h** |
| **ZOL-6941** | Story / Done | 1 | [MyZ][FE-2] Account Balance: build header from GET /users/eip-details | 14.5h | 0.0h | 0.0h | **14.5h** |
| **ZOL-6960** | Story / Done | 1 | [MyZ][SPIKE-3] Billing Performance: EIP read caching strategy | 14.5h | 0.0h | 0.0h | **14.5h** |
| **ZOL-5836** | Story / In Progress | 1 | [Track] WLT link forwarding for Production release | 9.5h | 2.5h | 0.0h | **12.0h** |
| **ZOL-7424** | Story / **In Progress** | 2 | [MyZ][EIP-Cache-01] EIP read cache: Redis client factory refactor + eipCacheClient | 9.5h | 2.5h | 0.0h | **12.0h** |
| **ZOL-7394** | Task / Done | 3 | Add workflows to auto-assign PR reviews (+ Slack digest) | 6.0h | 4.0h | 0.0h | **10.0h** |
| **ZOL-4295** | Epic / To Do | — | ZOL misc time reporting (non-project / Opex) | 0.0h | 0.0h | 10.0h | **10.0h** |
| **ZOL-6930** | Epic / In Progress | — | [MyZ] Account: Billing & Payment Management — parent epic of ZOL-7424/6960/6941; also receiving ZOL-7394's excess + a share of Jul-17's "EIS Cache Epic" catch-all | 9.5h | 0.0h | 0.0h | **9.5h** |
| **ZOL-6775** | Epic / In Progress | — | [CS] Role-Based Access Control & Admin UI — ZOL-6968's real parent epic | 4.0h | 0.0h | 0.0h | **4.0h** |
| **PENDING-ENG-TICKET** *(no ticket yet)* | — | — | Eng Initiatives Sync (FinOps+EngOps) + Service Catalog review + FinOps Weekly Follow-up ×2 — awaiting a dedicated engineering-initiative ticket | 0.0h | 2.5h | 0.0h | **2.5h** |
| **ZOL-6971** | Epic / Draft | — | Track launch | 1.0h | 0.0h | 0.0h | **1.0h** |
| **ZOL-7534** | Story / To Do | — | [MyZ] Implement region based logic for myzoleo New UI | 0.0h | 0.5h | 0.0h | **0.5h** |
| **ZOL-6961** | Story / To Do | 2 | [MyZ][SPIKE-4] Billing Performance: EIS/EngageIP database indexing | 0.0h | 0.0h | 0.0h | **0.0h** |
| **TOTAL** | | | | **79.5h** | **16.0h** | **10.0h** | **105.5h** |

*Note: ZOL-6941 and ZOL-6960's small Epic-walkthrough meeting shares (~0.1–0.25h/day each) rounded away to 0 under 30-min-per-day rounding — a side effect of the coarser granularity, not an error.*

*Note on the 2026-07-17 rebalance: ZOL-6968's actual freed pool was only 3.0h (not the ~7.5h I first estimated), because most of what I originally counted as "ZOL-6968 placeholder" was actually its PR #855 evidence merged into the same day's row — I've now kept that PR-evidenced time fully intact and only moved the genuinely-unevidenced portion. ZOL-6775 ends up smaller than my initial estimate as a result.*

## Day-by-day detail (ready for Tempo entry, pending your sign-off)

| Date | Ticket | Type | Hours | Notes |
|---|---|---|---|---|
| 2026-07-01 | ZOL-5836 | Dev | 1.00h | Capped per your 8h instruction |
| 2026-07-01 | ZOL-6775 | Dev | 1.00h | Excess dev time freed from ZOL-6968 this day, moved to ZOL-6775 (its real parent epic) — per your 2026-07-17 instruction |
| 2026-07-01 | ZOL-6941 | Dev | 1.50h | Redistributed share of ZOL-5836 reduction (story-point split, best-judgement placeholder) + excess dev time freed from ZOL-7394 this day, moved here instead of the parent epic (within 25h cap) |
| 2026-07-01 | ZOL-6960 | Dev | 0.50h | Redistributed share of ZOL-5836 reduction (story-point split, best-judgement placeholder) |
| 2026-07-01 | ZOL-6968 | Dev | 0.50h | Redistributed share of ZOL-5836 reduction (story-point split, best-judgement placeholder), scaled down 2026-07-17 |
| 2026-07-01 | ZOL-7394 | Dev | 0.50h | Redistributed share of ZOL-5836 reduction (story-point split, best-judgement placeholder), scaled down 2026-07-17 |
| 2026-07-01 | ZOL-7424 | Dev | 1.00h | Redistributed share of ZOL-5836 reduction (story-point split, best-judgement placeholder), scaled down 2026-07-17 |
| 2026-07-02 | ZOL-5836 | Dev | 1.00h | Capped per your 8h instruction |
| 2026-07-02 | ZOL-6775 | Dev | 0.50h | Excess dev time freed from ZOL-6968 this day, moved to ZOL-6775 (its real parent epic) — per your 2026-07-17 instruction |
| 2026-07-02 | ZOL-6930 | Dev | 1.00h | Excess dev time freed from ZOL-7394 this day, moved to ZOL-6930 (parent epic of ZOL-7424/6960/6941; ZOL-7394 itself has no Jira parent, but you confirmed routing its share here) |
| 2026-07-02 | ZOL-6941 | Dev | 1.00h | Redistributed share of ZOL-5836 reduction (story-point split, best-judgement placeholder) + excess dev time freed from ZOL-7424 this day, moved here instead of the parent epic (within 25h cap) |
| 2026-07-02 | ZOL-6960 | Dev | 0.50h | Redistributed share of ZOL-5836 reduction (story-point split, best-judgement placeholder) |
| 2026-07-02 | ZOL-6968 | Dev | 0.50h | Redistributed share of ZOL-5836 reduction (story-point split, best-judgement placeholder), scaled down 2026-07-17 |
| 2026-07-02 | ZOL-6968 | Meeting | 1.00h | ZOLEO Detailed EPIC Walkthrough (New Cycle) — share by story points 3/10 |
| 2026-07-02 | ZOL-7394 | Meeting | 1.00h | ZOLEO Detailed EPIC Walkthrough (New Cycle) — share by story points 3/10 |
| 2026-07-02 | ZOL-7424 | Meeting | 0.50h | ZOLEO Detailed EPIC Walkthrough (New Cycle) — share by story points 2/10 |
| 2026-07-03 | PENDING-ENG-TICKET | Meeting | 1.00h | Eng Initiatives Sync - FinOps + EngOps — engineering-initiative meeting, awaiting dedicated ticket |
| 2026-07-03 | ZOL-5836 | Dev | 2.00h | Capped per your 8h instruction |
| 2026-07-03 | ZOL-6775 | Dev | 0.50h | Excess dev time freed from ZOL-6968 this day, moved to ZOL-6775 (its real parent epic) — per your 2026-07-17 instruction |
| 2026-07-03 | ZOL-6930 | Dev | 2.00h | Excess dev time freed from ZOL-7394 this day (ZOL-7394 has no Jira parent, routed here per your instruction) + excess freed from ZOL-7424 this day (ZOL-6930 is ZOL-7424's actual parent epic) |
| 2026-07-03 | ZOL-6941 | Dev | 0.50h | Redistributed share of ZOL-5836 reduction (story-point split, best-judgement placeholder) |
| 2026-07-03 | ZOL-6960 | Dev | 0.50h | Redistributed share of ZOL-5836 reduction (story-point split, best-judgement placeholder) |
| 2026-07-03 | ZOL-6968 | Dev | 1.00h | Redistributed share of ZOL-5836 reduction (story-point split, best-judgement placeholder), scaled down 2026-07-17 |
| 2026-07-03 | ZOL-6968 | Meeting | 1.00h | ZOLEO Detailed EPIC Walkthrough (New Cycle) — share by story points 3/10 |
| 2026-07-03 | ZOL-7394 | Dev | 0.50h | Redistributed share of ZOL-5836 reduction (story-point split, best-judgement placeholder), scaled down 2026-07-17 |
| 2026-07-03 | ZOL-7394 | Meeting | 1.00h | ZOLEO Detailed EPIC Walkthrough (New Cycle) — share by story points 3/10 |
| 2026-07-03 | ZOL-7424 | Dev | 0.50h | Redistributed share of ZOL-5836 reduction (story-point split, best-judgement placeholder), scaled down 2026-07-17 |
| 2026-07-03 | ZOL-7424 | Meeting | 0.50h | ZOLEO Detailed EPIC Walkthrough (New Cycle) — share by story points 2/10 |
| 2026-07-06 | ZOL-4295 | Non-project | 0.50h | Generic team ceremony (1-1) — non-project per policy |
| 2026-07-06 | ZOL-5836 | Dev | 1.00h | Capped per your 8h instruction |
| 2026-07-06 | ZOL-6775 | Dev | 0.50h | Excess dev time freed from ZOL-6968 this day, moved to ZOL-6775 (its real parent epic) — per your 2026-07-17 instruction |
| 2026-07-06 | ZOL-6930 | Dev | 0.50h | Excess dev time freed from ZOL-7424 this day, moved to ZOL-6930 (ZOL-7424's actual parent epic) |
| 2026-07-06 | ZOL-6941 | Dev | 0.50h | Redistributed share of ZOL-5836 reduction (story-point split, best-judgement placeholder) |
| 2026-07-06 | ZOL-6960 | Dev | 1.50h | Redistributed share of ZOL-5836 reduction (story-point split, best-judgement placeholder) + excess dev time freed from ZOL-7394 this day, moved here instead of the parent epic (within 25h cap) |
| 2026-07-06 | ZOL-6968 | Dev | 0.50h | Redistributed share of ZOL-5836 reduction (story-point split, best-judgement placeholder), scaled down 2026-07-17 |
| 2026-07-06 | ZOL-6968 | Meeting | 1.00h | ZOLEO EPIC's Technical Design's Walkthrough — share by story points 3/10 |
| 2026-07-06 | ZOL-7394 | Meeting | 1.00h | ZOLEO EPIC's Technical Design's Walkthrough — share by story points 3/10 |
| 2026-07-06 | ZOL-7424 | Meeting | 0.50h | ZOLEO EPIC's Technical Design's Walkthrough — share by story points 2/10 |
| 2026-07-07 | ZOL-5836 | Dev | 2.00h | Capped per your 8h instruction |
| 2026-07-07 | ZOL-6775 | Dev | 0.50h | Excess dev time freed from ZOL-6968 this day, moved to ZOL-6775 (its real parent epic) — per your 2026-07-17 instruction |
| 2026-07-07 | ZOL-6941 | Dev | 1.50h | Redistributed share of ZOL-5836 reduction (story-point split, best-judgement placeholder) + excess dev time freed from ZOL-7394 this day, moved here instead of the parent epic (within 25h cap) |
| 2026-07-07 | ZOL-6960 | Dev | 1.00h | Redistributed share of ZOL-5836 reduction (story-point split, best-judgement placeholder) + excess dev time freed from ZOL-7424 this day, moved here instead of the parent epic (within 25h cap) |
| 2026-07-07 | ZOL-6968 | Dev | 1.00h | Redistributed share of ZOL-5836 reduction (story-point split, best-judgement placeholder), scaled down 2026-07-17 |
| 2026-07-07 | ZOL-6968 | Meeting | 0.50h | ZOLEO EPIC's Technical Design's Walkthrough — share by story points 3/10 |
| 2026-07-07 | ZOL-7394 | Dev | 0.50h | Redistributed share of ZOL-5836 reduction (story-point split, best-judgement placeholder), scaled down 2026-07-17 |
| 2026-07-07 | ZOL-7394 | Meeting | 0.50h | ZOLEO EPIC's Technical Design's Walkthrough — share by story points 3/10 |
| 2026-07-07 | ZOL-7424 | Dev | 0.50h | Redistributed share of ZOL-5836 reduction (story-point split, best-judgement placeholder), scaled down 2026-07-17 |
| 2026-07-07 | ZOL-7424 | Meeting | 0.50h | ZOLEO EPIC's Technical Design's Walkthrough — share by story points 2/10 |
| 2026-07-08 | ZOL-6930 | Dev | 4.00h | Excess dev time freed from ZOL-7394 this day, moved to ZOL-6930 (parent epic of ZOL-7424/6960/6941; ZOL-7394 itself has no Jira parent, but you confirmed routing its share here) |
| 2026-07-08 | ZOL-6941 | Dev | 1.50h | Done; story-point share of unattributed dev pool |
| 2026-07-08 | ZOL-6960 | Dev | 1.50h | Done; story-point share of unattributed dev pool |
| 2026-07-08 | ZOL-6968 | Meeting | 0.50h | ZOLEO Story and Sprint Planning Session — share by story points 3/10 |
| 2026-07-08 | ZOL-7394 | Dev | 1.00h | Done; story-point share of unattributed dev pool, scaled down 2026-07-17 |
| 2026-07-08 | ZOL-7394 | Meeting | 0.50h | ZOLEO Story and Sprint Planning Session — share by story points 3/10 |
| 2026-07-08 | ZOL-7424 | Meeting | 0.50h | ZOLEO Story and Sprint Planning Session — share by story points 2/10 |
| 2026-07-09 | ZOL-4295 | Non-project | 1.00h | Touchpoint + Standup — non-project per policy |
| 2026-07-09 | ZOL-7424 | Dev | 6.50h | PR #831 opened this day; user-directed 1 full day (evidenced — untouched by the 2026-07-17 rebalance) |
| 2026-07-10 | PENDING-ENG-TICKET | Meeting | 0.50h | Service Catalog review — engineering-initiative meeting, awaiting dedicated ticket |
| 2026-07-10 | ZOL-4295 | Non-project | 0.50h | Standup — non-project per policy |
| 2026-07-10 | ZOL-6941 | Dev | 5.00h | Done; story-point share of unattributed dev pool + excess dev time freed from ZOL-7394 this day, moved here instead of the parent epic (within 25h cap) |
| 2026-07-10 | ZOL-6960 | Dev | 1.50h | Done; story-point share of unattributed dev pool |
| 2026-07-10 | ZOL-7394 | Dev | 2.00h | Done; story-point share of unattributed dev pool, scaled down 2026-07-17 |
| 2026-07-13 | ZOL-4295 | Non-project | 1.50h | 1-1 + Standup + Team Lead Briefing — non-project per policy |
| 2026-07-13 | ZOL-5836 | Meeting | 0.50h | MyZOLEO testing / launch plan — topic matches ZOL-5836 production-release tracking |
| 2026-07-13 | ZOL-6930 | Dev | 1.00h | Excess dev time freed from ZOL-7394 this day, moved to ZOL-6930 (parent epic of ZOL-7424/6960/6941; ZOL-7394 itself has no Jira parent, but you confirmed routing its share here) |
| 2026-07-13 | ZOL-6941 | Dev | 0.50h | Done; story-point share of unattributed dev pool |
| 2026-07-13 | ZOL-6960 | Dev | 0.50h | Done; story-point share of unattributed dev pool |
| 2026-07-13 | ZOL-7394 | Dev | 0.50h | Done; story-point share of unattributed dev pool, scaled down 2026-07-17 |
| 2026-07-14 | ZOL-4295 | Non-project | 0.50h | Standup — non-project per policy |
| 2026-07-14 | ZOL-6941 | Dev | 1.50h | Done; story-point share of unattributed dev pool |
| 2026-07-14 | ZOL-6960 | Dev | 5.50h | Done; story-point share of unattributed dev pool + excess dev time freed from ZOL-7394 this day, moved here instead of the parent epic (within 25h cap) |
| 2026-07-14 | ZOL-7394 | Dev | 1.00h | Done; story-point share of unattributed dev pool, scaled down 2026-07-17 |
| 2026-07-15 | ZOL-4295 | Non-project | 0.50h | Standup — non-project per policy |
| 2026-07-15 | ZOL-5836 | Dev | 1.00h | Capped per your 8h instruction |
| 2026-07-15 | ZOL-6941 | Dev | 1.00h | Redistributed share of ZOL-5836 reduction (story-point split, best-judgement placeholder) + excess dev time freed from ZOL-7424 this day, moved here instead of the parent epic (within 25h cap) |
| 2026-07-15 | ZOL-6960 | Dev | 1.50h | Redistributed share of ZOL-5836 reduction (story-point split, best-judgement placeholder) + excess dev time freed from ZOL-7394 this day, moved here instead of the parent epic (within 25h cap) |
| 2026-07-15 | ZOL-6968 | Dev | 5.00h | PR #855 opened this day (half-day, user-directed, 4.5h protected) + 0.5h of that day's ZOL-5836-redistribution placeholder, which rounded back to its original amount after scaling (no net change) |
| 2026-07-16 | ZOL-4295 | Non-project | 4.00h | "Team lead stuff. reviewing tickets etc" + Standup + KT Meeting with product + half of undescribed time |
| 2026-07-16 | ZOL-5836 | Dev | 0.50h | Half of undescribed time, split across in-progress tickets by story points (1/3) |
| 2026-07-16 | ZOL-5836 | Meeting | 1.00h | "Pricing plan and track deployment walkthrough" + "track - launch go or no go meeting" — both topic-match ZOL-5836 |
| 2026-07-16 | ZOL-6968 | Dev | 1.00h | Explicitly labeled "ZOL-6968: Zoleo Track URL updates" |
| 2026-07-16 | ZOL-7424 | Dev | 1.00h | Half of undescribed time, split across in-progress tickets by story points (2/3) |
| 2026-07-17 | PENDING-ENG-TICKET | Meeting | 1.00h | "FinOps meeting -- Weekly Follow up meeting" ×2 — FinOps/eng-initiative, left unassigned per your instruction; you'll create the ticket |
| 2026-07-17 | ZOL-4295 | Non-project | 1.50h | Share of catch-all entry "Zoleo Track work + RBAC Epic + EIS Cache Epic + Team Leading work" (Team Leading quarter, evenly split, no weights given) + explicitly labeled "ZOL-4295: Misc. Meeting -- Standup" |
| 2026-07-17 | ZOL-5836 | Dev | 1.00h | Share of catch-all entry "Zoleo Track work + RBAC Epic + EIS Cache Epic + Team Leading work" (Zoleo Track work quarter, evenly split, no weights given) |
| 2026-07-17 | ZOL-5836 | Meeting | 1.00h | "Track discussion meeting" — topic matches ZOL-5836 (Track/production release), same classification used for other Track meetings in this report |
| 2026-07-17 | ZOL-6775 | Dev | 1.00h | Share of catch-all entry "Zoleo Track work + RBAC Epic + EIS Cache Epic + Team Leading work" (RBAC Epic quarter, evenly split, no weights given) |
| 2026-07-17 | ZOL-6930 | Dev | 1.00h | Share of catch-all entry "Zoleo Track work + RBAC Epic + EIS Cache Epic + Team Leading work" (EIS Cache Epic quarter — ZOL-6930 is the real epic housing both the EIP-cache work and the EIS/EngageIP-indexing spike; evenly split, no weights given) |
| 2026-07-17 | ZOL-6968 | Dev | 1.50h | Explicitly labeled "ZOL-6968: CS RBAC Lazy upsert" |
| 2026-07-17 | ZOL-6971 | Dev | 1.00h | Explicitly labeled "ZOL-6971: Track Launch Epic" — logged directly against the epic per your instruction to use ticket numbers as-is |
| 2026-07-17 | ZOL-7534 | Meeting | 0.50h | Explicitly labeled "ZOL-7534: Region based billing -- Meeting" |
| — | ZOL-6961 | — | 0.00h | Explicitly excluded per your instruction |

## Flags — please review before syncing to Tempo

1. **ZOL-5836 still capped at 8h** for Jul 1–15 (per your earlier instruction), with 27.25h of unattributed early-week time spread across 5 other tickets by story points — this remains a soft placeholder, not evidence. Jul 16 activity is added on top (1.5h meeting + 0.5h undescribed-time share = 2.0h more), so ZOL-5836's Jul1-16 total is 10.0h. (ZOL-5836 was untouched by the 2026-07-17 rebalance below.)
2. **`PENDING-ENG-TICKET` (1.5h)**: Eng Initiatives Sync (Jul 3, 1.0h) and Service Catalog review (Jul 10, 0.5h) are held against this placeholder, not ZOL-4295, per your correction. Once you create the real ticket, swap this label for the ticket key before syncing to Tempo.
3. **The Jul 16 undescribed-time split (170min, 50/50 between ZOL-4295 and in-progress tickets, then 1:2 by points between ZOL-5836/ZOL-7424) is my judgement call** — you said "divide... among team leading activities and my currently in progress tickets" without a ratio. Tell me if you want a different split.
4. **Account field**: the guide requires every ticket you log time against to have an "Account" value set (Capital vs Opex classification) — I haven't verified this for any ticket in this report, including the two new epic entries (ZOL-6930, ZOL-6775). Worth a quick check in Jira before syncing, since Tempo entries against tickets without an Account may get flagged by whoever audits this.
5. **Epic/Sprint-planning meetings (11h total) are still split across specific stories by story points**, not logged against a dedicated Epic-level planning task — the guide implies those should exist ("Most Epics should have tasks representing the planning... work"). If you have those tickets, tell me and I'll re-route this time there instead. (These meeting-hour rows were **not** touched by the 2026-07-17 rebalance — only unevidenced dev-hour placeholders moved.)
6. **PR search only covered `roadpostinc/MyZoleo`** via `gh search prs --author=@me`. If you also contribute to `ZMA` or another repo/account, that work isn't captured.
7. **96.00h vs 96.68h raw** — the −0.68h delta is from nearest-30-min rounding per day (some days round down now, not just up, per the guide's actual rule). If you want this tightened, I can bias rounding within a day.
8. **ZOL-6930/ZOL-6775 dev-hour entries (2026-07-17 rebalance) are pure redistribution, not evidence of work actually done on those epics** — same caveat as the story-point placeholders they replaced. If you have real evidence (PRs, Jira activity) for epic-level work on specific days, tell me and I'll swap it in instead of the redistributed estimate.
9. **The 40% epic / 30% ZOL-6960 / 30% ZOL-6941 split** (for ZOL-7394+ZOL-7424's freed hours) was assigned per-day using whole-day chunks (to keep entries clean 30-min multiples and preserve daily Toggl reconciliation), not a literal 40/30/30 split of every single day — the aggregate lands at 8.5h/6.5h/6.5h (39.5%/30.2%/30.2%), close enough to be a rounding artifact, not a methodology error.
10. **ZOL-6941 has no explicit cap from you** — I mirrored ZOL-6960's 25h cap since both are 1-point Done tickets with an identical profile. Current total is 14.5h, well under that. Tell me if you'd rather use a different ceiling.
11. **"EIS Cache Epic" (2026-07-17) doesn't exist as a literal ticket** — I mapped it to **ZOL-6930**, the real epic that houses both the EIP-cache work (ZOL-7424 and its siblings) and the EIS/EngageIP-indexing spike (ZOL-6961). The only ticket actually named for EIP caching, ZOL-7419, is Canceled. If you meant a different epic, tell me and I'll re-route that quarter-share.
12. **The 2026-07-17 catch-all split (4.03h across 3 Toggl entries, 4 named buckets) was divided evenly** — no weighting was given in "Zoleo Track work + RBAC Epic + EIS Cache Epic + Team Leading work." If your actual time split across those four wasn't even, tell me the ratio and I'll redo just this day.
13. **`PENDING-ENG-TICKET` is now 2.5h** (added the two 2026-07-17 FinOps Weekly Follow-up entries, 0.5h + 0.4h raw). Still awaiting the real ticket key.
14. **ZOL-6971 ("Track launch") is itself an Epic, currently in Draft status** — I logged its explicitly-labeled hour directly against it per your instruction to use ticket numbers as-is, but logging dev time directly to an Epic (rather than a task under it) is unusual; flagging in case that wasn't intentional.

## Next step

Once you confirm/adjust the flags above, this table can drive the actual Tempo worklog creation (via `JiraTempoAPI.add_worklog`, the same client this repo already uses) — happy to write that sync script next, but nothing has been logged to Tempo yet.
