# Jira/Confluence Automation Ideas

## 1. Project Status Summary Generator

**Problem it solves:** Managers spend significant time gathering updates from Jira and turning them into consistent weekly status reports. Automation can summarize progress, risks, blockers, and upcoming milestones in a Confluence page.

**Data needed:**

- Jira projects, epics, issues, statuses, assignees, and due dates
- Sprint progress and completed work
- Blocked or overdue issues
- Risk and dependency labels or custom fields
- The target Confluence page and reporting schedule

## 2. Delivery Risk and Escalation Alerts

**Problem it solves:** Delivery risks can remain unnoticed until a milestone is already threatened. Automation can detect warning signs and notify managers or create an escalation page in Confluence.

**Data needed:**

- Jira issue priorities, status history, due dates, and age
- Sprint velocity and carryover information
- Epic and milestone target dates
- Dependencies and blocked-issue relationships
- Manager notification preferences and escalation rules

## 3. Decision and Action-Item Tracker

**Problem it solves:** Decisions and follow-up actions from meetings are often scattered across Confluence pages and Jira comments, making ownership and deadlines difficult to track. Automation can extract action items, create or update Jira tasks, and maintain a Confluence decision log.

**Data needed:**

- Confluence meeting notes and decision-log pages
- Jira project, issue-type, assignee, and label mappings
- Action-item owners and due dates
- Existing Jira issues to prevent duplicate tasks
- Page permissions and audit-history requirements
