# Deck contract (for every slide author)

Read `../CLAUDE.md` and `../PLAN.md` first. This file is how slides plug into the shell.

## Files and ownership

| File | Owner | Notes |
|---|---|---|
| `index.html`, `engine.js`, `particles.js`, `styles.css`, `tools/` | orchestrator | **Don't edit.** Need a change? Put it in your final report. |
| `acts/act0.js` (slides 1–3) + `acts/act1.js` (4–6) | Act 0+1 author | |
| `acts/act2.js` (7–9) | Act 2 author | |
| `acts/act3.js` (10–18), `components/boundary.js`, `components/timeline.js` | Act 3 author | owns both hero components |
| `acts/act4.js` (19–23) | Act 4 author | uses `<boundary-diagram>` and `window.METRIC_A` |
| `acts/act5.js` (24–29, registers acts 5 **and** 6) | Act 5 + close author | |
| `data/metric-a.js`, `../demos/metric-a/` | metric-A author | |
| `../montage/`, `../assets/2023/stills/` | montage author | |

Don't `git commit`. Only write files you own. Put scratch files in `deck/.shots/` (gitignored).

## Registering slides

```js
Deck.act(3, 'Acto 3 · Las eras', [
  {
    id: 'era-2013',            // unique, kebab-case; the slide element is <section id="s-era-2013">
    title: 'Era 2013 → SAT',   // shown in the presenter view
    time: 150,                 // planned seconds (drives the presenter's ahead/behind clock)
    class: 'middle',           // optional extra classes: center | middle | bleed
    particles: 'two',          // see Particles below; may be an array indexed by step
    counter: '3 gráficas = 1 día', // bottom-right "Cuánto me tardé" box; array by step; omit = hidden
    label: undefined,          // bottom-left label; defaults to the act label; '' hides it
    html: `…`,                 // string or (ctx) => string
    notes: `<p>…</p>`,         // speaker notes, Spanish, HTML paragraphs
    onEnter(el, ctx, step) {}, // optional; el is the <section>
    onStep(el, step, ctx) {},  // optional; also called right after onEnter
    onLeave(el, ctx) {},       // optional; videos are paused for you
  },
]);
```

Act numbers and labels (use exactly these): 0 `Anteriormente` · 1 `Acto 1 · Scorecard 2023` · 2 `Acto 2 · El ejemplo mínimo` · 3 `Acto 3 · Las eras` · 4 `Acto 4 · El giro` · 5 `Acto 5 · Valor real vs. hype` · 6 `Cierre`.

Time budgets (sum of `time` per act, seconds): Act 0 180 · Act 1 300 · Act 2 300 · Act 3 1020 · Act 4 510 · Act 5 300 · Cierre 120.

## Build steps

