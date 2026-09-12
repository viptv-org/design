#!/usr/bin/env bash
set -euo pipefail
workspace="${1:?Usage: clone-workspace.sh /absolute/workspace/path}"
mkdir -p "$workspace"
for repo in design roku backend web android mediamp tauri-video-plugin video .github; do
  if [[ -e "$workspace/$repo" ]]; then
    git -C "$workspace/$repo" rev-parse --show-toplevel
    printf 'Keeping existing checkout: %s\n' "$repo"
  else
    gh repo clone "viptv-org/$repo" "$workspace/$repo"
  fi
done
printf 'For backend source work: git -C %q submodule update --init dashboard\n' "$workspace/backend"
printf 'Read design/DESIGN.md and each app AGENTS.md before editing.\n'
