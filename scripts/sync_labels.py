"""Applies the label pack in docs/labels.md to GitHub repositories through the gh CLI.

Core responsibilities:
- Parses the pack tables: label, colour, description, and the older names each label renames
- Creates, recolours or renames each repository's labels to match the pack
- Reports labels outside the pack and, with --prune, deletes those on no open issue
"""

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
DOC = ROOT / "docs" / "labels.md"
# Labels under this prefix belong to each repository and are never created, renamed or deleted.
REPO_OWNED_PREFIX = "area/"
# A pack row: | `label` | `colour` | description | renames |
ROW = re.compile(r"^\| `([^`]+)` \| `([0-9a-f]{6})` \| ([^|]+?) \| ([^|]+?) \|$")
MAX_DESCRIPTION = 100  # GitHub's limit


@dataclass(frozen=True)
class Label:
    name: str
    color: str
    description: str
    renames: tuple[str, ...]


def parse_pack(doc: Path) -> list[Label]:
    labels = []
    for line in doc.read_text(encoding="utf-8").splitlines():
        match = ROW.match(line)
        if match is None:
            continue
        name, color, description, renames = match.groups()
        old_names = tuple(re.findall(r"`([^`]+)`", renames))
        labels.append(Label(name, color, description.strip(), old_names))
    names = [label.name for label in labels]
    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        sys.exit(f"{doc}: label listed twice: {', '.join(duplicates)}")
    too_long = [label.name for label in labels if len(label.description) > MAX_DESCRIPTION]
    if too_long:
        sys.exit(f"{doc}: description over {MAX_DESCRIPTION} characters: {', '.join(too_long)}")
    if not labels:
        sys.exit(f"{doc}: no label rows found; the tables must keep the four fixed columns")
    return labels


def gh(*args: str) -> str:
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout


def gh_json(*args: str):
    return json.loads(gh(*args))


def open_issue_count(repo: str, label: str) -> int:
    # The REST issues endpoint lists pull requests too, so a label on an open PR also counts.
    path = f"repos/{repo}/issues?labels={quote(label, safe='')}&state=open&per_page=1"
    return len(gh_json("api", path))


class Sync:
    def __init__(self, pack: list[Label], dry_run: bool, prune: bool):
        self.pack = pack
        self.dry_run = dry_run
        self.prune = prune
        self.failed = False

    def run(self, repo: str) -> None:
        print(f"== {repo}")
        listed = gh_json(
            "label", "list", "-R", repo, "--limit", "200", "--json", "name,color,description"
        )
        existing = {label["name"]: label for label in listed}
        for label in self.pack:
            self.sync_label(repo, label, existing)
        pack_names = {label.name for label in self.pack}
        for name in sorted(existing):
            if name in pack_names or name.startswith(REPO_OWNED_PREFIX):
                continue
            count = open_issue_count(repo, name)
            if count == 0 and self.prune:
                self.act(
                    f"delete {name!r}, on no open issue",
                    "label", "delete", name, "-R", repo, "--yes",
                )
            else:
                print(f"   outside the pack: {name!r}" + (", on open issues" if count else ""))

    def sync_label(self, repo: str, label: Label, existing: dict) -> None:
        present = [old for old in label.renames if old in existing]
        if label.name in existing:
            if present:
                self.fail(f"{label.name!r} and {present!r} both exist; move the issues, then rerun")
                return
            current = existing[label.name]
            changed = (
                current["color"].lower() != label.color
                or current["description"] != label.description
            )
            if changed:
                self.act(
                    f"recolour {label.name!r}",
                    "label", "edit", label.name, "-R", repo,
                    "--color", label.color, "--description", label.description,
                )
            return
        if len(present) > 1:
            self.fail(f"{present!r} would all become {label.name!r}; merge them first, then rerun")
            return
        if present:
            self.act(
                f"rename {present[0]!r} -> {label.name!r}",
                "label", "edit", present[0], "-R", repo, "--name", label.name,
                "--color", label.color, "--description", label.description,
            )
            existing[label.name] = existing.pop(present[0])
            return
        self.act(
            f"create {label.name!r}",
            "label", "create", label.name, "-R", repo,
            "--color", label.color, "--description", label.description,
        )

    def act(self, what: str, *args: str) -> None:
        print(f"   {'would ' if self.dry_run else ''}{what}")
        if not self.dry_run:
            gh(*args)

    def fail(self, why: str) -> None:
        print(f"   ERROR: {why}", file=sys.stderr)
        self.failed = True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("repos", nargs="*", help="owner/name, or a name under the signed-in account")
    parser.add_argument("--all", action="store_true", help="every non-archived source repository")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--prune", action="store_true")
    parser.add_argument("--check", action="store_true", help="parse the pack and exit")
    args = parser.parse_args()

    pack = parse_pack(DOC)
    if args.check:
        print(f"{len(pack)} labels in {DOC.name}")
        return
    if not args.repos and not args.all:
        parser.error("name at least one repository, or pass --all")
    owner = gh("api", "user", "--jq", ".login").strip()
    repos = [repo if "/" in repo else f"{owner}/{repo}" for repo in args.repos]
    if args.all:
        listed = gh_json(
            "repo", "list", owner, "--limit", "200", "--no-archived", "--source", "--json", "name"
        )
        repos += [f"{owner}/{repo['name']}" for repo in listed]

    sync = Sync(pack, args.dry_run, args.prune)
    for repo in repos:
        sync.run(repo)
    if sync.failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
