# Module 12 Completion Report

## Instruction File
- Filename: instructions/use-`StoryPointcalculator.agent.md

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

## Script File
- Filename: tools/StoryPointcalculator.py
- Language: Python

"""Calculate committed, completed, and remaining sprint story points."""

import argparse


def calculate_story_points(issues: list[str]) -> tuple[float, float, float]:
    """Return committed, completed, and remaining points from status:points values."""
    committed = 0.0
    completed = 0.0

    for issue in issues:
        try:
            status, points_text = issue.rsplit(":", 1)
            points = float(points_text)
        except ValueError as error:
            raise ValueError(
                f"invalid issue '{issue}'; expected STATUS:STORY_POINTS"
            ) from error

        if points < 0:
            raise ValueError(f"story points must be non-negative: '{issue}'")

        committed += points
        if status.strip().lower() in {"done", "complete", "completed"}:
            completed += points

    return committed, completed, committed - completed


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calculate sprint story-point totals."
    )
    parser.add_argument(
        "issues",
        nargs="+",
        metavar="STATUS:STORY_POINTS",
        help="Sprint issue, such as Done:5 or In Progress:3",
    )
    args = parser.parse_args()

    try:
        committed, completed, remaining = calculate_story_points(args.issues)
    except ValueError as error:
        parser.error(str(error))

    print(f"Committed work: {committed:g} story points")
    print(f"Completed work: {completed:g} story points")
    print(f"Remaining work: {remaining:g} story points")


if __name__ == "__main__":
    main()

## Script Execution Output
usage: StoryPointcalculator.py [-h]
                               STATUS:STORY_POINTS [STATUS:STORY_POINTS ...]

Calculate sprint story-point totals.

positional arguments:
  STATUS:STORY_POINTS  Sprint issue, such as Done:5 or In Progress:3

options:
  -h, --help           show this help message and exit
