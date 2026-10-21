#!/usr/bin/env python3
"""Word-level captions for the "Anteriormente…" recap.

Two jobs:

1. `transcribe` (run once, needs mlx-whisper via uv):
       uv run --no-project --with mlx-whisper python montage/captions.py transcribe
   Cuts each clip in cues.tsv out of the source audio exactly as the edit uses it,
   transcribes it with word timestamps (Spanish, no conditioning on previous text,
   which avoids hallucinations) and writes work/words-raw.tsv. That is the starting
   point for montage/words.tsv, the hand-corrected file the build actually reads
   (names fixed: DuckDB, Riggan, Shiner, Snowflake…, group breaks and slams marked).
   It also prints each clip's text so first/last words can be checked for clipping.

2. `ass_document(...)` (stdlib only, imported by build.py): turns words.tsv + the
   edit timeline into an ASS file with influencer-style captions: 1–4 words on
   screen, upcoming words reserved but invisible (stable layout), the active word
   in amber #f5c542 with a pop, and occasional single-word "slams".

words.tsv columns: clip, start, end, word, mark
  start/end   absolute times in the 2023 source (seconds)
  mark ""     word continues the current caption group
       "/"    word starts a new group
       "*"    word starts a SLAM group (big amber); following "+" words join it
"""
import csv, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "work")
SRC = os.path.join(HERE, "src", "2023.mp4")
FFMPEG = "/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg"
if not os.path.exists(FFMPEG):
    FFMPEG = "ffmpeg"

AMBER = "&H0042C5F5&"     # #f5c542 in ASS BGR
WHITE = "&H00FFFFFF&"
CAP_FONT = "Avenir Next Condensed Heavy"   # one unambiguous face on every Mac
MONO_FONT = "Menlo"
CARD_FONT = "Avenir Next Condensed Heavy"


# ---------------------------------------------------------------- helpers
def ts(s):
    """'43:06.55' or '2586.55' -> seconds."""
    v = 0.0
    for p in str(s).strip().split(":"):
        v = v * 60 + float(p)
    return v


def ass_time(t):
    t = max(0.0, t)
    cs = int(round(t * 100))
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def read_cues(path=os.path.join(HERE, "cues.tsv")):
    rows = []
    with open(path, encoding="utf-8") as f:
        lines = [l for l in f if l.strip() and not l.startswith("#")]
    for r in csv.DictReader(lines, delimiter="\t"):
        rows.append({k: (v or "").strip() for k, v in r.items()})
    return rows


def read_words(path):
    out = []
    with open(path, encoding="utf-8") as f:
        lines = [l for l in f if l.strip() and not l.startswith("#")]
    for r in csv.DictReader(lines, delimiter="\t"):
        out.append({"clip": r["clip"], "start": float(r["start"]), "end": float(r["end"]),
                    "word": r["word"], "mark": (r.get("mark") or "").strip()})
    return out


# ---------------------------------------------------------------- transcribe
def transcribe():
    import mlx_whisper  # uv run --no-project --with mlx-whisper ...
    os.makedirs(os.path.join(WORK, "clipwav"), exist_ok=True)
    rows = [r for r in read_cues() if r["in"] != "card"]
    out = open(os.path.join(WORK, "words-raw.tsv"), "w", encoding="utf-8")
    out.write("clip\tstart\tend\tword\tmark\n")
    for r in rows:
        a, b = ts(r["in"]), ts(r["out"])
        wav = os.path.join(WORK, "clipwav", f"{r['id']}.wav")
        subprocess.run([FFMPEG, "-nostdin", "-v", "error", "-y", "-ss", f"{a:.3f}", "-t", f"{b - a:.3f}",
                        "-i", SRC, "-vn", "-ac", "1", "-ar", "16000", wav], check=True, stdin=subprocess.DEVNULL)
        res = mlx_whisper.transcribe(wav, path_or_hf_repo="mlx-community/whisper-large-v3-turbo",
                                     language="es", word_timestamps=True, condition_on_previous_text=False)
        words = [w for s in res["segments"] for w in s.get("words", [])]
        print(f"{r['id']:>10} [{a:.2f}-{b:.2f}] " + " ".join(w["word"].strip() for w in words))
        for i, w in enumerate(words):
            out.write(f"{r['id']}\t{a + w['start']:.3f}\t{a + w['end']:.3f}\t{w['word'].strip()}\t{'/' if i == 0 else ''}\n")
    out.close()
    print("->", os.path.join(WORK, "words-raw.tsv"))


# ---------------------------------------------------------------- ASS
HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Cap,{cap},118,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,1,0,1,7,5,5,40,40,0,1
Style: Slam,{cap},200,{amber},&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,2,0,1,10,7,5,40,40,0,1
Style: Card,{card},150,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,0,0,5,0,0,0,1
Style: Mono,{mono},40,&H00D6D6D6,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,8,0,1,0,0,5,0,0,0,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
""".format(cap=CAP_FONT, card=CARD_FONT, mono=MONO_FONT, amber=AMBER)


def esc(s):
    return s.replace("{", "(").replace("}", ")").replace("\\", "/")


def groups_for(words):
    """Split one clip's words into caption groups using the marks."""
    gs = []
    for w in words:
        m = w["mark"]
        if not gs or m in ("/", "*"):
            gs.append({"slam": m == "*", "words": [w]})
        elif m == "+" or not gs[-1]["slam"]:
            gs[-1]["words"].append(w)
        else:  # plain word after a slam group: start a new normal group
            gs.append({"slam": False, "words": [w]})
    return gs


