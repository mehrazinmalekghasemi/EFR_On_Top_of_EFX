#!/usr/bin/env bash
# Linux / GNU coreutils. Search for six days; reserve up to one day for replay.
# Hard limit: timeout + kill grace <= 604800 seconds (one week).
set -euo pipefail
cd -- "$(dirname -- "$0")"
workers="${1:-32}"
run_dir="${2:-week-run}"
if ! command -v timeout >/dev/null 2>&1; then
  echo 'GNU timeout is required for this hard-deadline wrapper. See README for portable commands.' >&2
  exit 1
fi
timeout --signal=TERM --kill-after=10s 604790s bash -c '
  set -e
  python3 search.py --goal extension --workers "$1" --hours 144 --out "$2"
  python3 verify.py "$2" --workers "$1" --hours 24 --timeout 120
' bash "$workers" "$run_dir"
