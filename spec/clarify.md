# Specification Clarifications

## Review Scope

This review compares [`spec/constitution.md`](./constitution.md) with
[`spec/specification.md`](./specification.md), using the Module 08 Jira sprint
report source specification as context. The items below should be resolved
before implementation is considered ready.

## Critical Gaps

### C-01: Product scope does not match the project identity

The constitution describes a Jira/Confluence automation project covering
status summaries, decision/action tracking, and controlled Confluence
publication. The specification defines only a read-only Jira sprint report.
There are no Confluence use cases, APIs, data models, page publication rules,
or acceptance criteria.

**Clarify:** Is this release only the Jira Sprint Report, or must it also
implement Confluence automation? If Confluence is in scope, define the
supported page spaces/templates, create-versus-update behavior, review/approval
workflow, conflict handling, permissions, idempotency key, and page version
policy. If not, narrow the constitution or explicitly mark those capabilities
as future scope.

### C-02: “Read-only” conflicts with controlled publication

The specification calls the product a “Read-only web application” and excludes
Jira editing, but the constitution includes controlled Confluence publication
and publication observability.

**Clarify:** Which writes are allowed in release one? If Confluence writes are
allowed, identify the exact write operations and user confirmation required.
If no writes are allowed, remove publication requirements from the release
governance language.

### C-03: Project configuration ownership is undefined

The specification says a user may select or configure the Jira project, while
the scope says one configured project is in scope. It does not define who may
change configuration, whether configuration is tenant-wide or user-specific,
or whether configuration is persisted in PostgreSQL.

**Clarify:** Define administrator permissions, configuration lifetime,
multi-tenant scope, persistence, audit history, and behavior when a user
selects a project outside the deployment's allowed project.

### C-04: Atlassian OAuth provider and token lifecycle are incomplete

The required OAuth scopes are not listed. The specification does not define
provider endpoints, redirect URI rules, PKCE, refresh-token rotation,
revocation, token expiry handling, consent denial, account identity mapping,
or logout semantics.

**Clarify:** Specify OAuth scopes, PKCE/state requirements, token encryption and
storage, refresh and revocation behavior, session duration, idle timeout,
logout behavior, and the response for consent denial or an expired refresh
token.

### C-05: Jira API and version behavior is unspecified

The specification does not identify Jira REST API version, Agile/Sprint API
usage, supported issue types, fields, or the exact source of changelog/activity
data. “Required fields” is not an implementable field list because the story
point field is configurable and Jira Cloud custom-field IDs differ by tenant.

**Clarify:** Define API versions/endpoints, field IDs and discovery strategy,
JQL or sprint query, maximum page size, pagination termination rules, and
whether changelog expansion or separate requests are used.

### C-06: Permission context and cache isolation are not implementable

The cache must be scoped by “permission context as appropriate,” but the
permission context is not defined. A shared cached report could expose data
visible to one user but not another.

**Clarify:** Define the cache key and isolation strategy, token/user identity
requirements, TTL, maximum size, eviction behavior, invalidation behavior,
whether cached data can outlive a session, and how permission changes are
handled.

### C-07: No exact report schema or error schema exists

The document lists conceptual fields but does not define types, nullability,
units, enum values, date formats, numeric precision, sorting, ordering, or
backward-compatibility rules. The “consistent structured error shape” is also
not specified.

**Clarify:** Add a versioned JSON schema or TypeScript contract for every
endpoint, including success and error responses, HTTP status mapping,
correlation ID format, pagination metadata, nullable values, and safe message
rules.

### C-08: Database responsibilities are unclear

PostgreSQL may store configuration, sessions, cache metadata, and operational
workflow state, but none of these are mandatory or modeled. There is no schema,
retention policy, migration tool, transaction boundary, or session-storage
decision.

**Clarify:** Decide what is persisted in release one, define tables and
relationships, retention/deletion rules, encryption requirements, migration
process, indexes, and whether sessions/cache are PostgreSQL-backed or handled
by another service.

## Functional Ambiguities

### F-01: Active sprint selection is ambiguous

The specification requires the active sprint by default but does not define
behavior when multiple sprints are active, when a sprint is in a non-standard
state, or when a project has no board associated with it.

**Clarify:** Define selection precedence, whether users can select a historical
or future sprint, and the behavior for multiple boards or multiple active
sprints.

### F-02: Sprint time and day calculations are undefined

“Elapsed days” and “remaining days” could mean calendar days, business days,
inclusive dates, or fractional durations. The forecast uses elapsed time but
does not define the clock precision or whether dates are converted to the
project timezone before calculation.