Elements inside a slide reveal on clicks:
- `data-step="2"`: visible from step 2 on (step 0 is the slide's first state).
- `data-step-only="2"`: visible only at step 2.
- `data-step-hide="3"`: fades out from step 3 on.

The slide's step count is the largest number used; set `steps` to override. The current step is on the section as `data-at="N"`, so CSS like `#s-era-2013[data-at="2"] .x { … }` works. Wrap a list in `.focus-last` to dim earlier revealed items.

## Particles

The field is one canvas behind every slide (1800 dots, stage coords 1920×1080). A slide sets a spec, and it **inherits** to later slides until one sets another.

Spec: `'name'` or `{ shape: 'name', opacity: 0.2 }` (default opacity 0.35; use 0.15–0.25 behind dense text, up to 0.9 when the particles are the point). `'none'` fades out.

Built-in shapes and what they mean (PLAN.md §5):
- `scatter`: slow drift (2023, the ignorance; default)
- `two`: two clusters that never touch (2013's unjoinable databases)
- `one`: one body (the warehouse, 2016–2020)
- `swarm`: 14 small groups each moving on its own (agents, 2026)
- `split`: two tight clusters far apart (two confident answers)
- `converge`: everything to one point (one answer)
- `timeline`: two horizontal tracks at y≈389 and y≈734 (the double timeline)
- `ring`, `grid`

Custom shapes (prefix the name with your act, e.g. `a3-…`):
- `Particles.fromText('a0-ep2', 'Episodio 2', { size: 200, x: 960, y: 760 })`
- `Particles.fromPoints('a3-pts', [[x, y], …])`
- `Particles.define('a3-x', (u, t) => [x, y])`: `u.i` index, `u.r(k)` stable uniform, `u.g(k)` stable gaussian, `t` seconds.

## Look (Welch Labs; see `../assets/refs/welch-style-transformer.png`)

- Black, white, thin lines, monospace uppercase labels, one accent (`--accent`, amber) for "inside the boundary" and for *the* important word. `--good` / `--bad` only on the scorecard.
- Utility classes in `styles.css`: `t-hero t-title t-sub t-body t-small t-label mono dim faint accent quote cite cite.foot bullets box chip frame fit row cols stack pre.code`. In SVG: `ln ln-dim ln-hair ln-acc lbl txt fill-acc fill-fg`, plus `draw` with `pathLength="1"` for draw-on lines.
- **Projector rules:** content text ≥ 28px on the stage, labels ≥ 20px, strokes ≥ 2px. Keep 120px side padding and leave the bottom 140px free (label + counter live there).
- Per-act CSS: `Deck.css(\`#s-my-id .x { … }\`)`. Scope every selector to your slide ids or an `aN-` class prefix.
- **No network at runtime:** no CDNs, no web fonts, no remote images. Assets via relative paths (`../assets/...`).
- Animation: prefer CSS transitions keyed off `.slide.active`, `.shown`, `[data-at]`. JS animation in `onEnter`/`onStep` must jump to its final state when `ctx.shot` is true.

## Content rules (from CLAUDE.md, enforced)

- Slide text in **Spanish** with correct accents (á é í ó ú ñ ¿ ¡). Code, ids and file names in English.
- **Every number on a slide needs a source in PLAN.md §6**, or it gets cut. Carlos's own anecdotes (his counters) are sourced by him.
- ≤ 6 proper nouns (tools, vendors) per act.
- Few words per slide. The speaker says the rest.
- **Speaker notes:** Spanish, first person, Carlos's spoken voice (casual, CDMX, a little self-deprecating). 60–160 words per slide, as `<p>` paragraphs. End with the bridge sentence to the next slide. Put stage directions in `<p class="dir">[…]</p>`.

## Shared components (Act 3 owns, Act 4 consumes)

- `<boundary-diagram state="2013|2016|2020|2023|2026"></boundary-diagram>`: one SVG, 1680×640 by default. Changing `state` animates to the new state. Act 4 slide 19 uses `state="2026"`.
- `<double-timeline at="0..5"></double-timeline>`: Act 3 only.

## Data

`data/metric-a.js` sets:

```js
window.METRIC_A = {
  question: 'frecuencia promedio en días de los clientes suscritos en el último año',
  cutoff: '2026-09-30',
  definitions: [ { id: 'a', label: '…', sql: '…', value: 12.4, unit: 'días' }, … ], // 3 entries
  defined: { label: '…', sql: '…', value: 11.9, unit: 'días' }, // the agreed definition
  source: 'demos/metric-a (synthetic data, DuckDB)',
};
```

Act 4 renders slide 22 from it and shows `—` while it is `null`.

## Montage outputs (Act 0 consumes)

- `../montage/out/anteriormente.mp4` + `../montage/out/poster.jpg`. Slide 1 tries the video and falls back to the stills if it fails to load.
- Stills: `../assets/2023/stills/00-escenario.jpg`, `01-birdman.jpg`, `02-nokia.jpg`, `03-retadores.jpg`, `04-anadirle.jpg`, `05-marketing.jpg`. If one is missing, show its caption alone.

## Verify before you report

1. `node --check` each file you wrote.
2. `deck/tools/shot.sh @<slide-id> <step>` for every slide and its last step. Address slides by id: other authors are adding slides at the same time, so numbers shift. It prints the PNG path and any console errors. **Look at each PNG** (Read tool). Fix overlaps, overflow, tiny text and console errors. (In a browser: `index.html#/@slide-id/2`.)
3. In your final report: slides built (id + title + steps), anything you couldn't source, and any engine change you need.
