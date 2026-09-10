# Module 10 Completion Report

## Instruction Files
instructions/create-status-report.agent.md
instructions/creating-instructions.agent.md
instructions/main.agent.md
instructions/shared-unit-test-pattern.agent.md
instructions/test-forecast-calculation-pattern.agent.md
instructions/test-risk-reason-pattern.agent.md
instructions/test-story-point-metrics-pattern.agent.md

## main.agent.md Contents
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

## Sample Instruction
- File: shared-unit-test-pattern.agent.md
- Contents:
# Shared Unit Test Pattern

- Use the existing unit-test framework.
- Keep tests focused on the logic under test rather than UI rendering, API transport, or network integration.
- Prefer table-driven scenarios when validating the same rule across multiple inputs.
- Keep each test independent, deterministic, and explicit about expected results.
- Use descriptive test names and exact assertions.
