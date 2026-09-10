# Implementation Task Analysis

## Review Scope

This analysis cross-checks:

- [`spec/tasks.md`](./tasks.md)
- [`spec/plan.md`](./plan.md)
- [`spec/specification.md`](./specification.md)
- [`spec/constitution.md`](./constitution.md)
- [`spec/clarify.md`](./clarify.md)

Complexity reflects implementation effort, integration difficulty, security
impact, and test burden. The plan remains blocked at M-000 until the
clarification decisions are approved.

## Summary

- **Tasks reviewed:** 42 implementation tasks, including 7 milestone gates.
- **Highest-risk work:** OAuth/session security, Jira integration, cache
  isolation, stale fallback, and domain semantics.
- **Primary blocker:** OAuth, API contracts, persistence, domain semantics,
  cache isolation, and operational targets remain unresolved and correctly
  block Phase 0 completion.
- **Main planning weakness:** There is no explicit requirements traceability
  matrix, decision-record artifact, fixture strategy, or ownership/status
  mechanism.
- **Resolved scope decision:** Release one is Jira-only and read-only against
  Jira/Confluence; the constitution's Confluence automation language is
  explicitly future scope.

## Complexity Scale

- **Low:** Localized work with limited external integration and straightforward
  verification.
- **Medium:** Multiple components or meaningful domain/infrastructure behavior,
  but bounded integration risk.
- **High:** Security-sensitive, cross-cutting, externally integrated, stateful,
  or difficult-to-test work.

## Task-by-Task Assessment

### Phase 0 — Specification Baseline

| ID | Task | Complexity | Dependencies | Key risks |
| --- | --- | --- | --- | --- |
| T-001 | Resolve release scope and write permissions | High | None | Resolved: release one is Jira-only and read-only against source systems. Remaining risk is keeping future Confluence work out of release-one APIs, scopes, and acceptance tests. |
| T-002 | Define tenant, project, and role model | High | T-001 | Project selection versus one configured project is unresolved. Incorrect isolation or role assumptions can cause unauthorized data exposure. |
| T-003 | Approve OAuth and session lifecycle | High | T-002 | Missing scopes, PKCE, token storage, refresh, revocation, and session rules block secure implementation. Provider behavior may constrain the design. |
| T-004 | Approve Jira integration contract | High | T-002, T-003 | Jira API/version, custom fields, changelog, pagination, and retry decisions affect the entire integration layer. |
| T-005 | Approve domain semantics | High | T-004 | Ambiguous time, points, status, blocker, risk, and filter rules can produce materially incorrect delivery decisions. |
| T-006 | Approve schemas, persistence, and operational targets | High | T-001–T-005 | No exact API/error schema or database model currently exists. Decisions affect frontend, migrations, cache, observability, and release testing. |
| M-000 | Specification baseline approved | High | T-001–T-006 | A governance gate, not coding work. Starting later phases without sign-off creates rework and security debt. |

**Phase 0 assessment:** Correctly identified as a prerequisite, but the tasks
should produce explicit decision records rather than only modifying prose in
the specification.

### Phase 1 — Foundation and Secure Runtime

| ID | Task | Complexity | Dependencies | Key risks |
| --- | --- | --- | --- | --- |
| T-101 | Establish repository and toolchain | Medium | M-000 | The repository currently has Python/MVP artifacts and package placeholders; layout ownership and migration from existing code are not defined. |
| T-102 | Provision local PostgreSQL | Medium | T-101, T-006 | Docker version, credentials, volumes, health checks, and developer reset behavior are unspecified. |
| T-103 | Implement configuration validation | Medium | T-101, T-006 | Configuration may mix deployment-wide, tenant, project, and user settings. Secret validation must not echo values. |
| T-104 | Implement persistence schema and migrations | High | T-102, T-006 | Session/token/cache persistence is unresolved. Retention, encryption, indexes, and migration rollback must be implemented consistently. |
| T-105 | Implement health, readiness, and safe observability | Medium | T-101, T-102 | Readiness semantics, log destination, sampling, PII redaction, and alert integration are not fully specified. |
| T-106 | Implement OAuth and secure sessions | High | T-003, T-104, T-105 | Highest security risk: CSRF/state, PKCE, token encryption, refresh races, session fixation, logout, and permission changes. |
| T-107 | Enforce transport and request security | High | T-106 | Proxy/TLS termination, CSRF model, security headers, CORS, request limits, and redirect policy are not defined. |
| M-100 | Secure application skeleton complete | High | T-101–T-107 | The milestone can appear complete while production OAuth, proxy, or secret-handling assumptions remain untested. |

