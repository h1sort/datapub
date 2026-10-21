#!/usr/bin/env python3
"""Build montage/out/anteriormente.mp4 (v2) + poster.jpg from cues.tsv + words.tsv.

stdlib only; needs an ffmpeg with libass (brew install ffmpeg-full) and the 2023
recording at montage/src/2023.mp4 (640x360: Carlos in a small panel on the left,
his slide on the right).

Pipeline (intermediates in montage/work/v2/):
  1. every shot of every clip is re-framed from the 640x360 source onto a 1920x1080
     "plate" (comp | face | slide | wide), then pushed/snapped with a sub-pixel zoom
     (perspective filter, evaluated per frame), graded and labelled;
  2. audio per clip with short fades, levelled per clip, plus 3 synthesized hits,
     then two-pass loudnorm to -16 LUFS;
  3. word-level ASS captions (captions.py) burned in on the final encode.

Usage: python3 montage/build.py   (see make.sh)
"""
import json, os, re, shutil, subprocess, sys, wave, array, math

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import captions as C  # noqa: E402

SRC = os.path.join(HERE, "src", "2023.mp4")
WORK = os.path.join(HERE, "work", "v2")
OUT = os.path.join(HERE, "out")
FFMPEG = os.environ.get("FFMPEG") or "/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg"
if not os.path.exists(FFMPEG):
    FFMPEG = shutil.which("ffmpeg")
FPS, W, H, SR = 30, 1920, 1080, 48000
MONO_TTF = "/System/Library/Fonts/Menlo.ttc"

# Source geometry (measured on the 2023 recording)
SLIDE = (163, 66, 476, 256)   # x, y, w, h of the slide inside the 640x360 frame
PANEL = (1, 165, 158, 106)    # Carlos's camera panel
# Composite layout on the 1920x1080 black stage
COMP_SLIDE = (624, 72, 1256, 676)
COMP_PANEL = (40, 72, 560, 376)


def run(cmd, **kw):
    print("+", " ".join(str(c) for c in cmd)[:300], file=sys.stderr)
    return subprocess.run(cmd, check=True, stdin=subprocess.DEVNULL, **kw)


def fr(sec):
    return int(round(sec * FPS))


def mmss(t):
    return f"{int(t // 60)}:{int(t % 60):02d}"


def dt_escape(s):
    return s.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")


# ------------------------------------------------------------------ shots
SHOT_RE = re.compile(r"^(?:(?P<t>\d+:\d+(?:\.\d+)?)\s+)?(?P<mode>comp|face|slide|wide)\s+(?P<z>[\d.]+(?:[>~][\d.]+)?)(?P<rest>.*)$")


def parse_shots(spec, src_in):
    shots = []
    for part in spec.split("|"):
        m = SHOT_RE.match(part.strip())
        if not m:
            raise SystemExit(f"bad shot spec: {part!r}")
        z = m.group("z")
        if ">" in z:
            a, b = z.split(">"); kind = "push"
        elif "~" in z:
            a, b = z.split("~"); kind = "snap"
        else:
            a = b = z; kind = "push"
        sh = {"t": C.ts(m.group("t")) if m.group("t") else src_in, "mode": m.group("mode"),
              "z0": float(a), "z1": float(b), "kind": kind, "cx": 0.5, "cy": 0.5, "fy": PANEL[1], "dx": 10}
        for tok in m.group("rest").split():
            if tok.startswith("@"):
                x, y = tok[1:].split(","); sh["cx"], sh["cy"] = float(x), float(y)
            elif tok.startswith("fy="):
                sh["fy"] = int(tok[3:])
            elif tok.startswith("dx="):
                sh["dx"] = int(tok[3:])
            elif tok.startswith("cap="):  # caption centre y for groups starting in this shot
                sh["cap"] = int(tok[4:])
        shots.append(sh)
    return shots


