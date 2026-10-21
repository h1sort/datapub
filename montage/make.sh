#!/usr/bin/env bash
# Rebuild the montage from montage/cues.tsv. Needs: brew install ffmpeg-full (libass), montage/src/2023.mp4.
# Transcript (optional, for finding cues): see notes-2023.md "How the cues were found".
set -euo pipefail
cd "$(dirname "$0")"
[ -f src/2023.mp4 ] || { echo "missing montage/src/2023.mp4 (move assets/refs/DataPub-2023.mp4 there)"; exit 1; }
python3 build.py
bash stills.sh
