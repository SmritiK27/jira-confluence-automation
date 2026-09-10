# Jira Sprint Report Specification

## 1. Document Control

- **Status:** Scope baseline approved; implementation remains gated by the
  remaining clarification decisions
- **Source:** Module 08 `project_spec.md` and `work/module-08-report.md`
- **Constitution:** [`spec/constitution.md`](./constitution.md)
- **Primary users:** Scrum Master and members of a 10-person engineering team
- **Release:** First release / MVP
- **Product type:** Read-only web application for Jira Cloud sprint health
- **Technology constraints:** React 18 + Vite, Node.js + Express,
  PostgreSQL 15, Docker/Docker Compose

### Release scope decision

Release one is **Jira-only**. It provides read-only access to one configured
Jira Cloud project and its active sprint. It does not integrate with Confluence
and does not write to Jira or Confluence.

The application may write its own operational state, including sessions,
short-lived cache metadata, configuration, refresh state, and safe telemetry,
subject to the constitution's retention, authorization, and privacy rules.
These application writes do not change the source systems.

## 2. Problem Statement

Teams need a fast, reliable daily view of active-sprint health. Jira contains
the authoritative issue data, but delivery progress, blockers, risk reasons,
and completion pace are difficult to assess consistently from the standard
workflow view.

The application shall provide one coherent report for one configured Jira
Cloud project and its active sprint. It shall normalize Jira data into
understandable categories, explain risks and blockers, and preserve the last
successful report when a refresh fails.

## 3. Goals

The product shall:

1. Provide a fast and reliable active-sprint health view.
2. Show progress using story points and Jira workflow status.
3. Make blockers and delivery risks immediately visible.
4. Forecast sprint pace using elapsed time and completed work.
5. Allow users to filter the report and open issues directly in Jira.
6. Authenticate each user without shared Jira credentials.
7. Preserve source-system authority, security, and data-integrity guarantees.

## 4. Non-Goals

The first release shall not provide:

- Historical sprint trends or velocity reporting.
- Multi-project reporting.
- Test coverage, deployment, incident, or other automation-quality metrics.
- Jira issue editing.
- PDF/CSV export or scheduled email/chat distribution.
- Long-term storage of Jira issue snapshots.
- Near-real-time webhook updates.
- Mobile-first optimization.
- Unreviewed destructive writes to Jira or Confluence.
- Confluence pages, comments, notifications, or other Confluence automation.
- Jira issue, comment, workflow, label, or link creation/update.

## 5. Users, Roles, and Access

### 5.1 Users

| User | Need |
| --- | --- |
| Scrum Master | Monitor sprint health, blockers, risks, and forecast. |
| Engineering team member | Understand current work, ownership, blockers, and risk. |

### 5.2 Authentication and authorization

1. Authenticate each user through the existing Atlassian account using OAuth
   2.0 authorization code flow.
2. Use the authenticated user's Jira permissions for every Jira-backed request.
3. Do not use a shared Jira API token in the browser or as a substitute for
   user authorization.
4. Keep OAuth client secrets, access tokens, and refresh tokens server-side.
5. Use secure, HTTP-only, same-site session cookies.
6. Validate OAuth state and callback parameters.
7. Show a clear, actionable authorization error when the user cannot access the
   configured project.

## 6. Scope and Assumptions

- Jira Cloud is the only supported Jira deployment.
- One configured Jira project is in scope.
- The active sprint is the default reporting period on every visit.
- The team estimates work with story points.
- Jira workflow statuses can be mapped to To Do, In Progress, and Done.
- The project has a reliable blocked label/flag convention and blocking issue
  links.
- Jira due dates are available where applicable.
- The application can deploy on the existing cloud platform.
- The existing company design system shall be used when available.
- The initial scale target is approximately 100 sprint issues and 10 team
  members.
- The first-release holiday policy either supports configured holidays or
  explicitly documents that only weekends are excluded.

## 7. User Scenarios and Acceptance Criteria

### US-01: View the active sprint

**As a** Scrum Master or team member, **I want** to sign in and view the
configured project's active sprint, **so that** I can assess delivery health
without shared credentials.

**Acceptance criteria**

- Given an authorized user and an active sprint, the report displays sprint
  name, start date, end date, elapsed time, remaining time, summary metrics,
  forecast, blockers, risks, and issue board.
- Given no active sprint, the application displays a useful empty state with
  next-step guidance.
