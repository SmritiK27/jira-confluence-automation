# Main Agent Instructions

- Act as an AI assistant using Copilot SDK in VS Code.
- Work directly in the current workspace and keep changes precise and scoped to the request.
- Prefer the smallest relevant search, read, and edit steps before making changes.
- Validate with the smallest existing test, build, or lint command that checks the changed behavior.
- Do not broaden scope to unrelated refactors or cleanup.
- Use Markdown links when referring to files in the workspace.
- Keep responses concise, professional, and focused on the user request.
- Do not add fluff, filler, or unnecessary commentary.
- When the task is ambiguous, ask a single clarifying question rather than making assumptions.
- Preserve existing project conventions and avoid introducing new dependencies unless required.
- If a fix is required, patch the root cause and verify the result.
- Follow [creating-instructions.agent.md](./creating-instructions.agent.md) when creating or updating instruction files.
- Use the following pattern-specific instruction files for repeated validation workflows:
  - [Shared unit test pattern](./shared-unit-test-pattern.agent.md)
  - [Story point and summary metrics test pattern](./test-story-point-metrics-pattern.agent.md)
  - [Forecast calculation test pattern](./test-forecast-calculation-pattern.agent.md)
  - [Risk reason test pattern](./test-risk-reason-pattern.agent.md)
- Summarize outcomes clearly at the end of the task.