### Phase 2 — Jira Integration and Domain Model

| ID | Task | Complexity | Dependencies | Key risks |
| --- | --- | --- | --- | --- |
| T-201 | Build authenticated Jira client | High | T-004, T-106, M-100 | Jira API behavior, user-scoped authorization, custom fields, pagination, timeouts, and response size can be difficult to reproduce locally. |
| T-202 | Implement Jira retry and error mapping | High | T-201 | Retrying non-idempotent operations is unsafe if scope expands to Confluence writes. Retry budgets can amplify rate limiting. |
| T-203 | Implement project and sprint discovery | Medium | T-201, T-202, T-002 | Multiple boards/sprints and Jira permissions are unresolved; project listing may expose metadata beyond intended scope. |
| T-204 | Define normalized domain types | Medium | T-005, T-006 | API contracts may change after clarification. Missing explicit schema generation risks drift between backend and frontend. |
| T-205 | Implement time and business-day rules | Medium | T-005, T-204 | Timezone, DST, date-only due dates, holiday configuration, and clock injection require careful test fixtures. |
| T-206 | Implement status normalization | Medium | T-005, T-204 | Mapping by status ID/name and unknown-status behavior are unresolved. Incorrect mapping corrupts all metrics. |
| T-207 | Implement story-point metrics | Medium | T-005, T-204, T-206 | Remaining-work and completion denominators are not yet chosen. Invalid and changed values can produce misleading forecasts. |
| T-208 | Implement pace forecast | Medium | T-205, T-207 | Division by zero and edge-state semantics are unresolved. Users may over-trust a simple pace comparison. |
| T-209 | Validate and normalize Jira issue data | High | T-201, T-202, T-204, T-206, T-207 | Required/optional field policy, safe text handling, URL trust, and partial-response behavior are unresolved. |
| M-200 | Deterministic domain report complete | High | T-203–T-209 | The milestone depends on safe fixtures and approved contracts that are not currently present as repository artifacts. |

### Phase 3 — Report API and Core UI

| ID | Task | Complexity | Dependencies | Key risks |
| --- | --- | --- | --- | --- |
| T-301 | Implement versioned report API | High | M-200, T-006 | “Versioned” endpoints are required but no version convention, OpenAPI document, or exact schemas exist. |
| T-302 | Implement report aggregation service | High | M-200, T-301 | Aggregation can accidentally convert partial failures into empty collections or mix filtered and unfiltered state. |
| T-303 | Build React application shell and authentication states | Medium | T-101, T-301 | Frontend routing, session expiry, backend error mapping, and design-system availability are unspecified. |
| T-304 | Build sprint summary and forecast UI | Medium | T-302, T-303 | Metric labels, units, edge-state copy, and accessibility design need product decisions, not only implementation. |
| T-305 | Build issue board | Medium | T-302, T-303, T-206 | Unknown statuses, safe links, sorting, large lists, and responsive behavior lack exact UI rules. |
| M-300 | End-to-end core report complete | High | T-301–T-305 | End-to-end acceptance requires a real or contract-tested Jira environment, which is not provisioned in the plan. |

### Phase 4 — Blockers, Risks, and Filtering

