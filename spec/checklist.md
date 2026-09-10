# Specification Implementation Checklist

**Specification reviewed:** [`spec/specification.md`](./specification.md)
**Review date:** 2026-09-10
**Implementation baseline:** Commit `4806769` plus the current worktree
**Validation performed:** `npm install` and `npm run build` now pass in `apps/frontend`. npm reports one moderate and one high dependency vulnerability that is tracked as a nice-to-have cleanup rather than silently ignored.

## Status legend

- **Implemented and verified:** The requirement is present in the implementation and a relevant check passed.
- **Partially implemented:** Some visible or structural portion exists, but the complete requirement is not covered.
- **Not implemented:** No supporting implementation exists.
- **Implemented but not working:** Code exists, but the available validation found a failure.
- **Not verifiable:** The requirement needs runtime, integration, or environment evidence that is not currently available.

## 1. Scope, goals, and technology

| Requirement | Implemented? | Works? | Evidence and gap |
| --- | --- | --- | --- |
| React 18 + Vite frontend | Partially implemented | Implemented but not working | Frontend manifest declares React 18 and Vite. Production build fails because empty repository-root configuration files are loaded by the Vite/TypeScript build. |
| Node.js + Express backend | Not implemented | No | Backend source and package manifest are empty placeholders; there is no Express application. |
| PostgreSQL 15 and Docker/Docker Compose | Not implemented | No | Root `Dockerfile`, `docker-compose.yml`, and backend persistence setup are empty or absent. |
| Jira-only, read-only release boundary | Partially implemented | No | UI labels itself read-only, but there is no authenticated Jira integration or enforcement layer. No Jira/Confluence write endpoint was found. |
| Active-sprint health view for one configured project | Partially implemented | No | `ReportPage` renders a hard-coded sprint and issue set. It does not load a configured project or active sprint. |
| Goals: progress, blockers, risks, forecast, filters, direct Jira links, authentication | Partially implemented | No | Mock UI includes progress, filters, a forecast notice, and placeholder links. Authentication, live data, blockers table, risks table, and real forecast logic are missing. |

## 2. Users, authentication, and authorization

| Requirement | Implemented? | Works? | Evidence and gap |
| --- | --- | --- | --- |
| Scrum Master and team-member views | Partially implemented | Not verifiable | The mock page is generic and has no role-aware behavior or permission model. |
| Atlassian OAuth 2.0 authorization-code flow | Not implemented | No | No backend OAuth route or working OAuth service exists. |
| Authenticated user's Jira permissions on every request | Not implemented | No | No backend request pipeline or Jira request exists. |
| No shared browser Jira token | Partially implemented | Not verifiable | No token is present in the frontend, but this is because integration is absent. |
| Server-side client/access/refresh token handling | Not implemented | No | OAuth and server-side token storage do not exist. |
| Secure HTTP-only same-site session cookies | Not implemented | No | No session middleware or cookie configuration exists. |
| OAuth state and callback validation | Not implemented | No | No callback implementation exists. |
| Actionable authorization error for inaccessible projects | Not implemented | No | No API, error model, or UI state exists for this scenario. |

## 3. User scenarios and acceptance criteria

### US-01: View the active sprint

| Acceptance criterion | Implemented? | Works? | Evidence and gap |
| --- | --- | --- | --- |
| Authorized user sees sprint metadata, timing, metrics, forecast, blockers, risks, and board | Partially implemented | No | Mock header, metrics, forecast notice, and board exist; authentication, live timing, blockers, and risk views do not. |
| No-active-sprint empty state | Not implemented | No | No data-driven empty state exists. |
| Inaccessible project shows actionable error and no fabricated data | Not implemented | No | Mock data is always rendered and there is no authorization error path. |
| Active sprint selected by default on every visit | Not implemented | No | No project/sprint selection or API request exists. |

### US-02: Understand progress and pace

