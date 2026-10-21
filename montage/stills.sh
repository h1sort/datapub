#!/usr/bin/env bash
# Export the six fallback stills (1920 wide JPEG) from the 2023 recording into assets/2023/stills/.
set -euo pipefail
cd "$(dirname "$0")"
FF=${FFMPEG:-$(command -v /opt/homebrew/opt/ffmpeg-full/bin/ffmpeg || command -v ffmpeg)}
OUT=../assets/2023/stills; mkdir -p "$OUT"
S=src/2023.mp4
frame() { "$FF" -y -loglevel error -ss "$1" -i "$S" -frames:v 1 -vf "scale=1920:-2:flags=lanczos" -q:v 3 "$OUT/$2"; }
frame 2640 00-escenario.jpg   # 44:00 Carlos on stage, mic in hand
frame 232  01-birdman.jpg     # 3:52 title slide: Birdman + "o la virtud inesperada de la ignorancia"
frame 1312 02-nokia.jpg       # 21:52 Nokia N95 5MP / iPhone 2MP
frame 1058 04-anadirle.jpg    # 17:38 minimal example: A 0.5 días, B 3 meses 5+ personas
frame 2595 05-marketing.jpg   # 43:15 MARKETING stamp
# 03: Hadoop -> Spark -> DuckDB, three slide crops (slide area of the composite = 478x268 at 162,60)
crop() { "$FF" -y -loglevel error -ss "$1" -i "$S" -frames:v 1 -vf "crop=478:258:162:63,scale=600:324:flags=lanczos" "work/c$2.png"; }
mkdir -p work
crop 1996 1; crop 2004 2; crop 662 3
"$FF" -y -loglevel error -i work/c1.png -i work/c2.png -i work/c3.png -filter_complex \
 "color=c=black:s=1920x1080[bg];[bg][0:v]overlay=0:378[a];[a][1:v]overlay=660:378[b];[b][2:v]overlay=1320:378[c];\
[c]drawtext=text='→':fontfile=/System/Library/Fonts/Supplemental/Arial.ttf:fontcolor=white:fontsize=64:x=600+(60-text_w)/2:y=540-text_h/2,\
drawtext=text='→':fontfile=/System/Library/Fonts/Supplemental/Arial.ttf:fontcolor=white:fontsize=64:x=1260+(60-text_w)/2:y=540-text_h/2" \
 -frames:v 1 -q:v 3 "$OUT/03-retadores.jpg"
ls -la "$OUT"
