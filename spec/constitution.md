# Jira/Confluence Automation Project Constitution

## Purpose

This project automates reliable, auditable workflows between Jira and
Confluence. It helps teams summarize delivery status, surface risks and
blockers, track decisions and action items, and publish useful documentation
without compromising source-system permissions or data integrity.

## Core Principles

1. **Specification before implementation**  
   Every feature must define its user outcome, scope, acceptance criteria,
   error behavior, and security considerations before implementation begins.

2. **Secure integration by default**  
   Jira and Confluence credentials, OAuth client secrets, access tokens, and
   session data must remain server-side. Use least-privilege scopes, validate
   OAuth state and callback parameters, protect sessions, and never log secrets
   or unnecessary source content.

3. **Respect source-system authority**  
   Jira remains authoritative for Jira issues, workflow state, ownership, and
   delivery data. Confluence remains authoritative for published pages and
   documentation. Automation must not silently overwrite user-authored data or
   conceal source-system failures.

4. **Explainable automation**  
   Generated summaries, risks, recommendations, and updates must identify
   their source data, timestamp, processing status, and applicable rules.
   Users must be able to distinguish observed facts from generated text.

5. **Reliable and idempotent workflows**  
   Re-running a workflow must not create duplicate pages, issues, comments, or
   notifications. Use stable identifiers, idempotency keys, retries with
   bounded backoff, timeouts, and explicit failure states.

6. **Fail visibly, preserve good data**  
   Jira, Confluence, network, rate-limit, authorization, and validation
   failures must produce actionable errors. Never convert a failed or partial
   upstream response into an empty success result. Preserve the last known
   good result where the workflow supports it and label it as stale.

7. **Clear separation of concerns**  
   Keep React presentation, Express API/orchestration, integration clients,
   domain rules, persistence, and background jobs independently testable.
   Business rules must not depend directly on UI or vendor-specific response
   shapes.

8. **Accessible and usable experiences**  
   Interfaces must work on desktop and tablet layouts, support keyboard
   navigation, provide meaningful labels and focus states, and never rely on
   color alone to communicate status, risk, or completion.

## Technology Standards

- **Frontend:** React 18 with Vite.
- **Backend:** Node.js with Express.
- **Database:** PostgreSQL 15.
- **Local infrastructure:** Docker and Docker Compose for PostgreSQL and
  repeatable development services.
- **API design:** Versioned, validated, documented JSON APIs with consistent
  error responses and request correlation identifiers.
- **Configuration:** Environment-based configuration with startup validation;
  secrets must be supplied through the environment or a deployment secret
  manager, never committed to source control.

Technology changes require a documented rationale and must preserve the
security, testability, and operational requirements in this constitution.

## Data and Persistence Rules

- Store only the minimum Jira and Confluence data required for the supported
  workflows.
- Define ownership, retention, and deletion behavior for synchronized data.
- Scope cached or persisted data by tenant, project, and permission context as
  appropriate.
- Use migrations for schema changes and transactions for multi-step writes.
- Protect personal, project, and internal business information in logs,
  fixtures, tests, and error messages.

## Quality Gates

Every change must satisfy the following applicable gates:

- Requirements and acceptance criteria are documented.
- Unit tests cover domain rules, transformations, idempotency, and edge cases.
- API tests cover validation, authorization, upstream failures, retries, and
  consistent error responses.
- UI changes include accessibility and loading, empty, stale, and error states.
- Integration tests cover Jira/Confluence pagination, rate limits, timeouts,
  permission failures, and partial responses using safe fixtures.
- Database changes include reversible migrations and constraint coverage.
- No access token, OAuth secret, password, or sensitive source content is
  exposed in browser code, logs, test output, or committed files.
- Existing lint, type-check, build, and test commands pass before delivery.

## Operational Requirements

- Record structured events for authentication, integration latency and
  failures, rate limits, workflow execution, retries, and publication results.
- Include correlation IDs and safe identifiers, but redact credentials,
  tokens, page bodies, issue descriptions, and other unnecessary sensitive
  payloads.
- Provide health and readiness checks that do not expose secrets.
- Make background work observable with status, timestamps, retry counts, and
  actionable failure details.
- Require HTTPS outside local development and use secure, HTTP-only,
  same-site cookies where browser sessions are used.

## Scope Boundary

The first release focuses on read-oriented reporting, delivery-risk
visibility, decision/action tracking, and controlled Confluence publication.
It excludes unrestricted bulk editing, broad cross-tenant synchronization,
unreviewed destructive actions, and unsupported Jira or Confluence deployments.

## Governance

This constitution is the governing standard for architecture, implementation,
testing, and operations. When a requirement conflicts with it, document the
conflict, assess the security and data-integrity impact, and obtain explicit
approval before implementation. Amendments must explain the motivation,
affected specifications and tests, and migration or rollout implications.