| Acceptance criterion | Implemented? | Works? | Evidence and gap |
| --- | --- | --- | --- |
| Required summary cards and totals | Partially implemented | Not verifiable | Mock cards show committed, completed, remaining, and at-risk points; issue totals, completed issue totals, elapsed/remaining days, and unestimated count are missing. |
| Missing/zero points do not fail calculations | Partially implemented | Not verifiable | `ReportPage` guards a zero committed total, but the implementation is mock-only and does not model missing points. |
| Unestimated issues identified separately | Partially implemented | No | One zero-point issue is labelled “Unestimated” as a risk, but there is no separate unestimated metric or semantic state. |
| Forecast labelled “Simple pace forecast” | Implemented | Not verifiable | Label is present in the notice text. |
| On-track/at-risk threshold follows point proportion versus elapsed-time proportion | Not implemented | No | The status and percentages are hard-coded; no elapsed-time calculation exists. |
| Forecast is not presented as statistically trained | Implemented | Not verifiable | The UI calls it a simple pace forecast. |
| Pre-start, post-end, and zero-duration handling | Not implemented | No | No sprint-time calculation exists. |

### US-03: Find blockers

| Acceptance criterion | Implemented? | Works? | Evidence and gap |
| --- | --- | --- | --- |
| Blocked label/flag detection | Partially implemented | No | One hard-coded issue has `blocked: true`; no Jira label/flag detection exists. |
| Blocking issue-link detection | Not implemented | No | No Jira issue-link retrieval or direction logic exists. |
| Blocker table with required fields and source | Not implemented | No | There is no blockers table. |
| Correct blocking-link direction | Not implemented | No | No link parser exists. |

### US-04: Understand delivery risk

| Acceptance criterion | Implemented? | Works? | Evidence and gap |
| --- | --- | --- | --- |
| Overdue risk reason | Not implemented | No | No due-date or current-time logic exists. |
| Three-business-day inactivity reason | Not implemented | No | No activity timestamps or business-day calculation exists. |
| Unresolved-blocker risk reason | Not implemented | No | No blocker service or resolution logic exists. |
| Late-addition risk reason | Not implemented | No | No sprint-start/created-date comparison exists. |
| Multiple reasons shown together | Partially implemented | No | Mock cards can display one risk tag and a separate blocked tag, but no calculated reason list exists. |
| Timezone-aware business days and documented holiday policy | Not implemented | No | No timezone or holiday policy implementation exists. |

### US-05: Inspect and filter the issue board

| Acceptance criterion | Implemented? | Works? | Evidence and gap |
| --- | --- | --- | --- |
| Issues grouped into configurable To Do/In Progress/Done categories | Partially implemented | Not verifiable | Three hard-coded columns exist; status mapping is not configurable. |
| Cards show key, summary, type, status, assignee, points, due date, blocked state, risks, and Jira link | Partially implemented | Not verifiable | Cards show key, summary, assignee, points, risk, blocked state, and link; type, raw status, and due date are missing. |
| Filters for assignee, issue type, status/category, and risk | Partially implemented | Not verifiable | Assignee, issue type, status, and risk filters now exist over the mock issue set; live API-backed filtering is missing. |
| One filtered set drives all metrics, visualizations, tables, and board groups | Partially implemented | Not verifiable | Mock metrics and board use the same filtered array; there are no visualizations, blockers, or risk tables. |
| Filtered subset is clearly indicated | Implemented | Not verifiable | The UI displays “Across filtered issues” and an issue count. |
| Status mapping does not assume exact Jira names | Not implemented | No | The mock issue type restricts statuses to exact display names and has no normalization layer. |

### US-06: Refresh safely

