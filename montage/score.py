#!/usr/bin/env python3
"""Solo jazz-drum score for the recap, in the spirit of Antonio Sánchez's
Birdman score (the 2023 talk was built on Birdman). Synthesized here, so no
licensed audio and no Content ID on the stream; mixed under the speech with ducking.

  uv run --no-project --with numpy --with scipy python score.py \
      work/v2/captions.ass work/v2/nomusic.mp4 out/anteriormente.mp4

Everything is placed from captions.ass, so a re-cut stays in sync:
  silence under the hook -> kick + crash on the "THE DATA PUB" stamp card
  swung ride + hi-hat on 2 and 4 + loose snare comping, busier act by act
  a tom fill into every Slam word, crash + kick on the word
  the tempo stretches between anchors so each hit lands on its word, like a
  drummer playing to picture
  cliffhanger: lone hi-hat, snare roll into 40 AÑOS, silence on "Tres años
  después", cymbal swell and a last hit on "¿Sigue siendo cierto?" that rings out
"""
import json, re, subprocess, sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, fftconvolve, sosfilt

FFMPEG = "/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg"
SR = 48000
TEMPO = 150                          # nominal BPM; each segment stretches to land on its anchor
SWING = 2 / 3                        # swung 8th sits 2/3 into the beat
MUSIC_LUFS = -19                     # score level before ducking; speech sits at -16
DUCK = "threshold=0.02:ratio=5:attack=15:release=380:knee=3"  # ~15 dB under the voice, full in the gaps
rng = np.random.default_rng(2026)


# ------------------------------------------------------------------ timeline
def ass_events(path):
    out = []
    for line in open(path, encoding="utf-8"):
        if not line.startswith("Dialogue:"):
            continue
        f = line.split(",", 9)
        h, m, s = f[1].split(":")
        out.append((int(h) * 3600 + int(m) * 60 + float(s), f[3], re.sub(r"\{[^}]*\}", "", f[9]).strip()))
    return out


def duration(path):
    r = subprocess.run(["/opt/homebrew/opt/ffmpeg-full/bin/ffprobe", "-v", "error", "-show_entries",
                        "format=duration", "-of", "csv=p=0", path], capture_output=True, text=True, check=True)
    return float(r.stdout)


# ------------------------------------------------------------------ the kit
def t_axis(sec): return np.arange(int(sec * SR)) / SR
def hp(x, fc, order=2): return sosfilt(butter(order, fc, "high", fs=SR, output="sos"), x)
def lp(x, fc, order=2): return sosfilt(butter(order, fc, "low", fs=SR, output="sos"), x)
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], "band", fs=SR, output="sos"), x)


def metal(sec, lo, hi, decay, seed_shift=1.0):
    """Cymbal tone: inharmonic square partials (the classic 808 ratios) plus noise."""
    t = t_axis(sec)
    x = sum(np.sign(np.sin(2 * np.pi * f * seed_shift * t + rng.random() * 6.28))
            for f in (205.3, 304.4, 369.6, 522.7, 540.0, 800.0)) / 6
    x = 0.65 * x + 0.35 * rng.standard_normal(len(t))
    return bp(x, lo, hi) * np.exp(-t / decay)


KIT = {}
def build_kit():
    t = t_axis(1.6)
    ping = np.sin(2 * np.pi * 4100 * t) * np.exp(-t / 0.05) * 0.25
    KIT["ride"] = metal(1.6, 3000, 11000, 0.55) + ping[: int(1.6 * SR)]
    KIT["ride_bell"] = metal(1.6, 1800, 8000, 0.7, 1.33) * 1.2 + ping[: int(1.6 * SR)] * 2
    KIT["chick"] = hp(metal(0.12, 5000, 14000, 0.025), 6000)
    KIT["hat_open"] = metal(0.5, 5000, 14000, 0.16)
    KIT["crash"] = metal(3.2, 2200, 13000, 1.1, 1.17) * 1.4
    tk = t_axis(0.45)
    f = 52 + 70 * np.exp(-tk / 0.025)
    KIT["kick"] = np.tanh(2 * (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tk / 0.16)
                               + lp(rng.standard_normal(len(tk)), 3000) * np.exp(-tk / 0.004) * 0.4))
    ts = t_axis(0.35)
    body = (np.sin(2 * np.pi * 190 * ts) + 0.6 * np.sin(2 * np.pi * 330 * ts)) * np.exp(-ts / 0.06)
    wires = bp(rng.standard_normal(len(ts)), 1500, 9000) * np.exp(-ts / 0.13)
    KIT["snare"] = np.tanh(1.5 * (0.6 * body + wires))
    rim = t_axis(0.08)
    KIT["rim"] = bp(rng.standard_normal(len(rim)), 1800, 6000) * np.exp(-rim / 0.012) \
        + np.sin(2 * np.pi * 1700 * rim) * np.exp(-rim / 0.01)
    for name, f0, dec in (("tom_hi", 210, 0.3), ("tom_mid", 150, 0.38), ("tom_floor", 98, 0.55)):
        tt = t_axis(dec * 4)
        f = f0 * (1 + 0.25 * np.exp(-tt / 0.03))
        KIT[name] = np.tanh(1.6 * (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / dec)
                                    + bp(rng.standard_normal(len(tt)), 400, 5000) * np.exp(-tt / 0.02) * 0.3))
    KIT["swell"] = metal(3.0, 2500, 12000, 99) * np.linspace(0, 1, int(3.0 * SR)) ** 2.2  # mallet roll on a cymbal


