# CLAUDE.md

The account-wide conventions repository: `docs/labels.md` holds the issue-label pack that every
erancha repository uses, and `scripts/sync-labels.sh` applies it. The repository is public, and
GitHub serves its `CONTRIBUTING.md` as the contributing guide of every repository without one.

## Scripts

- `scripts/sync-labels.sh [--dry-run] [--prune] <repo>... | --all`: create, recolour and rename a
  repository's labels to match the pack; `--check` only parses the pack.
- `scripts/test.sh`: `bash -n` on the scripts, a Python byte-compile, and the pack parse.

## Gotchas

- `sync_labels.py` parses the tables in `docs/labels.md`, so every pack table keeps the four
  columns label, colour, description, renames, with the label and colour in backticks. A row that
  breaks the shape is silently skipped; `scripts/test.sh` reports the label count to catch that.
- `area/` labels belong to each repository and are created by hand; the script never touches them.
- A label edit on GitHub is a write to an external system, so the Claude Code permission system
  may ask before each `gh label` call.