| Acceptance criterion | Implemented? | Works? | Evidence and gap |
| --- | --- | --- | --- |
| Automatic five-minute refresh | Partially implemented | Not verifiable | A five-minute timer updates the displayed refresh time; it does not refresh live report data until the API exists. |
| Manual refresh action | Partially implemented | Not verifiable | Button updates the displayed refresh time but does not fetch live data. |
| Refresh requests cannot overlap | Not implemented | No | No request state or single-flight guard exists. |
| Last successful refresh displayed | Partially implemented | Not verifiable | Static/mock `Just now` value is displayed. |
| Failed refresh preserves report and marks it stale with visible error | Not implemented | No | No API request, stale state, or error state exists. |
| Actionable rate-limit, session, permission, unavailable-data, timeout, and incomplete-response errors | Not implemented | No | No backend error mapping or frontend error presentation exists. |
| Failed/incomplete response is not treated as empty success | Not implemented | No | No response validation exists. |

## 4. Functional requirements

| ID | Requirement | Implemented? | Works? | Evidence and gap |
| --- | --- | --- | --- | --- |
| FR-01 | Project configuration, accessible-project listing, active-sprint detection, and no-sprint state | Not implemented | No | No backend API or configuration flow exists. |
| FR-02 | Safe sprint timing before start, after end, and zero duration | Not implemented | No | No timing service exists. |
| FR-03 | Retrieve required Jira fields, links, changelog/activity, status category, and paginate | Not implemented | No | Jira client is absent; backend files are empty. |
| FR-04 | Normalize vendor responses into domain types | Not implemented | No | No domain types or normalization pipeline exists. |
| FR-05 | Calculate all summary metrics and explicit unestimated handling | Partially implemented | Not verifiable | Basic mock point totals are calculated in the component; required issue counts, days, unestimated count, and refresh metadata are absent. |
| FR-06 | Explainable simple pace forecast with safe edge cases | Not implemented | No | Forecast text is hard-coded. |
| FR-07 | Detect blockers from labels/flags and direction-aware links | Not implemented | No | No blocker implementation exists. |
| FR-08 | Calculate overdue, inactivity, unresolved-blocker, and late-addition reasons | Not implemented | No | No risk implementation exists. |
| FR-09 | Render normalized issue board with configurable mappings and unknown-status path | Partially implemented | Not verifiable | Mock three-column board exists; normalization, configuration, and unknown handling do not. |
| FR-10 | Assignee, issue type, status/category, and risk filters drive one set | Partially implemented | Not verifiable | Only assignee and risk filters exist over mock data. |
| FR-11 | Scoped server cache, manual invalidation, and overlapping-refresh guard | Not implemented | No | No backend/cache implementation exists. |
| FR-12 | Structured errors and last-known-good stale fallback | Not implemented | No | No API error or stale-report implementation exists. |
| FR-13 | Server-side OAuth, token security, cookies, validation, authorization, safe encoding, and no writes | Not implemented | No | Backend is absent. React rendering is escaped by default, but this does not satisfy the integration requirement. |
| FR-14 | Safe operational events for latency, failures, rate limits, OAuth, cache, and refresh | Not implemented | No | No logging/telemetry implementation exists. |

## 5. Data model and API contract

| Requirement | Implemented? | Works? | Evidence and gap |
| --- | --- | --- | --- |
| Normalized `Report` shape with project, sprint, summary, forecast, blockers, risks, filters, board, refresh | Not implemented | No | No shared contract or API response exists. |
| Required normalized project/sprint/issue/summary/forecast/refresh fields | Not implemented | No | Mock `Issue` type is incomplete and frontend-only. |
| No long-term Jira issue snapshots | Not verifiable | Not verifiable | No persistence exists, but there is also no implemented storage policy or tests. |
| Required auth, project, sprint, report, and logout endpoints | Not implemented | No | No Express server or routes are implemented. |
| Versionable JSON responses with validated, consistent structured errors | Not implemented | No | No API exists. |

## 6. Frontend requirements

