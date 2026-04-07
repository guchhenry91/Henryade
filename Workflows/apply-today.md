# Apply Today — Local Browser Workflow

## Trigger phrase
When Adegboyega says **"apply to today's jobs"** — follow these steps.

---

## What this does
Opens Reed, TotalJobs, and LinkedIn job listings one by one.
For each role: fills in the application form using the candidate profile below.
Adegboyega reviews and clicks Submit.

---

## Candidate Profile (use to fill every form)

- **First name:** Adegboyega
- **Last name:** Ogidan
- **Email:** Adegboyega.Ogid@yahoo.com
- **Phone:** 07506 293 448
- **Location:** Dagenham, London, RM10
- **LinkedIn:** linkedin.com/in/adegboyega-ogidan-a81897217
- **Current title:** 1st Line IT Support Engineer
- **Right to work in UK:** Yes
- **Notice period:** Immediately available
- **Salary expectation:** £33,000–£45,000
- **CV file:** resources/ADE_IT_Black.pdf (IT roles) or resources/ADE_Broadcast_CV.pdf (Platform/NOC roles)

---

## Cover Letter (personalise per role)

> Dear Hiring Manager,
>
> I am writing to apply for the [ROLE TITLE] position at [COMPANY]. With over 10 years of IT support experience across enterprise service desk and 24/7 operational environments — including recent roles at Sky and Hachette UK — I am confident I can deliver reliable, SLA-driven support from day one.
>
> My background covers Windows 10/11, Active Directory, Microsoft 365, ServiceNow, and ITIL-aligned incident management. I hold CompTIA A+ and ITIL Foundation certifications. I am based in East London and available immediately.
>
> I would welcome the opportunity to discuss my application further.
>
> Kind regards,
> Adegboyega Ogidan
> 07506 293 448 | Adegboyega.Ogid@yahoo.com

---

## Steps

### 1. Check today's job list
- Open `Outputs/job-applications-log.csv`
- Find all rows where Applied = N and Notes = "Needs browser apply"
- These are today's targets

### 2. For each job (up to 20):
1. Open the Job URL in the browser
2. Click Apply / Easy Apply
3. Fill all form fields using the candidate profile above
4. Paste personalised cover letter
5. Upload CV if required (use ADE_IT_Black.pdf for IT roles, ADE_Broadcast_CV.pdf for Platform/NOC)
6. Tell Adegboyega: "Ready to submit — [Job Title] at [Company]. Click Submit when ready."
7. After confirmation, update the log: Applied = Y, Notes = Submitted

### 3. After all done
- Save the updated log
- Print summary: how many submitted today, how many remaining

---

## Common form fields cheat sheet

| Field | Answer |
|---|---|
| Do you have the right to work in the UK? | Yes |
| Are you currently employed? | No |
| Notice period | Immediately available |
| When can you start? | Immediately |
| Expected salary | £33,000–£45,000 |
| Do you require visa sponsorship? | No |
| Years of experience | 10+ years |
| Do you have ITIL certification? | Yes |
| Do you have CompTIA A+? | Yes |
