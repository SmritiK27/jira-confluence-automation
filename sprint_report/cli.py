from __future__ import annotations

import json
from datetime import datetime, timezone

from .models import Issue, Sprint
from .report import build_report


def main() -> None:
    issues = [
        Issue(
            key="KAN-1",
            summary="Implement API",
            issue_type="Story",
            status="In Progress",
            assignee="Sam",
            story_points=5,
            due_date="2026-09-10",
            updated_at="2026-09-08T10:00:00Z",
            labels={"blocked"},
            is_blocked=True,
        ),
        Issue(
            key="KAN-2",
            summary="Ship dashboard",
            issue_type="Task",
            status="Done",
            assignee="Ava",
            story_points=3,
            due_date="2026-09-09",
            updated_at="2026-09-07T14:00:00Z",
        ),
        Issue(
            key="KAN-3",
            summary="Add auth",
            issue_type="Bug",
            status="To Do",
            assignee="Sam",
            story_points=None,
            updated_at="2026-09-06T00:00:00Z",
        ),
    ]
    for issue in issues:
        issue.status_category = "In Progress" if issue.status == "In Progress" else "Done" if issue.status == "Done" else "To Do"

    sprint = Sprint(name="Sprint 18", start_date="2026-09-01", end_date="2026-09-15", project_key="KAN")
    report = build_report(issues, sprint=sprint, last_refresh=datetime.now(timezone.utc))
    print(json.dumps(report, indent=2, default=str))


if __name__ == "__main__":
    main()
