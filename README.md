# .github

The conventions shared by every repository under github.com/erancha: the issue-label pack, the
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

## Details

- `docs/labels.md`: the label groups, what each label means, how an issue is labelled, and how
  the pack reaches a repository.
- `CONTRIBUTING.md`: the short guide GitHub shows on repositories without their own, which links
  to the pack.

## License

MIT, see `LICENSE`.
