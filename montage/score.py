#!/usr/bin/env python3
"""Original trailer score for the recap, synthesized here (no licensed music,
so no Content ID on the stream), then mixed under the speech with ducking.

  uv run --no-project --with numpy --with scipy python score.py \
      work/v2/captions.ass work/v2/nomusic.mp4 out/anteriormente.mp4

Every hit is placed from captions.ass, so a re-cut stays in sync:
  Slam words (MARKETING, 3 MESES, ...) -> taiko hits; the last one (40 AÑOS) -> braam
  Card events -> "THE DATA PUB" stamp braam, "¿Sigue siendo cierto?" final braam
Shape: ticking drone under the hook -> 8th-note ostinato that thickens act by act
(D minor, then i-VI-III-VII) -> lift into TRIUNFAR -> near-silence + heartbeat +
riser for the cliffhanger -> braam on 40 AÑOS -> final braam that rings out.
"""
import json, re, subprocess, sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, fftconvolve, sosfilt

FFMPEG = "/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg"
SR = 48000
BEAT = 60 / 96                      # 96 BPM
EIGHTH = BEAT / 2
BAR = BEAT * 4
MUSIC_LUFS = -21                    # score level before ducking; speech sits at -16
DUCK = "threshold=0.02:ratio=5:attack=15:release=380:knee=3"  # ~14 dB under the voice, full in the gaps
rng = np.random.default_rng(2026)

# note frequencies (Hz)
N = {n: 440 * 2 ** ((i - 9) / 12) for i, n in enumerate(
    ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"])}
def hz(name, octave): return N[name] * 2 ** (octave - 4)

CHORDS = {  # root, triad tones (pitch classes) for the ostinato
    "Dm": ("D", ["D", "F", "A"]), "Bb": ("A#", ["A#", "D", "F"]),
    "F": ("F", ["F", "A", "C"]), "C": ("C", ["C", "E", "G"]), "A": ("A", ["A", "C#", "E"]),
}


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


# ------------------------------------------------------------------ synth
def t_axis(sec): return np.arange(int(sec * SR)) / SR

def lp(x, fc, order=2): return sosfilt(butter(order, fc, "low", fs=SR, output="sos"), x)
def hp(x, fc, order=2): return sosfilt(butter(order, fc, "high", fs=SR, output="sos"), x)
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], "band", fs=SR, output="sos"), x)

def saw(f, t, detune=0.0):
    ph = rng.random()
    return 2 * ((f * (1 + detune) * t + ph) % 1) - 1


def place(bus, t0, sig, pan=0.0, gain=1.0):
    """Add mono sig to stereo bus at t0 (s), equal-power pan in [-1, 1]."""
    i = int(t0 * SR)
    if i >= bus.shape[1]:
        return
    sig = sig[: bus.shape[1] - i]
    a = (pan + 1) * np.pi / 4
    bus[0, i:i + len(sig)] += sig * np.cos(a) * gain
    bus[1, i:i + len(sig)] += sig * np.sin(a) * gain


def taiko(heavy=True):
    t = t_axis(2.2 if heavy else 1.2)
    f = 42 + 70 * np.exp(-t / 0.07)                      # pitch drop: the "dum"
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / (0.55 if heavy else 0.3))
    skin = lp(rng.standard_normal(len(t)), 1800) * np.exp(-t / 0.03) * 0.6
    sub = np.sin(2 * np.pi * 36.7 * t) * np.exp(-t / 0.9) * (0.7 if heavy else 0)
    return np.tanh(1.8 * (body + skin + sub)) * (1.0 if heavy else 0.6)


def braam(chord_hz, sec=4.5, bright=3200):
    """Stacked detuned saws, filter snaps open then closes, saturated."""
    t = t_axis(sec)
    x = sum(saw(f, t, d) for f in chord_hz for d in (-0.004, 0, 0.005))
    x /= len(chord_hz) * 3
    env = np.minimum(t / 0.02, 1) * np.exp(-t / (sec / 3))
    # time-varying filter by crossfading a dark and a bright render
    mix = np.exp(-t / 0.35)
    x = lp(x, 260) * (1 - mix) + lp(x, bright) * mix
    return np.tanh(2.5 * x * env)