PAN = {"ride": 0.45, "ride_bell": 0.45, "chick": -0.4, "hat_open": -0.4, "crash": -0.25, "kick": 0,
       "snare": -0.08, "rim": -0.08, "tom_hi": -0.2, "tom_mid": 0.15, "tom_floor": 0.35, "swell": 0.3}


def hit(bus, t0, name, vel=1.0, jitter=0.006):
    t0 += rng.normal(0, jitter)
    vel *= 1 + rng.normal(0, 0.1)
    i = int(max(0, t0) * SR)
    if i >= bus.shape[1]:
        return
    sig = KIT[name][: bus.shape[1] - i] * vel
    a = (PAN[name] + 1) * np.pi / 4
    bus[0, i:i + len(sig)] += sig * np.cos(a)
    bus[1, i:i + len(sig)] += sig * np.sin(a)


def room_ir(sec=0.9):
    t = t_axis(sec)
    ir = np.stack([lp(rng.standard_normal(len(t)), 7000) * np.exp(-t / 0.18) for _ in range(2)])
    ir[:, 0] = 0
    return ir / np.abs(ir).sum(axis=1, keepdims=True).max() * 12


# ------------------------------------------------------------------ the drummer
def groove(bus, a, b, busy_at, end_fill=True):
    """Swing time from a to b, stretched so b lands on a downbeat. busy_at(t) -> 0..1."""
    beats = max(1, round((b - a) / (60 / TEMPO)))
    beat = (b - a) / beats
    fill_from = beats - (2 if beats >= 6 else 1) if end_fill else beats
    for k in range(beats):
        t = a + k * beat
        if k >= fill_from:                                   # fill into the anchor: triplets around the kit
            seq = ["tom_hi", "tom_hi", "tom_mid", "tom_mid", "tom_floor", "tom_floor"]  # toms: below the voice band
            for j in range(3):
                n = seq[min(len(seq) - 1, (k - fill_from) * 3 + j)]
                hit(bus, t + j * beat / 3, n, 0.4 + 0.25 * j / 2)
            continue
        busy = busy_at(t)
        if k % 16 == 15 and k < fill_from - 4:                 # pickup every 4 bars in long stretches
            hit(bus, t + SWING * beat, "snare", 0.4); hit(bus, t + SWING * beat, "tom_mid", 0.35 * busy)
        hit(bus, t, "ride", 0.55 if k % 2 == 0 else 0.42)     # ding
        if k % 2 == 1:
            hit(bus, t, "chick", 0.5)                        # hi-hat on 2 and 4
            hit(bus, t + SWING * beat, "ride", 0.33)         # the swung "a"
        hit(bus, t, "kick", 0.12)                            # feathered kick
        r = rng.random()                                     # comping on the swung 8th or the beat
        if r < 0.10 * busy:
            hit(bus, t + SWING * beat, "snare", 0.55)
        elif r < 0.45 * busy:
            hit(bus, t + SWING * beat, "snare", 0.14)        # ghost note
        if rng.random() < 0.05 * busy:
            hit(bus, t, "kick", 0.7)                         # a bomb
        if rng.random() < 0.04 * busy:
            hit(bus, t, "rim", 0.35)


