# Module 08 Completion Report

## Tracked Files
.gitignore
README.md
calculator.py
csv_to_json.py
main.py
project_spec.md

## Spec Commit History
4355b16 Add Jira sprint report specification

## project_spec.md Contents
# Jira Sprint Report - Technical Specification

## 1. Overview

Build a standalone web application that gives a Scrum Master and a 10-person engineering team a daily view of active-sprint health for an automation project.

The first release will use Jira Cloud data from one Jira project. It will focus on delivery progress, completion forecasting, blockers, and delivery risk. It will not introduce automation-specific quality metrics such as test coverage or pass rate.

## 2. Goals

- Provide a fast, reliable view of active-sprint health.
- Show progress using story points and Jira workflow status.
- Make blockers and delivery risks immediately visible.
- Forecast whether the sprint is on track based on elapsed time and remaining work.
- Let users filter the sprint and open source issues directly in Jira.
- Support the Scrum Master and the 10-person engineering team without requiring shared credentials.

## 3. Non-goals for the first release

- Historical sprint trends or velocity reporting.
- Multi-project reporting.
- Automation test, deployment, coverage, or incident metrics.
- Editing Jira issues from the report.
- PDF/CSV export or scheduled email/chat distribution.
- Long-term storage of Jira issue data.
- Near-real-time webhook updates.
- Mobile-first optimization.

## 4. Users and access

### Primary users

- Scrum Master
- Members of the 10-person engineering team

### Authentication and authorization

- Authenticate each user with their existing Atlassian account using OAuth 2.0.
- Access Jira data using the authenticated user's permissions.
- Do not use a shared Jira API token in the client.
- The application must not expose OAuth client secrets or Jira access tokens to browser JavaScript.
- Users without access to the configured Jira project must receive a clear authorization error.

## 5. Scope and assumptions

- Jira Cloud is the only supported Jira deployment.
- One configured Jira project is in scope.
- The active sprint is the default and primary reporting period.
- The team estimates work with story points.
- The workflow can be normalized into To Do, In Progress, and Done categories.
- The Jira project has a reliable blocked label/flag convention and uses linked blocking issues.
- Jira due dates are available when applicable.
- The team can deploy the application on its existing cloud platform.
- The application should use the existing company design system when one is available.
- The initial scale target is 10 team members and approximately 100 sprint issues.

## 6. Functional requirements

### 6.1 Sprint selection and project configuration

1. Allow an authorized user to select or configure the Jira project.
2. Detect and display the active sprint for that project.
3. Display a useful empty state when no sprint is active.
4. Show sprint name, start date, end date, and current elapsed/remaining time.
5. Use the active sprint by default on every visit.

### 6.2 Summary section

Display summary cards for:

- Total committed story points.
- Completed story points.
- Remaining story points.
- Completion percentage.
- Total issues and issues completed.
- Sprint days elapsed and remaining.
- Forecast status: On track or At risk.
- Last successful data refresh time.

Story-point calculations must handle issues with missing or zero story points without failing. The UI should identify unestimated issues separately.

### 6.3 Progress and forecast

Provide a progress visualization comparing:

- Planned/committed story points.
- Completed story points.
- Remaining story points.
- Elapsed sprint time.

The initial forecast should compare the proportion of completed story points with the proportion of sprint time elapsed:

- On track when progress is at least the elapsed-time proportion.
- At risk when progress is behind the elapsed-time proportion.

The report must explicitly label this as a simple pace forecast and should avoid implying a statistically trained prediction. Handle pre-start, post-end, and zero-duration sprint edge cases safely.

### 6.4 Blockers

Provide a blockers table containing issues that:

- Have the configured blocked label or blocked flag; or
- Have a Jira issue link indicating that another issue blocks them.

Each row should show issue key, summary, status, assignee, story points, blocker reason/source when available, and a link to open the issue in Jira.

### 6.5 Risk detection

Provide an at-risk table and risk indicators on issue rows. An issue is at risk when one or more of the following apply:

- Due date has passed and the issue is not Done.
- The issue has no status, assignee, or activity change for at least three business days.
- The issue has an unresolved blocker.
- The issue was added to the sprint after the sprint start date.

Show the applicable risk reasons rather than only a single opaque risk score. Define business-day calculation using the configured project timezone; weekends are excluded. The first release should make holidays configurable or document that only weekends are excluded.

### 6.6 Sprint issue board

Display all issues in the active sprint grouped into:

- To Do
- In Progress
- Done

Each issue card/row should show:

- Issue key and summary.
- Issue type.
- Status.
- Assignee.
- Story points.
- Due date, when present.
- Blocked and risk indicators.
- Direct Jira link.

Workflow statuses must be mapped through configuration rather than assuming exact Jira status names.

### 6.7 Filtering

Provide filters for:

- Assignee.
- Issue type.
- Status/category.
- Risk state.

Filters should update summary metrics, progress visualization, blockers, risks, and issue board consistently. Clearly indicate when metrics represent a filtered subset rather than the full sprint.

### 6.8 Refresh and error handling

