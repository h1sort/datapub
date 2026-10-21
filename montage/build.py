#!/usr/bin/env python3
"""Rebuild montage/out/anteriormente.mp4 + poster.jpg from montage/cues.tsv.

stdlib only. Needs an ffmpeg with libass (brew install ffmpeg-full).
Usage: uv run python montage/build.py   (see make.sh)
"""
import csv, os, subprocess, sys, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src", "2023.mp4")
WORK = os.path.join(HERE, "work")
OUT = os.path.join(HERE, "out")
FFMPEG = os.environ.get("FFMPEG") or shutil.which("ffmpeg")
for cand in ("/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg",):
    if os.path.exists(cand):
        FFMPEG = cand
W, H, FPS = 1920, 1080, 30
TITLE = "Anteriormente en The Data Pub…"
SUB = "Julio 2023"
TITLE_SECS = 4.0
FONT = "Helvetica Neue"


def ts(s):
    p = [float(x) for x in s.split(":")]
    v = 0.0
    for x in p:
        v = v * 60 + x
    return v


def ass_time(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def run(cmd):
    print("+", " ".join(cmd), file=sys.stderr)
    subprocess.run(cmd, check=True)


def main():
    os.makedirs(WORK, exist_ok=True); os.makedirs(OUT, exist_ok=True)
    rows = list(csv.DictReader(open(os.path.join(HERE, "cues.tsv"), encoding="utf-8"), delimiter="\t"))
    vf = f"scale={W}:{H}:flags=lanczos,fps={FPS},format=yuv420p,setsar=1"
    parts = []
    # title card (silent audio)
    title = os.path.join(WORK, "p00-title.mp4")
    run([FFMPEG, "-y", "-loglevel", "error", "-f", "lavfi", "-i", f"color=c=black:s={W}x{H}:r={FPS}:d={TITLE_SECS}",
         "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", str(TITLE_SECS),
         "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", title])
    parts.append(title)
    events = []  # (start, end, text) on the output timeline
    t0 = TITLE_SECS
    for i, r in enumerate(rows, 1):
        a, b = ts(r["start"]), ts(r["end"]); d = b - a
        p = os.path.join(WORK, f"p{i:02d}.mp4")
        af = f"aresample=48000,afade=t=in:d=0.04,afade=t=out:st={d-0.06:.3f}:d=0.06"
        run([FFMPEG, "-y", "-loglevel", "error", "-ss", f"{a:.3f}", "-t", f"{d:.3f}", "-i", SRC,
             "-vf", vf, "-af", af, "-ac", "2", "-c:v", "libx264", "-crf", "18", "-c:a", "aac", "-b:a", "128k", p])
        parts.append(p)
        chunks = [c.strip() for c in r["caption"].split("//") if c.strip()]
        weights = [max(len(c), 12) for c in chunks]
        tot = sum(weights); cur = t0 + 0.15
        avail = d - 0.3
        for c, w in zip(chunks, weights):
            dur = avail * w / tot
            events.append((cur, cur + dur, c)); cur += dur
        t0 += d
    total = t0
    # ASS: captions + title
    ass = os.path.join(WORK, "montage.ass")
    with open(ass, "w", encoding="utf-8") as f:
        f.write(f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Cap,{FONT},50,&H00FFFFFF,&H00FFFFFF,&HA0000000,&H00000000,-1,0,0,0,100,100,0,0,3,12,0,2,60,60,16,1
Style: Title,{FONT},96,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,0,0,5,0,0,0,1
Style: Sub,{FONT},46,&H00B8B8B8,&H00B8B8B8,&H00000000,&H00000000,0,0,0,0,100,100,6,0,1,0,0,5,0,0,0,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
""")
        f.write(f"Dialogue: 0,{ass_time(0.2)},{ass_time(TITLE_SECS-0.3)},Title,,0,0,0,,{{\\pos({W//2},{H//2-30})\\fad(600,400)}}{TITLE}\n")
        f.write(f"Dialogue: 0,{ass_time(0.9)},{ass_time(TITLE_SECS-0.3)},Sub,,0,0,0,,{{\\pos({W//2},{H//2+60})\\fad(600,400)}}{SUB}\n")
        for s, e, c in events:
            f.write(f"Dialogue: 0,{ass_time(s)},{ass_time(e)},Cap,,0,0,0,,{c}\n")
    lst = os.path.join(WORK, "concat.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    joined = os.path.join(WORK, "joined.mp4")
    run([FFMPEG, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", joined])
    out = os.path.join(OUT, "anteriormente.mp4")
    run([FFMPEG, "-y", "-loglevel", "error", "-i", joined, "-vf", f"ass={ass}", "-c:v", "libx264", "-crf", "20",
         "-preset", "slow", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", out])
    run([FFMPEG, "-y", "-loglevel", "error", "-ss", "2.0", "-i", out, "-frames:v", "1", "-q:v", "2",
         os.path.join(OUT, "poster.jpg")])
    print(f"duration {total:.1f}s, {os.path.getsize(out)/1e6:.1f} MB -> {out}")


if __name__ == "__main__":
    main()
