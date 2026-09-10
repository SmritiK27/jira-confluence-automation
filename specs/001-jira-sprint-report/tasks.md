# Tasks: Jira Sprint Report

## Phase 1 — Foundation

- [ ] Confirm framework, runtime, package manager, and design-system entry point.
- [ ] Create frontend, backend, and shared-types structure with local and
  production configuration.
- [ ] Define and validate OAuth, Jira, project, field, mapping, timezone,
  cache, stale-threshold, and session environment variables.
- [ ] Define normalized domain types and the report response contract.
- [ ] Implement secure sessions, OAuth login/callback/logout, state validation,
  least-privilege scopes, HTTPS enforcement, and health check.
- [ ] Implement structured logging and correlation with secret/content redaction.

## Phase 2 — Core Report

- [ ] Implement authenticated Jira client with selected fields, pagination,
  timeouts, rate-limit mapping, and project/sprint discovery.
- [ ] Implement active-sprint empty and boundary-time states.
- [ ] Implement configurable status normalization and story-point aggregation.
- [ ] Implement pace forecast and issue-board grouping.
- [ ] Implement report API and summary/progress/board presentation.

## Phase 3 — Blockers and Risks

- [ ] Detect configured blocked labels/flags and blocking-link directions.
- [ ] Implement timezone-aware business-day and stale-threshold calculations.
- [ ] Implement explainable overdue, inactivity, unresolved-blocker, and
  post-start risk reasons.
- [ ] Render blockers, risks, and issue-level indicators accessibly.

## Phase 4 — Filtering and Resilience

- [ ] Implement assignee, issue type, status/category, and risk filters across
  every report view.
- [ ] Add filtered-subset metric labeling.
- [ ] Add short-lived scoped cache, manual invalidation, and refresh single-flight
  protection.
- [ ] Add five-minute automatic refresh, manual refresh, stale fallback, and
  actionable error states.
- [ ] Add responsive styling, accessibility checks, issue-link validation, and
  operational telemetry.

## Phase 5 — Validation and Rollout

- [ ] Unit-test metrics, mappings, forecast boundaries, business days, blockers,
  risk combinations, and filtering.
- [ ] Test Jira pagination, required fields, timeout/rate-limit/partial-response
  handling, OAuth, sessions, token non-exposure, and API stale fallback.
- [ ] Add frontend/component and representative integration tests for roughly
  100 issues and 10 team members.
- [ ] Validate with a non-admin Jira user, deploy over HTTPS, and document
  environment variables, OAuth setup, and operations.