- Given an inaccessible project, the application displays an actionable
  authorization error and does not show fabricated report data.
- The active sprint is selected by default on every visit.

### US-02: Understand progress and pace

**As a** report user, **I want** committed, completed, remaining, and
unestimated work shown together, **so that** I can understand sprint progress.

**Acceptance criteria**

- Summary cards show committed points, completed points, remaining points,
  completion percentage, issue totals, completed issue totals, elapsed days,
  remaining days, forecast status, and last successful refresh.
- Missing or zero story points never cause a calculation failure.
- Missing or zero-point issues are identified separately as unestimated.
- The forecast is labelled **Simple pace forecast**.
- The forecast is **On track** when completed-point proportion is greater than
  or equal to elapsed-time proportion; otherwise it is **At risk**.
- The UI does not imply that the pace forecast is statistically trained.
- Pre-start, post-end, and zero-duration sprints are handled safely.

### US-03: Find blockers

**As a** report user, **I want** blocked work listed with its source, **so
that** I can focus on impediments.

**Acceptance criteria**

- An issue is included when it has the configured blocked label or flag.
- An issue is included when a Jira issue link indicates another issue blocks it.
- The blocker table shows issue key, summary, status, assignee, story points,
  blocker reason/source when available, and a direct Jira link.
- Blocking-link direction is interpreted correctly.

### US-04: Understand delivery risk

**As a** report user, **I want** each risk explained, **so that** I can act on
the underlying condition rather than an opaque score.

**Acceptance criteria**

- An incomplete issue with a passed due date receives an overdue reason.
- An issue with no status, assignee, or activity change for at least three
  business days receives an inactivity reason.
- An issue with an unresolved blocker receives an unresolved-blocker reason.
- An issue added after sprint start receives a late-addition reason.
- Multiple applicable reasons are displayed together.
- Business days use the configured project timezone; weekends are excluded.
- The holiday policy is configurable or clearly documented as weekend-only.

### US-05: Inspect and filter the issue board

**As a** team member, **I want** to filter and open issues, **so that** I can
focus on relevant work.

**Acceptance criteria**

- All active-sprint issues are grouped into configurable To Do, In Progress,
  and Done categories.
- Each issue row/card shows key, summary, issue type, status, assignee, story
  points, optional due date, blocked indicator, risk indicators, and Jira link.
- Users can filter by assignee, issue type, status/category, and risk state.
- Filters update summary metrics, progress visualization, blockers, risks, and
  issue-board groups consistently.
- The UI clearly indicates when metrics represent a filtered subset rather than
  the full sprint.
- Workflow mapping does not assume exact Jira status names.

### US-06: Refresh safely

**As a** report user, **I want** current data and honest failure states, **so
that** I do not act on silently incomplete information.

**Acceptance criteria**

- The report automatically refreshes every five minutes while open.
- A manual refresh action is available.
- Manual and automatic refresh requests cannot overlap.
- The last successful refresh time is displayed.
- When refresh fails, the last successful report remains visible and is marked
  stale with a visible error message.
- Rate limits, expired OAuth sessions, missing permissions, unavailable
  project/sprint data, timeouts, and incomplete responses produce actionable
  errors.
- A failed or incomplete response is never represented as an empty successful
  report.

## 8. Functional Requirements

### FR-01: Project and sprint configuration

The system shall allow an authorized user to select or configure the Jira
project, list accessible projects where applicable, detect the active sprint,
and show the no-active-sprint state.

Project configuration is application-owned and does not modify Jira. Release
one permits only the configured project's read access; configuration changes
must follow the approved application authorization model.

### FR-02: Sprint timing

The system shall display sprint name, start date, end date, elapsed time, and
remaining time. Time calculations shall be safe before sprint start, after
sprint end, and when start and end produce zero duration.

### FR-03: Issue retrieval

The backend shall retrieve, at minimum:

- Project and project key.
- Active sprint metadata.
- Issue key and summary.
- Issue type, status, assignee, labels/flags, and story points.
- Due date, created date, updated date, and changelog/activity information.
- Issue links, including blocking and is-blocked-by relationships.
- Status category or configured workflow mapping.

The Jira client shall request only required fields and support pagination even
though the initial scale is approximately 100 issues.

### FR-04: Normalization

The system shall normalize Jira responses into application domain types for
projects, sprints, issues, statuses/categories, blockers, risk reasons,
filters, metrics, forecasts, and structured errors. Vendor response shapes
shall not leak into UI business rules.

