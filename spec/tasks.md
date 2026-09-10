# Jira Sprint Report Implementation Tasks

## Task conventions

- **Status:** All tasks are initially `Not started`.
- **Dependencies:** A task must not begin until its listed dependencies and the
  relevant clarification decisions are complete.
- **Acceptance criteria:** Every criterion must be demonstrable or testable.
- **Source of truth:** [`specification.md`](./specification.md),
  [`constitution.md`](./constitution.md), and approved resolutions recorded from
  [`clarify.md`](./clarify.md).

## Phase 0 — Specification Baseline

### T-001 — Resolve release scope and write permissions

- **Dependencies:** None
- **Deliverable:** Approved release-scope decision recorded in the
  specification.
- **Acceptance criteria:**
  - The release explicitly states whether it is Jira-only or includes
    Confluence.
  - Any permitted Jira/Confluence write operations are listed.
  - Read-only source access is distinguished from application persistence.
  - Non-goals and APIs match the approved scope.

### T-002 — Define tenant, project, and role model

- **Dependencies:** T-001
- **Deliverable:** Tenant/project/role decision and configuration ownership
  rules.
- **Acceptance criteria:**
  - The supported tenant count and isolation model are documented.
  - Project configuration ownership and authorized administrators are defined.
  - Project changes, onboarding, removal, and audit behavior are specified.
  - Access to an unconfigured or unauthorized project has a defined response.

### T-003 — Approve OAuth and session lifecycle

- **Dependencies:** T-002
- **Deliverable:** OAuth and session security decision.
- **Acceptance criteria:**
  - Atlassian scopes, endpoints, redirect URIs, PKCE, and state validation are
    documented.
  - Token storage/encryption, refresh rotation, revocation, session lifetime,
    idle timeout, consent denial, and logout are defined.
  - User identity mapping and expired-refresh-token behavior are defined.

### T-004 — Approve Jira integration contract

- **Dependencies:** T-002, T-003
- **Deliverable:** Jira API integration decision.
- **Acceptance criteria:**
  - REST/Agile API versions and endpoints are listed.
  - Required fields, story-point field discovery, status data, issue links,
    and changelog/activity retrieval are defined.
  - JQL/sprint query, page size, page limit, pagination termination, timeout,
    retry, and `Retry-After` rules are specified.

### T-005 — Approve domain semantics

- **Dependencies:** T-004
- **Deliverable:** Decision record for timing, metrics, forecast, statuses,
  blockers, risks, and filters.
- **Acceptance criteria:**
  - Timezone, date boundaries, rounding, daylight-saving, and holiday rules
    are explicit.
  - Zero-point, invalid-point, remaining-work, completion, and zero-committed
    forecast behavior is explicit.
  - Status mapping and unmapped-status policy are explicit.
  - Blocker, inactivity, due-date, late-addition, and multiple-risk rules are
    explicit.
  - Filter combination, ordering, URL state, and filtered-total behavior are
    explicit.

### T-006 — Approve schemas, persistence, and operational targets

- **Dependencies:** T-001 through T-005
- **Deliverable:** Versioned API/data contracts and persistence decision.
- **Acceptance criteria:**
  - Success and error JSON schemas define types, nullability, enums, dates,
    precision, ordering, status codes, and correlation IDs.
  - PostgreSQL tables, migrations, indexes, retention, deletion, encryption,
    backup, and transaction rules are defined.
  - Cache/session storage choices and isolation rules are defined.
  - Response-time, availability, browser, accessibility, logging, alerting,
    and disaster-recovery targets are approved.

### M-000 — Specification baseline approved

- **Dependencies:** T-001 through T-006
- **Milestone acceptance criteria:**
  - Critical gaps C-01 through C-08 have approved resolutions.
  - Contradictions X-01 through X-05 are resolved or explicitly accepted.
  - Specification, constitution, schemas, and persistence decisions agree.
  - Product, technical, and security owners approve the baseline.

## Phase 1 — Foundation and Secure Runtime

### T-101 — Establish repository and toolchain

- **Dependencies:** M-000
- **Deliverable:** React/Vite, Express, shared-types, tests, scripts, and
  environment templates.
- **Acceptance criteria:**
  - React 18 + Vite and Node.js + Express applications start locally.
  - The selected Node.js version and package manager are documented.
  - Frontend, backend, domain, integration, and test boundaries are visible.
  - No secrets are present in committed templates.

### T-102 — Provision local PostgreSQL