def zoom_filter(sh, dur):
    """Sub-pixel zoom: map a W/Z x H/Z viewport (centred at cx,cy, clamped to the plate)
    onto the full frame with the perspective filter, evaluated per frame."""
    a, b = sh["z0"], sh["z1"]
    if abs(a - 1) < 1e-6 and abs(b - 1) < 1e-6:
        return None
    t = f"(in/{FPS})"
    if sh["kind"] == "snap":
        Z = f"({b}+({a}-{b})*exp(-{t}/0.11))"
    else:
        Z = f"({a}+({b}-{a})*min({t}/{max(dur, 0.04):.4f},1))"
    L = f"clip({sh['cx']}*W-W/(2*{Z}),0,W-W/{Z})"
    T = f"clip({sh['cy']}*H-H/(2*{Z}),0,H-H/{Z})"
    R, B = f"({L}+W/{Z})", f"({T}+H/{Z})"
    return (f"perspective=x0='{L}':y0='{T}':x1='{R}':y1='{T}':x2='{L}':y2='{B}':x3='{R}':y3='{B}'"
            f":interpolation=cubic:eval=frame")


def shot_graph(sh, dur, src_t):
    pre = "[0:v]hqdn3d=1.5:1.5:4:4,setsar=1"
    label = f"THE DATA PUB · JULIO 2023 · ▶ {mmss(src_t)}"
    z = zoom_filter(sh, dur)
    zoom = f",{z}" if z else ""
    top_label = (f",drawtext=fontfile={MONO_TTF}:text='{dt_escape(label)}':x=40:y=36:fontsize=26"
                 f":fontcolor=white@0.92:box=1:boxcolor=black@0.62:boxborderw=10")
    if sh["mode"] == "comp":
        sx, sy, sw, sh_ = COMP_SLIDE; px, py, pw, ph = COMP_PANEL
        g = (f"{pre},split[a][b];"
             f"[a]crop={SLIDE[2]}:{SLIDE[3]}:{SLIDE[0]}:{SLIDE[1]},scale={sw}:{sh_}:flags=lanczos[sl];"
             f"[b]crop={PANEL[2]}:{PANEL[3]}:{PANEL[0]}:{PANEL[1]},scale={pw}:{ph}:flags=lanczos[fc];"
             f"[sl]pad={W}:{H}:{sx}:{sy}:black[t1];[t1][fc]overlay={px}:{py},"
             f"drawbox=x={sx - 2}:y={sy - 2}:w={sw + 4}:h={sh_ + 4}:color=white@0.35:t=2,"
             f"drawbox=x={px - 2}:y={py - 2}:w={pw + 4}:h={ph + 4}:color=white@0.35:t=2"
             f"{zoom},eq=saturation=0.92:contrast=1.03,unsharp=5:5:0.5,"
             # labels after the (small, centred) push so they never get cropped
             f"drawtext=fontfile={MONO_TTF}:text='THE DATA PUB':x={px}:y={py + ph + 26}:fontsize=28:fontcolor=0xd6d6d6,"
             f"drawtext=fontfile={MONO_TTF}:text='JULIO 2023':x={px}:y={py + ph + 66}:fontsize=28:fontcolor=0xf5c542,"
             f"drawtext=fontfile={MONO_TTF}:text='{dt_escape('▶ ' + mmss(src_t))}':x={px}:y={py + ph + 106}:fontsize=28:fontcolor=0xa3a3a3[v]")
    elif sh["mode"] == "face":
        cw = PANEL[2]; ch = round(cw * 9 / 16)
        g = (f"{pre},crop={cw}:{ch}:{PANEL[0]}:{sh['fy']},scale={W}:{H}:flags=lanczos{zoom},"
             f"eq=saturation=0.9:contrast=1.06,unsharp=7:7:0.7,noise=alls=5:allf=t{top_label}[v]")
    elif sh["mode"] == "slide":
        cw = 455
        g = (f"{pre},crop={cw}:{SLIDE[3]}:{SLIDE[0] + sh['dx']}:{SLIDE[1]},scale={W}:{H}:flags=lanczos{zoom},"
             f"eq=saturation=0.92:contrast=1.03,unsharp=5:5:0.6{top_label}[v]")
    else:  # wide: the original layout
        g = f"{pre},scale={W}:{H}:flags=lanczos{zoom},unsharp=5:5:0.5[v]"
    return g


