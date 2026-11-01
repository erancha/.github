#!/usr/bin/env bash
# Shared helpers for the scripts: repo path, help text and the gh precondition.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Print the calling script's header comment block as --help text (single source of usage docs).
print_help() { awk 'NR==1 {next} /^#/ {sub(/^# ?/, ""); print; next} {exit}' "$0"; }

require_gh() {
  gh auth status >/dev/null 2>&1 \
    || { echo "gh is not signed in; sign in first:  gh auth login" >&2; exit 1; }
}
