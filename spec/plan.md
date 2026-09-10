# Implementation Plan: Jira Sprint Report

## 1. Plan Status and Baseline

- **Status:** Proposed; release scope is approved, but implementation is
  blocked until the remaining clarification decisions in
  [`spec/clarify.md`](./clarify.md) are accepted.
- **Specification:** [`spec/specification.md`](./specification.md)
- **Constitution:** [`spec/constitution.md`](./constitution.md)
- **Target stack:** React 18 + Vite, Node.js + Express, PostgreSQL 15,
  Docker/Docker Compose
- **Release target:** First-release MVP for one Jira Cloud project and its
  active sprint
- **Initial scale:** Approximately 100 sprint issues and 10 team members

The plan deliberately treats unresolved scope, OAuth, cache isolation, schema,
time-calculation, and persistence questions as exit criteria for planning.
Implementation must not silently invent answers to those questions.

## 2. Delivery Approach

Work is organized into vertical, demonstrable increments. Each phase has a
milestone, dependencies, verification activities, and an exit gate. Domain
rules are implemented as pure functions before they are connected to Jira or
the UI. The backend owns authentication, Jira access, normalization,
aggregation, caching, and error mapping. The frontend consumes only the
normalized API contract.

### Architectural boundaries

```text
React/Vite frontend
        |
Versioned Express API
        |
Application services
  |       |        |
Jira   Auth     Persistence/cache
client  flow    PostgreSQL 15
        |
Normalized domain/report model
```

- **Frontend:** presentation, filtering state, refresh UX, accessibility.
- **Backend:** authorization, orchestration, validation, error handling,
  refresh coordination, and safe response shaping.
- **Domain:** status mapping, metrics, forecast, blockers, risks, time rules.
- **Jira integration:** Atlassian API calls, pagination, rate limits, field
  selection, and response validation.
- **Database:** only approved configuration, session, cache metadata, and
  operational state; no long-term Jira issue snapshots in release one.

## 3. Pre-Implementation Milestone: Resolve the Specification

### Objective

Close the decisions that materially change architecture, API contracts, schema,
or acceptance tests.

### Required decisions

1. Define tenant model, project configuration ownership, and admin roles.
2. Select Atlassian OAuth scopes, PKCE/state requirements, token storage,
    refresh/revocation, session lifetime, and logout behavior.
3. Select Jira REST/Agile API versions, endpoints, fields, field-discovery
    strategy, pagination, and changelog retrieval.
4. Define cache isolation, TTL, eviction, invalidation, and permission context.
5. Approve versioned JSON/TypeScript schemas for success and error responses.
6. Decide PostgreSQL persistence, migrations, retention, and deletion rules.
7. Define exact sprint-time, forecast, story-point, status, blocker, risk, and
    filter semantics.
8. Set response-time, availability, browser, accessibility, logging, backup,
    and disaster-recovery targets.

### Milestone M0: Specification baseline approved

**Exit criteria**

- The release-scope decisions C-01, C-02, and X-01 are recorded and reflected
  in the specification.
- Remaining critical items C-03 through C-08 and contradictions X-02 through
  X-05 are resolved or explicitly accepted.
- Decisions are reflected in the specification and API/data contracts.
- Product owner, security owner, and technical owner approve the baseline.

## 4. Phase 1: Foundation and Secure Runtime

### Objective

Create a runnable React/Express/PostgreSQL application with validated
configuration, secure sessions, observability, and local Docker development.

### Work packages

1. Confirm Node.js version, package manager, repository layout, and approved
   libraries.
2. Create Vite React frontend, Express backend, shared domain/types package,
   test structure, and environment templates.
3. Add Docker Compose for PostgreSQL 15 and local service startup.
4. Add startup configuration validation for OAuth, Jira, database, project,
   field mappings, timezone, cache, and session settings.
5. Establish PostgreSQL migration tooling, connection pooling, health checks,
   and approved persistence schema.
6. Implement correlation IDs, structured logging, redaction, readiness, and
   liveness endpoints.
7. Implement secure OAuth login, callback, state/PKCE validation, session
   creation, logout, expiry, and authorization middleware.
8. Enforce HTTPS outside local development and secure cookie attributes.

### Milestone M1: Secure application skeleton

**Demonstration**

- Local Docker database starts reproducibly.
- Invalid required configuration fails clearly at startup.
- A user can complete the approved OAuth flow and log out.
- Health/readiness endpoints work without exposing secrets.
- Logs contain correlation IDs but no tokens or source content.

**Verification**