def render_shot(path, src_t, nframes, sh):
    gfile = path + ".graph"
    open(gfile, "w", encoding="utf-8").write(shot_graph(sh, nframes / FPS, src_t))
    run([FFMPEG, "-nostdin", "-v", "error", "-y", "-ss", f"{src_t:.4f}", "-i", SRC,
         "-/filter_complex", gfile, "-map", "[v]", "-frames:v", str(nframes), "-r", str(FPS),
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "12", "-pix_fmt", "yuv420p", "-an", path])


def render_black(path, nframes):
    run([FFMPEG, "-nostdin", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=black:s={W}x{H}:r={FPS}",
         "-frames:v", str(nframes), "-c:v", "libx264", "-preset", "veryfast", "-crf", "12", "-pix_fmt", "yuv420p", path])


# ------------------------------------------------------------------ audio
def wav_read(path):
    with wave.open(path) as w:
        assert w.getframerate() == SR and w.getnchannels() == 2 and w.getsampwidth() == 2
        a = array.array("h"); a.frombytes(w.readframes(w.getnframes()))
    return a


def wav_write(path, a):
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(a.tobytes())


def loudness(path):
    p = subprocess.run([FFMPEG, "-nostdin", "-hide_banner", "-i", path, "-af",
                        "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True, stdin=subprocess.DEVNULL)
    return json.loads(p.stderr[p.stderr.rindex("{"):p.stderr.rindex("}") + 1])


def clip_audio(path, src_in, nframes):
    d = nframes / FPS
    tmp = path + ".raw.wav"
    run([FFMPEG, "-nostdin", "-v", "error", "-y", "-ss", f"{src_in:.4f}", "-t", f"{d:.4f}", "-i", SRC, "-vn",
         "-af", f"aresample={SR},highpass=f=70,afade=t=in:st=0:d=0.015,afade=t=out:st={d - 0.035:.4f}:d=0.035",
         "-ac", "2", "-c:a", "pcm_s16le", tmp])
    # level each clip to roughly the same loudness (Q&A mic is much quieter than the talk)
    li = float(loudness(tmp)["input_i"])
    gain = max(-12.0, min(12.0, -20.0 - li)) if li > -70 else 0.0
    a = wav_read(tmp)
    k = 10 ** (gain / 20)
    a = array.array("h", (max(-32768, min(32767, int(s * k))) for s in a))
    n = nframes * (SR // FPS) * 2
    a = a[:n] + array.array("h", [0] * max(0, n - len(a)))
    os.remove(tmp)
    return a, li, gain


def parse_hit(s):
    """'hit@43:10.80:-14' -> ('43:10.80', -14.0); the dB part needs an explicit sign."""
    parts = s[4:].split(":")
    db = -10.0
    if len(parts) > 1 and parts[-1][:1] in "+-":
        db = float(parts.pop())
    return ":".join(parts), db


def make_hit(path):
    """A short low thump + noise tick, synthesized (no downloaded SFX)."""
    run([FFMPEG, "-nostdin", "-v", "error", "-y", "-f", "lavfi", "-i",
         "aevalsrc='0.85*sin(2*PI*t*(40+95*exp(-t*15)))*exp(-t*5.5)+0.22*(2*random(0)-1)*exp(-t*28)':d=1.1:s=48000",
         "-af", "lowpass=f=1600,afade=t=out:st=0.75:d=0.35", "-ac", "2", "-c:a", "pcm_s16le", path])
    return wav_read(path)


# ------------------------------------------------------------------ main
def main():
    os.makedirs(WORK, exist_ok=True); os.makedirs(OUT, exist_ok=True)
    cues = C.read_cues()
    words = C.read_words(os.path.join(HERE, "words.tsv"))
    timeline, cards, parts, hits = [], [], [], []
    audio = array.array("h")
    t_out = 0  # frames
    for i, r in enumerate(cues):
        tag = f"{i:02d}-{r['id']}"
        sfx = [s for s in r.get("sfx", "").split() if s.startswith("hit@")]
        if r["in"] == "card":
            n = fr(float(r["out"]))
            card = dict(kv.split("=", 1) for kv in r["shots"].split(";"))
            card["accent"] = card.get("accent") == "1"
            if "size" in card: card["size"] = int(card["size"])
            p = os.path.join(WORK, f"{tag}.mp4"); render_black(p, n); parts.append(p)
            cards.append((card, t_out / FPS, n / FPS))
            for s in sfx:
                at, db = parse_hit(s); hits.append((t_out / FPS + C.ts(at), db))
            audio.extend(array.array("h", [0] * (n * (SR // FPS) * 2)))
            print(f"{tag:>14} card {n / FPS:5.2f}s @ {t_out / FPS:6.2f}", file=sys.stderr)
            t_out += n
            continue
        a, b = C.ts(r["in"]), C.ts(r["out"])
        n = fr(b - a)
        shots = parse_shots(r["shots"], a)
        bounds = [max(0, min(n, fr(sh["t"] - a))) for sh in shots] + [n]
        for k, sh in enumerate(shots):
            f0, f1 = bounds[k], bounds[k + 1]
            if f1 <= f0:
                continue
            p = os.path.join(WORK, f"{tag}-{k}.mp4")
            render_shot(p, a + f0 / FPS, f1 - f0, sh)
            parts.append(p)
        clip, li, gain = clip_audio(os.path.join(WORK, f"{tag}.wav"), a, n)
        audio.extend(clip)
        for s in sfx:
            at, db = parse_hit(s); hits.append((t_out / FPS + C.ts(at) - a, db))
        caps = [(t_out / FPS + bounds[k] / FPS, sh.get("cap")) for k, sh in enumerate(shots)]
        timeline.append({"id": r["id"], "src_in": a, "src_out": a + n / FPS, "out_start": t_out / FPS, "caps": caps})
        print(f"{tag:>14} {n / FPS:5.2f}s @ {t_out / FPS:6.2f}  {len(shots)} shot(s)  {li:6.1f} LUFS {gain:+5.1f} dB",
              file=sys.stderr)
        t_out += n
    total = t_out / FPS

    # hits
    hit = make_hit(os.path.join(WORK, "hit.wav"))
    for at, db in hits:
        k = 10 ** (db / 20); o = int(round(at * SR)) * 2
        for j, s in enumerate(hit):
            if 0 <= o + j < len(audio):
                audio[o + j] = max(-32768, min(32767, audio[o + j] + int(s * k)))
    mix = os.path.join(WORK, "mix.wav"); wav_write(mix, audio)
    m = loudness(mix)
    final_wav = os.path.join(WORK, "final.wav")
    run([FFMPEG, "-nostdin", "-v", "error", "-y", "-i", mix, "-af",
         f"loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}"
         f":measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}"
         f":linear=true,aresample={SR}", "-c:a", "pcm_s16le", final_wav])

    # captions
    ass = os.path.join(WORK, "captions.ass")
    open(ass, "w", encoding="utf-8").write(C.ass_document(words, timeline, cards))

    # join + final encode
    lst = os.path.join(WORK, "concat.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    joined = os.path.join(WORK, "joined.mp4")
    run([FFMPEG, "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", joined])
    out = os.path.join(OUT, "anteriormente.mp4")
    run([FFMPEG, "-nostdin", "-v", "error", "-y", "-i", joined, "-i", final_wav,
         "-vf", f"ass={ass}", "-map", "0:v", "-map", "1:a",
         "-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-crf", "19",
         "-maxrate", "2400k", "-bufsize", "4800k", "-pix_fmt", "yuv420p", "-r", str(FPS),
         "-c:a", "aac", "-b:a", "160k", "-ar", str(SR), "-movflags", "+faststart", "-shortest", out])
    poster = os.path.join(OUT, "poster.jpg")
    run([FFMPEG, "-nostdin", "-v", "error", "-y", "-i", out, "-frames:v", "1", "-q:v", "2", "-update", "1", poster])
    print(f"duration {total:.2f}s, {os.path.getsize(out) / 1e6:.1f} MB -> {out}")


if __name__ == "__main__":
    main()