**Clarify:** Define timezone source, date parsing, inclusive/exclusive
boundaries, rounding, daylight-saving behavior, fractional-day handling, and
the exact values for pre-start, post-end, and zero-duration sprints.

### F-03: Zero committed points has no forecast rule

The forecast formula divides by committed points, but the required behavior for
zero committed points is only described as “safe.”

**Clarify:** Choose an explicit state such as `Not enough data`, define its UI
label and whether it counts as At risk, and specify how it interacts with
unestimated issues.

### F-04: Story-point semantics are unclear

The document treats missing and zero points as unestimated, but does not state
whether negative, decimal, non-numeric, or changed story points are accepted.
It also does not define whether completed issues with no points count toward
completion percentage.

**Clarify:** Define validation and normalization rules, precision, field
fallbacks, and the exact denominator for issue-based versus point-based
completion.

### F-05: Remaining work formula is not stated

The document requires remaining points but does not explicitly define whether
remaining means committed minus completed, sum of non-Done points, or another
Jira-derived value. Scope changes can make these differ.

**Clarify:** Define the authoritative formula and behavior for issues added
after sprint start, removed issues, reopened issues, and negative/invalid
values.

### F-06: Status mapping and unknown statuses lack a policy

Mappings are configurable, but the specification does not define whether
mapping is by status ID or name, whether mappings are tenant/project-specific,
what happens when a status is unmapped, or whether Done is determined by Jira
status category.

**Clarify:** Define precedence between explicit mapping and Jira category,
unmapped-status behavior, configuration validation, and whether an unmapped
issue is included in totals and forecast.

### F-07: Blocker semantics are underspecified

“Configured blocked label or flag” and “blocking link” do not define exact
label matching, flag fields, case sensitivity, link types, direction, or
whether a linked issue must itself be unresolved or in the same sprint.

**Clarify:** Define marker field/values, normalization, supported link type
names and directions, unresolved criteria, duplicate reason handling, and the
displayed blocker source.

### F-08: Risk inactivity rule is ambiguous

The phrase “no status, assignee, or activity change” could mean no change to
any one field, no change to all fields, or missing values in addition to
inactivity. It also does not define which Jira changelog events count as
activity or the reference timestamp.

**Clarify:** Define the boolean rule, tracked activity event types, whether
comments count, fallback when changelog is unavailable, and the exact
three-business-day threshold boundary.

### F-09: Due-date timezone and boundary are undefined

“Due date has passed” does not specify the timezone, whether the due date is
inclusive through the end of that date, or behavior for missing/invalid dates.

**Clarify:** Define comparison instant, project timezone, date-only handling,
and the precise transition from not overdue to overdue.

### F-10: Late-addition timestamp is unspecified

The specification asks for issues added after sprint start but does not define
the source timestamp. Created date, sprint-field changelog date, and sprint
membership date can differ.

**Clarify:** Use the sprint membership changelog as the authoritative source,
define fallback behavior, and specify how issues added and removed multiple
times are treated.

### F-11: Filtering semantics are incomplete

The document does not define whether filters combine with AND or OR, how
multi-valued filters behave, whether filtering is client-side or server-side,
how URL/deep-link state works, or whether filtered blockers/risk tables show
only matching issues.

**Clarify:** Define filter combination, empty selection behavior, URL/state
persistence, result ordering, and whether the unfiltered total remains visible
alongside filtered metrics.

### F-12: Refresh behavior needs lifecycle rules

“Every five minutes while open” does not define whether refresh pauses in a
background tab, what happens during an in-flight request, whether refresh
occurs immediately on page load, or how multiple browser tabs coordinate.

**Clarify:** Define timer lifecycle, visibility behavior, request timeout,
cancellation, retry policy, tab coordination, and manual-refresh UX.

### F-13: Partial response policy is missing

Partial or malformed Jira responses are prohibited from becoming successful
empty reports, but the specification does not say whether a report may render
with a subset of fields or must fail entirely.

**Clarify:** Define required versus optional fields, validation behavior,
degraded-mode rules, user messaging, telemetry, and whether last-known-good data
is used for partial responses.

### F-14: Pagination and rate-limit policy is incomplete

Pagination support is required, but maximum pages, response consistency, retry
count, `Retry-After` handling, backoff, and rate-limit user messaging are not
defined.

**Clarify:** Define page-size limits, maximum issue count, retryable status
codes, exponential-backoff bounds, timeout budget, and behavior after retry
exhaustion.

### F-15: Jira URL construction is not defined

The report requires direct Jira links and a tenant/base URL, but does not
define trusted URL discovery, normalization, validation, or behavior if a
returned URL is missing or points to another tenant.