### FR-05: Summary metrics

For the current issue set, the system shall calculate:

- Total committed story points.
- Completed story points.
- Remaining story points.
- Completion percentage.
- Total issue count and completed issue count.
- Sprint elapsed and remaining days.
- Count/list of unestimated issues.
- Forecast status and forecast inputs.
- Last successful refresh timestamp.

Missing and zero story-point values shall be handled explicitly without
exceptions or silent misclassification.

### FR-06: Forecast

The initial forecast shall compare:

```text
completed point proportion = completed points / committed points
elapsed time proportion = elapsed sprint time / total sprint time
```

The result shall be:

- **On track** when completed point proportion is at least elapsed time
  proportion.
- **At risk** when completed point proportion is below elapsed time proportion.

The implementation shall define safe behavior for zero committed points,
pre-start, post-end, and zero-duration sprints and expose enough inputs for the
UI to explain the result.

### FR-07: Blocker detection

The system shall identify blockers from the configured blocked label/flag and
from Jira issue-link relationships. It shall preserve the source/reason and
support direction-aware interpretation of blocking links.

### FR-08: Risk detection

The system shall calculate and preserve a list of applicable risk reasons for
each issue. Risk detection shall support overdue, inactivity, unresolved
blocker, and post-start addition conditions. Business-day logic shall use the
configured project timezone and documented holiday policy.

### FR-09: Issue board

The frontend shall display all normalized issues grouped into To Do, In
Progress, and Done. Status mappings shall be configuration-driven and unknown
statuses shall have an explicit safe handling path.

### FR-10: Filtering

The system shall support filters for assignee, issue type, status/category,
and risk state. A single filtered issue set shall drive all dependent metrics,
visualizations, tables, and board groups.

### FR-11: Refresh and cache

The backend shall use a short-lived server-side cache to reduce repeated Jira
requests. Cache entries shall be scoped by Jira tenant, project, and
permission context as appropriate. Manual refresh shall invalidate or bypass
the relevant cache. A single-flight or equivalent guard shall prevent
overlapping refreshes.

### FR-12: Error and stale-data behavior

The system shall use structured errors for authorization failures, expired
sessions, rate limits, unavailable data, timeouts, and partial responses.
Failed refreshes shall preserve the last successful report and expose stale
state, error details suitable for user action, and the last successful
timestamp.

### FR-13: Security

The backend shall implement server-side OAuth, secure token handling, secure
session cookies, callback/state validation, authorization checks on every
Jira-backed request, safe Jira-text encoding, and redacted operational logs.

The backend shall not expose or implement Jira or Confluence write operations
in release one.

### FR-14: Observability

The system shall record safe operational events for Jira latency and failures,
rate limits, OAuth failures, cache hits/misses, and report refresh success or
failure. Events shall not contain access tokens, secrets, unnecessary issue
descriptions, or other sensitive payloads.

## 9. Data Model

The normalized report response shall contain:

```text
Report
  project
  sprint
  summary
  forecast
  blockers[]
  risks[]
  filterOptions
  issueBoard
  refresh
```

### Required normalized fields

- **Project:** key, display name, Jira tenant/base URL.
- **Sprint:** id, name, start, end, elapsed time, remaining time, state.
- **Issue:** key, summary, type, raw status, normalized category, assignee,
  story points, estimated/unestimated state, due date, created/updated times,
  Jira URL, blocked state, blocker sources, risk reasons.
- **Summary:** committed, completed, remaining, completion percentage, issue
  counts, unestimated count, elapsed/remaining days, filtered indicator.
- **Forecast:** label, status, completed proportion, elapsed proportion, and
  edge-case state where applicable.
- **Refresh:** last successful time, current request state, stale flag, and
  safe user-facing error.

PostgreSQL 15 may store configuration, sessions, cache metadata, and
operational workflow state as needed. The first release shall not persist
long-term Jira issue snapshots.

## 10. API Contract

The application shall expose these application-level endpoints:

- `GET /auth/login`
- `GET /auth/callback`
- `POST /auth/logout`
- `GET /api/projects`
- `GET /api/projects/{projectKey}/active-sprint`
- `GET /api/projects/{projectKey}/active-sprint/report`

API responses shall be versionable, validated, JSON-based, and use a
consistent structured error shape containing a safe error code, message,
correlation ID, and actionable guidance where appropriate.

