# Post-AI Data Stack: ¿Qué cambió en la era de GPT?

**The Data Pub · Wed Oct 21, 2026 · 7:00 pm · Escuela de Gobierno y Transformación Pública (Tec), CDMX · also streamed on YouTube**
Solo, ~60 min total: **~45 min talk + ~15 min Q&A**. Talk in Spanish.

Sequel to *"Modern Data Stack: la virtud inesperada de la ignorancia"* (The Data Pub, July 2023).

---

## 1. The idea in one paragraph

Episode 2 of a series. In 2023 the question was *which stack*, and the cost of an answer depended on *where the metric lived* (5 min / 0.5 days / 3 months). In 2026 an agent walks any stack, so producing the answer costs minutes everywhere. The stack war didn't get won, it became invisible. What's left visible is **meaning**: which definition, which cutoff date, who can stop it. The history is told through Carlos's own career, with an on-screen counter of "how long it took me" that collapses to minutes in 2026, then flips into "¿y es verdad?".

**Thesis line:** *Producir el análisis se volvió barato. Acordar qué es verdad, no.*
(Credit Ian Macomber on a slide; his essay is the source of the era framing.)

**Closing line:** *En 2023 les dije que la ignorancia tenía una virtud inesperada. En 2026 la ignorancia se cura en una tarde. Lo que no se cura en una tarde es el criterio.*

---

## 2. Delivery phases (each one is shippable on its own)

| Phase | Deliverable | Depends on | Done when |
|---|---|---|---|
| **1. Plan** | this file | nothing | Carlos fills the TODOs in §5 |
| **2. Deck v1 (talk-only)** | `deck/index.html` + speaker notes | §5 answers | Carlos can give the full talk with zero demos and zero video |
| **3. Montage** | `montage/out/anteriormente.mp4` | the 2023 mp4 (local, not committed) | plays inside slide 1, ≤ 2 min |
| **4. Demos** | `demos/` + backup recordings | Docker, DuckDB | each demo has a `make` target and a recorded fallback |

**Rule for Deck v1:** every demo and video slot has a static fallback that works with Carlos just talking. Phases 3 and 4 *replace* a fallback; they never add new slides. That keeps the timing fixed from v1 onward.

---

## 3. Run of show (target ~45 min)

