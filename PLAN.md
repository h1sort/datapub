# Post-AI Data Stack: ¿Qué cambió en la era de GPT?

**The Data Pub · Wed Oct 21, 2026 · 7:00 pm · Escuela de Gobierno y Transformación Pública (Tec), CDMX · also streamed on YouTube**
Solo, ~60 min total: **~45 min talk + ~15 min Q&A**. Talk in Spanish.

Sequel to *"Modern Data Stack: la virtud inesperada de la ignorancia"* (The Data Pub, July 2023).

---

## 1. The idea in one paragraph

Episode 2 of a series. In 2023 the question was *which stack*, and the cost of an answer depended on *where the metric lived* (5 min / 0.5 days / 3 months). In 2026 an agent walks any stack, so producing the answer costs minutes everywhere. The stack war didn't get won, it became invisible. What's left visible is **meaning**: which definition, which cutoff date, who can stop it.

The history is told through Carlos's own career on a **double timeline**: the world's eras on top, the year each era actually reached him below. Every era reached him years late (in Mexico, in government, in consulting). **Except this one: the AI era arrived the same week here as in San Francisco.** That gap closing is a story nobody else in the room can tell.

**Thesis line:** *Producir el análisis se volvió barato. Acordar qué es verdad, no.* (Credit Ian Macomber on a slide; the era framing is his.)

**Closing line:** *En 2023 les dije que la ignorancia tenía una virtud inesperada. En 2026 la ignorancia se cura en una tarde. Lo que no se cura en una tarde es el criterio.*

---

## 2. Delivery phases (each one is shippable on its own)

| Phase | Deliverable | Depends on | Done when |
|---|---|---|---|
| **1. Plan** | this file | nothing | done |
| **2. Deck v1 (talk-only)** | `deck/index.html` + speaker notes | this plan | Carlos can give the full talk with zero demos and zero video |
| **3. Montage** | `montage/out/anteriormente.mp4` | the 2023 mp4 (local, not committed) | plays inside slide 1, ≤ 2 min |
| **4. Demos** | `demos/` + backup recordings | Docker, DuckDB | each demo has a `make` target and a recorded fallback |

**Rule for Deck v1:** every demo and video slot has a static fallback that works with Carlos just talking. Phases 3 and 4 *replace* a fallback; they never add new slides. The timing rehearsed on v1 is the timing given.

---

## 3. Run of show (target ~45 min)

