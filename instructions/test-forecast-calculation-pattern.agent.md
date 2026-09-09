# Forecast Calculation Test Pattern

- Use the existing unit-test framework and target pure forecast logic only.
- Validate one formula across many edge conditions using a repeated scenario pattern.
- Keep test names explicit about the sprint state being modeled.

## Input format
- Provide sprint input data in a simple structured object.
- Each scenario includes: sprint duration, elapsed time, completed points, total points, sprint state, and any configured timezone or holiday rules if applicable.
- Include edge-case scenarios such as pre-start, post-end, zero-duration, zero-point, and fully complete sprints.
- Where relevant, include explicit expected labels such as `ahead`, `behind`, or `not applicable`.

## Processing steps
- Establish the baseline sprint context for each scenario.
- Determine whether the sprint is pre-start, active, post-end, or zero-duration.
- Compute the elapsed proportion and completed proportion using the same business rules as production.
- Apply forecast logic exactly once per scenario.
- Confirm the output label and metric value remain valid for each edge case.
- Verify that invalid or non-actionable sprint states do not produce misleading numeric forecasts.

## Output format
- Write one test case per scenario.
- Use a clear naming convention such as `returns <forecast> when sprint is <state>`.
- Assert both the numeric result and the label when the label is part of the contract.
- Keep results readable and minimal.

## Constraints
- Do not include UI, API call, or network assumptions in this pattern.
- Do not mix unrelated business rules into the same test case.
- Keep calculations deterministic and timezone-aware when required.
- Treat zero values as intentional scenarios, not missing data.
- Ensure each edge case is covered explicitly rather than relying on a single happy-path test.
