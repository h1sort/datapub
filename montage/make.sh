#!/usr/bin/env bash
# Rebuild the "Anteriormente en The Data Pub…" recap (v2) from the 2023 recording.
#   montage/make.sh               cues.tsv + words.tsv -> out/anteriormente.mp4 + out/poster.jpg (+ fallback stills)
#   montage/make.sh --transcribe  first re-run word-level whisper on the cut clips -> work/words-raw.tsv
#                                 (use it after changing in/out points; then fold fixes into words.tsv)
# Needs: brew install ffmpeg-full (libass), montage/src/2023.mp4 (never committed), uv (score.py, --transcribe).
# Edit decisions: cues.tsv. Caption text/timing: words.tsv. Beat sheet: RECAP.md. Intermediates: work/v2/.
set -euo pipefail
cd "$(dirname "$0")"
[ -f src/2023.mp4 ] || { echo "missing montage/src/2023.mp4 (move assets/refs/DataPub-2023.mp4 there)"; exit 1; }
if [ "${1:-}" = "--transcribe" ]; then
  uv run --no-project --with mlx-whisper python captions.py transcribe
fi
python3 build.py
# music: original synthesized score (score.py), ducked under the speech; keeps the no-music cut in work/v2/
mv out/anteriormente.mp4 work/v2/nomusic.mp4
uv run --no-project --with numpy --with scipy python score.py work/v2/captions.ass work/v2/nomusic.mp4 out/anteriormente.mp4
bash stills.sh
