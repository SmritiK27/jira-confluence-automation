# Shared Unit Test Pattern

- Use the existing unit-test framework.
- Keep tests focused on the logic under test rather than UI rendering, API transport, or network integration.
- Prefer table-driven scenarios when validating the same rule across multiple inputs.
- Keep each test independent, deterministic, and explicit about expected results.
- Use descriptive test names and exact assertions.
