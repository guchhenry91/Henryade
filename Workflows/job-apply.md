# Daily Job Apply — Field Service Technician (London, £30–34k)

This is a plain-English recipe for the daily job search. It mirrors the remote routine (`Daily-FieldService-Job-Applications`) so I can run it manually if needed.

## Candidate

- **Name:** Adegboyega Ogidan
- **Email:** Adegboyega.Ogid@yahoo.com
- **Phone:** 07506 293 448
- **Location:** Dagenham RM10, East London
- **Target role:** Field Service Technician / Field Service Engineer / Mobile Engineer / On-site Technician
- **Salary band:** £30,000 – £34,000 (hard min £30k)
- **Background:** 10+ years IT support, on-site troubleshooting, hardware, M365, AD, ITIL, CompTIA A+
- **Right to work:** UK
- **Notice:** Immediately available

## Hard freshness rule — read first

ONLY include jobs posted within the last 48 HOURS from today.

- Acceptable: 'today', 'just posted', 'new', '1 hour ago', '12 hours ago', '1 day ago', '2 days ago'
- REJECT: '3 days ago' or older, anything '4 days ago', 'last week', expired/closed listings, or any listing without a visible posted date.

Quality over volume: 5 fresh jobs > 30 stale ones.

## Step 1 — LinkedIn (48h filter)

Fetch (fall back to WebSearch on 403):

- https://www.linkedin.com/jobs/search/?keywords=Field+Service+Technician&location=London&f_TPR=r172800&f_AL=true&sortBy=DD
- https://www.linkedin.com/jobs/search/?keywords=Field+Service+Engineer&location=London&f_TPR=r172800&f_AL=true&sortBy=DD
- https://www.linkedin.com/jobs/search/?keywords=Mobile+Engineer&location=London&f_TPR=r172800&f_AL=true&sortBy=DD
- https://www.linkedin.com/jobs/search/?keywords=Onsite+Technician&location=London&f_TPR=r172800&f_AL=true&sortBy=DD

`f_TPR=r172800` = posted ≤48h. Do not widen.

## Step 2 — Reed (LastThreeDays + manual filter to ≤48h)

- https://www.reed.co.uk/jobs/field-service-technician-jobs-in-london?datecreatedoffset=LastThreeDays&salaryFrom=30000&fulltime=True
- https://www.reed.co.uk/jobs/field-service-engineer-jobs-in-london?datecreatedoffset=LastThreeDays&salaryFrom=30000&fulltime=True
- https://www.reed.co.uk/jobs/mobile-engineer-jobs-in-london?datecreatedoffset=LastThreeDays&salaryFrom=30000&fulltime=True

Manually skip anything '3 days ago'. Reed only accepts these `datecreatedoffset` values: Today, Yesterday, LastThreeDays, LastWeek.

## Step 3 — TotalJobs (postedWithin=2 = 48h)

- https://www.totaljobs.com/jobs/field-service-technician/in-london?postedWithin=2&salary=30000&salarytype=annual
- https://www.totaljobs.com/jobs/field-service-engineer/in-london?postedWithin=2&salary=30000&salarytype=annual
- https://www.totaljobs.com/jobs/mobile-engineer/in-london?postedWithin=2&salary=30000&salarytype=annual

## Step 4 — Indeed (fromage=2 = 48h)

- https://uk.indeed.com/jobs?q=Field+Service+Technician+%C2%A330000&l=London&fromage=2
- https://uk.indeed.com/jobs?q=Field+Service+Engineer&l=London&fromage=2

## Step 5 — Per-job validation (every job, every check)

1. Posted date ≤48h from today, visible on listing → else SKIP.
2. No expiry indicator ('Expired', 'Closed', 'No longer accepting', 'Closing today') → else SKIP.
3. London / Greater London commutable from Dagenham RM10 within ~1hr → else SKIP.
4. Salary stated ≥£30,000 OR not stated and title clearly indicates field-service tech level → else SKIP.
5. Title matches: Field Service Technician, Field Service Engineer, Mobile Engineer, On-site Technician, Field Technician, IT Field Engineer.
6. Not Senior Manager / Head of / Director level.
7. Not already in `Outputs/job-applications-log.csv` (check Job URL column).

ALL seven must pass.

## Step 6 — Log qualifying jobs

Append to `Outputs/job-applications-log.csv` with columns:

`Date,Job Title,Company,Platform,Salary,Location,Applied (Y/N),Application Method,Job URL,Notes`

- Date = today
- Applied = N
- Application Method = "Needs manual apply"
- Notes MUST include: `Posted: <exact phrasing or date from listing>`
- If salary not stated: prepend `Not stated - verify before applying. ` to Notes

## Step 7 — Commit

```
git add Outputs/job-applications-log.csv
git commit -m "Job applications log — [TODAY DATE] — [N] fresh roles (≤48h)"
git push origin main
```

## Step 8 — Gmail draft summary

Create draft to `guchhenry91@gmail.com`:

- Subject: `Job Shortlist [TODAY DATE] — [N] fresh Field Service roles (posted ≤48h)`
- Body: For each logged job: Title, Company, Salary, Location, Posted-date, URL. State the freshness window (≤48h) at the top. End with manual-apply links.

## Step 9 — Print summary

- Total scanned
- Total logged (passed all 7 checks)
- Total skipped, by reason: stale (>48h) / expired / wrong location / low salary / wrong title / duplicate / missing date
- Any 403 errors and fallback used

## Goal

If a search returns zero ≤48h jobs, log zero and report it honestly. Do NOT pad with stale roles.
