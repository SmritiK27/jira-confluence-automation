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
