# Jira Sprint Report Implementation Backlog

This backlog is ordered for a smallest useful end-to-end MVP first, while preserving the security, reliability, and acceptance requirements in `project_spec.md`.

## Validation Approach Key

- **Approach 1** — Use for a quick, bounded operation involving only a few files.
- **Approach 2** — Use for a one-time, high-quality check across a moderate number of files.
- **Approach 3** — Use for repeatable automation, large file sets, or consistency-critical validation.

## Setup

- [ ] Confirm the application framework, runtime, package manager, and existing company design-system integration point. (GitHub issue #1) — **Approach 1**
- [ ] Create the frontend, backend, and shared-types application structure with local development and production configuration. (GitHub issue #12) — **Approach 2**
- [ ] Define environment variables for Atlassian OAuth, application URL, configured project, Jira field IDs, blocked marker, status mappings, project timezone, stale threshold, cache TTL, and session secret. (GitHub issue #10) — **Approach 1**
- [ ] Add configuration validation that fails clearly at startup when required secrets, URLs, or Jira settings are missing or invalid. (GitHub issue #5) — **Approach 2**
- [ ] Define normalized domain types for projects, sprints, issues, statuses/categories, blockers, risk reasons, filters, report metrics, forecast, and structured API errors. (GitHub issue #11) — **Approach 2**
- [ ] Define the report response contract containing sprint metadata, summary metrics, forecast, blocker/risk rows, filter options, and grouped issue-board data. (GitHub issue #2) — **Approach 2**
- [ ] Set up secure server-side session handling with encrypted or platform-secured session data and secure, HTTP-only, same-site cookies. (GitHub issue #7) — **Approach 2**
- [ ] Implement the OAuth authorization-code flow skeleton: login redirect, callback, state generation/validation, error handling, session creation, and logout. (GitHub issue #3) — **Approach 2**
- [ ] Configure least-privilege Atlassian OAuth scopes for project, sprint, issue, changelog/activity, and issue-link reads. (GitHub issue #6) — **Approach 1**
- [ ] Add baseline security middleware for HTTPS outside local development, CSRF/state protection where applicable, input validation, and safe Jira-text encoding. (GitHub issue #4) — **Approach 2**
- [ ] Add structured logging and request correlation without logging OAuth secrets, access tokens, or unnecessary Jira content. (GitHub issue #8) — **Approach 2**
- [ ] Add a health-check endpoint that reports application availability without exposing configuration secrets. (GitHub issue #9) — **Approach 1**

## Core Features

- [ ] Implement project selection/configuration UI and API for authorized users, including a clear authorization error for inaccessible projects. — **Approach 2**
- [ ] Implement active-sprint discovery and the no-active-sprint empty state. — **Approach 1**
- [ ] Display sprint name, start/end dates, elapsed days, remaining days, and pre-start/post-end/zero-duration-safe time calculations. — **Approach 2**
- [ ] Implement issue normalization into the configured To Do, In Progress, and Done categories rather than relying on exact Jira status names. — **Approach 2**
- [ ] Implement story-point aggregation for committed, completed, and remaining work, explicitly tracking missing or zero-point issues as unestimated. — **Approach 2**
- [ ] Implement issue-board rendering with issue key, summary, type, status, assignee, story points, due date, blocked/risk indicators, and direct Jira link. — **Approach 2**
- [ ] Implement summary cards for points, completion percentage, issue counts, sprint timing, forecast status, and last successful refresh time. — **Approach 2**
- [ ] Implement the simple pace forecast by comparing completed-point proportion with elapsed-sprint-time proportion; label it explicitly as a simple pace forecast. — **Approach 2**
- [ ] Implement blocker detection from the configured blocked label/flag and Jira blocking/is-blocked-by relationships. — **Approach 2**
- [ ] Render a blockers table with issue details, assignee, points, blocker source/reason when available, and Jira link. — **Approach 2**
- [ ] Implement risk detection and reason lists for overdue incomplete issues, three-business-day inactivity, unresolved blockers, and post-start sprint additions. — **Approach 2**
- [ ] Implement project-timezone business-day calculations with weekends excluded and a documented/configurable holiday policy. — **Approach 2**
- [ ] Render the at-risk table and issue-level risk indicators with each applicable reason visible. — **Approach 2**
- [ ] Implement assignee, issue type, status/category, and risk-state filters. — **Approach 2**
- [ ] Ensure filters consistently update summary metrics, progress visualization, blockers, risk rows, and issue-board groups. — **Approach 2**
- [ ] Clearly indicate when displayed metrics represent a filtered subset rather than the full sprint. — **Approach 1**
- [ ] Add accessible loading, empty, error, stale-data, status, blocker, and risk states that do not rely on color alone. — **Approach 2**
- [ ] Add desktop-first responsive styling with usable tablet-width layouts and company design-system components where available. — **Approach 2**

## Integration

- [ ] Build the server-side Jira Cloud API client with authenticated requests, required-field selection, timeouts, pagination, and structured error mapping. — **Approach 3**
- [ ] Implement project listing/lookup and `GET /api/projects`. — **Approach 1**
- [ ] Implement active-sprint lookup and `GET /api/projects/{projectKey}/active-sprint`. — **Approach 1**
- [ ] Implement paginated sprint-issue retrieval with all required fields: key, summary, type, status, assignee, labels/flags, story points, due date, created/updated dates, changelog/activity, and issue links. — **Approach 3**
- [ ] Implement `GET /api/projects/{projectKey}/active-sprint/report` to aggregate and return one coherent normalized report response. — **Approach 2**
- [ ] Enforce the authenticated user's Jira permissions on every Jira-backed request and map missing project/sprint access to actionable UI errors. — **Approach 2**
- [ ] Handle Jira rate limits, expired OAuth sessions, unavailable projects/sprints, timeouts, partial responses, and upstream failures without converting failures into empty success results. — **Approach 2**
- [ ] Add a short-lived server-side cache scoped to Jira tenant, project, and permission context as appropriate. — **Approach 2**
- [ ] Invalidate or bypass relevant cached data on manual refresh, and expose cache hit/miss operational events. — **Approach 2**
- [ ] Add a single-flight or equivalent refresh guard so automatic and manual refreshes cannot overlap. — **Approach 2**
- [ ] Add five-minute automatic refresh while the report is open and a manual refresh action. — **Approach 2**
- [ ] Preserve the last successful report on refresh failure and expose a visible stale-data/error state with the last successful refresh time. — **Approach 2**
- [ ] Add Jira issue-link construction/validation so every displayed issue opens directly in the correct Jira tenant. — **Approach 1**
- [ ] Add operational telemetry for Jira latency/failures, rate limits, OAuth failures, refresh outcomes, and cache behavior without sensitive payloads. — **Approach 2**
- [ ] Add environment-based deployment configuration for the existing cloud platform, HTTPS enforcement, secret-manager integration, and portable startup commands. — **Approach 2**

## Testing

- [ ] Add unit tests for story-point totals, completion percentage, unestimated handling, issue counts, and filtered-subset metrics. — **Approach 3**
- [ ] Add unit tests for status-to-category mappings, including unknown and newly configured statuses. — **Approach 3**
- [ ] Add unit tests for forecast calculations, including pre-start, post-end, zero-duration, zero-point, and 100%-complete sprints. — **Approach 3**
- [ ] Add unit tests for weekend/business-day and configured-timezone stale-threshold calculations. — **Approach 3**
- [ ] Add unit tests for each risk reason and combinations of multiple risk reasons on one issue. — **Approach 3**
- [ ] Add unit tests for blocker label/flag detection and blocking-link direction handling. — **Approach 3**
- [ ] Add tests for Jira pagination, required field selection, timeout/error mapping, rate-limit handling, and incomplete-response handling. — **Approach 3**
- [ ] Add tests for OAuth state validation, callback failures, logout, session expiry, secure cookie attributes, and token non-exposure. — **Approach 3**
- [ ] Add API tests for project access errors, no active sprint, report success, stale fallback after failed refresh, and overlapping-refresh prevention. — **Approach 3**
- [ ] Add frontend/component tests for summary cards, forecast labeling, blockers, risks, filters, loading/empty/error states, and direct Jira links. — **Approach 3**
- [ ] Add integration tests using representative fixtures for approximately 100 issues and 10 team members. — **Approach 3**
- [ ] Verify every acceptance criterion from the specification with an executable test or documented manual test case. — **Approach 3**
- [ ] Validate the workflow with a non-admin team member and confirm least-privilege OAuth scopes and project authorization behavior. — **Approach 2**
- [ ] Run accessibility checks for keyboard navigation, focus order, labels, contrast, and non-color status/risk communication. — **Approach 2**
- [ ] Run responsive checks at desktop and basic tablet widths. — **Approach 2**
- [ ] Run the existing build, type-check, lint, and targeted test commands before release; resolve regressions without changing unrelated behavior. — **Approach 3**

## Documentation

- [ ] Document local setup, supported runtime/package versions, environment variables, and development commands. — **Approach 2**
- [ ] Document Atlassian OAuth app creation, callback URLs, scopes, secret-manager setup, and token/session security expectations. — **Approach 2**
- [ ] Document Jira project configuration: project key, story-point field, blocked label/flag, status mappings, timezone, stale threshold, and holiday policy. — **Approach 2**
- [ ] Document the normalized report API contract, endpoint authentication requirements, pagination behavior, and structured error responses. — **Approach 2**
- [ ] Document the simple pace forecast formula, its On track/At risk threshold, and all sprint edge-case behavior. — **Approach 1**
- [ ] Document story-point treatment for missing/zero values and the distinction between full-sprint and filtered metrics. — **Approach 1**
- [ ] Document blocker detection sources and the four risk reasons, including business-day semantics. — **Approach 1**
- [ ] Document refresh cadence, cache TTL/invalidation, stale-data behavior, rate-limit handling, and session-expiry recovery. — **Approach 2**
- [ ] Document deployment steps for the existing cloud platform, HTTPS requirements, required secrets, health checks, and rollback considerations. — **Approach 2**
- [ ] Document operational logging/telemetry fields and explicitly prohibited sensitive data. — **Approach 1**
- [ ] Create a release checklist linking each acceptance criterion to its validation evidence. — **Approach 3**
- [ ] Record the first-release non-goals so historical trends, multi-project reporting, Jira editing, exports, scheduled distribution, long-term snapshots, webhooks, and mobile-first optimization are not accidentally added. — **Approach 1**

## MCP Server Coverage Classification

Existing MCP servers can provide Atlassian data and basic Jira/Confluence operations. They do not replace application code, deterministic business logic, UI, security, testing, or project documentation.

### Legend

- **MCP** - suitable for an existing Jira/Confluence MCP server.
- **Custom** - requires application-specific code or skills.
- **Hybrid** - MCP can provide data, but custom logic is required.

### Setup

| Backlog tasks | Classification |
| --- | --- |
| Framework/runtime/package manager/design-system selection; frontend/backend/shared-types structure | Custom |
| Environment variables, startup validation, normalized domain types, and report response contract | Custom |
| Secure sessions, cookies, security middleware, logging, request correlation, and health checks | Custom |
| OAuth authorization-code flow and least-privilege scope configuration | Hybrid |

### Core Features

| Backlog tasks | Classification |
| --- | --- |
| Project selection/configuration UI and API | Hybrid |
| Active-sprint discovery and no-active-sprint state | Hybrid |
| Sprint timing, status normalization, story-point aggregation, and pace forecast | Custom |
| Issue-board rendering, blockers table, and at-risk table | Hybrid |
| Blocker detection from labels/flags and issue links | Hybrid |
| Risk detection, business-day/timezone calculations, and risk reasons | Custom |
| Filters, filtered metrics, subset indication, accessibility, responsive styling, and design-system integration | Custom |

### Integration

| Backlog tasks | Classification |
| --- | --- |
| Project lookup, sprint lookup, JQL issue search, issue retrieval, and issue field retrieval | MCP |
| Server-side Jira client/adapter, project and sprint API endpoints | Hybrid |
| Paginated issue retrieval, changelog/activity, and issue-link retrieval | Hybrid; verify support in the selected server |
| Aggregated report endpoint | Custom |
| User-permission enforcement and actionable authorization errors | Hybrid |
| Rate limits, expired sessions, timeouts, partial responses, structured errors, cache, refresh locking, stale fallback, and telemetry | Custom |
| Issue-link construction/validation and cloud deployment configuration | Custom |

### Testing

All testing backlog tasks are **Custom**. This includes calculation, mapping, forecast, business-day, risk, blocker, Jira adapter, OAuth/session, API, frontend, integration, acceptance, least-privilege, accessibility, responsive, build, type-check, and lint validation.

### Documentation

All documentation backlog tasks are **Custom**, except Atlassian OAuth documentation, which is **Hybrid**. This includes local setup, project configuration, report API contracts, formulas, risk/blocker semantics, refresh/cache/error behavior, deployment, telemetry, release evidence, and first-release non-goals.

### Recommended MCP Usage

Use **[sooperset/mcp-atlassian](https://github.com/sooperset/mcp-atlassian)** or the official **[Atlassian Rovo MCP Server](https://github.com/atlassian/atlassian-mcp-server)** for:

- Project and sprint lookup
- JQL issue search and issue retrieval
- Status, assignee, labels, dates, story points, and custom fields
- Changelog/activity and issue links, when supported
- Confluence documentation search and page operations

Keep report aggregation, forecast/risk algorithms, business-day calculations, filtering semantics, caching, refresh behavior, OAuth session management, stale-data handling, UI/accessibility, tests, and release evidence in custom application code.