| ID | Task | Complexity | Dependencies | Key risks |
| --- | --- | --- | --- | --- |
| T-401 | Implement blocker detection | High | T-005, T-204, T-209 | Jira link types/directions, marker fields, unresolved criteria, and duplicate reasons are unresolved. |
| T-402 | Implement risk detection | High | T-005, T-205, T-401, T-209 | Risk rules depend on changelog availability, activity definitions, due-date boundaries, and sprint membership history. |
| T-403 | Add blockers and risks to report API | Medium | T-401, T-402, T-302 | Detection failures and degraded reports need an explicit response model; empty versus unavailable collections are easy to confuse. |
| T-404 | Build blockers and risk UI | Medium | T-403, T-303 | Multiple reasons, source links, long summaries, empty states, and accessible indicators need UX specifications. |
| T-405 | Implement filter model and URL state | Medium | T-005, T-204, T-302 | AND/OR semantics, URL encoding, permission validation, and sensitive query state are unresolved. |
| T-406 | Apply filters consistently | High | T-405, T-207, T-403 | Maintaining one consistent filtered set across every view is cross-cutting and prone to stale/race conditions. |
| M-400 | Explainable risk report complete | High | T-401–T-406 | Requires representative fixtures with combinations of blockers, risks, status changes, and filter states. |

### Phase 5 — Refresh, Cache, and Resilience

| ID | Task | Complexity | Dependencies | Key risks |
| --- | --- | --- | --- | --- |
| T-501 | Implement permission-safe cache | High | T-006, M-200, T-203 | Cache isolation is a security boundary. Tenant, user, permission, token, and configuration changes must not leak prior data. |
| T-502 | Implement refresh coordinator | High | T-501, T-302 | Single-flight behavior across processes/instances is not defined. In-memory locking is insufficient for horizontal scaling. |
| T-503 | Implement stale fallback | High | T-502, T-006 | Last-known-good data may become unauthorized or semantically obsolete. Retention and invalidation rules are unresolved. |
| T-504 | Implement automatic and manual refresh UX | Medium | T-502, T-503, T-303 | Browser visibility, multiple tabs, cancellation, retry UX, and timer behavior are unresolved. |
| T-505 | Add resilience telemetry | Medium | T-105, T-501, T-502 | Safe identifiers and alert thresholds are not fully defined; telemetry can leak tenant or issue information. |
| M-500 | Resilient daily operation complete | High | T-501–T-505 | Requires distributed concurrency, authorization-change, failure-injection, and browser lifecycle tests. |

### Phase 6 — Hardening and Release

| ID | Task | Complexity | Dependencies | Key risks |
| --- | --- | --- | --- | --- |
| T-601 | Complete automated verification | High | M-500 | No explicit test framework, coverage target, test ownership, or traceability matrix exists. |
| T-602 | Run scale and performance validation | High | T-601, T-006 | Performance budgets are still a clarification item. “10 users” does not define concurrency or test duration. |
| T-603 | Perform security review | High | T-601, T-602 | Security review scope, threat model, tooling, severity thresholds, and remediation ownership are missing. |
| T-604 | Validate deployment and operations | High | T-102, T-104, T-105, T-603 | Target cloud, deployment topology, backup provider, restore objectives, and rollback mechanism are unspecified. |
| T-605 | Conduct stakeholder acceptance | Medium | T-601–T-604 | Stakeholder identities, sign-off mechanism, representative fixture/project, and release decision record are missing. |
| M-600 | Release candidate approved | High | T-605 | Release gate is broad but has no artifact checklist, change-freeze rule, versioning, or rollback approval record. |

## Dependency and Sequencing Findings

### Correct dependency decisions

- The M-000 gate correctly prevents implementation before critical
  specification decisions.
- OAuth precedes the Jira client, and domain normalization precedes API/UI
  work.
- Blockers and risks depend on normalized issues and approved time semantics.
- Cache and stale fallback are placed after the domain/report path exists.

### Dependency gaps

1. **T-101 depends on M-000 but does not explicitly depend on a repository
   migration decision.** Existing Python/MVP files, package placeholders, and
   the selected Node package layout need an ownership decision.
2. **T-105 should depend on T-104** if operational events are persisted in
   PostgreSQL; otherwise the storage choice must be explicit.
3. **T-203 depends on T-002 but not T-004's exact project/board API contract.**
   Add the integration-contract dependency explicitly.
4. **T-207 depends on T-206, although metrics should consume a defined
   normalized category; clarify whether status mapping is required before
   aggregation or can be injected independently.**
