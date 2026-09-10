# Feature Specification: Jira Sprint Report

## Source

Derived from the Module 08 specification in
`work/module-08-report.md`, titled “Jira Sprint Report - Technical
Specification”.

## User Stories

### US1 — View active sprint health (P1)

As a Scrum Master or team member, I can authenticate with Atlassian OAuth and
view the configured Jira project’s active sprint so that I can understand
delivery health without shared credentials.

**Acceptance scenarios**

- Given an authorized user and an active sprint, when the report loads, then it
  shows sprint dates, elapsed/remaining time, summary metrics, forecast, and
  issue board.
- Given no active sprint, when the report loads, then it shows a useful empty
  state rather than an empty success report.
- Given an unauthorized project, when the report loads, then it shows an
  actionable authorization error.

### US2 — Understand progress and forecast (P1)

As a user, I can see committed, completed, remaining, and unestimated story
points plus issue counts and a clearly labelled simple pace forecast.

**Acceptance scenarios**

- Missing or zero story points do not fail calculations and are identified as
  unestimated.
- The forecast is **On track** when completed-point proportion is at least the
  elapsed-time proportion; otherwise it is **At risk**.
- Pre-start, post-end, and zero-duration sprints are handled safely.

### US3 — Find blockers and delivery risks (P1)

As a user, I can see blocked and at-risk issues with the reasons that caused
each indicator.

**Acceptance scenarios**

- Blockers include the configured blocked label/flag or a Jira blocking link.
- Risk reasons include overdue incomplete work, at least three business days of
  inactivity, unresolved blockers, and post-start sprint additions.
- Business-day calculations use the configured project timezone, exclude
  weekends, and follow the documented holiday policy.

### US4 — Filter and inspect issues (P1)

As a user, I can filter by assignee, issue type, status/category, and risk
state, and open any issue directly in Jira.

**Acceptance scenarios**

- Filters consistently update summary, progress, blockers, risks, and board
  data.
- The UI identifies when metrics represent a filtered subset.
- Issues are grouped into configurable To Do, In Progress, and Done categories.

### US5 — Refresh safely (P1)

As a user, I can manually refresh the report and receive automatic refreshes
without losing the last good data.

**Acceptance scenarios**

- Data refreshes every five minutes while the report is open.
- Manual and automatic refreshes cannot overlap.
- A failed refresh preserves the last successful report and shows a visible
  stale-data/error state with the last successful refresh time.
- Rate limits, expired sessions, timeouts, missing permissions, and unavailable
  Jira data produce actionable errors.

## Functional Requirements

1. Use server-side Atlassian OAuth 2.0 authorization-code flow with secure,
   HTTP-only, same-site session cookies and validated OAuth state.
2. Keep OAuth secrets and Jira tokens out of browser JavaScript and logs.
3. Retrieve only required Jira fields, paginate issue results, and support
   issue-link and changelog/activity data.
4. Provide project discovery, active-sprint lookup, and a coherent normalized
   report endpoint.
5. Normalize statuses using configuration, calculate metrics and risks
   deterministically, and preserve risk reasons.
6. Use a short-lived server-side cache scoped to tenant/project/permission
   context and invalidate it on manual refresh.
7. Escape Jira text rendered in the UI and enforce authorization on every
   Jira-backed request.
8. Provide structured operational events for latency, failures, rate limits,
   OAuth, refresh, and cache behavior without sensitive payloads.

## Non-Goals

Historical trends, velocity reporting, multi-project reports, automation
quality metrics, issue editing, exports, scheduled distribution, long-term
snapshots, webhooks, and mobile-first optimization are excluded from release
one.

## Edge Cases

- No active sprint.
- Pre-start, post-end, and zero-duration sprint.
- Missing, zero, or mixed story-point values.
- Unknown or newly configured workflow statuses.
- Multiple risk reasons on one issue.
- Weekend and timezone boundaries.
- Jira pagination, rate limits, partial responses, expired OAuth, and stale
  cached data.

## Success Criteria

- An authorized user can sign in and view one project’s active sprint.
- Metrics, forecast, blockers, risks, filters, and issue links satisfy the
  acceptance scenarios for approximately 100 issues and 10 team members.
- No Jira access token or OAuth secret is exposed to the browser.
- The report remains usable on desktop and basic tablet widths.
