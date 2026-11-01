#!/usr/bin/env bash
# Apply the issue-label pack in docs/labels.md to GitHub repositories.
#
# Usage:
#   scripts/sync-labels.sh [--dry-run] [--prune] <repo>...
#   scripts/sync-labels.sh [--dry-run] [--prune] --all
#   scripts/sync-labels.sh --check
#
# A repo is owner/name, or a bare name under the signed-in account. --all takes every
# non-archived source repository of the signed-in account. Labels are created, recoloured and
# renamed to match the tables; area/ labels belong to each repository and are never touched.
#
# Options:
#   --dry-run   Print what would change and change nothing
#   --prune     Also delete labels outside the pack that sit on no issue or pull request, open or
#               closed
#   --check     Parse the pack and report the label count, without touching GitHub
#   -h, --help  Show this help
#
# Examples:
#   scripts/sync-labels.sh --dry-run --all
#   scripts/sync-labels.sh --prune erancha/diet-tracker
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=common.sh
source "$SCRIPT_DIR/common.sh"

for arg in "$@"; do
  case "$arg" in
    -h|--help) print_help; exit 0 ;;
    --dry-run|--prune|--all|--check) ;;
    -*) print_help >&2; exit 2 ;;
  esac
done

[ "${1:-}" = "--check" ] || require_gh
exec python3 "$SCRIPT_DIR/sync_labels.py" "$@"