5. **T-301 and T-302 lack an explicit OpenAPI/schema artifact dependency.**
   T-006 says schemas are approved, but no file or generation task creates them.
6. **T-303 lacks a direct dependency on T-106** for frontend session-expiry and
   login behavior, even though it depends on the API.
7. **T-501 lacks an explicit dependency on T-104** for the selected cache
   storage implementation.
8. **T-502 only describes single-flight behavior but does not depend on a
   deployment topology decision.** A process-local lock is not enough for
   multiple backend instances.
9. **T-602 should depend on a fixture/data-generation task and an environment
   representative of production.**
10. **T-603 should depend on a threat-model artifact and a security test plan,
    neither of which is a task.
11. **T-604 should depend on an environment/deployment architecture artifact,
    not just foundation tasks.**

### Dependency notation issue

Expressions such as “T-001 through T-005” and “T-301 through T-305” are
human-readable but not machine-resolvable. If tasks are imported into an issue
tracker, enumerate dependency IDs or define range expansion rules.

## Gaps and Missing Artifacts

### Required before implementation

1. **Decision log:** Approved answers for C-01–C-08, F-01–F-15, and X-01–X-05,
   with decision owner and date.
2. **Requirements traceability matrix:** Map each FR and user-story acceptance
   criterion to task(s), test(s), and milestone(s).
3. **OpenAPI/API contract:** Versioned success/error schemas, examples, status
   codes, pagination, correlation IDs, and compatibility policy.
4. **Shared domain contract:** TypeScript types or generated schema source for
   report, issue, metrics, forecast, blocker, risk, filter, refresh, and error.
5. **Jira integration profile:** API endpoints, scopes, field IDs/discovery,
   JQL, link types, status mappings, pagination, retry, timeout, and rate-limit
   policy.
6. **Data model and retention document:** PostgreSQL schema, migrations,
   session/token/cache strategy, retention, deletion, encryption, backups, and
   restore objectives.
7. **Threat model and security test plan:** OAuth, CSRF, XSS, SSRF/link
   validation, cache isolation, session fixation, logging, and authorization
   changes.
8. **Test fixture catalog:** Safe Jira responses for active/no sprint, all time
   boundaries, status mappings, points, blockers, risks, pagination, partial
   responses, rate limits, and 100-issue scale.
9. **UX/accessibility specification:** Wireframes or component states,
   responsive breakpoints, WCAG target, copy for edge/error states, sorting,
   and keyboard behavior.
10. **Deployment architecture:** Cloud target, TLS/proxy topology, instance
    count, environment promotion, secrets manager, health checks, and rollback.
11. **Observability/runbook artifact:** Log/event schema, dashboards, alert
    thresholds, escalation path, and safe-data policy.
12. **Ownership and status model:** Assignees, reviewers, status transitions,
    definition of blocked, and sign-off authority for tasks/milestones.

### Missing functional tasks

- Configure or discover Jira custom fields and validate field compatibility.
- Define and implement issue-link/JQL fixture generation.
- Add API schema validation in CI to prevent backend/frontend drift.
- Add contract compatibility/versioning checks.
- Add database backup/restore automation and retention verification.
- Add explicit dependency/security review for Jira URL construction to prevent
  open redirects or cross-tenant links.
- Add browser support and accessibility automation setup.
- Add load-test data generation and concurrency scenario setup.
- Add migration rollback and production migration rehearsal.
- Add token revocation and authorization-change test scenarios.
- Add deployment smoke tests and rollback rehearsal.

## Contradictions and Inconsistencies

### A-01: Jira-only release versus Jira/Confluence constitution — resolved

The constitution's project-wide purpose and scope include Confluence
automation, while release one contains only a Jira sprint report. T-001
resolved this by recording Jira-only, read-only release scope and explicitly
marking Confluence automation as future scope.

**Remaining action:** Keep future Confluence work out of release-one APIs,
acceptance tests, and implementation tasks.

### A-02: Read-only source access versus application persistence — clarified

The specification now distinguishes read-only Jira/Confluence source access
from application-owned sessions, cache metadata, refresh state, configuration,
and safe telemetry. Confluence publication is outside release one.

