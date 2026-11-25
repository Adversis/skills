"""Prepare a River Archive change or score an assessment from a skill run."""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
VALIDATOR = HERE.parents[1] / "scripts/validate_assessment.py"
CASES = ("export-worker", "docs-only", "deployment")
DENIED = "SEC-001/denied-export"
PERMITTED = "SEC-001/permitted-export"
APPROVAL = "SEC-002/independent-approval"


def git(directory, *args):
    command = ["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
               "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null", *args]
    return subprocess.run(command, cwd=directory, check=True, text=True, stdout=subprocess.PIPE).stdout.strip()


def prepare(case, directory):
    if directory.exists():
        raise ValueError(f"Choose a new fixture directory: {directory}")
    shutil.copytree(HERE / "base", directory, ignore=shutil.ignore_patterns("__pycache__"))
    git(directory, "init", "--quiet")
    git(directory, "add", ".")
    git(directory, "commit", "--quiet", "-m", "Base")
    shutil.copytree(HERE / "candidates" / case, directory, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__"))
    git(directory, "add", ".")
    git(directory, "commit", "--quiet", "-m", case)
    print(f"{directory}: compare HEAD^ with HEAD")


def score(case, directory, assessment, kind):
    subprocess.run([sys.executable, VALIDATOR, assessment, "--register",
                    directory / "docs/security-requirements.yaml"], check=True)
    record = json.loads(assessment.read_text(encoding="utf-8"))
    if git(directory, "log", "-1", "--format=%s") != case:
        raise ValueError("The checkout contains a different evaluation case")
    if record["base_revision"] != git(directory, "rev-parse", "HEAD^"):
        raise ValueError("The assessment names a different base revision")
    if record["revision"] != git(directory, "rev-parse", "HEAD") or record["kind"] != kind:
        raise ValueError("The candidate revision or assessment kind differs")
    if kind == "verification":
        source = directory / record.get("source_assessment", "")
        if source.resolve() != (directory / "review/assessment.json").resolve() or not source.is_file():
            raise ValueError("The verification must reference the preserved review")

    expected_ids = {"export-worker": ["SEC-001"], "docs-only": [], "deployment": ["SEC-002"]}
    if record["affected_requirements"] != expected_ids[case]:
        raise ValueError("The affected requirement IDs differ from the fixture")
    checks = {key: result["status"] for key, result in record["checks"].items()}
    if case == "docs-only" and (checks or record["findings"]):
        raise ValueError("The documentation change has no affected check or finding")
    if case == "deployment":
        if checks.get(APPROVAL) not in ("blocked", "not_run") or not record["limitations"]:
            raise ValueError("Record the missing production policy and leave the case open")
    if case == "export-worker":
        if not any("SEC-001" in item["requirement_ids"] for item in record["findings"]):
            raise ValueError("The worker finding must identify SEC-001")
        expected = {DENIED: "not_run", PERMITTED: "not_run"} if kind == "review" else {
            DENIED: "failed", PERMITTED: "passed"}
        if checks != expected:
            raise ValueError(f"Expected {expected}, received {checks}")
    print("Machine checks passed. Apply the evidence criteria in the evaluation guide.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_subparsers(dest="action", required=True)
    for action in ("prepare", "score"):
        command = actions.add_parser(action)
        command.add_argument("case", choices=CASES)
        command.add_argument("directory", type=Path)
        if action == "score":
            command.add_argument("kind", choices=("review", "verification"))
            command.add_argument("assessment", type=Path)
    args = parser.parse_args()
    try:
        if args.action == "prepare":
            prepare(args.case, args.directory)
        else:
            score(args.case, args.directory, args.assessment, args.kind)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