def caption_events(words, timeline, cap_pos=(960, 905), slam_pos=(960, 880)):
    """timeline: list of dicts {id, src_in, src_out, out_start} for footage clips.
    Returns ASS Dialogue lines (strings)."""
    lines = []
    by_clip = {}
    for w in words:
        by_clip.setdefault(w["clip"], []).append(w)
    for seg in timeline:
        ws = sorted(by_clip.get(seg["id"], []), key=lambda w: w["start"])
        if not ws:
            continue
        off = seg["out_start"] - seg["src_in"]
        clip_end = seg["out_start"] + (seg["src_out"] - seg["src_in"])
        gs = groups_for(ws)
        for gi, g in enumerate(gs):
            gw = g["words"]
            g_start = max(seg["out_start"], gw[0]["start"] + off - 0.04, 0.15)  # frame 0 = clean poster
            # per-shot override (cap=Y in cues.tsv) when a framing puts something to read low in frame
            y = None
            for t0, cy in seg.get("caps", []):
                if t0 <= g_start + 0.01:
                    y = cy
            pos = (cap_pos[0], y) if y else cap_pos
            spos = (slam_pos[0], y) if y else slam_pos
            nxt = gs[gi + 1]["words"][0]["start"] + off - 0.04 if gi + 1 < len(gs) else None
            g_end = gw[-1]["end"] + off + (0.45 if g["slam"] else 0.30)
            if nxt is not None:
                g_end = min(max(g_end, gw[-1]["end"] + off), nxt)
            g_end = min(g_end, clip_end - 0.01)
            if g["slam"]:
                txt = " ".join(esc(w["word"]).upper() for w in gw).rstrip(".,;:")
                tag = (f"{{\\pos({spos[0]},{spos[1]})\\fscx165\\fscy165\\frz-2"
                       f"\\t(0,130,\\fscx100\\fscy100\\frz0)}}")
                lines.append(f"Dialogue: 2,{ass_time(g_start)},{ass_time(g_end)},Slam,,0,0,0,,{tag}{txt}")
                continue
            # one event per active word; upcoming words keep their space but are invisible
            for i, w in enumerate(gw):
                s = g_start if i == 0 else max(g_start, w["start"] + off - 0.03)
                e = g_end if i == len(gw) - 1 else max(s + 0.02, gw[i + 1]["start"] + off - 0.03)
                parts = []
                for j, u in enumerate(gw):
                    t = esc(u["word"]).upper()
                    if j < i:
                        parts.append(f"{{\\c{WHITE}\\alpha&H00&}}{t}")
                    elif j == i:
                        parts.append(f"{{\\c{AMBER}\\alpha&H00&\\fscx116\\fscy116\\t(0,110,\\fscx100\\fscy100)}}{t}"
                                     f"{{\\fscx100\\fscy100}}")
                    else:
                        parts.append(f"{{\\c{WHITE}\\alpha&HFF&}}{t}")
                body = " ".join(parts)
                lines.append(f"Dialogue: 1,{ass_time(s)},{ass_time(e)},Cap,,0,0,0,,{{\\pos({pos[0]},{pos[1]})}}{body}")
    return lines


def card_events(card, t0, dur):
    """Full-screen black text cards. 2023 framing uses mono + heavy sans; the 2026
    framing cards are sentence case with an explicit 'OCTUBRE 2026' label so they
    can never be mistaken for something said in 2023."""
    E = []
    a, b = ass_time(t0), ass_time(t0 + dur)
    kind = card["kind"]
    if kind == "stamp":
        E.append(f"Dialogue: 3,{ass_time(t0 + 0.05)},{b},Mono,,0,0,0,,{{\\pos(960,430)\\fad(120,0)}}ANTERIORMENTE EN")
        E.append(f"Dialogue: 3,{a},{b},Card,,0,0,0,,{{\\pos(960,545)\\fs190\\fscx120\\fscy120\\t(0,160,\\fscx100\\fscy100)}}THE DATA PUB")
        E.append(f"Dialogue: 3,{ass_time(t0 + 0.25)},{b},Mono,,0,0,0,,{{\\pos(960,670)\\c{AMBER}\\fs46\\fad(150,0)}}JULIO 2023")
    elif kind == "q2026":
        E.append(f"Dialogue: 3,{a},{b},Mono,,0,0,0,,{{\\pos(960,400)\\c{AMBER}\\fs36\\fad(150,0)}}THE DATA PUB · OCTUBRE 2026")
        col = AMBER if card.get("accent") else WHITE
        E.append(f"Dialogue: 3,{a},{b},Card,,0,0,0,,{{\\pos(960,545)\\c{col}\\fs{card.get('size', 150)}"
                 f"\\fscx112\\fscy112\\t(0,180,\\fscx100\\fscy100)\\fad(90,0)}}{card['text']}")
    return E


def ass_document(words, timeline, cards):
    """cards: list of (card_dict, out_start, dur)."""
    body = caption_events(words, timeline)
    for c, t0, d in cards:
        body += card_events(c, t0, d)
    return HEADER + "\n".join(body) + "\n"


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "transcribe":
        transcribe()
    else:
        print(__doc__)
