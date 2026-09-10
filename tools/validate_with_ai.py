#!/usr/bin/env python3
"""Validate files with an AI CLI or an OpenAI-compatible HTTP API.

Examples:
    python tools/validate_with_ai.py
    python tools/validate_with_ai.py --provider cli --cli-command copilot
    AI_API_KEY=... python tools/validate_with_ai.py --provider api
"""

from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path


def build_prompt(rules: str, file_path: Path, contents: str) -> str:
    return (
        "Apply the validation rules below to the specified file. "
        "Report each issue with a severity and a concise explanation. "
        "If there are no issues, say so explicitly.\n\n"
        f"VALIDATION RULES:\n{rules}\n\n"
        f"FILE: {file_path}\n"
        f"FILE CONTENTS:\n{contents}\n"
    )


def run_cli(command: str, prompt: str) -> str:
    argv = shlex.split(command)
    if not argv:
        raise ValueError("The CLI command must not be empty.")
    completed = subprocess.run(
        [*argv, "-p", prompt, "-s"],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode:
        details = completed.stderr.strip() or "no error output"
        raise RuntimeError(f"AI CLI exited with {completed.returncode}: {details}")
    return completed.stdout.strip()


def run_api(prompt: str, model: str, url: str, api_key: str) -> str:
    payload = json.dumps(
        {"model": model, "messages": [{"role": "user", "content": prompt}]}
    ).encode()
    request = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request) as response:
            body = json.load(response)
    except urllib.error.HTTPError as error:
        detail = error.read().decode(errors="replace")
        raise RuntimeError(f"AI API returned HTTP {error.code}: {detail}") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"AI API request failed: {error.reason}") from error
    try:
        return body["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError) as error:
        raise RuntimeError("AI API response did not contain message content.") from error


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rules", type=Path, default=Path("validation-rules.md"))
    parser.add_argument(
        "--pattern", default="modules/**/walkthrough.md",
        help="Glob pattern for target files, relative to the current directory.",
    )
    parser.add_argument("--output-dir", type=Path, default=Path("validation-results"))
    parser.add_argument("--provider", choices=("cli", "api"), default="cli")
    parser.add_argument(
        "--cli-command",
        default=os.environ.get("AI_VALIDATE_COMMAND", "copilot"),
        help="AI CLI executable and fixed arguments (also set AI_VALIDATE_COMMAND).",
    )
    parser.add_argument("--api-url", default=os.environ.get("AI_API_URL"))
    parser.add_argument("--api-key", default=os.environ.get("AI_API_KEY"))
    parser.add_argument("--model", default=os.environ.get("AI_MODEL", "gpt-4o-mini"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.rules.is_file():
        print(f"Rules file not found: {args.rules}", file=sys.stderr)
        return 2
    if args.provider == "api" and (not args.api_url or not args.api_key):
        print("--api-url and --api-key (or AI_API_URL and AI_API_KEY) are required.", file=sys.stderr)
        return 2

    rules = args.rules.read_text(encoding="utf-8")
    files = sorted(Path(".").glob(args.pattern))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    manifest: list[dict[str, str]] = []
    failures = 0

    print("Target files:")
    for file_path in files:
        print(f"- {file_path.as_posix()}")

    for file_path in files:
        relative_path = file_path.as_posix()
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

        output_path = args.output_dir / file_path.with_suffix(".validation.md")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            f"# Validation: `{relative_path}`\n\n{result}\n",
            encoding="utf-8",
        )
        manifest.append({"file": relative_path, "output": output_path.as_posix(), "status": status})

    (args.output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Validated {len(files)} file(s); results are in {args.output_dir}/.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
