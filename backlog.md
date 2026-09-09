# Jira Sprint Report Implementation Backlog

This backlog is ordered for a smallest useful end-to-end MVP first, while preserving the security, reliability, and acceptance requirements in `project_spec.md`.

## Setup

- [ ] Confirm the application framework, runtime, package manager, and existing company design-system integration point.
- [ ] Create the frontend, backend, and shared-types application structure with local development and production configuration.
- [ ] Define environment variables for Atlassian OAuth, application URL, configured project, Jira field IDs, blocked marker, status mappings, project timezone, stale threshold, cache TTL, and session secret.
- [ ] Add configuration validation that fails clearly at startup when required secrets, URLs, or Jira settings are missing or invalid.
- [ ] Define normalized domain types for projects, sprints, issues, statuses/categories, blockers, risk reasons, filters, report metrics, forecast, and structured API errors.
- [ ] Define the report response contract containing sprint metadata, summary metrics, forecast, blocker/risk rows, filter options, and grouped issue-board data.
- [ ] Set up secure server-side session handling with encrypted or platform-secured session data and secure, HTTP-only, same-site cookies.
- [ ] Implement the OAuth authorization-code flow skeleton: login redirect, callback, state generation/validation, error handling, session creation, and logout.
- [ ] Configure least-privilege Atlassian OAuth scopes for project, sprint, issue, changelog/activity, and issue-link reads.
- [ ] Add baseline security middleware for HTTPS outside local development, CSRF/state protection where applicable, input validation, and safe Jira-text encoding.
- [ ] Add structured logging and request correlation without logging OAuth secrets, access tokens, or unnecessary Jira content.
- [ ] Add a health-check endpoint that reports application availability without exposing configuration secrets.

## Core Features

- [ ] Implement project selection/configuration UI and API for authorized users, including a clear authorization error for inaccessible projects.
- [ ] Implement active-sprint discovery and the no-active-sprint empty state.
- [ ] Display sprint name, start/end dates, elapsed days, remaining days, and pre-start/post-end/zero-duration-safe time calculations.
- [ ] Implement issue normalization into the configured To Do, In Progress, and Done categories rather than relying on exact Jira status names.
- [ ] Implement story-point aggregation for committed, completed, and remaining work, explicitly tracking missing or zero-point issues as unestimated.
- [ ] Implement issue-board rendering with issue key, summary, type, status, assignee, story points, due date, blocked/risk indicators, and direct Jira link.
- [ ] Implement summary cards for points, completion percentage, issue counts, sprint timing, forecast status, and last successful refresh time.
- [ ] Implement the simple pace forecast by comparing completed-point proportion with elapsed-sprint-time proportion; label it explicitly as a simple pace forecast.
- [ ] Implement blocker detection from the configured blocked label/flag and Jira blocking/is-blocked-by relationships.
- [ ] Render a blockers table with issue details, assignee, points, blocker source/reason when available, and Jira link.
- [ ] Implement risk detection and reason lists for overdue incomplete issues, three-business-day inactivity, unresolved blockers, and post-start sprint additions.
- [ ] Implement project-timezone business-day calculations with weekends excluded and a documented/configurable holiday policy.
- [ ] Render the at-risk table and issue-level risk indicators with each applicable reason visible.
- [ ] Implement assignee, issue type, status/category, and risk-state filters.
- [ ] Ensure filters consistently update summary metrics, progress visualization, blockers, risk rows, and issue-board groups.
- [ ] Clearly indicate when displayed metrics represent a filtered subset rather than the full sprint.
- [ ] Add accessible loading, empty, error, stale-data, status, blocker, and risk states that do not rely on color alone.
- [ ] Add desktop-first responsive styling with usable tablet-width layouts and company design-system components where available.

## Integration

