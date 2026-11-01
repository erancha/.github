#!/usr/bin/env bash
# Run the quality gate: a syntax check of every script, a byte-compile of the Python, and a parse
# of the label pack in docs/labels.md.
#
# Usage:
#   scripts/test.sh
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=common.sh
source "$SCRIPT_DIR/common.sh"

case "${1:-}" in
  -h|--help) print_help; exit 0 ;;
  "") ;;
  *) print_help >&2; exit 2 ;;
esac

for script in "$ROOT"/scripts/*.sh; do bash -n "$script"; done
python3 -m py_compile "$ROOT/scripts/sync_labels.py"
"$ROOT/scripts/sync-labels.sh" --check
echo "ok"
