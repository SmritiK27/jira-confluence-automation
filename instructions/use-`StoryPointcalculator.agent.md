# Story Point Calculator Instructions

Use `tools/StoryPointcalculator.py` when a sprint's issue statuses and story
points are available and you need committed, completed, and remaining work
totals.

Run it from the workspace root with one or more issue arguments:

```bash
python3 tools/StoryPointcalculator.py <STATUS:STORY_POINTS> [<STATUS:STORY_POINTS> ...]
```

For example:

```bash
python3 tools/StoryPointcalculator.py Done:5 "In Progress:3" "To Do:2"
```

Each argument must contain a status, a colon, and a non-negative story-point
value. Quote arguments when the status contains spaces. Issues with statuses
`Done`, `Complete`, or `Completed` count as completed; all other statuses
contribute to committed work but not completed work.

Present the script's output as:

- **Committed work**: Total story points across all supplied issues.
- **Completed work**: Story points for completed issues.
- **Remaining work**: Committed work minus completed work.
