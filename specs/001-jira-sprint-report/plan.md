# Implementation Plan: Jira Sprint Report

## Technical Context

- Existing repository: Python domain-model/MVP direction with frontend,
  backend, and shared-types package placeholders.
- Integration: Jira Cloud REST APIs through a server-side client.
- Authentication: Atlassian OAuth 2.0 authorization-code flow.
- Runtime/framework: to be confirmed during setup; keep deployment portable
  through environment-based configuration.
- Initial scale: one project, roughly 100 sprint issues, 10 team members.

## Architecture

### Domain layer

Define normalized types for project, sprint, issue, status category, blocker,
risk reason, filters, metrics, forecast, and structured errors. Keep status
mapping, story-point totals, pace forecast, business-day calculations, blocker
detection, risk detection, and filtered aggregation pure and deterministic.

### Integration layer

Implement a Jira Cloud client with selected fields, pagination, timeouts,
rate-limit handling, authorization checks, issue-link direction handling, and
structured errors. Add short-lived permission-scoped caching and a
single-flight refresh guard.

### API and security layer

Implement OAuth login/callback/logout, state validation, secure sessions,
project discovery, active-sprint lookup, and one normalized report endpoint.
Enforce authorization on every Jira-backed request and prevent token leakage.

### Presentation layer

Build summary cards, pace visualization, blockers table, risk table, filters,
issue board, refresh/stale states, authentication states, and responsive
accessible styling. Escape Jira text and do not rely on color alone.

## API Boundaries

- `GET /auth/login`
- `GET /auth/callback`
- `POST /auth/logout`
- `GET /api/projects`
- `GET /api/projects/{projectKey}/active-sprint`
- `GET /api/projects/{projectKey}/active-sprint/report`

## Delivery Sequence

1. Foundation: runtime, configuration validation, normalized types, health
   check, secure sessions, OAuth skeleton, and Jira client.
2. Core report: project/sprint discovery, issue normalization, metrics,
   forecast, and board.
3. Blockers and risks: relationship/label detection and explainable reasons.
4. Usability and resilience: filters, refresh scheduling, cache, stale/error
   states, accessibility, responsive layout, and telemetry.
5. Validation and rollout: representative workflows, non-admin permissions,
   deployment, OAuth scope review, and operational documentation.

## Risks and Mitigations

- Jira schema/workflow variation: use explicit configuration and normalized
  types.
- Partial or stale upstream data: structured errors and last-known-good
  fallback.
- Token exposure: server-only token handling, secure cookies, redacted logs,
  and security tests.
- Incorrect time/risk calculations: timezone-aware pure functions and edge-case
  tests.