**Remaining action:** Define retention and authorization rules for each
application-owned persistence category during T-006.

### A-03: “All fields” acceptance versus no exact field/schema artifact

Tasks require approved fields, types, nullability, and ordering, but the
specification only lists conceptual fields. T-006 is expected to resolve this,
yet no artifact-producing task creates the schema files.

### A-04: Versioned API requirement versus unversioned endpoints

The specification requires versionable APIs but lists `/api/projects` rather
than a concrete version convention such as `/api/v1/projects`. T-301 cannot
make this decision implicitly.

### A-05: Long-term snapshot prohibition versus stale fallback

The specification prohibits long-term Jira snapshots but requires preserving
the last successful report and the tasks add persisted stale fallback. The
retention duration, storage medium, and authorization revalidation rule must
distinguish short-lived cache/report fallback from prohibited snapshots.

### A-06: Automatic refresh versus “near-real-time webhook” non-goal

Five-minute polling is allowed, but no explicit freshness expectation,
jitter, rate-limit budget, or behavior when a tab is continuously open is
defined. This can conflict with Jira quotas and the “fast, reliable” goal.

### A-07: Constitution requires idempotency beyond current scope

The constitution requires idempotent pages, issues, comments, and notifications,
but the specification excludes Jira editing and does not define Confluence
writes. Either scope the principle to supported operations or add write
workflows and their tasks.

### A-08: Technology stack is fixed, but runtime/tooling is not

React 18, Vite, Node.js, Express, PostgreSQL 15, and Docker are fixed, but Node
version, package manager, migration library, test runner, validation library,
and deployment platform remain open. T-101 identifies this but no approved
selection criteria exist.

## Missing Acceptance Coverage

The following specification requirements are not clearly covered by a
dedicated task acceptance criterion:

- Company design-system integration or documented fallback.
- API response backward compatibility and version deprecation.
- Database backup/restore and disaster recovery.
- Log/audit retention and deletion.
- Browser support matrix and WCAG conformance level.
- Correlation ID propagation into frontend-visible errors and telemetry.
- Configuration audit history and project change authorization.
- OAuth scope minimization verification against actual app registration.
- Protection against invalid/cross-tenant Jira links.
- Report ordering and deterministic output.
- No-data behavior when the first refresh fails.
- Authorization revalidation for cached or stale reports.
- Alert delivery and escalation behavior.
- Deployment rollback and migration failure handling.

## Recommended Changes to the Task Plan

1. Add T-007 “Create decision log and update all governing documents” for
   remaining Phase 0 decisions; T-001 now records the release-scope decision.
2. Add T-008 “Create requirements traceability matrix.”
3. Add T-009 “Publish OpenAPI and shared domain schema artifacts.”
4. Add T-010 “Create Jira integration profile and safe fixture catalog.”
5. Add T-011 “Create data model, retention, threat model, and deployment
   architecture artifacts.”
6. Add T-108 “Add schema validation, API contract checks, and secret scanning to
   CI.”
7. Add T-210 “Build Jira fixture generator and 100-issue load dataset.”
8. Add T-306 “Add browser/accessibility test harness and responsive state
   fixtures.”
9. Add T-506 “Implement distributed refresh lock or explicitly constrain
   deployment to one backend instance.”
10. Add T-606 “Run migration/backup/restore/rollback rehearsal and deployment
    smoke test.”
11. Replace dependency ranges with explicit dependency IDs.
12. Add owners, estimates, status transitions, and approval evidence to every
    task and milestone.

## Overall Readiness Assessment

**Status: Not ready for implementation.**

The task decomposition is broad and generally follows the plan, and T-001 has
resolved the release-scope contradiction. Implementation should still remain
at M-000 because OAuth, API schema, database, cache-isolation,
domain-semantics, and operational decisions are architecture-level blockers.
Once the remaining decision and artifact gaps are closed, the task list is a
workable delivery breakdown, with T-106, T-201, T-401/T-402, T-501–T-503, and
T-603 requiring senior review and dedicated test ownership.