- **Dependencies:** T-101, T-006
- **Deliverable:** Docker Compose PostgreSQL 15 service and database tooling.
- **Acceptance criteria:**
  - A clean checkout can start PostgreSQL 15 with Docker Compose.
  - Connection configuration is environment-driven.
  - Migrations run forward and rollback according to the approved policy.
  - Database credentials are not committed or printed in logs.

### T-103 — Implement configuration validation

- **Dependencies:** T-101, T-006
- **Deliverable:** Typed startup configuration loader.
- **Acceptance criteria:**
  - Missing/invalid OAuth, Jira, database, project, mapping, timezone, cache,
    and session settings fail startup with actionable field-level errors.
  - Local development exceptions are explicit and limited.
  - Valid configuration loads without logging secret values.

### T-104 — Implement persistence schema and migrations

- **Dependencies:** T-102, T-006
- **Deliverable:** Approved PostgreSQL schema for configuration, sessions/cache
  metadata, and operational state.
- **Acceptance criteria:**
  - Tables, constraints, indexes, ownership, and retention match the decision.
  - Multi-step writes use transactions.
  - No long-term Jira issue snapshot is persisted unless explicitly approved.
  - Migration tests cover a clean install and upgrade path.

### T-105 — Implement health, readiness, and safe observability

- **Dependencies:** T-101, T-102
- **Deliverable:** Health/readiness endpoints, correlation IDs, structured
  logging, and redaction.
- **Acceptance criteria:**
  - Health reports application availability without exposing configuration.
  - Readiness detects required database/service availability.
  - Requests and background operations receive correlation IDs.
  - Tokens, secrets, page bodies, issue descriptions, and credentials are
    redacted from logs and errors.

### T-106 — Implement OAuth and secure sessions

- **Dependencies:** T-003, T-104, T-105
- **Deliverable:** Login, callback, logout, session middleware, token lifecycle,
  and authorization middleware.
- **Acceptance criteria:**
  - Valid users can complete the approved Atlassian OAuth flow.
  - Invalid state, PKCE, callback, consent, and refresh-token cases fail safely.
  - Cookies use approved secure, HTTP-only, same-site attributes.
  - Logout invalidates the application session and approved provider tokens.
  - Access tokens and client secrets never reach browser JavaScript or logs.

### T-107 — Enforce transport and request security

- **Dependencies:** T-106
- **Deliverable:** HTTPS enforcement, request validation, security headers, and
  safe error handling.
- **Acceptance criteria:**
  - Non-local HTTP requests are redirected or rejected according to policy.
  - Invalid request parameters produce the standard error schema.
  - Security headers and CSRF/state protections match the approved threat model.

### M-100 — Secure application skeleton complete

- **Dependencies:** T-101 through T-107
- **Milestone acceptance criteria:**
  - Docker database, migrations, configuration, health checks, OAuth, sessions,
    and redacted logs work in a clean local environment.
  - Foundation tests pass, including OAuth failure and secure-cookie cases.
  - Secret/token scanning reports no committed or emitted credentials.

## Phase 2 — Jira Integration and Domain Model

### T-201 — Build authenticated Jira client

- **Dependencies:** T-004, T-106, M-100
- **Deliverable:** User-scoped Jira Cloud client.
- **Acceptance criteria:**
  - Requests use approved endpoints, scopes, fields, and authenticated user
    context.
  - Timeouts, cancellation, pagination, and response-size limits are enforced.
  - No access token appears in client responses, logs, or thrown errors.

### T-202 — Implement Jira retry and error mapping

- **Dependencies:** T-201
- **Deliverable:** Bounded retry/backoff and structured integration errors.
- **Acceptance criteria:**
  - Only approved transient failures are retried.
  - `Retry-After`, maximum attempts, timeout budget, and backoff bounds are
    honored.
  - Authorization, rate-limit, timeout, unavailable, malformed, and partial
    responses map to documented error codes.
  - Retry exhaustion returns an actionable non-success response.

### T-203 — Implement project and sprint discovery

- **Dependencies:** T-201, T-202, T-002
- **Deliverable:** Project list/access check and active-sprint discovery service.
- **Acceptance criteria:**
  - Only authorized projects are returned.
  - Configured selection precedence handles multiple boards/sprints.
  - No active sprint and unavailable sprint states are distinct and actionable.
  - The service does not fabricate empty project/sprint data after failure.

### T-204 — Define normalized domain types