| Requirement | Implemented? | Works? | Evidence and gap |
| --- | --- | --- | --- |
| Authentication and authorization states | Not implemented | No | No auth UI or API integration. |
| Sprint header and timing | Partially implemented | Not verifiable | Static sprint header exists; timing is hard-coded text. |
| Summary cards | Partially implemented | Not verifiable | Four cards exist, but the full required metric set is absent. |
| Clearly labelled simple pace visualization | Partially implemented | Not verifiable | Text notice exists; there is no visualization. |
| Blockers table | Partially implemented | Not verifiable | A blockers panel now lists filtered blocked mock issues; Jira-derived blocker sources and the complete table schema are missing. |
| At-risk table | Partially implemented | Not verifiable | An at-risk panel now lists filtered mock risk reasons; calculated Jira risk reasons are missing. |
| Filter controls | Partially implemented | Not verifiable | Assignee and risk controls exist; two required filter dimensions are missing. |
| Three-category issue board | Implemented | Not verifiable | Three columns are rendered from mock data. |
| Loading, no-sprint, stale, error, empty, and refresh states | Partially implemented | No | Manual refresh label exists; the other states are missing. |
| Direct Jira links | Partially implemented | Not verifiable | Placeholder `jira.example.com` links exist; tenant URL is not validated or sourced from Jira. |
| Responsive desktop-first/tablet layout | Implemented and verified | Yes | CSS includes responsive breakpoints and the production build now passes. |
| Keyboard access, labels, focus states, non-color indicators | Partially implemented | Not verifiable | Native select/checkbox/button and text labels exist; explicit focus styling and complete state semantics are not present. |
| No OAuth secrets/tokens in frontend | Implemented | Not verifiable | No credentials are present in the frontend; no integration exists to prove the boundary. |

## 7. Backend and infrastructure requirements

| Requirement | Implemented? | Works? | Evidence and gap |
| --- | --- | --- | --- |
| Express owns OAuth, sessions, Jira calls, normalization, aggregation, cache, errors | Not implemented | No | Backend package and source files are empty. |
| Startup environment validation | Not implemented | No | Missing. |
| HTTPS enforcement outside development | Not implemented | No | Missing. |
| PostgreSQL 15 via Docker | Not implemented | No | Missing. |
| Migrations and transactions | Not implemented | No | Missing. |
| Health and readiness checks without secrets | Not implemented | No | Missing. |
| Portable environment-based deployment configuration | Not implemented | No | Missing. |

## 8. Non-functional requirements and edge cases

| Requirement | Implemented? | Works? | Evidence and gap |
| --- | --- | --- | --- |
| Least-privilege scopes and no secret/token leakage | Not implemented | No | OAuth and backend logging are absent. |
| Secure cookies, state validation, per-request authorization, safe Jira text encoding | Not implemented | No | Backend security boundary is absent. |
| Timeouts, rate limits, pagination, stale fallback, idempotent refresh | Not implemented | No | No integration or refresh services exist. |
| Approximately 100 issues and 10 team members | Not implemented | No | Only five mock issues are rendered; no scale test exists. |
| Short-lived server cache and no long-term snapshots | Not implemented | No | No cache or persistence policy is implemented. |
| Desktop-first/tablet compatibility and non-color status cues | Partially implemented | Not verifiable | Responsive CSS and text tags exist, but build and browser validation have not passed. |
| All listed edge cases (sprint timing, points, statuses, risks, pagination, OAuth, permissions, malformed data, stale refresh, concurrency) | Not implemented | No | No backend logic, automated tests, or integration fixtures cover them. |

## 9. Verification and Definition of Done

| Requirement | Implemented? | Works? | Evidence and gap |
| --- | --- | --- | --- |
| Unit tests for calculations, filtering, mapping, forecast, business days, blockers, and risks | Not implemented | No | No frontend/backend test suite for this feature exists. |
| API/integration tests for Jira, OAuth, errors, cookies, stale fallback, and concurrency | Not implemented | No | No backend test suite exists. |
| Frontend tests for cards, forecast, blockers, risks, filters, states, responsive behavior, and links | Not implemented | No | No frontend test files exist. |
| Operational validation with representative Jira project and non-admin user | Not implemented | No | No live integration or deployment validation exists. |
| Documentation for setup, environment, OAuth, deployment, health checks, and operations | Partially implemented | No | Specification documents intended behavior, but runnable setup and operational documentation are not implemented. |
| All in-scope requirements implemented and validated | Not implemented | No | The current implementation is an unverified mock UI and does not meet the release Definition of Done. |