def pluck(f, sec=EIGHTH * 1.6):
    t = t_axis(sec)
    x = 0.6 * saw(f, t) + 0.4 * saw(f, t, 0.006)
    return lp(x, 1300) * np.minimum(t / 0.004, 1) * np.exp(-t / 0.13)   # dark: leave 1-4 kHz to the voice


def tick():
    t = t_axis(0.05)
    return hp(rng.standard_normal(len(t)), 5000) * np.exp(-t / 0.008)


def thump():
    t = t_axis(0.35)
    f = 40 + 25 * np.exp(-t / 0.04)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.12)


def reverb_ir(sec=2.4):
    t = t_axis(sec)
    ir = np.stack([lp(rng.standard_normal(len(t)), 5200) * np.exp(-t / 0.55) for _ in range(2)])
    ir[:, 0] = 0
    return ir / np.abs(ir).sum(axis=1, keepdims=True).max() * 30


# ------------------------------------------------------------------ score
def compose(events, dur):
    slams = [(t, x) for t, s, x in events if s == "Slam"]
    cards = sorted({round(t, 2) for t, s, _ in events if s == "Card"})
    stamp, tres, cierto = cards[0], cards[-2], cards[-1]
    t_triunfar = next(t for t, x in slams if "TRIUNF" in x)
    t_40, t_jug = slams[-1][0], next(t for t, x in slams if "JUGUETE" in x)
    t_meses = next(t for t, x in slams if "MESES" in x)

    total = dur + 4
    dry = np.zeros((2, int(total * SR)))     # percussion, ticks: mostly dry
    wet = np.zeros((2, int(total * SR)))     # tonal parts: through the reverb

    # 1. drone (D1 + A1 + D2), dark under the hook, opening up act by act
    t = t_axis(total)
    drone = sum(saw(f, t, d) for f in (hz("D", 1), hz("A", 1), hz("D", 2)) for d in (-0.003, 0.003)) / 6
    dark, bright = lp(drone, 160, 4), lp(drone, 700, 4)
    open_ = np.interp(t, [0, stamp, t_jug, t_meses, t_triunfar, t_triunfar + 1.5, t_40, cierto, total],
                      [0, 0.1, 0.35, 0.6, 1.0, 0.2, 0.0, 0.3, 0.0])
    level = np.interp(t, [0, 1.5, t_triunfar + 1, t_triunfar + 2.5, t_40 - 3.5, t_40, tres, tres + 0.2, cierto, dur, total],
                      [0, 0.55, 0.85, 0.35, 0.35, 0.9, 0.9, 0.0, 0.0, 0.0, 0.0])
    sub = np.sin(2 * np.pi * hz("D", 1) * t) * 0.5
    d = (dark * (1 - open_) + bright * open_ + sub) * level * 0.5
    wet[0] += d; wet[1] += d

    # 2. clock ticks under the hook and the first act
    k = 0.0
    while k < min(t_jug, 20.0):
        if not (stamp - 0.3 < k < stamp + 1.9):
            place(dry, k, tick(), pan=0.5 if int(k / BEAT) % 2 else -0.5, gain=0.18)
        k += BEAT

    # 3. ostinato: 8ths from after the stamp to TRIUNFAR, thickening
    def chord_at(x):
        if x < t_jug:
            return "Dm"
        if x < t_triunfar - 4 * BAR:
            return ["Dm", "Bb", "F", "C"][int((x - t_jug) / (2 * BAR)) % 4]
        return ["Bb", "C", "Dm", "A"][min(3, int((x - (t_triunfar - 4 * BAR)) / BAR))]

    pattern = [0, 2, 1, 2, 0, 2, 1, 2]                    # root-fifth-third-fifth
    x, i = stamp + 1.9, 0
    while x < t_triunfar:
        root, tones = CHORDS[chord_at(x)]
        oct_ = 3
        f = hz(tones[pattern[i % 8]], oct_)
        gain = np.interp(x, [stamp, t_jug, t_meses, t_triunfar], [0.18, 0.28, 0.38, 0.55])
        place(wet, x, pluck(f), pan=-0.35 if i % 2 else 0.35, gain=gain)
        if x > t_meses:                                   # octave layer joins after 3 MESES
            place(wet, x, pluck(f * 2), pan=0.6 if i % 2 else -0.6, gain=gain * 0.3)
        if i % 8 == 0 and x > t_jug:                      # bass note per bar
            place(wet, x, lp(saw(hz(root, 1), t_axis(BAR)), 220) * np.exp(-t_axis(BAR) / 1.2), gain=0.5)
        x += EIGHTH; i += 1

    # 4. low toms on beats 1 and 3 once the challengers arrive
    x = t_jug + BAR
    while x < t_triunfar - 0.2:
        place(dry, x, taiko(heavy=False), gain=0.35)
        x += 2 * BEAT

    # 5. hits on the slam words (40 AÑOS gets the braam instead)
    for ts_, word in slams[:-1]:
        heavy = word not in ("5 MINUTOS",)
        place(dry, ts_ - 0.03, taiko(heavy), gain=0.95 if heavy else 0.6)
    place(dry, t_triunfar - 0.03, taiko(True), gain=1.0)
    place(wet, t_triunfar - 0.03, braam([hz("A#", 1), hz("F", 2), hz("A#", 2), hz("D", 3)], 3.0), gain=0.55)

    # 6. stamp: THE DATA PUB · JULIO 2023
    place(wet, stamp - 0.02, braam([hz("D", 1), hz("A", 1), hz("D", 2), hz("F", 3)], 3.2), gain=0.75)
    place(dry, stamp - 0.02, taiko(True), gain=0.9)

    # 7. cliffhanger: heartbeat + riser into 40 AÑOS
    x = t_triunfar + 2.5
    while x < t_40 - 0.6:
        place(dry, x, thump(), gain=0.7); place(dry, x + 0.28, thump(), gain=0.45)
        x += 0.95
    rt = t_axis(4.0)
    # the riser runs under "no ha cambiado en 40 años": air above 3 kHz plus a low rising tone, no mid-band noise
    riser = bp(rng.standard_normal(len(rt)), 3200, 9000) * (rt / 4) ** 2.5
    riser += np.sin(2 * np.pi * np.cumsum(55 * 2 ** (rt / 2)) / SR) * (rt / 4) ** 3 * 0.5
    place(wet, t_40 - 4.0, riser, gain=0.3)
    place(wet, t_40 - 0.02, braam([hz("D", 1), hz("A", 1), hz("D", 2), hz("A", 2), hz("F", 3)], 4.0, 4200), gain=1.0)
    place(dry, t_40 - 0.02, taiko(True), gain=1.0)

    # 8. "¿Sigue siendo cierto?": the last braam, unresolved (A major over D), rings out
    place(wet, cierto - 0.02, braam([hz("D", 1), hz("A", 1), hz("C#", 3), hz("E", 3), hz("A", 3)], 5.0, 3800), gain=0.9)
    place(dry, cierto - 0.02, taiko(True), gain=0.9)

    ir = reverb_ir()
    rev = np.stack([fftconvolve(wet[c], ir[c])[: wet.shape[1]] for c in range(2)])
    out = dry + 0.75 * wet + 0.35 * rev
    out = out[:, : int(dur * SR)]
    fade = np.minimum(1, (dur - t_axis(dur)) / 0.6)       # last 0.6 s fades to silence
    out *= fade
    out = np.tanh(out / max(1e-9, np.abs(out).max()) * 1.3) * 0.89
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
