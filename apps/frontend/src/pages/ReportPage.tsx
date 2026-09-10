import { useMemo, useState } from "react";

type Issue = {
  key: string;
  title: string;
  status: "To Do" | "In Progress" | "Done";
  assignee: string;
  points: number;
  risk?: string;
  blocked?: boolean;
};

const issues: Issue[] = [
  { key: "KAN-21", title: "OAuth callback handling", status: "Done", assignee: "Ava", points: 5 },
  { key: "KAN-24", title: "Sprint report API", status: "In Progress", assignee: "Sam", points: 8, blocked: true, risk: "Blocked" },
  { key: "KAN-27", title: "Responsive dashboard layout", status: "In Progress", assignee: "Maya", points: 5, risk: "Due soon" },
  { key: "KAN-29", title: "Rate-limit retry policy", status: "To Do", assignee: "Lee", points: 3 },
  { key: "KAN-31", title: "Accessibility review", status: "To Do", assignee: "Nora", points: 0, risk: "Unestimated" },
];

const columns: Issue["status"][] = ["To Do", "In Progress", "Done"];

export function ReportPage() {
  const [assignee, setAssignee] = useState("All assignees");
  const [riskOnly, setRiskOnly] = useState(false);
  const [lastRefresh, setLastRefresh] = useState("Just now");

  const filteredIssues = useMemo(
    () =>
      issues.filter(
        (issue) =>
          (assignee === "All assignees" || issue.assignee === assignee) &&
          (!riskOnly || Boolean(issue.risk)),
      ),
    [assignee, riskOnly],
  );

  const completed = filteredIssues.filter((issue) => issue.status === "Done");
  const committed = filteredIssues.reduce((total, issue) => total + issue.points, 0);
  const completedPoints = completed.reduce((total, issue) => total + issue.points, 0);
  const completion = committed === 0 ? 0 : Math.round((completedPoints / committed) * 100);

  return (
    <main className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">JIRA SPRINT REPORT</p>
          <h1>Automation Platform Sprint 42</h1>
          <p className="muted">Project KAN · 02 Sep – 16 Sep 2026 · 4 days remaining</p>
        </div>
        <div className="topbar-actions">
          <span className="auth-badge"><span className="status-dot" /> Atlassian connected</span>
          <button className="button button-secondary" onClick={() => setLastRefresh("Just now")}>
            Refresh data
          </button>
        </div>
      </header>

      <section className="notice" aria-label="forecast status">
        <span className="notice-icon">✓</span>
        <div>
          <strong>On track</strong>
          <span>Simple pace forecast · 62% of committed points complete against 58% of sprint time elapsed.</span>
        </div>
      </section>

      <section className="metrics-grid" aria-label="Sprint summary">
        <Metric label="Committed points" value={committed.toString()} detail="Across filtered issues" />
        <Metric label="Completed points" value={completedPoints.toString()} detail={`${completion}% complete`} />
        <Metric label="Remaining points" value={(committed - completedPoints).toString()} detail="6 issues remaining" />
        <Metric label="At-risk issues" value={filteredIssues.filter((issue) => issue.risk).length.toString()} detail="Needs attention" tone="warning" />
      </section>

      <section className="content-grid">
        <div className="panel board-panel">
          <div className="panel-heading">
            <div>
              <p className="eyebrow">SPRINT BOARD</p>
              <h2>Current work</h2>
            </div>
            <span className="filter-note">{filteredIssues.length} issues shown</span>
          </div>
          <div className="board">
            {columns.map((column) => (
              <div className="board-column" key={column}>
                <div className="column-heading">
                  <span>{column}</span>
                  <span className="count">{filteredIssues.filter((issue) => issue.status === column).length}</span>
                </div>
                {filteredIssues.filter((issue) => issue.status === column).map((issue) => (
                  <article className="issue-card" key={issue.key}>
                    <div className="issue-card-top"><a href={`https://jira.example.com/browse/${issue.key}`}>{issue.key}</a><span className="points">{issue.points || "—"} pts</span></div>
                    <h3>{issue.title}</h3>
                    <div className="issue-meta"><span>{issue.assignee}</span>{issue.risk && <span className="risk-tag">{issue.risk}</span>}{issue.blocked && <span className="blocked-tag">Blocked</span>}</div>
                  </article>
                ))}
              </div>
            ))}
          </div>
        </div>

        <aside className="panel filters-panel">
          <div className="panel-heading"><div><p className="eyebrow">VIEW</p><h2>Filters</h2></div></div>
          <label>
            Assignee
            <select value={assignee} onChange={(event) => setAssignee(event.target.value)}>
              <option>All assignees</option>
              <option>Ava</option><option>Sam</option><option>Maya</option><option>Lee</option><option>Nora</option>
            </select>
          </label>
          <label className="checkbox-row"><input type="checkbox" checked={riskOnly} onChange={(event) => setRiskOnly(event.target.checked)} /> Show at-risk issues only</label>
          <div className="filter-summary"><strong>Last successful refresh</strong><span>{lastRefresh}</span><small>Automatic refresh every 5 minutes</small></div>
        </aside>
      </section>

      <footer className="footer">Read-only Jira data · Metrics represent the current sprint view · <a href="https://jira.example.com">Open Jira</a></footer>
    </main>
  );
}

function Metric({ label, value, detail, tone }: { label: string; value: string; detail: string; tone?: "warning" }) {
  return <article className={`metric-card ${tone === "warning" ? "metric-warning" : ""}`}><span>{label}</span><strong>{value}</strong><small>{detail}</small></article>;
}