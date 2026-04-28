# Job Application Workflow — Daily Runner

## Overview
Automated daily job application workflow for Adegboyega Ogidan.
Target: 20 applications per day, Monday–Friday.
Start date: Monday 6 April 2026.

---

## Candidate Profile

- **Name:** Adegboyega Ogidan
- **Email:** Adegboyega.Ogid@yahoo.com
- **Phone:** 07506 293 448
- **Location:** Dagenham, London
- **LinkedIn:** linkedin.com/in/adegboyega-ogidan-a81897217
- **Salary minimum:** £33,000
- **CVs:**
  - IT/Service Desk roles → `resources/ADE_IT_Black.pdf`
  - Platform Ops/Broadcast roles → `resources/ADE_Broadcast_CV.pdf`

---

## Target Roles

Search for these job titles (use variations):
- 1st Line IT Support Engineer
- 2nd Line IT Support Engineer
- IT Support Analyst
- Service Desk Analyst
- Service Desk Engineer
- Helpdesk Analyst / IT Helpdesk Officer
- IT Technician
- Desktop Support Engineer
- Platform Operations Analyst (use Broadcast CV)
- NOC Analyst (use Broadcast CV)

---

## Search Parameters

| Parameter | Value |
|---|---|
| Location | London (within ~1hr commute of Dagenham RM10) |
| Salary | £33,000 minimum |
| Job type | Full-time, Contract, Temp-to-perm |
| Date posted | **Last 48 hours — HARD FILTER. Skip anything older.** |
| Platforms | LinkedIn Easy Apply, Reed, TotalJobs |

### Exclude:
- Roles below £33,000
- Roles MUST be inside London — no exceptions (no Watford, Slough, Reading, Croydon outskirts, etc.)
- Senior Manager / Head of IT roles (overqualified mismatch)
- **Anything posted >48h ago. Anything tagged "Expired", "Closing today", or "Closed". Anything without a visible posted date.**

---

## Freshness Validation (MANDATORY before logging)

Before adding any job to the application log, the agent MUST:

1. **Read the posted date** from the listing page (e.g. "Posted 1 day ago", "Posted today", or absolute date).
2. **Reject if older than 48 hours** from current run time.
3. **Reject if any expiry indicator is visible:** "Expired", "No longer accepting applications", "Closed", "Closing today".
4. **If posted date is missing or ambiguous, SKIP the role** — do not guess.
5. Log the posted date in the CSV `Notes` column as `Posted: <date or "X hours ago">` for audit.

Only after a job passes ALL four checks may it be applied to and logged.

---

## Daily Steps

### Step 1 — LinkedIn Easy Apply (48h freshness REQUIRED)

**Use this URL — `f_TPR=r172800` is the 48-hour filter:**
```
https://www.linkedin.com/jobs/search/?keywords=IT%20Support%20OR%20Service%20Desk%20OR%20Helpdesk&location=London&f_AL=true&f_TPR=r172800&f_SB2=4
```
- `f_TPR=r172800` → posted within 48h (use `r86400` for strict 24h)
- `f_AL=true` → Easy Apply only
- `f_SB2=4` → £30k+ salary band (LinkedIn's closest filter, then verify £33k in listing)

1. Open the URL above
2. For each result: open the listing, **verify posted date ≤48h** and salary ≥£33k
3. Apply to up to 10 roles using Easy Apply
4. Use pre-filled profile data + attach `resources/ADE_IT_Black.pdf`
5. Log to `Outputs/job-applications-log.csv` with `Posted: <date>` in Notes

### Step 2 — Reed (48h freshness REQUIRED)

**Use this URL — `datecreatedoffset=LastThreeDays` is the closest Reed offers, then filter manually:**
```
https://www.reed.co.uk/jobs/it-support-engineer-jobs-in-london?datecreatedoffset=LastThreeDays&salaryfrom=33000
```
- Acceptable values: `Today`, `Yesterday`, `LastThreeDays` — NEVER use `LastWeek` or wider
- After loading, manually skip any listing showing >48h ago

1. Open the URL above (and the same URL with keyword swaps for "service-desk-analyst", "2nd-line-support")
2. For each: verify "Posted today" or "Posted 1 day ago" or "Posted 2 days ago" ONLY
3. Apply to up to 5 roles via Reed Direct Apply
4. Attach `resources/ADE_IT_Black.pdf`
5. Log with `Posted: <date>` in Notes

### Step 3 — TotalJobs (48h freshness REQUIRED)

**Use this URL — `postedwithin=2` is the 2-day filter:**
```
https://www.totaljobs.com/jobs/it-support/in-london?salary=33000&salarytype=annual&postedwithin=2
```
- `postedwithin=1` → 24h, `postedwithin=2` → 48h, `postedwithin=3` → 72h (DO NOT exceed 2)

1. Open the URL above (also try `service-desk-analyst`, `2nd-line-support` keyword swaps)
2. For each: verify posted date ≤48h
3. Apply to up to 5 roles
4. Attach `resources/ADE_IT_Black.pdf`
5. Log with `Posted: <date>` in Notes

---

## Application Log Format

Save to: `Outputs/job-applications-log.csv`

Columns:
```
Date, Job Title, Company, Platform, Salary, Location, Applied (Y/N), CV Used, Notes
```

---

## Cover Letter Template

Use this as a base — personalise the company name and role title each time:

> Dear Hiring Manager,
>
> I'm applying for the [ROLE TITLE] position at [COMPANY]. With 10+ years of IT support experience across enterprise and 24/7 service desk environments — including roles at Sky and Hachette UK — I'm confident I can deliver reliable, SLA-driven support from day one.
>
> My background covers Windows 10/11, Active Directory, Microsoft 365, ServiceNow, and ITIL-aligned incident management. I'm based in East London and available immediately.
>
> Please find my CV attached. I'd welcome the opportunity to discuss further.
>
> Kind regards,
> Adegboyega Ogidan
> 07506 293 448 | Adegboyega.Ogid@yahoo.com

---

## Notes
- Always check if role is "Easy Apply" before opening full application
- If application asks for right to work: Yes (UK)
- Notice period: Available immediately
- Preferred shift: Any (available for 24/7 roles)
