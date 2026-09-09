from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any, Optional


@dataclass
class Issue:
    key: str
    summary: str
    issue_type: str = "Task"
    status: str = ""
    assignee: str = "Unassigned"
    story_points: Optional[float] = None
    due_date: Optional[str | date] = None
    created_at: Optional[datetime | date | str] = None
    updated_at: Optional[datetime | date | str] = None
    labels: set[str] = field(default_factory=set)
    blocking_issues: set[str] = field(default_factory=set)
    is_blocked: bool = False
    status_category: str = "To Do"
    added_after_start: bool = False
    project_key: str = ""
    jira_url: str = ""


@dataclass
class Sprint:
    name: str
    start_date: str | date
    end_date: str | date
    project_key: str = ""


@dataclass
class FilterOptions:
    assignee: Optional[str] = None
    issue_type: Optional[str] = None
    status_category: Optional[str] = None
    risk_state: Optional[str] = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "assignee": self.assignee,
            "issue_type": self.issue_type,
            "status_category": self.status_category,
            "risk_state": self.risk_state,
        }
