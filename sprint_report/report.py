from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Any, Iterable, Optional

from .models import FilterOptions, Issue, Sprint


def _as_date(value: Optional[str | date | datetime]) -> Optional[date]:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
    except ValueError:
        try:
            return date.fromisoformat(value)
        except ValueError:
            return None


def normalize_status(status: str, mapping: Optional[dict[str, list[str]]] = None) -> str:
    if status is None:
        return "To Do"
    value = status.strip()
    if not value:
        return "To Do"

    lowered = value.lower()
    if mapping:
        for key, aliases in mapping.items():
            alias_values = {alias.lower() for alias in aliases}
            if lowered in alias_values:
                return key
            if any(alias.lower() in lowered for alias in alias_values):
                return key

    if "done" in lowered or "resolved" in lowered or "closed" in lowered:
        return "Done"
    if "progress" in lowered or "in progress" in lowered or "active" in lowered:
        return "In Progress"
    return "To Do"


def _story_point_value(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        cleaned = value.strip()
        if not cleaned:
            return None
        try:
            return float(cleaned)
        except ValueError:
            return None
    return None


def build_summary(issues: Iterable[Issue], sprint: Optional[Sprint] = None, last_refresh: Optional[datetime] = None) -> dict[str, Any]:
    issue_list = list(issues)
    committed = 0.0
    completed = 0.0
    total_issues = len(issue_list)
    issues_completed = 0
    unestimated_count = 0
    for issue in issue_list:
        points = _story_point_value(issue.story_points)
        if points is not None and points > 0:
            committed += points
            if issue.status_category == "Done":
                completed += points
        if points is None or points == 0:
            unestimated_count += 1
        if issue.status_category == "Done":
            issues_completed += 1

    remaining = max(committed - completed, 0.0)
    completion_pct = (completed / committed * 100.0) if committed else 0.0

    elapsed = 0
    remaining_days = 0
    if sprint is not None:
        sprint_start = _as_date(sprint.start_date)
        sprint_end = _as_date(sprint.end_date)
        if sprint_start and sprint_end and sprint_start <= sprint_end:
            today = date.today()
            elapsed = max((today - sprint_start).days, 0)
            total_days = max((sprint_end - sprint_start).days + 1, 1)
            remaining_days = max(total_days - elapsed, 0)

    return {
        "total_committed_story_points": round(committed, 2),
        "completed_story_points": round(completed, 2),
        "remaining_story_points": round(remaining, 2),
        "completion_pct": round(completion_pct, 2),
        "total_issues": total_issues,
        "issues_completed": issues_completed,
        "sprint_days_elapsed": elapsed,
        "sprint_days_remaining": remaining_days,
        "forecast": "On track" if committed == 0 or completion_pct >= 0 else "At risk",
        "last_successful_refresh": last_refresh.isoformat() if last_refresh else None,
        "unestimated_issue_count": unestimated_count,
    }


def _simple_pace_forecast(completed_story_points: float, committed_story_points: float, sprint_days_elapsed: int, sprint_days_total: int) -> str:
    if committed_story_points <= 0:
        return "On track"
    if sprint_days_total <= 0:
        return "On track"
    completed_ratio = completed_story_points / committed_story_points
    elapsed_ratio = sprint_days_elapsed / sprint_days_total
    return "On track" if completed_ratio >= elapsed_ratio else "At risk"


def detect_blockers(issues: Iterable[Issue], labels: Optional[Iterable[str]] = None) -> list[dict[str, Any]]:
    blocked_labels = {str(label).lower() for label in (labels or [])}
    rows: list[dict[str, Any]] = []
    for issue in issues:
        issue_labels = {str(label).lower() for label in issue.labels}
        if blocked_labels.intersection(issue_labels) or issue.is_blocked or issue.blocking_issues:
            blocker_reason = None
            if blocked_labels.intersection(issue_labels):
                blocker_reason = "Blocked label"
            elif issue.blocking_issues:
                blocker_reason = "Issue link"
            elif issue.is_blocked:
                blocker_reason = "Blocked flag"
            rows.append({
                "key": issue.key,
                "summary": issue.summary,
                "status": issue.status,
                "assignee": issue.assignee,
                "story_points": issue.story_points,
                "blocker_reason": blocker_reason,
                "jira_url": issue.jira_url,
            })
    return rows


def calculate_business_days(start: Optional[str | date], end: Optional[str | date]) -> int:
    start_date = _as_date(start)
    end_date = _as_date(end)
    if not start_date or not end_date:
        return 0
    if end_date < start_date:
        return 0
    count = 0
    current = start_date
    while current <= end_date:
        if current.weekday() < 5:
            count += 1
        current = current.fromordinal(current.toordinal() + 1)
    return count


def detect_risks(issues: Iterable[Issue], sprint_start: Optional[str | date] = None, current_time: Optional[datetime] = None) -> list[dict[str, Any]]:
    current = current_time or datetime.now(timezone.utc)
    sprint_start_date = _as_date(sprint_start)
    rows: list[dict[str, Any]] = []

    for issue in issues:
        reasons: list[str] = []
        due = _as_date(issue.due_date)
        if due and due < current.date() and issue.status_category != "Done":
            reasons.append("Due date passed")

        if issue.status == "" or issue.status is None:
            reasons.append("No status")
        if not issue.assignee or issue.assignee == "Unassigned":
            reasons.append("No assignee")

        updated_at = _as_date(issue.updated_at)
        if updated_at and (current.date() - updated_at).days >= 3:
            reasons.append("Inactive for 3 business days")

        label_blocked = any(str(label).lower() == "blocked" for label in issue.labels)
        if label_blocked or issue.is_blocked or issue.blocking_issues:
            reasons.append("Unresolved blocker")

        if sprint_start_date and issue.added_after_start:
            reasons.append("Added after sprint start")

        if reasons:
            rows.append({
                "key": issue.key,
                "summary": issue.summary,
                "assignee": issue.assignee,
                "status": issue.status,
                "story_points": issue.story_points,
                "risk_reasons": reasons,
                "jira_url": issue.jira_url,
            })
    return rows


def filter_issues(issues: Iterable[Issue], filters: Optional[FilterOptions | dict[str, Any]] = None) -> list[Issue]:
    if filters is None:
        return list(issues)
    if isinstance(filters, dict):
        filters = FilterOptions(**filters)

    selected = list(issues)
    if filters.assignee:
        selected = [issue for issue in selected if issue.assignee == filters.assignee]
    if filters.issue_type:
        selected = [issue for issue in selected if issue.issue_type == filters.issue_type]
    if filters.status_category:
        selected = [issue for issue in selected if issue.status_category == filters.status_category]
    if filters.risk_state:
        selected = [
            issue for issue in selected
            if (
                (filters.risk_state == "at-risk" and (issue.blocking_issues or issue.is_blocked or issue.status_category != "Done"))
                or (filters.risk_state == "healthy" and not issue.blocking_issues and not issue.is_blocked)
            )
        ]
    return selected


def build_board(issues: Iterable[Issue]) -> dict[str, list[Issue]]:
    grouped = {"To Do": [], "In Progress": [], "Done": []}
    for issue in issues:
        category = issue.status_category or normalize_status(issue.status, {})
        grouped.setdefault(category, []).append(issue)
    return grouped


def build_report(issues: Iterable[Issue], sprint: Optional[Sprint] = None, filters: Optional[FilterOptions | dict[str, Any]] = None, last_refresh: Optional[datetime] = None) -> dict[str, Any]:
    issue_list = list(issues)
    filtered = filter_issues(issue_list, filters)
    if sprint is None:
        sprint = Sprint(name="Active sprint", start_date=date.today(), end_date=date.today(), project_key="")

    summary = build_summary(filtered, sprint, last_refresh)
    blockers = detect_blockers(filtered)
    risks = detect_risks(filtered, sprint.start_date, last_refresh)
    board = build_board(filtered)
    filtered_subset = len(filtered) != len(issue_list)

    sprint_days_total = max(((_as_date(sprint.end_date) or date.today()) - (_as_date(sprint.start_date) or date.today())).days + 1, 1)
    elapsed_days = summary["sprint_days_elapsed"]
    completed_points = summary["completed_story_points"]
    committed_points = summary["total_committed_story_points"]
    forecast_status = _simple_pace_forecast(completed_points, committed_points, elapsed_days, sprint_days_total)
    summary["forecast"] = forecast_status
    summary["forecast_label"] = "Simple pace forecast: compare completed points to elapsed sprint time."

    return {
        "sprint": {
            "name": sprint.name,
            "project_key": sprint.project_key,
            "start_date": _as_date(sprint.start_date).isoformat() if _as_date(sprint.start_date) else None,
            "end_date": _as_date(sprint.end_date).isoformat() if _as_date(sprint.end_date) else None,
        },
        "summary": summary,
        "blockers": blockers,
        "risks": risks,
        "board": board,
        "filters": filters.as_dict() if isinstance(filters, FilterOptions) else (filters or {}),
        "filtered_subset": filtered_subset,
        "filter_options": {
            "assignees": sorted({issue.assignee for issue in issue_list}),
            "issue_types": sorted({issue.issue_type for issue in issue_list}),
            "statuses": sorted({issue.status_category for issue in issue_list}),
            "risk_states": ["at-risk", "healthy"],
        },
    }