- **Dependencies:** T-005, T-006
- **Deliverable:** Shared types for project, sprint, issue, category, blocker,
  risk, filters, metrics, forecast, refresh, and errors.
- **Acceptance criteria:**
  - Types match the approved versioned contract.
  - Nullability, units, precision, date format, enums, and ordering are encoded.
  - Jira-specific response objects do not leak into frontend/domain contracts.

### T-205 — Implement time and business-day rules

- **Dependencies:** T-005, T-204
- **Deliverable:** Pure timezone-aware sprint timing and business-day helpers.
- **Acceptance criteria:**
  - Pre-start, active, post-end, zero-duration, DST, weekend, and holiday cases
    return approved values.
  - Inclusive/exclusive boundaries and rounding are covered by tests.
  - The functions are deterministic with an injected clock.

### T-206 — Implement status normalization

- **Dependencies:** T-005, T-204
- **Deliverable:** Configuration-driven To Do/In Progress/Done mapping.
- **Acceptance criteria:**
  - Mapping precedence and status ID/name behavior match the decision.
  - Unknown/unmapped statuses follow the approved safe path.
  - Status changes do not require UI code changes.

### T-207 — Implement story-point metrics

- **Dependencies:** T-005, T-204, T-206
- **Deliverable:** Metrics aggregation service.
- **Acceptance criteria:**
  - Committed, completed, remaining, completion percentage, issue counts, and
    unestimated values match the approved formulas.
  - Missing, zero, decimal, negative, and invalid points follow the policy.
  - Reopened, removed, and late-added issue behavior is tested.
  - Filtered and unfiltered metrics are distinguishable.

### T-208 — Implement pace forecast

- **Dependencies:** T-205, T-207
- **Deliverable:** Explainable simple pace forecast.
- **Acceptance criteria:**
  - Completed-point and elapsed-time proportions are returned.
  - On-track/at-risk comparison uses the approved inclusive threshold.
  - Zero committed points and zero-duration/pre-start/post-end states use the
    approved non-misleading status.
  - Output is labelled as a simple pace forecast.

### T-209 — Validate and normalize Jira issue data

- **Dependencies:** T-201, T-202, T-204, T-206, T-207
- **Deliverable:** Issue normalization pipeline with required/optional field
  validation.
- **Acceptance criteria:**
  - Required-field failures follow the approved fail/degraded policy.
  - Optional missing fields become explicit null/unknown values.
  - Issue text is safe for downstream rendering.
  - Jira URLs are constructed from a validated tenant base URL and issue key.

### M-200 — Deterministic domain report complete

- **Dependencies:** T-203 through T-209
- **Milestone acceptance criteria:**
  - Safe Jira fixtures produce the approved normalized report contract.
  - Domain tests cover metrics, status, timing, forecast, parsing, pagination,
    rate limits, malformed data, permissions, and partial responses.
  - No domain calculation requires live Jira access.

## Phase 3 — Report API and Core UI

### T-301 — Implement versioned report API

- **Dependencies:** M-200, T-006
- **Deliverable:** Versioned project, active-sprint, and report endpoints.
- **Acceptance criteria:**
  - Endpoints validate inputs and return approved success/error schemas.
  - Every Jira-backed request enforces user/project authorization.
  - Correlation IDs are returned and safe user guidance is included on errors.
  - Response ordering and pagination metadata match the contract.

### T-302 — Implement report aggregation service

- **Dependencies:** M-200, T-301
- **Deliverable:** Service that combines sprint metadata, normalized issues,
  metrics, forecast, blockers/risks placeholders, filters, and refresh state.
- **Acceptance criteria:**
  - One coherent response drives all core views.
  - Failed or incomplete upstream calls cannot become empty success reports.
  - No secrets or unnecessary Jira content appear in the response.

### T-303 — Build React application shell and authentication states

- **Dependencies:** T-101, T-301
- **Deliverable:** Vite routes/layout with loading, authentication,
  authorization, no-sprint, empty, and error states.
- **Acceptance criteria:**
  - Unauthenticated, unauthorized, loading, no-sprint, and integration-error
    states are distinct and actionable.
  - State transitions preserve safe user context and do not expose tokens.
  - Controls are keyboard accessible with meaningful labels and focus states.

### T-304 — Build sprint summary and forecast UI

- **Dependencies:** T-302, T-303
- **Deliverable:** Sprint header, summary cards, timing, and pace visualization.
- **Acceptance criteria:**
  - All approved summary metrics are displayed with units and timestamps.
  - Unestimated work is visibly distinct.
  - Forecast is labelled “Simple pace forecast” and exposes its inputs/status.
  - Status is not conveyed by color alone.

