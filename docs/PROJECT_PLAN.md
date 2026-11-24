# ApplyEase — Complete Project Plan & System Design

> **ApplyEase: An AI-Powered Job Application Assistant with Smart Autofill**
> TY BSc IT, Semester VI | Academic Year 2026–27
> Team: Gladwin Gomes (2405001) & Ashley A Noronha (2405060)
> Version 2: aligned with the CIA I synopsis (schema additions are listed at the start of Section 6)

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Problem Statement & Goals](#2-problem-statement--goals)
3. [Technology Stack](#3-technology-stack)
4. [High-Level Architecture](#4-high-level-architecture)
5. [Module Breakdown & Feature Specs](#5-module-breakdown--feature-specs)
6. [Database Design](#6-database-design)
7. [API Design](#7-api-design)
8. [AI/ML Pipeline Design](#8-aiml-pipeline-design)
9. [Chrome Extension Architecture](#9-chrome-extension-architecture)
10. [Frontend Page Map & UI Wireframes](#10-frontend-page-map--ui-wireframes)
11. [Security Design](#11-security-design)
12. [Project Structure (Directory Layout)](#12-project-structure-directory-layout)
13. [Development Workflow](#13-development-workflow)
14. [Testing Strategy](#14-testing-strategy)
15. [Deployment Plan](#15-deployment-plan)
16. [Risk Analysis & Mitigation](#16-risk-analysis--mitigation)
17. [12-Week Timeline & Task Ownership](#17-12-week-timeline--task-ownership)
18. [Future Scope / Nice-to-Haves](#18-future-scope--nice-to-haves)

---

## 1. Project Overview

ApplyEase is a **web platform + Chrome browser extension** that helps students and fresh graduates manage their entire job-application lifecycle in one place:

- **Store your profile once** — personal info, education, experience, skills, projects, links.
- **Auto-fill application forms** — the Chrome extension detects fields and maps them to your saved profile.
- **Track every application** — a Kanban board with stages (Saved → Applied → Interview → Offer / Rejected).
- **AI-powered resume tools** — match score against job descriptions, missing keyword suggestions, and AI-generated cover letters.
- **Job board** — browse listings with search & filters.
- **Admin dashboard** — manage users, jobs, companies; view analytics.

### Two Deliverables

| Deliverable | Technology | Purpose |
|---|---|---|
| **Web Application** | Django + DRF + Bootstrap 5 + MySQL | Profile, tracker, job board, AI tools, admin |
| **Chrome Extension** | Manifest V3, JavaScript | Smart autofill on external job application pages |

---

## 2. Problem Statement & Goals

### Problems

| # | Problem |
|---|---------|
| P1 | Applicants re-type the same information (name, education, skills) across dozens of forms |
| P2 | Applications are scattered across emails, spreadsheets, and notes — deadlines and follow-ups are missed |
| P3 | Applicants don't know how well their resume matches a job or which keywords are missing |
| P4 | Writing a tailored cover letter for every job is slow, so most skip it |

### Goals

| Goal | Maps to |
|------|---------|
| One-click autofill of job application forms via browser extension | P1 |
| Centralized Kanban tracker with reminders | P2 |
| AI match score + missing keyword report | P3 |
| LLM-generated cover letter drafts | P4 |

---

## 3. Technology Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| **Language** | Python 3.11+, JavaScript ES6+, HTML5, CSS3, SQL | Core languages for full-stack + extension |
| **Backend** | Django 5.x + Django REST Framework | Rapid development, built-in auth, ORM, admin |
| **Frontend** | Django Templates + Bootstrap 5 + Vanilla JS | Server-rendered pages, responsive UI, no SPA complexity |
| **Browser Extension** | Chrome Manifest V3 (service worker + content script) | Modern Chrome extension standard |
| **Database** | MySQL 8 | Required by synopsis; relational, normalized |
| **AI / NLP** | spaCy, scikit-learn (TF-IDF + cosine similarity) | Resume parsing, match scoring |
| **PDF Parsing** | pdfplumber (primary), PyPDF2 (fallback) | Extract text from uploaded resumes |
| **LLM** | Google Gemini API via the current `google-genai` SDK (free tier) | Cover letter generation. Verify the model name and free-tier limits in Google's docs before pinning them |
| **Scheduled Jobs** | Django management command (`send_reminders`) run by an OS scheduler (cron / Task Scheduler / PythonAnywhere scheduled task) | Email reminders. No Celery or Redis needed, and it works on Windows |
| **Email** | Django `send_mail` + Gmail SMTP (or Mailtrap for dev) | Verification, password reset, reminders |
| **Charts** | Chart.js | Admin analytics dashboard |
| **Version Control** | Git + GitHub | Collaboration, branching, CI |
| **Testing** | Django TestCase, Postman, manual test cases | Unit, API, integration, and manual testing |

---

## 4. High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                          USER'S BROWSER                              │
│                                                                      │
│  ┌─────────────────────┐        ┌──────────────────────────────┐    │
│  │   Chrome Extension   │        │    ApplyEase Web App (Browser)   │    │
│  │  (Manifest V3)       │        │    Django Templates + BS5     │    │
│  │                      │        │                               │    │
│  │  - Content Script    │        │  Pages:                       │    │
│  │    (reads forms,     │        │  - Login / Signup             │    │
│  │     injects values)  │        │  - Dashboard                  │    │
│  │                      │        │  - Profile Editor             │    │
│  │  - Popup UI          │        │  - Job Board                  │    │
│  │    (quick actions)   │        │  - Application Tracker        │    │
│  │                      │        │  - AI Tools (Match/Cover)     │    │
│  │  - Service Worker    │        │  - Admin Dashboard            │    │
│  │    (background API)  │        │                               │    │
│  └──────────┬───────────┘        └──────────────┬────────────────┘    │
│             │ REST API calls                     │ HTTP requests      │
└─────────────┼───────────────────────────────────┼────────────────────┘
              │                                    │
              ▼                                    ▼
┌──────────────────────────────────────────────────────────────────────┐
│                     DJANGO BACKEND SERVER                            │
│                                                                      │
│  ┌────────────────┐  ┌──────────────┐  ┌──────────────────────┐     │
│  │  Django Views   │  │  DRF API     │  │  Django Admin        │     │
│  │  (SSR pages)    │  │  (JSON REST) │  │  (built-in admin)    │     │
│  └───────┬─────────┘  └──────┬───────┘  └──────────┬───────────┘     │
│          │                    │                      │                │
│          ▼                    ▼                      ▼                │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │                    Django ORM (Models)                        │    │
│  └──────────────────────────┬───────────────────────────────────┘    │
│                              │                                       │
│  ┌───────────────────┐      │      ┌─────────────────────────┐      │
│  │  AI / NLP Engine   │      │      │  Email Service           │      │
│  │  - spaCy pipeline  │      │      │  - Verification          │      │
│  │  - TF-IDF scorer   │      │      │  - Password reset        │      │
│  │  - Gemini API      │      │      │  - Reminders             │      │
│  │  - pdfplumber      │      │      │                           │      │
│  └───────────────────┘      │      └─────────────────────────┘      │
│                              │                                       │
└──────────────────────────────┼───────────────────────────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     MySQL 8 DB       │
                    │                      │
                    │  users, profiles,    │
                    │  education, skills,  │
                    │  resumes, jobs,      │
                    │  applications, etc.  │
                    └─────────────────────┘
```

### Request Flow Summary

1. **Web App flow**: Browser → Django View → ORM → MySQL → Template → HTML response
2. **API flow (extension)**: Extension → DRF endpoint (Token Auth) → ORM → MySQL → JSON response
3. **AI flow**: User triggers match/cover → Django view calls AI service → spaCy/sklearn/Gemini processes → result saved to DB → returned to user

---

## 5. Module Breakdown & Feature Specs

### Module 1: Authentication & User Management

| Feature | Description | Priority |
|---------|-------------|----------|
| Signup | Form: full name, email, password, confirm password. Validation: email unique, password strength. | Must |
| Email verification | Send verification link on signup. `email_verified` stays false until the link is clicked and login is blocked until then. `is_active` is reserved for admin deactivation. Resend link supported. | Must |
| Login / Logout | Session-based auth for web. Token auth for the extension using a DRF token with an expiry check (custom `ExpiringTokenAuthentication`, e.g., 7 days). Logout deletes the token. | Must |
| Password reset | "Forgot password" → email link → reset form. | Must |
| Role-based access | Two roles: `applicant`, `admin`. Decorators/mixins restrict views by role. | Must |
| Profile picture | Optional avatar upload (JPEG/PNG, max 2 MB). | Nice |

**Django apps**: `accounts`

**Key models**: `User` (extend `AbstractUser` with `role` field)

**Key views/endpoints**:
- `POST /api/auth/signup/`
- `POST /api/auth/login/` → returns token
- `POST /api/auth/logout/`
- `POST /api/auth/password-reset/`
- `GET /api/auth/verify-email/<token>/`
- `POST /api/auth/resend-verification/`

---

### Module 2: Profile & Resume Manager

| Feature | Description | Priority |
|---------|-------------|----------|
| Profile editor | Sections: personal info, education (multiple), experience (multiple), projects (multiple), skills, links (LinkedIn, GitHub, portfolio). | Must |
| Resume upload | Upload PDF resumes. Mark one as default. Store file on disk, parsed text in DB. | Must |
| Resume parsing | On upload: extract text with pdfplumber → run spaCy and match against the skills dictionary (NER optional) → suggest skills. User confirms/edits. | Must |
| Profile completeness | Progress bar showing % of profile filled. | Nice |

**Django apps**: `profiles`

**Key models**: `Profile`, `Education`, `Experience`, `Project`, `Resume`

**Key endpoints**:
- `GET/PUT /api/profile/` — get/update profile
- `GET/POST /api/profile/education/` — list/add education
- `PUT/DELETE /api/profile/education/<id>/`
- Same pattern for experience, projects
- `GET/POST /api/resumes/` — list/upload resume
- `POST /api/resumes/<id>/parse/` — trigger parsing
- `PUT /api/resumes/<id>/set-default/`

---

### Module 3: Job Board

| Feature | Description | Priority |
|---------|-------------|----------|
| Job listing page | Cards showing: title, company, location, type, skills, posted date. Paginated (20/page). | Must |
| Search | Keyword search on title, company, description (MySQL `FULLTEXT` index, with `icontains` as fallback). | Must |
| Filters | Filter by: location, job type (Full-time/Part-time/Internship/Contract), work mode (On-site/Hybrid/Remote), skills. | Must |
| Job detail page | Full description, required skills, apply link, "Save" button, match score button. | Must |
| Saved jobs | Bookmark jobs. View saved jobs list. | Must |
| Admin: manage jobs | CRUD for jobs, companies. Bulk import from CSV. | Must |
| Job API import | Optional: fetch from open APIs (e.g., Adzuna, Arbeitnow). | Nice |

**Django apps**: `jobs`

**Key models**: `Company`, `Job`, `JobSkill`, `SavedJob`

**Key endpoints**:
- `GET /api/jobs/` — list with search & filter query params
- `GET /api/jobs/<id>/`
- `POST /api/jobs/<id>/save/`
- `GET /api/jobs/saved/`
- Admin: `POST/PUT/DELETE /api/admin/jobs/`

---

### Module 4: Application Tracker

| Feature | Description | Priority |
|---------|-------------|----------|
| Kanban board | Columns: Saved → Applied → Interview → Offer → Rejected. Drag-and-drop to change status. | Must |
| Application detail | Job info, resume used, date applied, notes (editable), cover letter, match score. | Must |
| Add application | From job board ("Apply & Track") or manually (external job URL). | Must |
| Reminders | Set a reminder date per application. Email alert sent on that date. | Must |
| Status history | Log of status changes with timestamps. | Nice |
| Export | Export applications to CSV. | Nice |

**Django apps**: `tracker`

**Key models**: `Application`, `Reminder`, `StatusLog`

**Key endpoints**:
- `GET /api/applications/` — list (filterable by status)
- `POST /api/applications/` — create
- `PUT /api/applications/<id>/` — update (status, notes)
- `POST /api/applications/<id>/reminders/` — set reminder
- `GET /api/applications/board/` — grouped by status (for Kanban)

---

### Module 5: Smart Autofill Chrome Extension

| Feature | Description | Priority |
|---------|-------------|----------|
| Login in extension | Popup UI: enter ApplyEase credentials → receive & store API token. | Must |
| Field detection | Content script scans the page for `<input>`, `<select>`, `<textarea>`. Reads `name`, `id`, `label`, `placeholder`, `aria-label` attributes. | Must |
| Field mapping | Heuristic mapper: matches detected fields to profile data using keyword matching (e.g., "first_name", "fname", "first name" → first name). The profile-data endpoint splits `full_name` into first and last name. | Must |
| Framework-safe filling | Set values with the native value setter and dispatch `input` and `change` events so React/Angular forms register them. | Must |
| On-demand injection | Content script is injected with `chrome.scripting.executeScript` when the user clicks Fill (uses `activeTab`), not on every page. | Must |
| Resume file field | Browsers block programmatic file selection, so the user attaches the resume manually. | Must |
| One-click fill | Popup shows "Fill Form" button → content script fills mapped fields. User reviews before submitting. | Must |
| Post-submit tracking | After user submits, extension popup asks "Log this application?" → creates application in tracker via API. | Must |
| Mock forms | 3–5 mock application forms hosted on our Django app for demo purposes. | Must |
| Mapping config | User can manually correct field mappings; extension remembers corrections per domain. | Nice |

**Extension components**:

| File | Role |
|------|------|
| `manifest.json` | Permissions (`storage`, `activeTab`, `scripting`), allowed API hosts, service worker |
| `popup.html/js` | Login form, "Fill Form" button, "Log Application" button |
| `content.js` | Injected on demand into the active tab; scans fields, fills values |
| `background.js` | Service worker; manages API token, communicates between popup & content script |
| `mapper.js` | Field-to-profile mapping logic |
| `styles.css` | Popup styling |

---

### Module 6: AI Resume Tools

| Feature | Description | Priority |
|---------|-------------|----------|
| Match score | Upload/select resume + select job → TF-IDF cosine similarity → score 0–100. | Must |
| Missing keywords | Keywords in job description absent from resume → listed with suggestions. | Must |
| Cover letter | Profile + job description → Gemini API prompt → draft letter. User can edit & save. | Must |
| Score history | Store past match scores for reference. | Nice |

**Django apps**: `ai_tools`

**Key endpoints**:
- `POST /api/ai/match-score/` — body: `{resume_id, job_id}` → returns score + missing keywords
- `POST /api/ai/cover-letter/` — body: `{application_id}` → returns generated letter
- `GET /api/ai/match-history/`

---

### Module 7: Admin Dashboard & Analytics

| Feature | Description | Priority |
|---------|-------------|----------|
| User management | List users, view profiles, deactivate accounts. | Must |
| Job management | CRUD for companies, jobs, skills. | Must |
| Analytics charts | Total users, applications by status (pie), popular skills (bar), top companies (bar), signups over time (line). | Must |
| Skill management | Master list of skills; merge duplicates. | Nice |

**Django apps**: `dashboard` (admin-specific views beyond Django's built-in admin)

---

## 6. Database Design

> **Differences from the CIA I synopsis (14 tables).** This plan adds three tables: `projects` (the profile module already lists projects), `saved_jobs` (the job board "Save" feature) and `status_logs` (optional, Nice priority). It also adds columns: `users.email_verified`, `profiles.portfolio_url`, `jobs.work_mode`, `applications.external_url`, `resumes.file_name`, `companies.logo_url`, `skills.category`. The synopsis column `users.created_at` is kept. Use this updated schema and ER diagram in the final report, and mention the additions to your guide.

### 6.1 Entity-Relationship Diagram

```
┌──────────┐       1:1       ┌──────────┐      1:M      ┌───────────┐
│  users   │────────────────│ profiles  │──────────────│ education  │
│          │                │           │              └───────────┘
│ user_id  │                │profile_id │      1:M      ┌────────────┐
│ email    │                │ phone     │──────────────│ experience  │
│ password │                │ location  │              └────────────┘
│ role     │                │ linkedin  │      1:M      ┌───────────┐
│ is_active│                │ github    │──────────────│  projects  │
│created_at│                │ summary   │              └───────────┘
└────┬─────┘                └───────────┘
     │
     │ 1:M                   M:M (via user_skills)
     │        ┌──────────────────────────────────────┐
     │        │                                      │
     │   ┌────┴─────┐                         ┌─────┴─────┐
     │   │user_skills│                         │  skills    │
     │   │ user_id   │                         │ skill_id   │
     │   │ skill_id  │                         │ skill_name │
     │   │proficiency│                         └─────┬──────┘
     │   └───────────┘                               │
     │                                               │ M:M (via job_skills)
     │ 1:M          ┌────────────┐    M:1     ┌─────┴──────┐    M:1    ┌───────────┐
     ├─────────────│applications │──────────│    jobs     │──────────│ companies  │
     │             │             │           │            │          │            │
     │             │app_id       │           │ job_id     │          │company_id  │
     │             │status       │           │ title      │          │company_name│
     │             │applied_date │           │ description│          │ website    │
     │             │notes        │           │ location   │          │ industry   │
     │             └──┬───┬──────┘           │ job_type   │          └────────────┘
     │                │   │                  │ apply_url  │
     │                │   │ 1:M              │ posted_date│
     │ 1:M            │   └──────┐           │ status     │
┌────┴─────┐    M:1   │    ┌─────┴────┐      └────────────┘
│ resumes  │◄─────────┘    │reminders │
│          │               │          │
│resume_id │               │remind_on │
│file_path │               │message   │
│parsed_txt│               │is_sent   │
│is_default│               └──────────┘
│uploaded  │
└──────────┘

     ┌──────────────┐          ┌──────────────┐
     │ match_scores  │          │cover_letters  │
     │ match_id      │          │ letter_id     │
     │ user_id (FK)  │          │ app_id (FK)   │
     │ job_id (FK)   │          │ content       │
     │ resume_id(FK) │          │ created_at    │
     │ score         │          └───────────────┘
     │ missing_keys  │
     │ generated_at  │
     └───────────────┘

     ┌──────────────┐          ┌──────────────┐
     │  saved_jobs   │          │ status_logs   │
     │ user_id (FK)  │          │ log_id        │
     │ job_id (FK)   │          │ app_id (FK)   │
     │ saved_at      │          │ old_status    │
     └───────────────┘          │ new_status    │
     (users M:M jobs)           │ changed_at    │
                                └───────────────┘
```

### 6.2 Table Definitions

> **Implementation note:** Django's custom user model names its columns `id`, `password` and `date_joined`. The names below are the logical design used in the ER diagram and report. Either map them with `db_column` or note in the report that Django generates the physical names. The profile-data endpoint exposes `first_name` and `last_name` by splitting `full_name`.

#### `users`
| Column | Type | Constraints |
|--------|------|-------------|
| `user_id` | INT AUTO_INCREMENT | PK |
| `full_name` | VARCHAR(150) | NOT NULL |
| `email` | VARCHAR(254) | UNIQUE, NOT NULL |
| `password_hash` | VARCHAR(128) | NOT NULL (Django PBKDF2 hash) |
| `role` | ENUM('applicant','admin') | DEFAULT 'applicant' |
| `email_verified` | BOOLEAN | DEFAULT FALSE (login blocked until TRUE) |
| `is_active` | BOOLEAN | DEFAULT TRUE (admin can deactivate) |
| `created_at` | DATETIME | DEFAULT NOW() (Django: `date_joined`) |

#### `profiles`
| Column | Type | Constraints |
|--------|------|-------------|
| `profile_id` | INT AUTO_INCREMENT | PK |
| `user_id` | INT | FK → users, UNIQUE, ON DELETE CASCADE |
| `phone` | VARCHAR(15) | NULL |
| `location` | VARCHAR(100) | NULL |
| `linkedin_url` | VARCHAR(500) | NULL |
| `github_url` | VARCHAR(500) | NULL |
| `portfolio_url` | VARCHAR(500) | NULL |
| `summary` | TEXT | NULL |

#### `education`
| Column | Type | Constraints |
|--------|------|-------------|
| `edu_id` | INT AUTO_INCREMENT | PK |
| `profile_id` | INT | FK → profiles, ON DELETE CASCADE |
| `institution` | VARCHAR(200) | NOT NULL |
| `degree` | VARCHAR(100) | NOT NULL |
| `field_of_study` | VARCHAR(100) | NULL |
| `start_year` | YEAR | NOT NULL |
| `end_year` | YEAR | NULL |
| `grade` | VARCHAR(20) | NULL |

#### `experience`
| Column | Type | Constraints |
|--------|------|-------------|
| `exp_id` | INT AUTO_INCREMENT | PK |
| `profile_id` | INT | FK → profiles, ON DELETE CASCADE |
| `company_name` | VARCHAR(200) | NOT NULL |
| `job_title` | VARCHAR(100) | NOT NULL |
| `start_date` | DATE | NOT NULL |
| `end_date` | DATE | NULL (NULL = current) |
| `description` | TEXT | NULL |

#### `projects`
| Column | Type | Constraints |
|--------|------|-------------|
| `project_id` | INT AUTO_INCREMENT | PK |
| `profile_id` | INT | FK → profiles, ON DELETE CASCADE |
| `title` | VARCHAR(200) | NOT NULL |
| `description` | TEXT | NULL |
| `tech_stack` | VARCHAR(300) | NULL |
| `url` | VARCHAR(500) | NULL |

#### `skills`
| Column | Type | Constraints |
|--------|------|-------------|
| `skill_id` | INT AUTO_INCREMENT | PK |
| `skill_name` | VARCHAR(100) | UNIQUE, NOT NULL |
| `category` | VARCHAR(50) | NULL (e.g., "language", "framework", "tool") |

#### `user_skills`
| Column | Type | Constraints |
|--------|------|-------------|
| `user_id` | INT | FK → users, ON DELETE CASCADE |
| `skill_id` | INT | FK → skills, ON DELETE CASCADE |
| `proficiency` | ENUM('beginner','intermediate','advanced') | DEFAULT 'intermediate' |
| | | PK = (user_id, skill_id) |

#### `resumes`
| Column | Type | Constraints |
|--------|------|-------------|
| `resume_id` | INT AUTO_INCREMENT | PK |
| `user_id` | INT | FK → users, ON DELETE CASCADE |
| `file_name` | VARCHAR(255) | NOT NULL |
| `file_path` | VARCHAR(500) | NOT NULL |
| `parsed_text` | LONGTEXT | NULL |
| `is_default` | BOOLEAN | DEFAULT FALSE |
| `uploaded_at` | DATETIME | DEFAULT NOW() |

#### `companies`
| Column | Type | Constraints |
|--------|------|-------------|
| `company_id` | INT AUTO_INCREMENT | PK |
| `company_name` | VARCHAR(200) | NOT NULL |
| `website` | VARCHAR(500) | NULL |
| `industry` | VARCHAR(100) | NULL |
| `logo_url` | VARCHAR(500) | NULL |

#### `jobs`
| Column | Type | Constraints |
|--------|------|-------------|
| `job_id` | INT AUTO_INCREMENT | PK |
| `company_id` | INT | FK → companies, ON DELETE CASCADE |
| `title` | VARCHAR(200) | NOT NULL |
| `description` | TEXT | NOT NULL |
| `location` | VARCHAR(150) | NULL |
| `job_type` | ENUM('full-time','part-time','internship','contract') | NOT NULL |
| `work_mode` | ENUM('on-site','hybrid','remote') | DEFAULT 'on-site' |
| `apply_url` | VARCHAR(500) | NULL |
| `posted_date` | DATE | DEFAULT CURDATE() |
| `status` | ENUM('active','closed') | DEFAULT 'active' |

#### `job_skills`
| Column | Type | Constraints |
|--------|------|-------------|
| `job_id` | INT | FK → jobs, ON DELETE CASCADE |
| `skill_id` | INT | FK → skills, ON DELETE CASCADE |
| | | PK = (job_id, skill_id) |

#### `saved_jobs`
| Column | Type | Constraints |
|--------|------|-------------|
| `user_id` | INT | FK → users, ON DELETE CASCADE |
| `job_id` | INT | FK → jobs, ON DELETE CASCADE |
| `saved_at` | DATETIME | DEFAULT NOW() |
| | | PK = (user_id, job_id) |

#### `applications`
| Column | Type | Constraints |
|--------|------|-------------|
| `application_id` | INT AUTO_INCREMENT | PK |
| `user_id` | INT | FK → users, ON DELETE CASCADE |
| `job_id` | INT | FK → jobs, ON DELETE SET NULL, NULL |
| `resume_id` | INT | FK → resumes, ON DELETE SET NULL, NULL |
| `status` | ENUM('saved','applied','interview','offer','rejected') | DEFAULT 'saved' |
| `applied_date` | DATETIME | NULL |
| `notes` | TEXT | NULL |
| `external_url` | VARCHAR(500) | NULL (for manually added external jobs) |

#### `status_logs` (optional, Nice priority)
| Column | Type | Constraints |
|--------|------|-------------|
| `log_id` | INT AUTO_INCREMENT | PK |
| `application_id` | INT | FK → applications, ON DELETE CASCADE |
| `old_status` | ENUM('saved','applied','interview','offer','rejected') | NULL |
| `new_status` | ENUM('saved','applied','interview','offer','rejected') | NOT NULL |
| `changed_at` | DATETIME | DEFAULT NOW() |

#### `reminders`
| Column | Type | Constraints |
|--------|------|-------------|
| `reminder_id` | INT AUTO_INCREMENT | PK |
| `application_id` | INT | FK → applications, ON DELETE CASCADE |
| `remind_on` | DATETIME | NOT NULL |
| `message` | VARCHAR(300) | NULL |
| `is_sent` | BOOLEAN | DEFAULT FALSE |

#### `match_scores`
| Column | Type | Constraints |
|--------|------|-------------|
| `match_id` | INT AUTO_INCREMENT | PK |
| `user_id` | INT | FK → users, ON DELETE CASCADE |
| `job_id` | INT | FK → jobs, ON DELETE CASCADE |
| `resume_id` | INT | FK → resumes, ON DELETE CASCADE |
| `score` | DECIMAL(5,2) | NOT NULL (0.00–100.00) |
| `missing_keywords` | JSON | NULL |
| `generated_at` | DATETIME | DEFAULT NOW() |

#### `cover_letters`
| Column | Type | Constraints |
|--------|------|-------------|
| `letter_id` | INT AUTO_INCREMENT | PK |
| `application_id` | INT | FK → applications, ON DELETE CASCADE |
| `content` | TEXT | NOT NULL |
| `created_at` | DATETIME | DEFAULT NOW() |

### 6.3 Normalization Walkthrough

**Unnormalized (UNF):**
```
Application(user_name, user_email, job_title, company_name, company_website,
            skills_required, status, applied_date, resume_file)
```

**→ 1NF:** Remove repeating group `skills_required` ("Python, SQL, Django") → separate `job_skills` table with one skill per row.

**→ 2NF:** `user_name` and `user_email` depend only on the user (not the full composite key). `job_title` depends only on the job. Split into `users`, `jobs`, `applications`.

**→ 3NF:** `company_website` depends on `company_name`, not on `job_id` (transitive dependency: job → company → website). Extract `companies` table.

**Result:** All tables are in 3NF. No redundancy, no update/delete anomalies. The added tables (`projects`, `saved_jobs`, `status_logs`) each store facts about one entity or relationship only, so they stay in 3NF.

---

## 7. API Design

### 7.1 Authentication Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/signup/` | Register new user | Public |
| GET | `/api/auth/verify-email/<token>/` | Verify email | Public |
| POST | `/api/auth/resend-verification/` | Resend verification link (rate limited) | Public |
| POST | `/api/auth/login/` | Login, returns auth token | Public |
| POST | `/api/auth/logout/` | Invalidate token | Token |
| POST | `/api/auth/password-reset/` | Request password reset email | Public |
| POST | `/api/auth/password-reset/confirm/` | Set new password with token | Public |

### 7.2 Profile Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/profile/` | Get current user's profile | Token |
| PUT | `/api/profile/` | Update profile | Token |
| GET/POST | `/api/profile/education/` | List / add education | Token |
| PUT/DELETE | `/api/profile/education/<id>/` | Update / delete entry | Token |
| GET/POST | `/api/profile/experience/` | List / add experience | Token |
| PUT/DELETE | `/api/profile/experience/<id>/` | Update / delete entry | Token |
| GET/POST | `/api/profile/projects/` | List / add projects | Token |
| PUT/DELETE | `/api/profile/projects/<id>/` | Update / delete entry | Token |
| GET/POST | `/api/profile/skills/` | List / add user skills | Token |
| DELETE | `/api/profile/skills/<id>/` | Remove a skill | Token |

### 7.3 Resume Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/resumes/` | List user's resumes | Token |
| POST | `/api/resumes/` | Upload resume (multipart PDF) | Token |
| DELETE | `/api/resumes/<id>/` | Delete resume | Token |
| POST | `/api/resumes/<id>/parse/` | Trigger PDF parsing + skill extraction | Token |
| PUT | `/api/resumes/<id>/set-default/` | Mark as default resume | Token |

### 7.4 Job Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/jobs/` | List jobs (search, filter, paginate) | Token |
| GET | `/api/jobs/<id>/` | Job detail | Token |
| POST | `/api/jobs/<id>/save/` | Save/bookmark a job | Token |
| DELETE | `/api/jobs/<id>/unsave/` | Remove bookmark | Token |
| GET | `/api/jobs/saved/` | List saved jobs | Token |

### 7.5 Application Tracker Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/applications/` | List user's applications | Token |
| GET | `/api/applications/board/` | Grouped by status (Kanban) | Token |
| POST | `/api/applications/` | Create application | Token |
| PUT | `/api/applications/<id>/` | Update status, notes | Token |
| DELETE | `/api/applications/<id>/` | Delete application | Token |
| POST | `/api/applications/<id>/reminders/` | Set reminder | Token |

### 7.6 AI Tool Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/ai/match-score/` | Compute match score | Token |
| POST | `/api/ai/cover-letter/` | Generate cover letter | Token |
| GET | `/api/ai/match-history/` | Past match scores | Token |

### 7.7 Extension-Specific Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/extension/profile-data/` | Flattened profile for autofill (splits `full_name` into first/last, uses the latest education entry) | Token |
| POST | `/api/extension/log-application/` | Quick-log an application from extension | Token |

### 7.8 Admin Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/admin/users/` | List all users | Admin |
| PUT | `/api/admin/users/<id>/` | Deactivate/activate user | Admin |
| CRUD | `/api/admin/companies/` | Manage companies | Admin |
| CRUD | `/api/admin/jobs/` | Manage job listings | Admin |
| CRUD | `/api/admin/skills/` | Manage skill master list | Admin |
| GET | `/api/admin/analytics/` | Dashboard statistics | Admin |

---

## 8. AI/ML Pipeline Design

### 8.1 Resume Parsing Pipeline

```
PDF Upload
    │
    ▼
┌─────────────┐
│ pdfplumber   │──── Extract raw text from PDF
└──────┬──────┘
       │
       ▼
┌──────────────┐
│ Text Cleanup  │──── Remove extra whitespace, special chars, normalize
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ spaCy NLP     │──── Tokenize, POS tag, Named Entity Recognition
│ (en_core_web_sm) │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│ Skill Extraction  │──── Match tokens against skills master list
│ (dictionary-based │     + optional NER hints (low weight)
│  + NER)           │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Store Results     │──── parsed_text → resumes table
│                   │     suggested skills → shown to user for confirmation
└──────────────────┘
```

### 8.2 Match Score Pipeline

```
Input: resume_text + job_description
              │
              ▼
┌─────────────────────┐
│ Preprocessing        │
│ - lowercase           │
│ - remove stopwords    │
│ - lemmatize (spaCy)   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ TF-IDF Vectorization │──── scikit-learn TfidfVectorizer
│ (fit on job corpus)   │     vocabulary includes skills dictionary
└──────────┬──────────┘    with boosted weights
           │
           ▼
┌─────────────────────┐
│ Cosine Similarity    │──── sklearn.metrics.pairwise.cosine_similarity
└──────────┬──────────┘
           │
           ▼
    score × 100 → Match Score (0–100)
           │
           ▼
┌─────────────────────────┐
│ Missing Keywords          │
│ job_keywords - resume_kw  │──── Set difference on extracted skill terms
│ → sorted by TF-IDF weight │
└──────────┬───────────────┘
           │
           ▼
    Return: { score: 78.5, missing_keywords: ["Docker", "AWS", "CI/CD"] }
```

**Scoring notes**

- Fit the `TfidfVectorizer` on a corpus (all job descriptions in the database plus the resume), not on just the two documents. With two documents the IDF weights carry almost no information.
- Raw cosine similarity between a resume and a job description is usually low (roughly 0.1–0.4). Combine it with a skill-overlap ratio, for example `final = 0.5 × cosine + 0.5 × (matched required skills ÷ total required skills)`, then scale to 0–100. The 50/50 split is a starting point to tune on a few sample resumes.
- Show the score as guidance, and show which skills matched and which are missing so the number is explainable.

### 8.3 Cover Letter Generation Pipeline

```
Input: user_profile + job_description
              │
              ▼
┌──────────────────────────────┐
│ Build Structured Prompt       │
│                               │
│ "You are a career advisor.    │
│  Write a cover letter for:    │
│  - Name: {name}               │
│  - Skills: {skills}           │
│  - Experience: {exp_summary}  │
│  - Education: {edu}           │
│  For this job:                 │
│  - Title: {job_title}         │
│  - Company: {company}         │
│  - Description: {job_desc}    │
│  Rules:                       │
│  - Professional tone          │
│  - Do NOT invent facts        │
│  - Under 300 words            │
│  - Highlight matching skills" │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────┐
│ Gemini API Call       │──── google-genai (Python SDK)
│ model: from .env       │    Free tier: check current limits
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Response Processing   │──── Strip markdown formatting
│                       │     Basic safety check
└──────────┬───────────┘
           │
           ▼
    Return draft → User edits → Save to cover_letters table
```

**Fallback:** If API is down/rate-limited → template-based cover letter with placeholders filled from profile.

---

## 9. Chrome Extension Architecture

### 9.1 Manifest V3 Structure

```json
{
  "manifest_version": 3,
  "name": "ApplyEase - Smart Autofill",
  "version": "1.0.0",
  "description": "Auto-fill job application forms with your ApplyEase profile",
  "permissions": ["storage", "activeTab", "scripting"],
  "host_permissions": [
    "http://localhost:8000/*",
    "https://applyease.pythonanywhere.com/*"
  ],
  "background": {
    "service_worker": "background.js"
  },
  "action": {
    "default_popup": "popup.html",
    "default_icon": "icons/icon48.png"
  },
  "icons": {
    "16": "icons/icon16.png",
    "48": "icons/icon48.png",
    "128": "icons/icon128.png"
  }
}
```

The manifest has no `content_scripts` block. When the user clicks **Fill Form**, the popup asks the service worker to inject `content.js` into the active tab with `chrome.scripting.executeScript`. `activeTab` grants access only to that tab, and `host_permissions` covers only the ApplyEase API, so the extension does not request access to every website.

### 9.2 Component Interaction

```
┌─────────────────┐      message       ┌──────────────────┐
│   Popup (UI)     │◄──────────────────►│  Service Worker   │
│                  │                    │  (background.js)  │
│ - Login form     │                    │                   │
│ - Fill button    │    chrome.runtime  │ - Stores API token│
│ - Log app button │    .sendMessage()  │ - Calls ApplyEase API│
└────────┬─────────┘                    │ - Relays profile  │
         │                              └────────┬──────────┘
         │ chrome.tabs                            │
         │ .sendMessage()                         │ fetch() to
         │                                        │ ApplyEase server
         ▼                                        ▼
┌─────────────────┐                    ┌──────────────────┐
│ Content Script   │                    │  ApplyEase Django    │
│ (content.js)     │                    │  REST API         │
│                  │                    │                   │
│ - Scans <form>s  │                    │  /api/extension/  │
│ - Reads field    │                    │   profile-data/   │
│   attributes     │                    │   log-application/│
│ - Fills values   │                    └──────────────────┘
│ - Highlights     │
│   filled fields  │
└──────────────────┘
```

### 9.3 Field Mapping Strategy

The content script uses a **keyword-matching heuristic** to map form fields to profile data:

```javascript
const FIELD_MAP = {
  // field keywords → profile data path
  'first_name|fname|first name|given name':     'first_name',
  'last_name|lname|last name|surname|family':   'last_name',
  'full_name|full name|your name|applicant name': 'full_name',
  'email|e-mail|email_address':                 'email',
  'phone|telephone|mobile|contact number':      'phone',
  'linkedin|linked_in':                         'linkedin_url',
  'github|git_hub':                             'github_url',
  'portfolio|website|personal site':            'portfolio_url',
  'university|college|institution|school':      'institution',
  'degree|qualification':                       'degree',
  'gpa|grade|cgpa|percentage':                  'grade',
  'city|location|address':                      'location',
  'summary|about|objective|bio':                'summary',
  // ... more mappings
};
```

For each `<input>`, `<select>`, or `<textarea>`:
1. Concatenate `name`, `id`, `placeholder`, associated `<label>` text, and `aria-label`.
2. Lowercase and match against `FIELD_MAP` keys.
3. If matched → set the value with the native value setter (`Object.getOwnPropertyDescriptor(...).set`), dispatch `input` and `change` events so React/Angular forms register it, and add a green highlight border.
4. If no match → skip (user can manually map via popup).
5. Check more specific keys first (for example `first_name` before a generic `name`) to avoid wrong matches.
6. Skip `<input type="file">` fields; the user attaches the resume manually.

---

## 10. Frontend Page Map & UI Wireframes

### 10.1 Page Map

```
/                           → Landing page (hero, features, CTA)
/signup/                    → Signup form
/login/                     → Login form
/verify-email/<token>/      → Email verification
/password-reset/            → Request reset
/password-reset/confirm/    → New password form

/dashboard/                 → Applicant dashboard (overview stats)
/profile/                   → Profile editor (tabbed: personal, education, experience, projects, skills)
/resumes/                   → Resume manager (upload, list, parse, set default)

/jobs/                      → Job board (search, filters, cards)
/jobs/<id>/                 → Job detail page (description, skills, match score, apply)

/tracker/                   → Application tracker (Kanban board)
/tracker/<id>/              → Application detail (notes, cover letter, score)

/ai/match/                  → Match score tool (select resume + job → score)
/ai/cover-letter/<app_id>/ → Cover letter generator/editor

/admin/dashboard/           → Admin analytics (charts)
/admin/users/               → User management
/admin/jobs/                → Job management (CRUD)
/admin/companies/           → Company management
/admin/skills/              → Skill management

/mock-forms/                → Mock job application forms (for extension demo)
```

### 10.2 Key UI Descriptions

**Dashboard:**
- Welcome bar with user's name
- Stats cards: Total Applications, Interviews Scheduled, Offers Received, Profile Completeness %
- Recent activity timeline
- Quick actions: "Browse Jobs", "Upload Resume", "View Tracker"

**Profile Editor (Tabbed):**
- Tab 1: Personal Info (name, email, phone, location, links, summary)
- Tab 2: Education (add/edit/delete entries, each a card)
- Tab 3: Work Experience (same pattern)
- Tab 4: Projects (same pattern)
- Tab 5: Skills (tag-style multi-select from master list + custom add)

**Job Board:**
- Top: search bar + filter dropdowns (location, type, skills)
- Grid of job cards (title, company, location, type, skill tags, posted date)
- Each card: "View", "Save", "Quick Match" buttons
- Pagination at bottom

**Application Tracker (Kanban):**
- 5 columns: Saved | Applied | Interview | Offer | Rejected
- Each column has draggable application cards
- Card shows: job title, company, date, match score badge
- Click card → detail modal/page

**AI Match Tool:**
- Dropdown: select resume / select job (or paste job description)
- "Calculate Match" button
- Result: circular score gauge (0–100, color-coded), missing keywords list with suggestions

---

## 11. Security Design

| Concern | Implementation |
|---------|---------------|
| **Password storage** | Django's `make_password()` / `check_password()` (PBKDF2 with SHA256 by default) |
| **Authentication** | Session-based for web views; Token authentication (DRF) for API/extension |
| **CSRF protection** | Django CSRF middleware enabled for all form submissions |
| **Input validation** | Django forms + DRF serializer validation; whitelist allowed file types for uploads |
| **SQL injection** | Django ORM parameterized queries (never raw SQL with user input) |
| **XSS** | Django template auto-escaping; `mark_safe()` never used on user input |
| **File upload safety** | Only `.pdf` allowed (max 5 MB); store in a private directory that is not served by static/media URLs; serve files only through an authenticated view that checks ownership; validate MIME type and `%PDF` header server-side |
| **CORS** | `django-cors-headers`: whitelist only the extension's origin for API access |
| **Rate limiting** | `django-ratelimit` on login, signup, AI endpoints to prevent abuse |
| **HTTPS** | Enforced in production via `SECURE_SSL_REDIRECT = True` |
| **Role-based access** | Custom `@admin_required` decorator; DRF permission classes (`IsAdminUser`, `IsAuthenticated`) |
| **API token for extension** | Token stored in `chrome.storage.local`; sent via `Authorization: Token <token>` header; expires after a set period (re-login in popup) and is deleted on logout |
| **Email verification** | Signed token (Django's `TimestampSigner`) with expiry |
| **Sensitive settings** | `.env` file for `SECRET_KEY`, DB credentials, API keys; never committed to Git |

---

## 12. Project Structure (Directory Layout)

```
applyease/
├── .env                          # Environment variables (SECRET_KEY, DB, API keys)
├── .gitignore
├── requirements.txt              # Python dependencies
├── manage.py                     # Django management script
│
├── applyease/                       # Django project config
│   ├── __init__.py
│   ├── settings.py               # Django settings (reads from .env)
│   ├── urls.py                   # Root URL configuration
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/                     # Module 1: Auth & User Management
│   ├── models.py                 # Custom User model (extends AbstractUser)
│   ├── serializers.py            # DRF serializers for auth
│   ├── views.py                  # Signup, login, logout, verify, reset views
│   ├── urls.py                   # /api/auth/* routes
│   ├── forms.py                  # Django forms for web views
│   ├── decorators.py             # @admin_required, etc.
│   ├── authentication.py         # ExpiringTokenAuthentication for the extension
│   ├── tokens.py                 # Email verification token logic
│   ├── templates/accounts/       # Login, signup, reset HTML templates
│   └── tests.py
│
├── profiles/                     # Module 2: Profile & Resume Manager
│   ├── models.py                 # Profile, Education, Experience, Project, Resume
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── services.py               # Resume parsing logic (pdfplumber + spaCy)
│   ├── templates/profiles/
│   └── tests.py
│
├── jobs/                         # Module 3: Job Board
│   ├── models.py                 # Company, Job, JobSkill, SavedJob
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── filters.py                # DRF filter backends for search/filter
│   ├── management/commands/      # seed_jobs.py (import sample data)
│   ├── templates/jobs/
│   └── tests.py
│
├── tracker/                      # Module 4: Application Tracker
│   ├── models.py                 # Application, Reminder, StatusLog
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── management/commands/      # send_reminders.py (run daily by a scheduler)
│   ├── templates/tracker/
│   └── tests.py
│
├── ai_tools/                     # Module 6: AI Resume Tools
│   ├── models.py                 # MatchScore, CoverLetter
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── matcher.py                # TF-IDF + cosine similarity logic
│   ├── cover_letter.py           # Gemini API integration + prompt template
│   ├── skills_dict.py            # Curated skills dictionary for boosted matching
│   └── tests.py
│
├── dashboard/                    # Module 7: Admin Dashboard
│   ├── views.py                  # Analytics views
│   ├── urls.py
│   ├── templates/dashboard/
│   └── tests.py
│
├── core/                         # Shared utilities
│   ├── models.py                 # Skill model (shared across apps)
│   ├── mixins.py                 # Common view mixins
│   ├── pagination.py             # Custom pagination classes
│   └── permissions.py            # Custom DRF permission classes
│
├── templates/                    # Global templates
│   ├── base.html                 # Base layout (navbar, footer, Bootstrap)
│   ├── landing.html              # Landing page
│   └── includes/                 # Partials (navbar, alerts, etc.)
│
├── static/                       # Static assets
│   ├── css/
│   ├── js/
│   └── images/
│
├── private_media/                # User uploads (resumes, avatars) — gitignored, served only via authenticated view
│
├── mock_forms/                   # Mock job application forms for extension demo
│   ├── templates/mock_forms/
│   ├── views.py
│   └── urls.py
│
├── extension/                    # Module 5: Chrome Extension source
│   ├── manifest.json
│   ├── popup.html
│   ├── popup.js
│   ├── popup.css
│   ├── content.js
│   ├── background.js
│   ├── mapper.js
│   ├── icons/
│   └── README.md
│
├── docs/                         # Documentation
│   ├── PROJECT_PLAN.md           # ← This file
│   └── ...
│
├── seed_data/                    # Sample data for development
│   ├── companies.csv
│   ├── jobs.csv
│   └── skills.csv
│
└── tests/                        # Integration / E2E tests
    └── ...
```

---

## 13. Development Workflow

### Git Strategy

- **Main branch**: `main` — always deployable
- **Development branch**: `dev` — integration branch
- **Feature branches**: `feature/<module>-<description>` (e.g., `feature/auth-login`, `feature/tracker-kanban`)
- **Flow**: `feature/*` → PR to `dev` → tested → PR to `main`

### Setup Steps (for new developer)

```bash
# 1. Clone
git clone https://github.com/<username>/applyease.git
cd applyease

# 2. Virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux / macOS

# 3. Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# 4. Environment file
copy .env.example .env         # Windows (Linux/macOS: cp .env.example .env)
# Fill in DB creds, SECRET_KEY, GEMINI_API_KEY, GEMINI_MODEL

# 5. Database
mysql -u root -p -e "CREATE DATABASE applyease_db CHARACTER SET utf8mb4;"
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Seed sample data
python manage.py seed_jobs

# 8. Run
python manage.py runserver
```

**Installation notes**

- If `mysqlclient` fails to install on Windows, use a prebuilt wheel or install the MySQL C connector and build tools. On Ubuntu run `sudo apt install libmysqlclient-dev pkg-config build-essential` first.
- Add `rest_framework`, `rest_framework.authtoken`, `corsheaders` and `django_filters` to `INSTALLED_APPS`.
- Run the reminder command manually while developing: `python manage.py send_reminders`.

### `requirements.txt`

```
Django>=5.0,<6.0
djangorestframework>=3.15
django-cors-headers>=4.0
mysqlclient>=2.2
python-dotenv>=1.0
spacy>=3.7
scikit-learn>=1.4
pdfplumber>=0.11
PyPDF2>=3.0
google-genai
django-filter>=24.0
django-ratelimit>=4.1
Pillow>=10.0
gunicorn>=22.0        # production only
whitenoise>=6.6       # production only
```

---

## 14. Testing Strategy

### Unit Tests (per app)

| App | What to Test |
|-----|-------------|
| `accounts` | Signup validation, login returns token, password hashing, email verification token generation/validation, role checks |
| `profiles` | Profile CRUD, education/experience create/update/delete, resume upload validates PDF only |
| `jobs` | Job listing, search returns relevant results, filter combinations, save/unsave |
| `tracker` | Application CRUD, status transitions, reminder creation, board grouping |
| `ai_tools` | Match score calculation (with known inputs → expected score), keyword extraction, prompt building |

### API Tests (Postman Collection)

- Test every endpoint: valid request, invalid request, unauthenticated request, wrong role.
- Organize by module in Postman collection.
- Environment variables for `base_url`, `token`.

### Integration Tests

- Full flow: signup → verify email → login → create profile → upload resume → browse jobs → compute match → apply → track application.
- Extension: login in popup → navigate to mock form → fill → verify values → log application.

### Manual Test Cases

- Cross-browser testing (Chrome required for extension; web app on Chrome, Firefox, Edge).
- Responsive testing (mobile, tablet, desktop).
- Edge cases: empty profile fills, PDF with no text, very long job descriptions.

---

## 15. Deployment Plan

### Development (Local)

- Django dev server (`runserver`) on `localhost:8000`
- MySQL 8 local instance
- Chrome extension loaded unpacked (`chrome://extensions` → Developer mode)

### Production (Recommended)

| Component | Service | Notes |
|-----------|---------|-------|
| Web App | PythonAnywhere or Railway (check current free-tier terms) | Django + Gunicorn (PythonAnywhere uses its own WSGI setup) |
| Database | PythonAnywhere MySQL or Railway MySQL | Same host as app for low latency |
| Static Files | WhiteNoise middleware | Serve static directly from Django in small-scale deployment |
| Media Files | Private directory on the host disk | Uploaded resumes, served only through an authenticated view |
| Extension | Chrome Web Store (or unpacked for demo) | Publish or demo with unpacked |
| Domain | Free subdomain from host | e.g., `applyease.pythonanywhere.com` |
| Scheduler | Host scheduled task or cron | Runs `python manage.py send_reminders` daily |

**Hosting caveats (check before committing to a host):**

- Free PythonAnywhere accounts restrict outbound internet access to a whitelist, so test the Gemini API call and SMTP from the host early.
- spaCy and scikit-learn need a fair amount of disk and memory. Check the free-tier limits and use only `en_core_web_sm`.
- Free-tier terms change, so confirm them on the provider's site.
- Fallback: run the app locally and load the extension unpacked for the demo.

### Deployment Checklist

- [ ] `DEBUG = False`
- [ ] `ALLOWED_HOSTS` configured
- [ ] `SECRET_KEY` from environment variable
- [ ] `SECURE_SSL_REDIRECT = True`
- [ ] Static files collected (`collectstatic`)
- [ ] Database migrations applied
- [ ] Superuser created
- [ ] CORS configured for extension
- [ ] `.env` not committed
- [ ] Gemini call and email sending tested from the host
- [ ] Reminder scheduler configured
- [ ] Resume files not reachable by any public URL

---

## 16. Risk Analysis & Mitigation

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|-----------|--------|------------|
| R1 | Real job sites change HTML → autofill breaks | High | Medium | Demo on own mock forms + a few simple public forms; use flexible label-based matching |
| R2 | Websites block extension / forbid scraping | Medium | Low | We don't scrape; autofill works client-side on user-initiated pages; job data is seeded or admin-entered |
| R3 | PDF parsing fails on complex layouts (tables, columns) | Medium | Medium | Support text-based PDFs first; user can correct extracted data manually; use pdfplumber (better than PyPDF2 for tables) |
| R4 | Match score inaccuracy | Medium | Low | Combine TF-IDF with curated skills dictionary; show as "guidance" not "verdict"; allow user to re-match after updating resume |
| R5 | Gemini API rate limits / downtime | Low | Medium | Respect the current free-tier limits (check Google's docs); cache generated letters; fallback to template-based generation |
| R6 | Personal data leak | Low | High | Hash passwords, HTTPS, validate all inputs, store files outside web root, role-based access, CSRF protection |
| R7 | Team member unavailable | Low | High | Clear module ownership, daily Git commits, shared task board |
| R8 | Scope creep | Medium | High | Strict "Must / Nice" priority labels; cut "Nice" features first if behind schedule |
| R9 | MySQL connection issues in shared hosting | Low | Medium | Test early with target host; have SQLite fallback for local dev |
| R10 | Free host blocks outbound calls or lacks resources for spaCy/scikit-learn | Medium | Medium | Do a trial deployment in Week 6; fall back to a local demo with the unpacked extension |

---

## 17. 12-Week Timeline & Task Ownership

| Week | Phase | Tasks | Owner |
|------|-------|-------|-------|
| **1** | **Setup & Research** | Finalize requirements. Study similar tools (Simplify, JobHero). Study Chrome Manifest V3. Set up GitHub repo, project structure, virtual environment, Django project scaffold, MySQL database. Get a Gemini API key and run a test call. | Both |
| **2** | **Foundation** | Design ER diagram in draw.io. Write MySQL schema (all tables). Implement Django models + migrations. Build signup, login, logout, email verification, password reset. | A: Database + Models, B: Auth views |
| **3** | **Profile** | Build profile editor (personal info, education, experience, projects, skills — tabbed UI). Resume upload + storage. DRF serializers + API endpoints for profile. | A: Profile module, B: Resume upload |
| **4** | **Job Board** | Build Company + Job models. Job listing page with search + filters. Job detail page. Save/unsave functionality. Seed sample data (CSV import command). | B: Job board, A: seed data |
| **5** | **Tracker** | Build Application model. Kanban board UI (drag-and-drop with JS). Application detail page. Create application from job board. | A |
| **6** | **Tracker + Admin** | Add reminders (model + `send_reminders` command + scheduler). Build admin dashboard views (user management, job CRUD). Basic analytics queries. Trial deployment to the chosen host (check outbound access and resource limits). | A: Reminders, B: Admin dashboard |
| **7** | **AI — Parsing + Matching** | Resume parsing pipeline (pdfplumber + spaCy). TF-IDF match score engine. Missing keyword extraction. Match score UI page. | A |
| **8** | **AI — Cover Letter** | Gemini API integration. Prompt engineering. Cover letter generation + editor UI. Fallback template. Connect match score to job detail page. | B |
| **9** | **Chrome Extension** | Build extension: manifest, popup (login, fill button), content script (field detection, mapping, filling), service worker (API communication). Build 3–5 mock application forms (include one with JS-rendered fields to test event dispatch). | Both |
| **10** | **Integration** | Connect extension to tracker (log application after fill). Analytics charts (Chart.js). Landing page. Polish all UI with Bootstrap. Cross-module testing. | Both |
| **11** | **Testing & Polish** | Unit tests for all modules. API testing with Postman. Integration test (full user flow). Bug fixes. UI/UX improvements. Responsive testing. | Both |
| **12** | **Documentation & Demo** | Final documentation (synopsis, report). README.md. Demo preparation (scripted walkthrough). Presentation slides. Viva practice. | Both |

### Milestone Checkpoints

| Milestone | Week | Deliverable |
|-----------|------|-------------|
| M1: Core Working | 5 | User can sign up, create profile, browse jobs, track applications |
| M2: AI Integrated | 8 | Match score, missing keywords, cover letter generation all working |
| M3: Extension Working | 9 | Extension can login, fill mock forms, log application |
| M4: Feature Complete | 10 | All modules integrated, admin dashboard with charts |
| M5: Release Ready | 11 | Tested, polished, documented |
| M6: Submission | 12 | Final report, demo, presentation |

---

## 18. Future Scope / Nice-to-Haves

These features are **out of scope** for the current semester but could be added later:

| Feature | Description |
|---------|-------------|
| **Real-time notifications** | WebSocket-based in-app notifications for status changes and reminders |
| **Interview prep** | AI-generated interview questions based on job description |
| **Resume builder** | Generate formatted PDF resume from profile data (multiple templates) |
| **Job API aggregation** | Auto-import listings from Adzuna, LinkedIn, Indeed APIs |
| **Multi-browser extension** | Firefox, Edge versions of the extension |
| **Mobile app** | React Native companion app for tracking on the go |
| **Collaborative features** | Share application boards with mentors/placement cells |
| **Advanced analytics** | Application success rate, response time tracking, salary insights |
| **OAuth login** | Sign in with Google / LinkedIn |
| **Multilingual support** | Interface and cover letters in multiple languages |

---

> **This document is the single source of truth for ApplyEase's planning and system design. All development should reference this plan. Update this document as decisions change.**