# Jira Sprint Report MVP

This project contains a lightweight sprint-report domain model and aggregation logic inspired by the Jira sprint dashboard specification in `project_spec.md` and the backlog in `backlog.md`.

## Features

- Status normalization into To Do / In Progress / Done
- Story-point aggregation with missing or zero-point handling
- Simple pace forecast with explicit labeling
- Blocker detection from labels and issue links
- Risk detection for due dates, inactivity, blockers, and late additions
- Filtered report generation and issue-board grouping

## Run tests

```bash
python -m pytest
```

## Example usage

```python
from sprint_report import build_report, Issue

issues = [
    Issue(key="KAN-1", summary="Build API", status="In Progress", assignee="Sam", story_points=5, due_date="2026-09-10"),
    Issue(key="KAN-2", summary="Ship UI", status="Done", assignee="Ava", story_points=3),
]

report = build_report(issues, sprint_start="2026-09-01", sprint_end="2026-09-15")
print(report["summary"]["completion_pct"])
```
