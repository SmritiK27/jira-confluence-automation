# Jira Sprint Report Constitution

## Purpose

The Jira Sprint Report is a secure, read-only operational view of the active
sprint for a Scrum Master and a 10-person engineering team.

## Principles

1. **Specification-first delivery** — Requirements, acceptance criteria, and
   decisions are recorded before implementation.
2. **Secure by default** — Atlassian OAuth uses a server-side authorization-code
   flow. OAuth secrets and Jira access tokens never reach browser JavaScript,
   logs, or source control.
3. **Reliable reporting** — Upstream failures are explicit. Failed refreshes
   preserve the last successful report and show its stale state; they never
   become empty success responses.
4. **Configuration over assumptions** — Workflow status mappings, story-point
   field, blocked marker, timezone, stale threshold, and Jira project are
   configurable.
5. **Explainable metrics** — Forecasts and risks expose their inputs and
   reasons. A pace forecast is not presented as statistical prediction.
6. **Accessible usability** — Status, risk, and blocker information is not
   conveyed by color alone. Desktop and basic tablet layouts are supported.
7. **Testable increments** — Domain calculations are deterministic and tested
   independently from Jira transport and UI concerns.

## Quality Gates

- Every feature maps to a requirement and acceptance criterion.
- Security-sensitive flows have tests for authorization, session handling, and
  token non-exposure.
- Domain calculations cover missing values, zero values, time boundaries,
  business days, and filtering.
- Jira calls use required-field selection, pagination, timeouts, and structured
  errors.
- Documentation describes required environment variables, OAuth setup, and
  operational health checks.

## Scope Boundary

The first release is limited to one Jira Cloud project and its active sprint.
It does not include historical velocity, multi-project reporting, issue
editing, exports, scheduled distribution, long-term issue snapshots, webhook
updates, or mobile-first optimization.