- Automatically refresh Jira data every five minutes while the report is open.
- Provide a manual refresh action.
- Prevent overlapping refresh requests.
- Display the last successful refresh time.
- If refresh fails, preserve the last successful data and show a visible stale-data/error message.
- Handle Jira rate limits, expired OAuth sessions, missing permissions, and unavailable project/sprint data with actionable messages.
- Do not silently replace failed or incomplete Jira responses with empty success-shaped results.

## 7. Data requirements

The Jira integration should retrieve, at minimum:

- Project and project key.
- Active sprint metadata.
- Sprint issue key, summary, issue type, status, assignee, labels/flags, story points, due date, created date, updated date, and changelog/activity information.
- Issue links, specifically blocking and is-blocked-by relationships.
- Status category or configured workflow mapping.

Use Jira Cloud REST APIs and request only fields required by the report. Pagination must be supported even though the initial target is approximately 100 issues.

### Caching

- Use a short-lived server-side cache to reduce repeated Jira API calls.
- Do not persist long-term issue snapshots in the first release.
- Scope cached data by Jira tenant/project/user permission context as appropriate.
- Invalidate or refresh cached data on manual refresh.

## 8. Proposed architecture

### Frontend

- Desktop-first responsive web UI with basic tablet support.
- Components for summary cards, progress chart, blockers table, risk table, filters, issue board, refresh state, and authentication state.
- Accessible color and icon treatment for risk and status; do not rely on color alone.
- Use the company design system where available.

### Backend

- Server-side OAuth flow and secure token handling.
- Jira Cloud API client with pagination, field selection, timeout handling, rate-limit handling, and structured errors.
- Sprint/report aggregation service that normalizes Jira statuses and calculates metrics/risk reasons.
- Short-lived cache.
- Configuration for Jira project, blocked label/flag, story-point field, status mappings, timezone, and stale threshold.

### Deployment

- Deploy to the team’s existing cloud platform.
- Keep deployment portable through environment-based configuration.
- Require HTTPS in all non-local environments.
- Store OAuth secrets and application configuration in the platform’s secret manager.

## 9. Suggested API boundaries

These are application-level endpoints; exact framework naming may vary:

- `GET /auth/login`
- `GET /auth/callback`
- `POST /auth/logout`
- `GET /api/projects`
- `GET /api/projects/{projectKey}/active-sprint`
- `GET /api/projects/{projectKey}/active-sprint/report`

The report endpoint should return normalized sprint metadata, summary metrics, forecast, blocker/risk reasons, filter options, and issue board data in one coherent response where practical.

## 10. Security and privacy

- Use OAuth authorization code flow with server-side secret protection.
- Encrypt or securely store tokens according to the deployment platform’s standard.
- Use secure, HTTP-only, same-site session cookies.
- Validate OAuth state and callback parameters.
- Enforce authorization on every Jira-backed request.
- Do not log access tokens, issue descriptions unnecessarily, or other sensitive Jira content.
- Apply least-privilege Atlassian scopes required to read project, sprint, issue, and issue-link data.
- Escape/encode Jira text rendered in the UI.

## 11. Observability and operations

Record operational events without sensitive payloads:

- Jira API latency and response failures.
- Rate-limit responses.
- OAuth failures.
- Cache hit/miss behavior.
- Report refresh success/failure.

Provide a health check for application availability and document required environment variables and Jira OAuth setup.

## 12. Acceptance criteria

1. An authorized user can sign in with Atlassian OAuth and view the configured project’s active sprint.
2. The report shows committed, completed, remaining, and unestimated story points accurately for the returned Jira issues.
3. Issues are grouped into To Do, In Progress, and Done using configurable mappings.
4. Blocked issues are shown when they have the configured blocked marker or a blocking relationship.
5. Risk rows correctly identify overdue, stale, unresolved-blocker, and post-start scope-change conditions.
6. The forecast changes between On track and At risk based on progress versus elapsed sprint time and handles sprint edge cases.
7. Assignee, issue type, status, and risk filters update all affected views consistently.
8. Users can open any issue directly in Jira.
9. Data automatically refreshes every five minutes and can be refreshed manually.
10. Failed refreshes preserve the last successful data and visibly communicate staleness.
11. No Jira access token or OAuth secret is exposed to the browser.
12. The report remains usable for at least 100 sprint issues and 10 team members.
13. The interface is usable on desktop and basic tablet widths and follows the company design system where available.

## 13. Recommended implementation phases

### Phase 1 - Foundation

- Set up application shell, configuration, OAuth, session handling, and Jira Cloud client.
- Add project and active-sprint discovery.

### Phase 2 - Core report

- Implement issue retrieval and normalization.
- Add summary cards, progress calculation, forecast, and issue board.

### Phase 3 - Blockers and risks

- Implement blocker relationship/label detection.
- Implement overdue, stale, unresolved-blocker, and scope-change risk reasons.

### Phase 4 - Usability and resilience

- Add filters, refresh scheduling, caching, error states, responsive styling, accessibility, and observability.

### Phase 5 - Validation and rollout

- Test against representative Jira workflows and edge cases.
- Validate OAuth scopes and permissions with a non-admin team member.
- Deploy to the existing cloud platform and document operations.