## 11. Frontend Requirements

The React 18 + Vite frontend shall provide:

- Authentication and authorization states.
- Sprint header and timing.
- Summary cards.
- Clearly labelled simple pace visualization.
- Blockers table.
- At-risk table.
- Filter controls.
- Issue board with three normalized categories.
- Loading, no-sprint, stale-data, error, empty, and refresh states.
- Direct Jira links.
- Responsive desktop-first layout with basic tablet support.
- Keyboard-accessible controls, meaningful labels, focus states, and
  non-color status indicators.

The frontend shall never receive OAuth client secrets, Jira access tokens, or
unredacted sensitive integration data.

## 12. Backend and Infrastructure Requirements

The Node.js + Express backend shall:

- Own OAuth, sessions, Jira API calls, normalization, aggregation, caching,
  and structured error mapping.
- Validate environment configuration at startup.
- Enforce HTTPS outside local development.
- Use PostgreSQL 15 through Docker for supported persistent data.
- Use migrations and transactions for database changes.
- Provide health and readiness checks without exposing secrets.
- Keep deployment portable through environment-based configuration and a
  platform secret manager.

## 13. Non-Functional Requirements

### Security and privacy

- Least-privilege Atlassian scopes.
- No secrets or access tokens in client code, logs, source control, or test
  output.
- HTTP-only, secure, same-site cookies where sessions are used.
- Validated OAuth state and callback parameters.
- Authorization enforced for every Jira-backed request.
- Jira text escaped/encoded before rendering.

### Reliability

- Explicit timeout and rate-limit handling.
- Paginated Jira retrieval.
- Last-known-good fallback on failed refresh.
- No empty success-shaped response for failed or incomplete upstream data.
- Idempotent refresh behavior and no overlapping requests.

### Performance and scale

- Support approximately 100 sprint issues and 10 team members.
- Use short-lived server-side caching.
- Request only fields required by the report.
- Avoid long-term snapshot persistence in release one.

### Accessibility and compatibility

- Desktop-first responsive behavior with basic tablet support.
- Status, blocker, and risk information cannot depend on color alone.
- Use the company design system when available.

## 14. Edge Cases and Error Scenarios

The implementation and tests shall cover:

1. No active sprint.
2. Sprint before its start date.
3. Sprint after its end date.
4. Zero-duration sprint.
5. Zero committed points.
6. Missing, zero, or mixed story points.
7. Unknown and newly configured Jira statuses.
8. Multiple risk reasons on one issue.
9. Weekend and timezone boundaries.
10. Configured holiday behavior.
11. Jira pagination and empty pages.
12. Jira rate limits and retry exhaustion.
13. Expired OAuth/session.
14. Missing project permissions.
15. Timeout, unavailable project, and unavailable sprint.
16. Partial or malformed Jira responses.
17. Failed refresh with an existing successful report.
18. Concurrent manual and scheduled refresh requests.

## 15. Verification Plan

### Unit tests

Cover story-point totals, completion percentage, unestimated handling, issue
counts, filtering, status mappings, forecast boundaries, timezone-aware
business days, stale thresholds, blocker link direction, and every risk reason
including combinations.

### API and integration tests

Cover Jira field selection, pagination, timeout/error mapping, rate limits,
partial responses, OAuth state/callback failures, logout, session expiry,
secure cookie attributes, token non-exposure, project access errors, no active
sprint, successful reports, stale fallback, and overlapping-refresh
prevention.

### Frontend tests

Cover summary cards, forecast labelling, blockers, risks, filters, loading,
empty, stale, and error states, responsive behavior where supported, and
direct Jira links.

### Operational validation

Validate representative Jira workflows with approximately 100 issues and 10
team members. Verify OAuth scopes and permissions with a non-admin team member,
HTTPS deployment, required environment variables, health checks, safe logs, and
cache/refresh telemetry.

## 16. Definition of Done

A release is complete only when:

- All in-scope requirements and acceptance scenarios are implemented.
- The constitution's security, reliability, accessibility, and data rules are
  satisfied.
- Unit, API, integration, and frontend tests applicable to the change pass.
- No secret, token, or sensitive source content is exposed.
- Failed refreshes preserve and label last-known-good data.
- Documentation covers setup, environment variables, OAuth configuration,
  deployment, health checks, and operations.
- The report is validated against a representative project by an authorized
  non-admin user.