### T-305 — Build issue board

- **Dependencies:** T-302, T-303, T-206
- **Deliverable:** To Do, In Progress, and Done issue groups.
- **Acceptance criteria:**
  - Every issue displays approved fields, optional values, and normalized status.
  - Direct Jira links are validated and open the configured tenant.
  - Empty groups and unknown statuses have approved messaging.
  - The layout works at the approved desktop and tablet widths.

### M-300 — End-to-end core report complete

- **Dependencies:** T-301 through T-305
- **Milestone acceptance criteria:**
  - An authorized user can sign in and view a coherent active-sprint report.
  - Summary, forecast, board, and links come from the same API contract.
  - API contract and frontend tests pass.
  - Accessibility checks pass for core navigation and non-color indicators.

## Phase 4 — Blockers, Risks, and Filtering

### T-401 — Implement blocker detection

- **Dependencies:** T-005, T-204, T-209
- **Deliverable:** Label/flag and direction-aware issue-link blocker service.
- **Acceptance criteria:**
  - Marker matching, case normalization, link types, direction, and duplicate
    reasons follow the approved policy.
  - The service identifies whether a linked blocker is unresolved as required.
  - Blocker source and reason are preserved in the normalized response.

### T-402 — Implement risk detection

- **Dependencies:** T-005, T-205, T-401, T-209
- **Deliverable:** Explainable risk rule engine.
- **Acceptance criteria:**
  - Overdue, inactivity, unresolved-blocker, and late-addition rules are
    independently testable.
  - Due-date timezone/boundary and activity event rules are respected.
  - Sprint membership timestamp and fallback behavior are respected.
  - Multiple risk reasons are returned without collapsing them into an opaque
    score.

### T-403 — Add blockers and risks to report API

- **Dependencies:** T-401, T-402, T-302
- **Deliverable:** Populated blockers and risks in the versioned report.
- **Acceptance criteria:**
  - Blockers and risk rows contain all approved issue fields and direct links.
  - A report with no blockers/risks is a valid, explicit empty collection.
  - Detection failures follow the partial-response policy.

### T-404 — Build blockers and risk UI

- **Dependencies:** T-403, T-303
- **Deliverable:** Blocker table, at-risk table, and issue-level indicators.
- **Acceptance criteria:**
  - Source and reason are visible for each blocker/risk.
  - Multiple reasons remain distinguishable.
  - Empty, loading, stale, and error states are accessible and actionable.

### T-405 — Implement filter model and URL state

- **Dependencies:** T-005, T-204, T-302
- **Deliverable:** Shared filter state and approved combination semantics.
- **Acceptance criteria:**
  - Assignee, issue type, status/category, and risk filters are supported.
  - AND/OR semantics, empty selections, ordering, and deep-link persistence
    match the decision.
  - Filter state is validated and cannot bypass authorization.

### T-406 — Apply filters consistently

- **Dependencies:** T-405, T-207, T-403
- **Deliverable:** Filtered report aggregation and UI wiring.
- **Acceptance criteria:**
  - One filtered issue set drives summary, progress, blockers, risks, and board.
  - Filtered metrics are labelled and unfiltered totals remain available as
    approved.
  - No stale filter results remain after filter changes.

### M-400 — Explainable risk report complete

- **Dependencies:** T-401 through T-406
- **Milestone acceptance criteria:**
  - Fixtures demonstrate multiple blocker/risk reasons.
  - Boundary and combination tests pass.
  - Filters update every dependent view consistently.
  - Users can distinguish filtered metrics from full-sprint metrics.

## Phase 5 — Refresh, Cache, and Resilience

### T-501 — Implement permission-safe cache

- **Dependencies:** T-006, M-200, T-203
- **Deliverable:** Scoped short-lived cache with approved key and retention
  behavior.
- **Acceptance criteria:**
  - Cache keys isolate tenant, project, user/permission context as approved.
  - TTL, maximum size, eviction, and invalidation are enforced.
  - Cache entries cannot outlive approved authorization/session boundaries.
  - Cache hits/misses and evictions are observable without sensitive payloads.

### T-502 — Implement refresh coordinator

