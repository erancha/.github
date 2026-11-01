# Issue labels

Every repository under github.com/erancha uses one label pack, so a reader who knows one repo reads
the next. This page is the pack: the label groups, what each label means, and how an issue is
labelled. `scripts/sync-labels.sh` in this repository reads the tables below and applies them to a
repository, so the tables are the single source and their columns are fixed: label, colour,
description, and the older names the script renames. The contributing guide, `CONTRIBUTING.md`,
links here.

## How an issue is labelled

- Exactly one label from each of **Type**, **Priority**, **Risk** and **Effort**.
- `long-term` when the issue is valid but parked; `epic` on an umbrella issue.
- Any number of **Subject** labels, the same set in every repository.
- Any number of `area/` labels, which each repository defines for its own parts.
- `duplicate` or `wontfix` when an issue closes for that reason.

The groups measure different things, so one does not stand in for another:

- **Priority** is how much the gap matters. It says nothing about when the work happens.
- **`long-term`** is scheduling. A whole domain can be out of scope for a while without its issues
  mattering less, so `priority/medium` with `long-term` is a normal combination. The one exception
  is `priority/high`: a gap that breaks a guarantee is fixed or re-rated, never parked quietly.
- **Risk** is the danger of making the change, not the damage of leaving the gap. Priority already
  covers the gap.
- **Effort** is the owner's own time: sessions to run, decisions to make, deploys and manual steps
  to perform, results to verify. AI assistance makes the typing fast, so calendar time no longer
  separates issues; the owner's attention does.

## Type

Exactly one. What kind of change closes the issue.

| Label | Colour | Description | Renames |
|---|---|---|---|
| `bug` | `d73a4a` | Behavior the code promises but does not deliver | — |
| `enhancement` | `a2eeef` | New behavior | `functional` |
| `documentation` | `0075ca` | Docs only; code unchanged | — |
| `tech-debt` | `e99695` | Cleanup with behavior preserved | `hygiene` |

## Priority

Exactly one. How much the gap matters.

| Label | Colour | Description | Renames |
|---|---|---|---|
| `priority/high` | `b60205` | Breaks a guarantee or blocks the core flow | `priority: high`, `priority:high`, `priority/P1` |
| `priority/medium` | `fbca04` | Important, but not blocking | `priority: medium`, `priority:medium`, `priority/P2` |
| `priority/low` | `0e8a16` | Nice to have | `priority: low`, `priority:low`, `priority/P3`, `low priority` |

An old `priority/P4` ("Someday") becomes `priority/low` plus `long-term`.

## Risk

Exactly one. The danger of making the change.

| Label | Colour | Description | Renames |
|---|---|---|---|
| `risk/high` | `f9d0c4` | Touches auth, money or stored user data; hard to revert | `risk: high`, `risk:high` |
| `risk/medium` | `fef2c0` | Touches a contract or more than one repo | `risk: medium`, `risk:medium` |
| `risk/low` | `c2e0c6` | Contained change, easy to revert | `risk: low`, `risk:low` |

## Effort

Exactly one. The owner's own time, not calendar time.

| Label | Colour | Description | Renames |
|---|---|---|---|
| `effort/S` | `e6f4ea` | One session, no decision; ships without a deploy or with a routine one | `effort: small` |
| `effort/M` | `bfdadc` | One session with a design decision, a deploy, or a manual step | `effort: medium` |
| `effort/L` | `7fb3d5` | Several sessions, more than one component, or a migration to watch | `effort: large` |
| `effort/XL` | `3f6e9a` | Several repos or a staged rollout, each stage reviewed | — |

## Planning flags

Optional.

| Label | Colour | Description | Renames |
|---|---|---|---|
| `long-term` | `8779af` | Parked: valid, but not scheduled; never with priority/high | `Long term` |
| `epic` | `5319e7` | Umbrella issue tracked as stories | — |

## Subject

Optional, any number. The same set in every repository.

| Label | Colour | Description | Renames |
|---|---|---|---|
| `security` | `d73a4a` | Authentication, tokens, data isolation | `auth` |
| `privacy` | `5319e7` | User data leaving the app or over-shared | — |
| `correctness` | `b60205` | Results and figures must be right | — |
| `reliability` | `e99695` | Faults outside the app's control: failures, restarts, recovery | — |
| `durability` | `5319e7` | Committed work must survive a crash or restart | — |
| `scalability` | `1d76db` | Serving more people from more replicas; pairs with scaling-safety or scaling-out | — |
| `scaling-safety` | `e99695` | N copies of the service must behave exactly as one would | — |
| `scaling-out` | `c5def5` | Adding replicas serves more users without degrading anyone's experience | — |
| `performance` | `d93f0b` | Throughput and latency | — |
| `observability` | `1d76db` | Logs, traces, metrics | `area: logging` |
| `cost` | `fbca04` | Per-use spend or resource ceilings | — |
| `accessibility` | `f143ab` | Barrier affecting people with disabilities | — |
| `ux` | `f9c513` | What the person sees on the page | — |
| `architecture` | `5319e7` | Structure of the system | — |
| `tests` | `006b75` | Test coverage and fixtures | — |
| `ci-build` | `bfd4f2` | Pipelines, locks, images | — |
| `infra-ops` | `0e8a16` | Compose, deployment, hosting | — |

Two rules keep the subjects honest: `scalability` always goes with `scaling-safety` or
`scaling-out`, and `reliability` is only for faults outside the app's control, never for code
written for one process.

## Area

Optional, any number. Each repository names its own parts under the `area/` prefix, in kebab case
(`area/field-app`, `area/chat`). The sync script leaves `area/` labels alone, so they are created
by hand: `gh label create "area/<name>" -R erancha/<repo> --description "<what the part is>"`.

## Closing

Set when an issue closes for that reason.

| Label | Colour | Description | Renames |
|---|---|---|---|
| `duplicate` | `cfd3d7` | Another issue already covers this | — |
| `wontfix` | `ffffff` | This will not be worked on | — |

## Searching

- What comes next: `is:open -label:long-term label:priority/high`
- Quick wins: `is:open label:effort/S label:risk/low`
- Parked work: `is:open label:long-term`
- Not yet triaged: `is:open -label:priority/high -label:priority/medium -label:priority/low`

## Applying the pack

- `scripts/sync-labels.sh --dry-run --all` shows what every repository of the signed-in account
  would change; without `--dry-run` it creates, recolours and renames labels to match the tables.
- `--prune` also deletes labels outside the pack that sit on no issue or pull request, open or
  closed. Labels still in use are reported, so triage moves their issues first.
- A new repository runs `scripts/sync-labels.sh --prune <repo>` before its first issue, then
  creates its `area/` labels.