- Configuration and migration tests.
- OAuth success, denial, invalid-state, callback-error, expiry, logout, and
  secure-cookie tests.
- Secret/token scanning and redacted-log tests.

## 5. Phase 2: Jira Integration and Domain Model

### Objective

Build a safe Jira Cloud client and deterministic normalized domain layer.

### Work packages

1. Implement the Jira client with approved API endpoints, authenticated
   user-scoped requests, required field selection, timeouts, and pagination.
2. Implement retry/backoff and `Retry-After` handling for approved retryable
   failures.
3. Map authorization, rate-limit, timeout, unavailable-resource, malformed,
   and partial responses to structured errors.
4. Implement project listing and configured-project access checks.
5. Implement active-sprint discovery and the approved multiple-sprint/board
   selection policy.
6. Define normalized project, sprint, issue, status, blocker, risk, filter,
   metric, forecast, refresh, and error types.
7. Implement timezone-aware sprint timing and business-day helpers.
8. Implement configurable status normalization, including unmapped-status
   handling.
9. Implement story-point validation, unestimated handling, totals, remaining
   work, completion percentage, and issue counts.
10. Implement safe forecast states, including zero points, zero duration,
    pre-start, and post-end cases.

### Milestone M2: Deterministic domain report

**Demonstration**

- Jira fixtures normalize into the approved report contract.
- Metrics and forecast are reproducible without network access.
- Invalid and partial Jira responses fail or degrade according to the approved
  policy.
- Domain calculations handle all documented edge cases.

**Verification**

- Unit tests for metrics, statuses, timing, business days, forecast, parsing,
  and error mapping.
- Fixture tests for pagination, required fields, rate limits, malformed data,
  and authorization failures.

## 6. Phase 3: Report API and Core User Experience

### Objective

Expose the normalized report and deliver the primary sprint-health experience.

### Work packages

1. Implement versioned project, active-sprint, and report endpoints.
2. Validate request parameters and enforce project/user authorization.
3. Implement summary cards, sprint header, timing, and simple pace forecast.
4. Implement issue board with To Do, In Progress, and Done groups.
5. Implement issue rows/cards, safe Jira links, assignee/type/status display,
   story points, due dates, and unestimated indicators.
6. Implement loading, empty, no-sprint, authorization, integration-error, and
   authentication states.
7. Add accessible labels, keyboard navigation, focus states, semantic tables,
   and non-color status indicators.
8. Apply desktop-first responsive layout and company design-system components
   where available.

### Milestone M3: End-to-end core report

**Demonstration**

- An authorized user signs in and views one project's active sprint.
- Summary, forecast, issue board, and direct Jira links use the same normalized
  response.
- No active sprint and project-access failures are actionable.

**Verification**

- API contract tests against the approved schemas.
- Frontend component tests for summary, forecast, board, links, loading,
  empty, and authorization/error states.
- Accessibility checks for keyboard and non-color requirements.

## 7. Phase 4: Blockers, Risks, and Filtering

### Objective

Make impediments and delivery risk explainable and consistently filterable.

### Work packages

1. Implement exact configured blocked-label/flag matching.
2. Implement direction-aware blocking-link detection and source/reason output.
3. Implement overdue, inactivity, unresolved-blocker, and late-addition rules
   using the approved timestamps and business-day policy.
4. Preserve and display multiple risk reasons per issue.
5. Build blockers and at-risk tables with direct Jira links.
6. Implement assignee, issue type, status/category, and risk-state filters.
7. Apply the approved AND/OR semantics, ordering, URL/state persistence, and
   filtered-subset labeling.
8. Ensure one filtered issue set drives metrics, progress, blockers, risks, and
   board groups.

### Milestone M4: Explainable risk report

**Demonstration**

- A fixture issue can show multiple blocker and risk reasons.
- Each risk reason is understandable and traceable to source data.
- Filters update every dependent view consistently.
- The UI distinguishes filtered metrics from full-sprint metrics.

**Verification**

- Unit tests for each rule and combinations.
- Boundary tests for due dates, inactivity, timezone, weekends, holidays, and
  sprint membership changes.
- Frontend tests for filters, risk reasons, blocker sources, and filtered labels.

## 8. Phase 5: Refresh, Caching, and Resilience

### Objective

Make the report safe for daily use under stale data, concurrency, and upstream
failures.

### Work packages

1. Implement the approved scoped short-lived cache and cache observability.
2. Add permission-safe cache keys, TTL, eviction, invalidation, and manual
   refresh bypass.