- **Dependencies:** T-501, T-302
- **Deliverable:** Single-flight refresh service with timeout and cancellation.
- **Acceptance criteria:**
  - Concurrent manual/scheduled requests share or reject work according to the
    approved policy; Jira is not redundantly refreshed.
  - Timeout and cancellation do not corrupt last-known-good data.
  - Refresh status includes request state, stale flag, and safe error.

### T-503 — Implement stale fallback

- **Dependencies:** T-502, T-006
- **Deliverable:** Last-known-good report persistence/retention and fallback.
- **Acceptance criteria:**
  - Successful reports are retained only for the approved period and scope.
  - Failed refreshes preserve the last successful report and mark it stale.
  - No prior report is shown to a user who is no longer authorized.
  - A first-ever failed refresh shows an explicit no-data error state.

### T-504 — Implement automatic and manual refresh UX

- **Dependencies:** T-502, T-503, T-303
- **Deliverable:** Five-minute refresh timer, visibility behavior, manual action,
  retry, and multi-tab behavior.
- **Acceptance criteria:**
  - Timer starts/stops according to the approved page-visibility policy.
  - Manual refresh gives progress feedback and cannot overlap.
  - Retry and error messages provide approved actionable guidance.
  - Multiple tabs follow the approved coordination behavior.

### T-505 — Add resilience telemetry

- **Dependencies:** T-105, T-501, T-502
- **Deliverable:** Safe metrics/events for refresh and integration behavior.
- **Acceptance criteria:**
  - Events include correlation ID, safe tenant/project identifiers, latency,
    retry count, stale age, cache result, and failure category.
  - Tokens, issue descriptions, page bodies, and credentials are excluded.
  - Alert thresholds are implemented for approved stale/failure conditions.

### M-500 — Resilient daily operation complete

- **Dependencies:** T-501 through T-505
- **Milestone acceptance criteria:**
  - Scheduled/manual refreshes do not overlap.
  - Failed refresh preserves and labels last-known-good data.
  - Cache isolation, invalidation, expiry, and permission changes are tested.
  - Timeout, rate-limit, partial-response, and expired-session flows are
    actionable.

## Phase 6 — Hardening and Release

### T-601 — Complete automated verification

- **Dependencies:** M-500
- **Deliverable:** Passing unit, API, integration, frontend, migration, build,
  type-check, and lint results.
- **Acceptance criteria:**
  - Every applicable specification acceptance criterion maps to a passing test.
  - Edge cases and failure paths are covered.
  - Tests are deterministic and do not require production credentials.

### T-602 — Run scale and performance validation

- **Dependencies:** T-601, T-006
- **Deliverable:** Performance report for approximately 100 issues and 10 users.
- **Acceptance criteria:**
  - Approved initial-load, refresh, API, and filter response budgets are met.
  - Pagination, memory, database, and browser behavior remain stable at target
    scale.
  - Any exceeded budget has an approved mitigation or release decision.

### T-603 — Perform security review

- **Dependencies:** T-601, T-602
- **Deliverable:** Security review and remediation record.
- **Acceptance criteria:**
  - OAuth, cookies, authorization, cache isolation, URL validation, XSS-safe
    rendering, logs, and secret handling are reviewed.
  - No unresolved critical/high security or data-integrity issue remains.
  - Secret/token scanning passes for source, artifacts, logs, and test output.

### T-604 — Validate deployment and operations

- **Dependencies:** T-102, T-104, T-105, T-603
- **Deliverable:** Deployment, migration, backup/restore, monitoring, alerting,
  and rollback runbooks.
- **Acceptance criteria:**
  - Docker/local and target deployment startup are reproducible.
  - Migrations, backup, restore, rollback, health/readiness, and alert checks
    are exercised.
  - Required environment variables, OAuth setup, support ownership, and
    escalation paths are documented.

### T-605 — Conduct stakeholder acceptance

- **Dependencies:** T-601 through T-604
- **Deliverable:** Recorded product, technical, and security sign-off.
- **Acceptance criteria:**
  - A non-admin user validates authorization and representative Jira behavior.
  - All in-scope user scenarios pass against safe representative data.
  - Accessibility target and responsive behavior are accepted.
  - Release risks, known limitations, and rollback owner are recorded.

### M-600 — Release candidate approved

- **Dependencies:** T-605
- **Milestone acceptance criteria:**
  - All specification and constitution quality gates pass.
  - Performance/scale targets are met.
  - No unresolved critical security or data-integrity findings remain.
  - Operational runbooks, backups, monitoring, and rollback are ready.
  - Product, technical, and security owners approve release.
