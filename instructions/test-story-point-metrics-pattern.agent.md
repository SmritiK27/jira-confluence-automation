# Story Point and Summary Metrics Test Pattern

- Use the existing unit-test framework and keep coverage focused on the metric logic.
- Treat this as a table-driven test pattern: one scenario covers one expected result.
- Keep assertions explicit and avoid broad snapshots.

## Input format
- Provide a list of issue fixtures in structured form.
- Each fixture includes: issue key, status/category, story points, whether it is estimated or unestimated, assignee if relevant, and any filter values used by the test.
- Include a base case plus edge cases such as zero points, missing points, mixed categories, and filtered subsets.
- For subset tests, provide both the full sprint data and the filtered subset.

## Processing steps
- Build a minimal dataset that exercises the metric under test.
- Calculate totals for committed, completed, and remaining story points.
- Verify completion percentage is computed from the intended numerator and denominator.
- Confirm unestimated items are counted or labeled consistently without silently dropping them.
- Check issue counts for totals and filtered subsets.
- Validate that filtering updates all dependent metrics, not just the visible board.
- Assert expected values using exact numbers and clear names.

## Output format
- Write one test block per scenario.
- Use a descriptive title in this pattern: `returns expected <metric> for <case>`.
- Keep expected values in plain, readable assertions.
- Prefer a compact table of cases over repeated custom setup code.

## Constraints
- Do not test UI rendering, API transport, or Jira integration in this pattern.
- Do not use hard-coded values that hide the business rule being tested.
- Keep each test independent and deterministic.
- Cover only the metric logic directly affected by the issue.
- Ensure tests fail clearly when the formula changes unexpectedly.
