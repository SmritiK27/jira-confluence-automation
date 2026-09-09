# Jira Workflow Instructions

- Use Jira as the source of truth for work items, status, ownership, priority, and delivery tracking.
- Preserve existing project conventions for issue types, workflows, labels, components, and naming.
- Do not expose credentials, access tokens, private comments, or sensitive project data.

## Input format

- Accept a Jira issue key, project key, sprint name, filter, or a structured issue request.
- For issue creation or updates, include the summary, description, issue type, priority, assignee, labels, acceptance criteria, and relevant links when available.
- For searches, specify the project, status, assignee, sprint, date range, or other JQL constraints.

## Processing steps

- Confirm the target project and issue before making changes.
- Confirm the requested issue type explicitly before creation; do not infer `Bug`, `Task`, or `Story` from the summary.
- Before submitting a create request, restate the requested issue type and require confirmation when the request is ambiguous.
- Inspect existing issue fields and workflow state before updating them.
- Use the smallest valid change that satisfies the request.
- Preserve existing descriptions and fields unless the request explicitly replaces them.
- Validate required fields, issue transitions, duplicate risks, and project permissions.
- After creation, verify the returned issue type matches the requested type.
- If the returned type is wrong, do not report success as if it were correct; report the mismatch and, when supported, correct it with an explicit update or ask for approval before changing it.
- Report the issue key, confirmed issue type, fields changed, transition performed, and any blocked action.

## Output format

- For issue creation, return the issue key, summary, requested issue type, confirmed Jira issue type, status, assignee, and Jira link.
- For updates, list each changed field and its resulting value.
- For searches, return a concise table containing issue key, summary, status, priority, assignee, and updated date.
- For blocked or mismatched operations, state the missing permission, invalid transition, required input, requested type, actual type, and next action.

## Constraints

- Never invent Jira issue keys, statuses, fields, or transition names.
- Never silently substitute a Jira issue type or claim that a requested Bug or Task was created when Jira created a Story.
- Do not transition an issue without confirming the requested target status.
- Do not modify unrelated issues or bulk-update without explicit scope.
- Keep descriptions and comments factual, concise, and actionable.
- Treat Jira API failures, rate limits, and permission errors as failures; do not report them as successful updates.