def compose(events, dur):
    build_kit()
    slams = [(t, x) for t, s, x in events if s == "Slam"]
    cards = sorted({round(t, 2) for t, s, _ in events if s == "Card"})
    stamp, tres, cierto = cards[0], cards[-2], cards[-1]
    t_40 = slams[-1][0]
    t_triunfar = next(t for t, x in slams if "TRIUNF" in x)
    t_jug = next(t for t, x in slams if "JUGUETE" in x)
    t_meses = next(t for t, x in slams if "MESES" in x)

    bus = np.zeros((2, int((dur + 4) * SR)))

    # silence under the hook (MARKETING lands dry); the drums enter on the stamp card
    hit(bus, stamp, "kick", 1.0, 0); hit(bus, stamp, "crash", 0.9, 0)

    # time from the stamp to TRIUNFAR, anchored on every slam word in between
    anchors = [stamp + 1.8] + [t for t, _ in slams if stamp + 2 < t < t_triunfar] + [t_triunfar]
    hit(bus, anchors[0], "ride_bell", 0.6, 0)
    for a, b in zip(anchors, anchors[1:]):
        groove(bus, a, b, lambda x: float(np.interp(x, [stamp, t_jug, t_meses, t_triunfar], [0.2, 0.55, 0.85, 1.0])))
        heavy = not any(abs(b - t) < 0.01 and "5 MIN" in x for t, x in slams)
        hit(bus, b, "kick", 1.0 if heavy else 0.7, 0)
        hit(bus, b, "crash" if heavy else "snare", 0.8 if heavy else 0.6, 0)

    # TRIUNFAR: the biggest crash, then the floor drops out
    hit(bus, t_triunfar, "crash", 1.0, 0); hit(bus, t_triunfar + 0.02, "tom_floor", 0.8, 0)

    # cliffhanger: a lone hi-hat like a clock, then a floor-tom rumble + cymbal swell into 40 AÑOS
    # (a snare roll would sit on "no ha cambiado en 40 años"; toms and cymbal leave the voice band free)
    roll_start = t_40 - 3.0
    t = t_triunfar + 2.2
    while t < roll_start:
        hit(bus, t, "chick", 0.45)
        t += 60 / 132
    n = int(3.0 / 0.05)
    for j in range(n):
        x = j / n
        hit(bus, roll_start + j * 0.05, "tom_floor", 0.06 + 0.6 * x ** 2.2, 0.003)
    hit(bus, t_40 - 3.0, "swell", 0.3, 0)
    hit(bus, t_40, "kick", 1.0, 0); hit(bus, t_40, "crash", 1.0, 0); hit(bus, t_40, "tom_floor", 0.9, 0)

    # "Tres años después" in silence; a cymbal swell into "¿Sigue siendo cierto?", one last hit
    hit(bus, cierto - 3.0, "swell", 0.35, 0)
    hit(bus, cierto, "kick", 1.0, 0); hit(bus, cierto, "crash", 1.0, 0); hit(bus, cierto, "rim", 0.7, 0)

    ir = room_ir()
    room = np.stack([fftconvolve(bus[c], ir[c])[: bus.shape[1]] for c in range(2)])
    out = (bus + 0.3 * room)[:, : int(dur * SR)]
    out *= np.minimum(1, (dur - t_axis(dur)) / 0.6)          # last 0.6 s fades out
    out = np.tanh(out / max(1e-9, np.abs(out).max()) * 1.2) * 0.89
    return out.T


# ------------------------------------------------------------------ mix
def loudnorm_json(path, extra=""):
    r = subprocess.run([FFMPEG, "-nostdin", "-hide_banner", "-i", path, "-af",
                        f"{extra}loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    e = r.stderr; return json.loads(e[e.rindex("{"):e.rindex("}") + 1])


def mix(video, score_wav, out):
    gain = MUSIC_LUFS - float(loudnorm_json(score_wav)["input_i"])
    graph = (f"[0:a]aformat=sample_rates={SR}:channel_layouts=stereo,asplit=2[sp][key];"
             f"[1:a]volume={gain:.2f}dB[m];"
             f"[m][key]sidechaincompress={DUCK}[duck];"
             "[sp][duck]amix=inputs=2:normalize=0:duration=first[mix]")
    tmp = "work/v2/premaster.wav"
    subprocess.run([FFMPEG, "-nostdin", "-v", "error", "-y", "-i", video, "-i", score_wav,
                    "-filter_complex", graph, "-map", "[mix]", "-c:a", "pcm_s16le", tmp], check=True)
    m = loudnorm_json(tmp)
    norm = (f"loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}"
            f":measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}"
            f":offset={m['target_offset']}:linear=true")
    subprocess.run([FFMPEG, "-nostdin", "-v", "error", "-y", "-i", video, "-i", tmp,
                    "-map", "0:v", "-c:v", "copy", "-map", "1:a", "-af", f"{norm},aresample={SR}",
                    "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "-shortest", out], check=True)
    return gain


def main():
    ass, video, out = sys.argv[1:4]
    dur = duration(video)
    audio = compose(ass_events(ass), dur)
    score_wav = "work/v2/score.wav"                       # run from montage/
    wavfile.write(score_wav, SR, (audio * 32767).astype(np.int16))
    gain = mix(video, score_wav, out)
    print(f"score: {score_wav} ({dur:.1f}s), music gain {gain:+.1f} dB -> {out}")


if __name__ == "__main__":
    main()
