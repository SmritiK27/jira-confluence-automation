# Risk Reason Test Pattern

- Follow [Shared Unit Test Pattern](./shared-unit-test-pattern.agent.md).
- Test one risk rule at a time before testing combinations.
- Treat this as a deterministic rule-evaluation workflow, not a data-collection workflow.
- Keep the expected reason list concise and fully traceable to the input conditions.

## Input format
- Provide issue data as a structured object for each scenario.
- Each fixture includes: issue key, status, due date, updated date, blocker state, created date, assignee if relevant, and sprint timing information.
- Include single-risk scenarios and multi-risk scenarios on the same issue.
- Cover the expected risk reasons: overdue incomplete work, inactivity, unresolved blockers, and post-start additions.

## Processing steps
- Evaluate each issue against the risk rules independently.
- Determine which reasons apply to the current issue state.
- Combine applicable reasons when multiple conditions are true.
- Verify the final reason list order and content are consistent with the expected rule precedence.
- Check that a risk is reported once per reason and not duplicated.
- Confirm the issue remains correctly labeled even when multiple reasons overlap.

## Output format
- Write one test per rule and one test for combined-risk scenarios.
- Use names like `marks issue as <reason>` and `applies multiple reasons when <conditions>`.
- Assert the exact set of reasons, not a partial match.
- Keep output compact and easy to review in a table-driven format.

## Constraints

- Do not allow hidden state or ordering assumptions to drive the expected results.
- Ensure the same issue can trigger multiple reasons without causing collisions or omission.
- Avoid broad integration tests when the risk classification itself is the target behavior.