Slots marked **[D#]** are demo slots, **[M]** is the montage slot. In v1 each shows its fallback.

### Act 0 · Cold open (3 min)
1. **[M] "Anteriormente en The Data Pub…"** (black screen, then montage). *v1 fallback:* 5 stills from 2023 with one caption each (Birdman · Nokia 5MP vs iPhone 2MP · Hadoop → Spark → DuckDB · "¿Puedes solo añadirle…?" · "esto es marketing").
2. **Title.** Post-AI Data Stack · *Episodio 2*.
3. **¿Quién es este tipo?** Hot takes callback (pandas, perros, Santos). "Hace 3 años: consultor de datos. Hoy: AI Engineer en Santander."

### Act 1 · Scorecard de 2023 (5 min)
4. **Lo que les dije en julio de 2023:**
   - El Modern Data Stack es marketing.
   - DuckDB: el retador "de juguete".
   - No migres porque algo es nuevo: migrar cuesta años (la migración más corta que evalué, on-prem → Snowflake: 3 años).
   - Riggan puede tomar todas las decisiones erróneas y aún así triunfar.
5. **La calificación:**
   - ✅ MDS era marketing: ya ni lo decimos.
   - ✅ DuckDB.
   - ❌ dbt: tres años después, todavía no en producción en mi banco.
   - 🔄 **"Migrar cuesta años": eso ya no es cierto.** Migrations that took years now take months (Gergely Orosz's field reports, see §6). The advice survives (don't migrate for novelty); the *reason* I gave collapsed.
   - ⚠️ Lo que no vi venir: los agentes.
6. **Puente:** "Hoy nadie habla de stacks. Todo el mundo habla de agentes. ¿Cambió el stack, o cambió otra cosa?"

### Act 2 · El ejemplo mínimo, recargado (5 min)
7. **El diagrama de 2023**, as is (`assets/2023/ejemplo-minimo-diagrama.png`). "¿Puedes solo añadirle…?" Metrics A and B.
8. **Las respuestas de 2023:** A y B en visualización → 5 min. A en modelo semántico → 0.5 días. B en sistema fuente → 3 meses, 5+ personas. (`ejemplo-minimo-5min.png`, `ejemplo-minimo-3meses.png`)
9. **El mismo diagrama en 2026:** every label animates to "≈ minutos", because the agent walks straight to the source. End on **"¿y es verdad?"**. Left unanswered; Act 4 pays it off with metric A itself.

### Act 3 · Las eras del mundo vs. las eras que me tocaron (~18 min)
One hero visual: the **double timeline**. Top track: Ian's eras (2013 · 2016 · 2020 · 2026). Bottom track: Carlos's jobs. An arrow from each era to the year it reached him; the arrows get shorter, and the last one is vertical. Each beat also advances the **boundary diagram** (one SVG, Welch Labs look) and the **counter** ("cuánto me tardé").

10. **Mapa de eras** (Ian Macomber's four eras, credited) + the empty bottom track.
11. **Era 2013 · preguntas que caben en un servidor → me llegó en 2018 (SAT, Data Scientist).** Boundary: two OLTP databases that can't be joined; clickstream outside. Story: R/tidyverse; finished the notebook, "¿y mi ML engineer?" "Somos tres." **Counter: 3 gráficas pulidas = 1 día.** **[D1]** *v1 fallback:* slide with the cross-database join and its error.
12. **El desvío full-stack → 2020 (Bancomext, Software Engineer).** Story: a data person asked to be a software engineer; React + backend; never reached prod. **Counter: ∞, nunca llegó a producción.** Line: "hoy ese código es casi gratis".
13. **Eras 2016 + 2020 · toda la empresa en un lugar, y de reportero a operador → me llegaron juntas en 2021 (Accenture).** Boundary absorbs clickstream and the warehouse, then managed ETL in / reverse ETL out. Story: Databricks ETLs + Power BI, no time for tests ("¿cómo testeas un bookmark?"). **Counter: jornadas de 18 horas.** **[D2, optional]** *v1 fallback:* the same join working in one place.
14. **Las abstracciones son tus amigas → 2023–2025 (Accenture, Sr Data & ML Engineer).** Story: Terraform + SageMaker. **Counter: TODO (or none).**
15. **Julio 2023 · este escenario.** Photo from 2023, on the bottom track. "Les dije que la virtud era la ignorancia."
16. **Era 2026 · el avión → me llegó en 2026.** First vertical arrow. `assets/2026/avion-5-agentes.png`: five agents building the Snowflake deck in one flight. **Counter: 1 vuelo.** Line: "Por primera vez, la era me llegó al mismo tiempo que a San Francisco."
17. **Todos los contadores colapsan a "minutos".**
18. **Interludio (30 s): ¿qué hay dentro de la caja mágica?** Welch-style transformer computing 41 + 26 (`assets/refs/welch-style-transformer.png` as the look reference).

### Act 4 · El giro (8–10 min)
19. **El boundary de 2026:** everything inside, an agent harness spanning the stack, company context feeding it, a feedback loop of evals.
20. **La cita:** Ian Macomber on producing vs. agreeing (one short quote, credited).
21. **La escalera renace:** the 2023 ladder of *time* becomes a ladder of *trust*. Same stages, new questions: ¿con qué definición respondió? ¿con qué fecha de corte? ¿quién lo puede detener?
22. **[D3] Métrica A, otra vez.** The 2023 metric "frecuencia promedio en días de los clientes suscritos en el último año" is ambiguous: suscrito *cuándo*, último año *desde qué corte*, promedio *de qué*. Ask two agents/models the same question on the same synthetic data: two confident, different answers. Add the definition: one answer. Nobody in the room has seen this demo, including people who saw the 2023 talk. *v1 fallback:* three valid SQL definitions of metric A side by side, three different numbers.
23. **El consenso como prueba** (Ian's loop): ask in every interface × model, count distinct answers, fix context until there is one. Gergely's parallel from software: AI writes the tests too, but the time spent on tests vs. code hasn't changed (Jarred Sumner, via Gergely). *Verification didn't get cheaper; production did.*

### Act 5 · Valor real vs. hype (5 min)
24. **Aporta valor real:** definiciones con dueño y versión (capa semántica); herramientas operables por cualquier agente (APIs / MCP); evals que leen trazas, no solo respuestas; formatos abiertos + DuckDB; clasificadores tipados (Jev) cuando la pregunta es un juicio, no un texto.
25. **"No todo necesita un LLM": la historia de terror.** Astronomer: Snowflake `AI_CLASSIFY` over ~250k job titles; a bug returned NULLs, a retry path re-sent them every 30 min in dev for two weeks → **~44 mil millones de tokens, ~61,600 créditos**. Then: the same job with a typed classifier is cents. **Say tokens and credits, not dollars** (see §6).
26. **Vive del hype:** vendors that want you to use *their* agent; agents wired to raw data with no definitions; "migra todo porque ahora hay IA"; zombie reviews (Gergely: everyone approves, nobody reads) and their data twin, zombie dashboards.
27. **Predicciones para el episodio 3 (2029).** See §4. Interaction: hands up per prediction, photo of the room, graded next time.

### Close (2 min)
28. **Birdman callback** → closing line. Extra beat now available: in 2023 Riggan's mistakes were expensive; in 2026 a wrong stack decision costs months, not years. What's still expensive is not knowing *why* it was wrong.
29. **Gracias** · h1sort.com/datapub · QR.

**Protected time:** slides 24–29 are rehearsed first and never cut. If running long, cut from Act 3 (slides 14 and 15 are expendable).

**No poll this time.** Repeat attendees have taken it. The interaction is the bets on slide 27, which feeds episode 3.

---

## 4. Predictions for 2029 (Carlos's, worded for slides)

1. **Aprender un lenguaje de programación seguirá siendo útil.** (Gergely: old patterns get rediscovered; the right words make agents write better code.)
2. **Todos van a necesitar habilidades de ingeniería y ciencia de datos.** (swyx, Oct 2026: data engineers > AI engineers; the "data-intensive applications" person is in demand.)
3. **La IA frenará temporalmente la contratación de talento nuevo, y se ajustará cuando quede claro que ser AI-native es una habilidad profunda.** (Gergely: junior hiring keeps falling.)
4. **Los roles se reorganizan por arquetipo, no por función** (Boris Cherny's five: prototyper, builder, sweeper, grower, maintainer).
5. **Democratización de stacks: competencia feroz y proveedores de datos convertidos en commodity.**

---

## 5. Visual system

- **Look:** Welch Labs. Black background, thin white strokes, monospace labels, one accent color for "inside the boundary". No logo walls.
- **Two hero visuals:** the **double timeline** (Act 3) and the **boundary diagram** (5 states: 2013, 2016, 2020, 2026, plus the 2023 callback). One inline SVG each; transitions animate; after settling, the SVG blurs and loops behind slide text.
- **The counter:** fixed bottom-right element across Act 3, updated per slide.
- **Format:** single self-contained `deck/index.html`, no build step, arrow keys to navigate, `N` toggles speaker notes. Images from `../assets/`. Publish with GitHub Pages.
- **Name budget:** ≤ 6 proper nouns per act.

---

## 6. Sources and fact-checks (every number on a slide has one, or gets cut)

- **Ian Macomber**, *The Shape and Feel of the Post-AI Data Stack* (Aug 30, 2026): https://www.iandmacomber.com/blog/post-ai-data-stack/ — eras, boundary diagrams, consensus loop.
- **Astronomer**, *What Jev will do to data engineering* (Julian LaNeve & Kaxil Naik, Sep 22, 2026): https://www.astronomer.io/blog/what-jev-will-do-to-data-engineering/ — `AI_CLASSIFY`, ~250k titles, ~44B tokens, ~61,600 credits, two weeks.
  - ⚠️ **Don't say "$10,000".** The article's own dollar figure (~$1,900) doesn't match its credit count (61,600 credits at $2–4 list is far more). Use tokens and credits only.
  - Jev benchmark (4k titles): $0.16 vs $11–21 for Cortex; 88% persona agreement; "a valid type is not a correct answer" (their caveat; worth quoting the idea).
- **Gergely Orosz**, talk (Oct 2026; event name TODO): migrations in months (Airbnb tests in 6 weeks, Uber JUnit 4→5 in 4 months, OpenAI API Python→Rust ~90% in 4–5 months), test-to-code time ratio unchanged (Jarred Sumner), zombie code reviews, junior hiring falling, teams still the unit of work.
- **swyx**, X post, Oct 19, 2026: "Data engineers > AI engineers".
- **Boris Cherny**, X post on five archetypes (date TODO).
- **Carlos's career** (LinkedIn): SAT Data Scientist 2018–2019 · Bancomext Software Engineer 2020 · Accenture Data & ML Engineer 2021–2023, Sr (Manager) 2023–2025 · Santander AI Engineer 2025–present.
- Birdman: 4 Oscars (Picture, Director, Original Screenplay, Cinematography), dir. Alejandro G. Iñárritu.
- Nokia N95 5MP, iPhone (1st gen) 2MP, HTC Dream 3.15MP.

**Open item:** confirm which job had Databricks + Power BI and which had Terraform + SageMaker. This plan assumes both were Accenture projects (in that order).

---

## 7. Phase briefs

### Phase 3 · Montage (for the Claude Code session that has the mp4)
- Source: the July 2023 recording at `montage/src/2023.mp4` (gitignored, never committed).
- Find shots by transcribing the video (e.g. whisper) and matching these cue phrases:
  1. "la virtud inesperada de la ignorancia" (title)
  2. "birdman" / "Riggan" + "Mike" (the two characters)
  3. "¿Puedes solo añadirle…?" + "5 minutos" … "3 meses" (the minimal example)
  4. "Nokia" / "5 megapíxeles" / "iPhone" (modern ≠ more advanced)
  5. "haduk" → "Spark" → "dog divi" (the challengers)
  6. "esto es marketing" (the verdict)
  7. "puede tomar todas las decisiones erróneas … y aún así … puede triunfar" (the close)
- Target **90–120 s**, 7 clips of 8–15 s, hard cuts, burned-in Spanish captions, title card "Anteriormente en The Data Pub… · Julio 2023".
- Output: `montage/out/anteriormente.mp4` (H.264, 1080p, ≤ 30 MB) + `montage/out/poster.jpg` + 5 stills in `assets/2023/stills/` for the v1 fallback.

### Phase 4 · Demos
- `demos/docker-compose.yml`: two Postgres containers, `orders_db` and `payments_db`, a few hundred seeded rows.
- `make era2013`: the cross-database join fails; no clickstream table exists.
- `make era2016` (optional): DuckDB attaches both + a JSON clickstream file; the join works.
- `make metric-a`: synthetic subscription + usage events (Linear-like project tool, as in 2023). Two agents/models answer metric A → two numbers. `make metric-a-defined` adds a definition file → one number.
- Every target pre-warmed before the talk; every demo has a screen recording in `demos/recordings/` as fallback.
