# Module 15 Completion Report

## Script Metadata
- Filename: `tools/validate_instructions.py`
- Language: Python
- Purpose: Processes each `instructions/*.agent.md` file individually. It supplies the validation instruction and file contents to an AI CLI or OpenAI-compatible API, then saves one Markdown validation result per file and a JSON manifest.

## Script Contents

```python
#!/usr/bin/env python3
"""Validate instruction files one at a time with an AI CLI or API."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from validate_with_ai import build_prompt, run_api, run_cli


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--instruction",
        type=Path,
        default=Path("instructions/validate-instructions.agent.md"),
        help="Instruction file supplied to the AI for each validation.",
    )
    parser.add_argument(
        "--pattern",
        default="instructions/*.agent.md",
        help="Target glob relative to the current directory.",
    )
    parser.add_argument("--output-dir", type=Path, default=Path("validation-results/instructions"))
    parser.add_argument("--provider", choices=("cli", "api"), default="cli")
    parser.add_argument(
        "--cli-command",
        default=os.environ.get("AI_VALIDATE_COMMAND", "copilot"),
    )
    parser.add_argument("--api-url", default=os.environ.get("AI_API_URL"))
    parser.add_argument("--api-key", default=os.environ.get("AI_API_KEY"))
    parser.add_argument("--model", default=os.environ.get("AI_MODEL", "gpt-4o-mini"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.instruction.is_file():
        print(f"Instruction file not found: {args.instruction}", file=sys.stderr)
        return 2
    if args.provider == "api" and (not args.api_url or not args.api_key):
        print("--api-url and --api-key (or AI_API_URL and AI_API_KEY) are required.", file=sys.stderr)
        return 2

    rules = args.instruction.read_text(encoding="utf-8")
    files = sorted(Path(".").glob(args.pattern))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    manifest: list[dict[str, str]] = []
    failures = 0

    print("Target files:")
    for file_path in files:
        print(f"- {file_path.as_posix()}")

    for file_path in files:
        prompt = build_prompt(rules, file_path, file_path.read_text(encoding="utf-8"))
        try:
            if args.provider == "cli":
                result = run_cli(args.cli_command, prompt)
            else:
                result = run_api(prompt, args.model, args.api_url, args.api_key)
            status = "ok"
        except (OSError, RuntimeError, ValueError) as error:
            result = f"Validation failed to run: {error}"
            status = "error"
            failures += 1

        output_path = args.output_dir / file_path.with_suffix(".validation.md").name
        output_path.write_text(
            f"# Validation: `{file_path.as_posix()}`\n\n{result}\n",
            encoding="utf-8",
        )
        manifest.append(
            {"file": file_path.as_posix(), "output": output_path.as_posix(), "status": status}
        )

    (args.output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Processed {len(files)} file(s); results are in {args.output_dir}/.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Parameters
| Parameter | Description | Default |
|-----------|-------------|---------|
| `--instruction` | Instruction file supplied to the AI for each validation | `instructions/validate-instructions.agent.md` |
| `--pattern` | Target file glob relative to the current directory | `instructions/*.agent.md` |
| `--output-dir` | Directory for per-file results and `manifest.json` | `validation-results/instructions` |
| `--provider` | AI provider mode: `cli` or `api` | `cli` |
| `--cli-command` | AI CLI executable and arguments; `AI_VALIDATE_COMMAND` can also set it | `copilot` |
| `--api-url` | OpenAI-compatible API endpoint; `AI_API_URL` can also set it | unset |
| `--api-key` | API bearer key; `AI_API_KEY` can also set it | unset |
| `--model` | API model name; `AI_MODEL` can also set it | `gpt-4o-mini` |

## Test Run Output

Command:

```bash
python3 tools/validate_instructions.py \
  --pattern 'instructions/validate-instructions.agent.md' \
  --cli-command echo \
  --output-dir /tmp/module-15-validation
```

Output:

```text
Target files:
- instructions/validate-instructions.agent.md
Processed 1 file(s); results are in /tmp/module-15-validation/.
```