**Clarify:** Construct links from a validated tenant base URL and issue key,
define allowed hosts, and specify whether invalid links are omitted or treated
as an integration error.

## Contradictions and Inconsistencies

### X-01: Constitution says “Jira/Confluence”; specification says “Jira only”

The constitution's purpose and scope mention Confluence automation, but the
specification has no Confluence feature requirements and explicitly focuses on
Jira sprint health.

**Resolution needed:** Align the product name, release scope, APIs, data
model, and acceptance criteria across both documents.

### X-02: Constitution requires minimum data retention rules; specification
prohibits long-term Jira snapshots without defining retention

The constitution requires ownership, retention, and deletion behavior for
synchronized data. The specification says no long-term snapshots but allows
configuration, sessions, cache metadata, and operational state without
retention rules.

**Resolution needed:** Define retention/deletion for each persisted category,
including sessions, cache entries, logs, audit events, and any generated
reports.

### X-03: “Read-only” product versus PostgreSQL workflow state and publication

The product is described as read-only, while the platform may persist
operational workflow state and the constitution discusses publication. Reading
Jira is distinct from writing application state or publishing Confluence.

**Resolution needed:** Explicitly distinguish read-only source-system access
from application persistence and any permitted publication writes.

### X-04: “No shared API token” versus server-side OAuth token reuse

The specification correctly prohibits a shared token in the client, but does
not state whether a server-side service token is forbidden. The constitution
requires user/source permissions, implying impersonated or user-scoped access.

**Resolution needed:** State that all Jira access is user-authorized and
whether any service account is permitted for non-user operations.

### X-05: “Every feature has security considerations” versus incomplete
requirements for filtering, links, cache, and persistence

The constitution makes security a quality gate, but the specification leaves
several security-sensitive decisions unresolved, especially cache isolation,
Jira URL trust, session/token storage, and authorization changes.

**Resolution needed:** Add explicit security acceptance criteria for these
areas before implementation.

## Missing Product and Operational Decisions

1. What is the deployment environment and expected availability/SLA?
2. What are the target response-time budgets for initial load, refresh, and
   filter changes?
3. What Node.js version and package manager are required?
4. Which validation, logging, testing, migration, and API documentation
   libraries are approved?
5. Which Atlassian OAuth scopes are required and who owns app registration?
6. How are tenant onboarding, tenant removal, and project changes performed?
7. Is there one Atlassian tenant only, or must the application support multiple
   tenants?
8. What roles exist beyond Scrum Master and team member, and who can view
   configuration or operational errors?
9. What accessibility conformance target applies (for example, WCAG 2.1 AA)?
10. What browsers and minimum viewport widths must be supported?
11. What happens if the company design system is unavailable?
12. What is the source and retention period for logs and audit events?
13. What operational alert thresholds apply to Jira failures, stale data, and
    repeated refresh failures?
14. What database backup, restore, and disaster-recovery requirements apply?
15. How are migrations run safely across local, staging, and production?
16. Are generated summaries in scope, and if so, is an AI provider involved,
    what data may leave the tenant, and how are outputs reviewed?
17. Are Confluence pages, comments, notifications, or Jira issue links ever
    written, and what approval is required?
18. What is the support and escalation path for OAuth, Jira, and database
    failures?

## Recommended Clarification Order

Resolve these first because they change architecture and acceptance tests:

1. Product/release scope and the Jira-versus-Confluence contradiction
   (C-01, C-02, X-01).
2. Authentication, tenant model, authorization, and cache isolation
   (C-03 through C-06, X-04).
3. Exact report/error schemas and database persistence (C-07, C-08).
4. Time, forecast, story-point, status, blocker, and risk semantics (F-02
   through F-10).
5. Refresh, pagination, partial-response, and URL-security behavior (F-12
   through F-15).
6. Operational, accessibility, performance, and deployment targets.

## Resolved Decisions

### C-01 / C-02 / X-01: Release scope and write permissions

- Release one is **Jira-only**.
- Jira access is read-only and uses the authenticated user's Atlassian
  permissions.
- Release one does not integrate with Confluence and does not create or update
  Jira issues, comments, labels, links, workflow state, or notifications.
- Application-owned persistence is allowed for sessions, configuration,
  short-lived cache/refresh state, and safe operational telemetry, subject to
  retention and authorization rules.
- The constitution remains project-wide; Confluence automation is future scope
  and is not part of this release's specification, APIs, or acceptance tests.

The specification's release scope and non-goals are the authoritative
implementation boundary for this release. Remaining clarification items are
still open.