## Unchecked-item disposition review

The original checklist marked most items as incomplete because the repository was
only a mock frontend. Each incomplete item is classified below so that an
unchecked box is not mistaken for an unreviewed defect.

### Real gaps implemented in this pass

- Repaired the repository-root `package.json` and `tsconfig.json`, which were
  preventing the frontend build from resolving its project configuration.
- Added a repository `.gitignore` for dependency, build, environment, log, and
  Python-cache artifacts.
- Added issue type, due-date, and status filtering to the mock report.
- Added blockers and at-risk issue panels driven by the same filtered issue set.
- Added five-minute automatic refresh of the displayed refresh timestamp and
  retained the manual refresh action.
- Added the missing issue type/status metadata to issue cards.
- Verified the frontend production build after these changes.

### Real gaps deferred, not out of scope

These remain required by the specification and are not minor polish. They are
deferred because the approved plan still requires decisions T-002 through T-006
before implementation can safely choose tenant isolation, OAuth behavior, Jira
API semantics, schemas, persistence, and operational targets:

- Atlassian OAuth, secure sessions, authorization, and logout.
- Express backend, health/readiness endpoints, structured errors, and
  environment validation.
- Jira client, pagination, field discovery, normalization, live project/sprint
  retrieval, blocker links, risk calculations, and forecast edge cases.
- PostgreSQL 15/Docker persistence, migrations, cache isolation, and retention.
- Versioned API contracts and frontend API integration.
- Stale last-known-good data, rate-limit/timeout handling, and single-flight
  refresh.
- Security logging/redaction, HTTPS enforcement, observability, and deployment.
- Unit, API, integration, frontend, accessibility, performance, and operational
  verification against Jira.

These are **real gaps**, not out-of-scope features. They must be implemented
after the specification baseline milestone M-000 is approved.

### Out-of-scope items

The following are correctly excluded from release one and should not be
implemented while completing this checklist:

- Confluence pages, comments, notifications, or other Confluence automation.
- Jira issue, comment, workflow, label, or link writes.
- Historical sprint trends, multi-project reporting, exports, scheduled
  distribution, webhooks, and long-term Jira issue snapshots.
- Mobile-first optimization and statistical/ML forecasting.

### Nice-to-have list

These are minor polish or maintenance items and do not block the MVP contract:

- Replace placeholder `jira.example.com` links with the configured tenant URL
  once the live API contract exists.
- Add explicit custom focus-ring styling and richer screen-reader announcements
  for refresh completion.
- Add a visual chart to complement the existing text-only pace forecast.
- Resolve the npm audit warnings after dependency policy and upgrade
  compatibility are reviewed.
- Add browser-level visual regression coverage after the runtime and API are
  stable.

## Summary

- **Implemented and verified:** The frontend scaffold now builds successfully and the mock UI covers summary cards, three board columns, assignee/type/status/risk filtering, blocker and risk panels, refresh controls, responsive CSS, and placeholder Jira links.
- **Partially implemented:** The mock UI still does not consume live Jira data and cannot prove authentication, authorization, timing, forecast, or failure behavior.
- **Real gaps remaining:** Live Jira integration, OAuth, backend APIs, PostgreSQL/Docker infrastructure, normalization, cache/stale behavior, structured errors, observability, and required automated tests.
- **Out of scope:** Confluence automation and source-system writes remain intentionally excluded from release one.
- **Immediate next gate:** Resolve T-002 through T-006 and approve M-000 before implementing the backend and live integration.
