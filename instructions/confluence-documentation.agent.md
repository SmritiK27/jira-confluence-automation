# Confluence Documentation Instructions

- Use Confluence as the source of truth for team documentation, decisions, procedures, and project knowledge.
- Preserve the destination space’s existing page hierarchy, templates, labels, and writing conventions.
- Do not expose credentials, access tokens, private comments, or restricted page content.

## Input format

- Accept a page title, Confluence space key, parent page, document purpose, source material, or page URL.
- For new or updated pages, provide the intended audience, scope, owner, status, and required sections when known.
- For searches, specify the space, page title, labels, author, update date, or relevant keywords.

## Processing steps

- Confirm the target space, page, and parent hierarchy before making changes.
- Inspect existing page content and metadata before updating it.
- Reuse the existing page structure and template where possible.
- Organize content with clear headings, concise paragraphs, lists, tables, and links.
- Preserve useful existing content unless the request explicitly replaces it.
- Validate links, labels, page status, permissions, and version-conflict handling.
- Identify assumptions, stale information, and unresolved ownership or review dates.

## Output format

- For page creation, return the page title, space, parent, status, labels, and Confluence link.
- For updates, list the sections changed and summarize the resulting page structure.
- For searches, return a concise table containing title, space, owner, last updated date, and link.
- For blocked operations, state the missing permission, invalid parent, or required input.

## Constraints

- Never invent page IDs, space keys, page hierarchy, links, or approval status.
- Do not overwrite existing documentation without checking its current version and scope.
- Do not modify unrelated pages or bulk-update without explicit scope.
- Keep documentation factual, accessible, and easy to maintain.
- Treat API failures, rate limits, permission errors, and version conflicts as failures; do not report them as successful changes.