3. Implement single-flight refresh coordination and request timeouts.
4. Add five-minute refresh scheduling with approved tab-visibility and
   multi-tab behavior.
5. Preserve last-known-good reports after failed refreshes and mark them stale.
6. Render actionable rate-limit, expired-session, timeout, permission, partial,
   and unavailable-data messages.
7. Add retry controls and manual refresh state without overlapping requests.
8. Add operational metrics for refresh success/failure, latency, stale age,
   retries, cache hit/miss, and rate-limit events.

### Milestone M5: Resilient daily operation

**Demonstration**

- Scheduled and manual refreshes never overlap.
- A failed refresh keeps the last successful report visible and labelled stale.
- Permission-safe cache behavior is proven across users/tenants.
- Rate limits and expired sessions give actionable next steps.

**Verification**

- API concurrency and stale-fallback tests.
- Cache isolation, invalidation, expiry, and permission-change tests.
- Browser lifecycle tests for timer, visibility, retry, and refresh UX.
- Failure-injection tests for timeout, rate limit, partial response, and
  expired OAuth.

## 9. Phase 6: Hardening, Operations, and Release

### Objective

Validate the complete product against security, scale, accessibility, and
operational requirements.

### Work packages

1. Run full unit, API, integration, frontend, migration, and type/build checks.
2. Test representative fixtures with approximately 100 issues and 10 users.
3. Verify non-admin Jira permissions and inaccessible-project behavior.
4. Perform security review for OAuth, cookies, authorization, cache isolation,
   XSS-safe rendering, URL validation, logs, and secrets.
5. Validate Docker startup, migrations, backups, restore procedure, and
   environment-based deployment.
6. Validate health/readiness checks, dashboards, alerts, correlation IDs, and
   escalation documentation.
7. Perform accessibility review against the approved conformance target.
8. Document setup, environment variables, OAuth registration, Jira field
   configuration, status/risk rules, deployment, operations, and rollback.
9. Conduct stakeholder acceptance review and obtain release approval.

### Milestone M6: Release candidate

**Exit criteria**

- All applicable specification acceptance criteria pass.
- Constitution quality gates pass.
- No unresolved critical security or data-integrity findings remain.
- Performance and scale target is met.
- Operational runbooks, backups, monitoring, and rollback are ready.
- An authorized non-admin user validates the report in a representative Jira
  project.

## 10. Cross-Phase Dependency Map

| Dependency | Required before |
| --- | --- |
| Scope and Confluence decision | All implementation |
| OAuth, tenant, and permission decisions | Foundation and Jira client |
| Exact normalized/API schemas | Jira integration and frontend |
| Time, status, blocker, risk, and filter semantics | Domain implementation |
| Persistence and retention decisions | Database and cache implementation |
| Security review of cache and links | Resilience and release |
| Representative Jira fixtures | Integration and release validation |

## 11. Risk Register

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Unresolved Jira/Confluence scope | Rework and incompatible APIs | Make M0 approval mandatory. |
| OAuth or permission mismatch | Data exposure or unusable report | Use user-scoped access, explicit scopes, and non-admin tests. |
| Permission-unsafe cache | Cross-user data disclosure | Define cache key/isolation before implementation; test it. |
| Jira workflow variation | Incorrect metrics and risk | Configure by approved status IDs/mappings and handle unknowns explicitly. |
| Ambiguous time semantics | Incorrect forecast/risk decisions | Approve timezone, boundary, rounding, and holiday rules at M0. |
| Partial upstream data | Misleading report | Validate required fields and preserve last-known-good data. |
| Rate limiting or slow Jira API | Poor refresh experience | Paginate, cache safely, bound retries, and show stale state. |
| Sensitive content in logs/UI | Privacy/security incident | Redaction, encoding, secret scanning, and security tests. |

## 12. Definition of Ready

A phase or milestone may start only when:

- Its requirements and acceptance tests are linked to the specification.
- Required upstream decisions are resolved.
- Test fixtures and safe sample data are available.
- Security and data-retention implications are understood.
- The implementation owner and validation owner are identified.

## 13. Definition of Done

The implementation is complete only when:

- All in-scope acceptance criteria pass.
- Unit, API, integration, frontend, migration, and security checks applicable
  to the release pass.
- OAuth secrets, access tokens, passwords, and sensitive Jira content are not
  exposed in source, browser code, logs, or test output.
- Failed refreshes preserve and label last-known-good data.
- The report supports the target issue/team scale.
- Documentation covers configuration, OAuth, deployment, health checks,
  monitoring, backup/restore, and rollback.
- Release approval is recorded by the product, technical, and security owners.
