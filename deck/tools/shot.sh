#!/usr/bin/env bash
# Screenshot one slide/step of the deck at 1920×1080 with headless Chrome.
# Usage: deck/tools/shot.sh <slide (1-based) | @slide-id> [step=0] [out.png]
# Prints the PNG path, then any console errors/warnings from the page.
set -euo pipefail
DIR="$(cd "$(dirname "$0")/.." && pwd)"
slide=${1:?usage: shot.sh <slide> [step] [out.png]}; step=${2:-0}
name=${slide#@}; [[ $name =~ ^[0-9]+$ ]] && name=$(printf %02d "$name")
out=${3:-$DIR/.shots/s-$name-$step.png}
mkdir -p "$(dirname "$out")"
prof=$(mktemp -d); log=$(mktemp)
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars \
  --user-data-dir="$prof" --window-size=1920,1080 --force-device-scale-factor=1 --virtual-time-budget=5000 \
  --allow-file-access-from-files --enable-logging=stderr --v=0 \
  --screenshot="$out" "file://$DIR/index.html?shot#/$slide/$step" </dev/null >"$log" 2>&1 || true
rm -rf "$prof"
echo "$out"
grep -E 'CONSOLE|Uncaught|ERROR:.*(js|script)' "$log" | grep -vE 'dbus|gpu|GPU|viz|sandbox|Fontconfig|crashpad|google_apis|registration' || true
rm -f "$log"