- [ ] Build the server-side Jira Cloud API client with authenticated requests, required-field selection, timeouts, pagination, and structured error mapping.
- [ ] Implement project listing/lookup and `GET /api/projects`.
- [ ] Implement active-sprint lookup and `GET /api/projects/{projectKey}/active-sprint`.
- [ ] Implement paginated sprint-issue retrieval with all required fields: key, summary, type, status, assignee, labels/flags, story points, due date, created/updated dates, changelog/activity, and issue links.
- [ ] Implement `GET /api/projects/{projectKey}/active-sprint/report` to aggregate and return one coherent normalized report response.
- [ ] Enforce the authenticated user's Jira permissions on every Jira-backed request and map missing project/sprint access to actionable UI errors.
- [ ] Handle Jira rate limits, expired OAuth sessions, unavailable projects/sprints, timeouts, partial responses, and upstream failures without converting failures into empty success results.
- [ ] Add a short-lived server-side cache scoped to Jira tenant, project, and permission context as appropriate.
- [ ] Invalidate or bypass relevant cached data on manual refresh, and expose cache hit/miss operational events.
- [ ] Add a single-flight or equivalent refresh guard so automatic and manual refreshes cannot overlap.
- [ ] Add five-minute automatic refresh while the report is open and a manual refresh action.
- [ ] Preserve the last successful report on refresh failure and expose a visible stale-data/error state with the last successful refresh time.
- [ ] Add Jira issue-link construction/validation so every displayed issue opens directly in the correct Jira tenant.
- [ ] Add operational telemetry for Jira latency/failures, rate limits, OAuth failures, refresh outcomes, and cache behavior without sensitive payloads.
- [ ] Add environment-based deployment configuration for the existing cloud platform, HTTPS enforcement, secret-manager integration, and portable startup commands.

## Testing

- [ ] Add unit tests for story-point totals, completion percentage, unestimated handling, issue counts, and filtered-subset metrics.
- [ ] Add unit tests for status-to-category mappings, including unknown and newly configured statuses.
- [ ] Add unit tests for forecast calculations, including pre-start, post-end, zero-duration, zero-point, and 100%-complete sprints.
- [ ] Add unit tests for weekend/business-day and configured-timezone stale-threshold calculations.
- [ ] Add unit tests for each risk reason and combinations of multiple risk reasons on one issue.
- [ ] Add unit tests for blocker label/flag detection and blocking-link direction handling.
- [ ] Add tests for Jira pagination, required field selection, timeout/error mapping, rate-limit handling, and incomplete-response handling.
- [ ] Add tests for OAuth state validation, callback failures, logout, session expiry, secure cookie attributes, and token non-exposure.
- [ ] Add API tests for project access errors, no active sprint, report success, stale fallback after failed refresh, and overlapping-refresh prevention.
- [ ] Add frontend/component tests for summary cards, forecast labeling, blockers, risks, filters, loading/empty/error states, and direct Jira links.
- [ ] Add integration tests using representative fixtures for approximately 100 issues and 10 team members.
- [ ] Verify every acceptance criterion from the specification with an executable test or documented manual test case.
- [ ] Validate the workflow with a non-admin team member and confirm least-privilege OAuth scopes and project authorization behavior.
- [ ] Run accessibility checks for keyboard navigation, focus order, labels, contrast, and non-color status/risk communication.
- [ ] Run responsive checks at desktop and basic tablet widths.
- [ ] Run the existing build, type-check, lint, and targeted test commands before release; resolve regressions without changing unrelated behavior.

## Documentation

- [ ] Document local setup, supported runtime/package versions, environment variables, and development commands.
- [ ] Document Atlassian OAuth app creation, callback URLs, scopes, secret-manager setup, and token/session security expectations.
- [ ] Document Jira project configuration: project key, story-point field, blocked label/flag, status mappings, timezone, stale threshold, and holiday policy.
- [ ] Document the normalized report API contract, endpoint authentication requirements, pagination behavior, and structured error responses.
- [ ] Document the simple pace forecast formula, its On track/At risk threshold, and all sprint edge-case behavior.
- [ ] Document story-point treatment for missing/zero values and the distinction between full-sprint and filtered metrics.
- [ ] Document blocker detection sources and the four risk reasons, including business-day semantics.
- [ ] Document refresh cadence, cache TTL/invalidation, stale-data behavior, rate-limit handling, and session-expiry recovery.
- [ ] Document deployment steps for the existing cloud platform, HTTPS requirements, required secrets, health checks, and rollback considerations.
- [ ] Document operational logging/telemetry fields and explicitly prohibited sensitive data.
- [ ] Create a release checklist linking each acceptance criterion to its validation evidence.
- [ ] Record the first-release non-goals so historical trends, multi-project reporting, Jira editing, exports, scheduled distribution, long-term snapshots, webhooks, and mobile-first optimization are not accidentally added.
