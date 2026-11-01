# .github

The conventions shared by every repository of one GitHub account: the issue-label pack, the
contributing guide GitHub shows on repositories without their own, and the script that applies the
labels.

## Overview

- One label pack for every repository, so an issue reads the same way everywhere.
- Each label's meaning, and the rules for combining them, on one page: `docs/labels.md`.
- A script that creates, recolours and renames a repository's labels to match that page.

## Scripts

- `scripts/sync-labels.sh`: apply the pack to one repository or to all of them, with a dry run
  and an optional prune of labels outside the pack.
- `scripts/test.sh`: syntax-check the scripts and parse the pack.

## Using the sync script

**What it does.** "Sync" makes a repository's labels match the pack. The tables in `docs/labels.md`
are the correct list, and `scripts/sync-labels.sh` compares each repository's labels with them.

**Who can run it.** Anyone: these are ordinary bash and Python scripts, and no AI tool is involved.
It needs `bash`, `python3`, the `gh` CLI signed in, a local clone of this repository, and write
access to each repository it changes. Reading this repository grants no access to anything else.

```bash
scripts/sync-labels.sh --dry-run owner/repo   # show what would change, change nothing
scripts/sync-labels.sh owner/repo             # apply the pack to one repository
scripts/sync-labels.sh --all                  # every non-archived repository you own
scripts/sync-labels.sh --help                 # all options
```

**When to run it.** Nothing runs on its own, so a person starts it in two cases. A new repository
holds GitHub's default labels until it is synced. A change to the pack reaches repositories only
after `--all` runs. Running it again is safe: a repository that already matches does not change.

**What happens to each label.**

| The repository has | Result |
|---|---|
| No label for a pack row | The label is created |
| A pack label with another colour or description | The pack's values overwrite them |
| A name in a row's Renames column | It is renamed and stays on its issues |
| An `area/` label | Left alone: each repository owns these |
| Any other label | Reported and kept |
| Any other label, with `--prune` | Deleted when it is on no open issue or pull request |
| An old name and its new name together, or two old names for one label | An error for that label; move the issues by hand, then rerun |

`--prune` looks only at open items, so a deleted label also disappears from closed issues. Check
the `--dry-run` output first.

## Adapting the pack

The script names no repository, but it has been applied and tested only on the author's own
repositories: 46 public and private repositories of one personal account. It has not been run on
an organization or on repositories shared with other people. Its automated checks cover only
script syntax and parsing the pack, so start with `--dry-run` anywhere else.

The pack's labels and meanings suit one solo-owned set of projects, so a different set of
repositories may need a different pack.

**To keep a repository's existing label,** do one of these in `docs/labels.md` before syncing:

- Map it to a pack label by adding its name to that row's Renames column, so its issues move over.
- Add a row of its own to the table of the group it belongs to.
- Name it `area/<something>` in that repository, so the script leaves it alone.

**To use a different pack,** copy this repository and edit only `docs/labels.md`. Add, remove or
reword rows, and add tables for new groups. The script reads every row in the page, whatever its
heading. A row must keep this shape, because any other line is skipped without a warning:

```markdown
| `label` | `0e8a16` | Description, up to 100 characters | `old name`, `other old name` |
```

- The colour is six lowercase hex digits, and the label and colour stay in backticks.
- The last column is `—` when nothing is renamed. The description cannot contain a `|`.
- Run `scripts/test.sh` after editing. It prints the label count, which shows a skipped row.
- `REPO_OWNED_PREFIX` in `scripts/sync_labels.py` sets which prefix the script leaves alone.
- A shared `CONTRIBUTING.md` needs a public repository named `.github` in the owning account. Its
  text, and the opening of `docs/labels.md`, name the repositories they apply to, so reword both.

## Details

- `docs/labels.md`: the label groups, what each label means, how an issue is labelled, and how
  the pack reaches a repository.
- `CONTRIBUTING.md`: the short guide GitHub shows on repositories without their own, which links
  to the pack.

## License

MIT, see `LICENSE`.
