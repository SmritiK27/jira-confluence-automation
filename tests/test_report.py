from datetime import date, datetime

from sprint_report import Issue, Sprint, build_report, build_summary, calculate_business_days, detect_blockers, detect_risks, normalize_status


def test_story_point_totals_and_completion():
    issues = [
        Issue(key="KAN-1", summary="A", status="Done", assignee="Sam", story_points=5, status_category="Done"),
        Issue(key="KAN-2", summary="B", status="In Progress", assignee="Ava", story_points=3, status_category="In Progress"),
        Issue(key="KAN-3", summary="C", status="To Do", assignee="Sam", story_points=None, status_category="To Do"),
    ]
    sprint = Sprint(name="Sprint 18", start_date="2026-09-01", end_date="2026-09-15", project_key="KAN")
    report = build_report(issues, sprint=sprint, last_refresh=datetime(2026, 9, 9, 8, 0, 0))
    summary = report["summary"]

    assert summary["total_committed_story_points"] == 8.0
    assert summary["completed_story_points"] == 5.0
    assert summary["remaining_story_points"] == 3.0
    assert summary["completion_pct"] == 62.5
    assert summary["unestimated_issue_count"] == 1


def test_status_mapping_and_blockers():
    assert normalize_status("In Progress") == "In Progress"
    assert normalize_status("Closed") == "Done"
    assert normalize_status("Backlog") == "To Do"

    issues = [
        Issue(key="KAN-7", summary="Blocked issue", status="In Progress", assignee="Sam", story_points=2, labels={"blocked"}, is_blocked=True),
        Issue(key="KAN-8", summary="Clear issue", status="To Do", assignee="Ava", story_points=1),
    ]
    blockers = detect_blockers(issues, labels=["blocked"])
    assert blockers[0]["key"] == "KAN-7"
    assert blockers[0]["blocker_reason"] == "Blocked label"


def test_simple_forecast_and_risk_reasons():
    sprint = Sprint(name="Sprint 18", start_date="2026-09-01", end_date="2026-09-15", project_key="KAN")
    issues = [
        Issue(key="KAN-9", summary="Late work", status="In Progress", assignee="Sam", story_points=8, due_date=date(2026, 9, 5), updated_at="2026-09-01T00:00:00Z", status_category="In Progress"),
        Issue(key="KAN-10", summary="Blocked work", status="To Do", assignee="Sam", story_points=2, labels={"blocked"}, status_category="To Do", blocking_issues={"KAN-9"}),
    ]
    report = build_report(issues, sprint=sprint, last_refresh=datetime(2026, 9, 9, 12, 0, 0))
    assert report["summary"]["forecast"] in {"On track", "At risk"}
    assert any("Due date passed" in reason["risk_reasons"] for reason in report["risks"])
    assert any("Unresolved blocker" in reason["risk_reasons"] for reason in report["risks"])


def test_business_day_count():
    assert calculate_business_days("2026-09-05", "2026-09-11") == 5