Slots marked **[D#]** are demo slots, **[M]** is the montage slot. In v1 each shows its fallback.

### Act 0 · Cold open (3 min)
1. **[M] "Anteriormente en The Data Pub…"** (black screen, then montage). *v1 fallback:* 5 stills from 2023 with one caption each (Birdman · Nokia 5MP vs iPhone 2MP · Hadoop → Spark → DuckDB · "¿Puedes solo añadirle…?" · "esto es marketing").
2. **Title.** Post-AI Data Stack · *Episodio 2*.
3. **¿Quién es este tipo?** Hot takes callback (pandas, perros, Santos). One line: "hace 3 años: economista que movía datos del punto A al B".

### Act 1 · Scorecard de 2023 (5 min)
4. **Lo que les dije en julio de 2023.** Four claims:
   - El Modern Data Stack es marketing.
   - DuckDB: el retador "de juguete".
   - No migres porque algo es nuevo (Bellotti, *Kill It With Fire*).
   - Riggan puede tomar todas las decisiones erróneas y aún así triunfar.
5. **La calificación.** ✅ MDS era marketing: ya ni lo decimos. ✅ DuckDB. ❌ dbt: tres años después, todavía no en producción en mi banco. ⚠️ Lo que no vi venir: los agentes.
6. **Puente:** "Hoy nadie habla de stacks. Todo el mundo habla de agentes. ¿Cambió el stack, o cambió otra cosa?"

### Act 2 · El ejemplo mínimo, recargado (5 min)
7. **El diagrama de 2023**, as is (`assets/2023/ejemplo-minimo-diagrama.png`). "¿Puedes solo añadirle…?" Metrics A and B.
8. **Las respuestas de 2023:** A y B en visualización → 5 min. A en modelo semántico → 0.5 días. B en sistema fuente → 3 meses, 5+ personas. (`ejemplo-minimo-5min.png`, `ejemplo-minimo-3meses.png`)
9. **El mismo diagrama en 2026:** every label animates to "≈ minutos", because the agent walks straight to the source (CF1: raw D1, no ETL). End on **"¿y es verdad?"**. Leave it unanswered; Act 4 pays it off.

### Act 3 · Cuatro eras, contadas por mi vida (~20 min, ~3–4 min per beat)
Each beat = the **boundary diagram** in a new state (one SVG, animated between states, Welch Labs look) + one personal story + the **counter** ("cuánto me tardé").

10. **Mapa de eras:** 2013 · 2016 · 2020 · 2026. Credit Ian Macomber.
11. **2013 · Preguntas que caben en un servidor.** Boundary holds only `orders` and `payments`, in two databases that can't be joined. Clickstream outside, not even logged. **[D1]** *v1 fallback:* slide showing the cross-database join and its error.
12. **2016–2018 · Toda la empresa en un solo lugar.** Clickstream and warehouse come inside. Story: first job 2018, R/tidyverse. **Counter: 3 gráficas pulidas = 1 día.** **[D2, optional]** *v1 fallback:* the same join working in one place.
13. **2020 · De reportero a operador.** Managed ETL in, reverse ETL out. Story: Databricks ETLs + Power BI, no time for tests ("¿cómo testeas un bookmark?"). **Counter: jornadas de 18 horas.**
14. **El desvío full-stack.** Story: the job that asked a data person to be a software engineer; React + backend; never reached prod. **Counter: ∞, nunca llegó a producción.** Line: "hoy ese código es casi gratis".
15. **Las abstracciones son tus amigas.** Story: Terraform + SageMaker. **Counter: TODO**.
16. **Julio 2023 · Este escenario.** Photo from 2023. "Les dije que la virtud era la ignorancia."
17. **2026 · El avión.** `assets/2026/avion-5-agentes.png`. Five agents building the Snowflake deck in one flight. **Counter: 1 vuelo.**
18. **Todos los contadores colapsan a "minutos".**
19. **Interludio (30 s): ¿qué hay dentro de la caja mágica?** Welch-style transformer computing 41 + 26 (`assets/refs/welch-style-transformer.png` as the look reference).

### Act 4 · El giro (8–10 min)
20. **El boundary de 2026:** everything inside, an agent harness spanning the stack, company context feeding it, a feedback loop of evals.
21. **La cita:** Ian Macomber, short quote on producing vs. agreeing, credited.
22. **La escalera renace:** the 2023 ladder of *time* becomes a ladder of *trust*. Same stages, new questions: ¿con qué definición respondió? ¿con qué fecha de corte? ¿quién lo puede detener?
23. **[D3] La respuesta segura y equivocada.** *v1 fallback:* the GBM case narrated over static slides: `COUNT(*)` = 3,743 → filtered = 0 → real = 627 → the model silently dropped incomplete responses, "un supuesto que no le pedí".
24. **[D4] El consenso como prueba** (Ian's loop): ask the same question in every interface × model, count distinct answers, fix context until there is one. *v1 fallback:* the pseudocode on a slide.

### Act 5 · Valor real vs. hype (5 min)
25. **Aporta valor real:** definiciones con dueño y versión (capa semántica); herramientas operables por cualquier agente (APIs / MCP); evals que leen trazas, no solo respuestas; formatos abiertos + DuckDB.
26. **Vive del hype:** vendors that want you to use *their* agent; agents wired to raw data with no definitions; "migra todo porque ahora hay IA"; "no todo necesita un LLM" (the null-retry classifier story, *source TODO*).
27. **Predicciones para el episodio 3 (2029).** 4–5 bets, graded next time. *Carlos picks, see §5.*

### Close (2 min)
28. **Birdman callback** → the closing line.
29. **Gracias** · h1sort.com/datapub · QR.

**Protected time:** slides 25–29 are rehearsed first and never cut. If running long, cut from Act 3 (slides 15 and 16 are the expendable ones).

---

## 4. Visual system

- **Look:** Welch Labs. Black background, thin white strokes, monospace labels, one accent color for "inside the boundary". No logos walls.
- **One hero visual:** the boundary diagram, a single inline SVG with 5 states (2013, 2016, 2020, 2023-callback, 2026). Transitions animate; after settling, the SVG blurs and loops behind the slide text.
- **The counter:** fixed bottom-right element that persists across Act 3, updated per slide.
- **Format:** single self-contained `deck/index.html`, no build step, arrow keys to navigate, `N` toggles speaker notes. Images referenced from `../assets/`. Publish with GitHub Pages.
- **Name budget:** ≤ 6 proper nouns per act. If a tool can't be explained in one sentence, it doesn't get mentioned.

---

## 5. TODOs for Carlos (blocking Deck v1)

- [ ] **Years per job:** R/tidyverse (2018) · Databricks + Power BI (____) · full-stack detour (____) · Terraform + SageMaker (____) · Santander (____). Where were you in 2013?
- [ ] **Counter value for the Terraform/SageMaker beat** (slide 15), or cut the counter there.
- [ ] **Pick 4–5 predictions for 2029** (slide 27). Starting menu:
  - La capa semántica pasa a ser el entregable por defecto de un equipo de datos.
  - El dashboard deja de ser destino: los agentes lo leen y lo recortan.
  - OLTP → ETL → OLAP sigue igual; lo que cambia es quién lo opera.
  - El rol junior de datos se redefine alrededor de verificar, no de producir.
  - El modelado tipo dbt sobrevive con otro nombre.
- [ ] **Poll at the start, yes or no?** If yes, it feeds [D3] live in phase 4. v1 doesn't need it.
- [ ] **Source for the null-retry classifier story** ($ amount, tokens, vendor), or say it without numbers.

---

## 6. Fact-check list (every number on a slide gets a source or gets cut)

- Birdman: 4 Oscars (Best Picture, Director, Original Screenplay, Cinematography), dir. Alejandro G. Iñárritu.
- Nokia N95 5MP, iPhone (1st gen) 2MP, HTC Dream 3.15MP.
- Ian Macomber, *The Shape and Feel of the Post-AI Data Stack* (Aug 30, 2026): era years and framing.
- GBM poll numbers (3,743 / 0 / 627) from the GBM transcript.
- Null-retry story: see §5.

---

## 7. Phase briefs

### Phase 3 · Montage (for the Claude Code session that has the mp4)
- Source: the July 2023 recording, placed locally at `montage/src/2023.mp4` (gitignored, never committed).
- Find shots by transcribing the video (e.g. whisper) and matching these cue phrases:
  1. "la virtud inesperada de la ignorancia" (title)
  2. "birdman" / "Riggan" + "Mike" (the two characters)
  3. "¿Puedes solo añadirle…?" + "5 minutos" … "3 meses" (the minimal example)
  4. "Nokia" / "5 megapíxeles" / "iPhone" (modern ≠ more advanced)
  5. "haduk" → "Spark" → "dog divi" (the challengers)
  6. "esto es marketing" (the verdict)
  7. "puede tomar todas las decisiones erróneas … y aún así … puede triunfar" (the close)
- Target **90–120 s**, 7 clips of 8–15 s each, hard cuts, burned-in Spanish captions, a title card "Anteriormente en The Data Pub… · Julio 2023".
- Output: `montage/out/anteriormente.mp4` (H.264, 1080p, ≤ 30 MB) + `montage/out/poster.jpg` + 5 stills for the v1 fallback in `assets/2023/stills/`.

### Phase 4 · Demos
- `demos/docker-compose.yml`: two Postgres containers, `orders_db` and `payments_db`, seeded with a few hundred rows.
- `make era2013`: the cross-database join fails; no clickstream table exists.
- `make era2016`: DuckDB attaches both + a JSON clickstream file; the join works.
- `make trap`: an agent answers a question confidently and wrong; `make trap-fixed` adds a context file and the answer changes.
- `make consensus`: same question, two models or harnesses, count distinct answers.
- Every target pre-warmed before the talk; every demo has a screen recording in `demos/recordings/` as fallback.
