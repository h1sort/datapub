# "Anteriormente en The Data Pub…" · v2 beat sheet

`montage/out/anteriormente.mp4` · 105.4 s · 1920×1080 · 30 fps · H.264 High + AAC · 24.7 MB · −16.0 LUFS (−1.3 dBTP).
Rebuild: `montage/make.sh` (edit list in `cues.tsv`, caption words in `words.tsv`). v1 backup: `montage/work/anteriormente-v1.mp4`.

**The idea.** The recap is a set of confident 2023 bets: *"esto es marketing"*, *"DuckDB, de juguete"*, *"migrar cuesta años"*, *"5 minutos o 3 meses"*, *"puede triunfar"*. It ends on the cockiest one, from the Q&A: the stack *"no ha cambiado en 40 años"*. Then the only 2026 voice in the cut, two black cards labelled **THE DATA PUB · OCTUBRE 2026**: *"Tres años después."* / *"¿Sigue siendo cierto?"*. Carlos picks up live from there.

**Visual grammar.** Everything from 2023 is labelled **THE DATA PUB · JULIO 2023 · ▶ mm:ss** (the timestamp in the original recording, for provenance). Captions from 2023 are ALL CAPS, word by word, with the active word in amber. The 2026 cards are sentence case on black, with no outline and a mono date label, so they can never be read as a 2023 quote.

## Music (v3)

An original trailer score, synthesized by `score.py`, so there's no licensed music and no Content ID claim on the stream. It's placed from `captions.ass`, so it stays in sync after a re-cut. A Birdman-style jazz-drum version was tried and dropped because it didn't blend.
- **Silence** under the hook: "esto es marketing" lands dry. The score enters with a braam and taiko boom on **THE DATA PUB · JULIO 2023**.
- **Pulse:** an 8th-note pulse in D minor that thickens act by act (i–VI–III–VII after JUGUETE, an octave layer after 3 MESES).
- **Hits:** taiko hits on every slam word, with a lift into **TRIUNFAR**.
- **Cliffhanger:** near-silence, a heartbeat and a riser (kept above 3 kHz so it doesn't cover "no ha cambiado en 40 años"), then a braam on **40 AÑOS**. A final unresolved braam (A over D) lands on **¿Sigue siendo cierto?**.

Mix: the bed is at about −21 LUFS before ducking and drops about 16 dB under the voice (sidechain on the speech), coming back up in the gaps. In the 300–4000 Hz speech band the voice sits a median 33 dB above the music, and every spoken word clears 6 dB. Final −16 LUFS. The no-music cut is kept at `work/v2/nomusic.mp4`.

## Beats

Out = time in the recap. Src = time in the 2023 recording (talk 3:08–45:25, Q&A after).

| # | Out | Src | Quote (his words, as captioned) | Why it's in | Sets up tonight |
|---|---|---|---|---|---|
| 1 | 0:00 | 43:06.6–43:12.4 | "La realidad que nadie les va a decir, y yo sí, y esta es mi opinión, es que esto es **marketing**." | The hook: the cockiest line of the talk, and the red MARKETING stamp lands on the word. Hit on the stamp. | Slide 4 (#1) → slide 5 ✅ *"MDS era marketing: ya ni lo decimos"*. |
| — | 0:05.8 | card | ANTERIORMENTE EN / **THE DATA PUB** / JULIO 2023 | Series stamp, after the hook rather than before it. Hit. | Episode framing (slide 2, *Episodio 2*). |
| 2 | 0:07.6 | 3:58.6–4:02.4 | "La plática se llama Modern Data Stack, o la virtud inesperada de la ignorancia." | Names the 2023 thesis. Punch-in on the Birdman title slide. | Closing line (28): *"la ignorancia se cura en una tarde"*; slide 15. |
| 3 | 0:11.5 | 9:50.3–9:55.8 | "Riggan tiene gran promesa y fama en papeles de juguete o papeles poco serios." | Introduces Riggan and the word *juguete*. | Birdman callback (28); the DuckDB "juguete" bet. |
| 4 | 0:17.0 | 11:05.1–11:13.6 | "De un lado tenemos a Riggan… su carita tiene a DuckDB enfrente. Y del otro lado tenemos a Mike Shiner, teniendo a Spark…" | The matchup. Snap zooms onto each fighter. | DuckDB vs. the incumbent (5 ✅ DuckDB). |
| 5 | 0:25.5 | 21:40.2–21:43.4 | "Es el Nokia N95, tiene una cámara de 5 megapíxeles." | Setup of the Nokia gag. | — |
| 6 | 0:28.7 | 21:51.1–21:56.8 | "El siguiente celular no es nada más y nada menos que el iPhone, primera generación. Tiene una cámara de **2 megapíxeles**." | Punchline. Zoom onto the slide's "5MP / 2MP" labels. | Act 3: eras arrive late; "new ≠ better". |
| 7 | 0:34.3 | 22:19.3–22:21.4 | "Lo moderno no es lo más avanzado." | His thesis in five words. Face punch-in. | Act 5 "vive del hype" (*"migra todo porque ahora hay IA"*). |
| 8 | 0:36.5 | 31:58.4–32:00.2 | "¿Alguien usa Hadoop?" | One-line reminder that challengers win and incumbents die. | Cycles: Hadoop → Spark → DuckDB. |
| 9 | 0:38.3 | 33:54.1–34:04.0 | "Ahora el establecido es Spark, y quien viene como challenger, que está siendo usado otra vez en casos **juguete** y que no sabemos si puede hacer algo en producción, es DuckDB." | The bet he gets to win tonight, in its most doubtful form ("no sabemos si puede hacer algo en producción"). | 5 ✅ DuckDB; 24 *"formatos abiertos + DuckDB"*. |
| 10 | 0:48.2 | 15:19.1–15:23.8 | "¿Puedes añadirle solo…? Porque tu pregunta puede ser fácil o muy, muy difícil de responder." | The minimal example's catchphrase, zoomed on the slide text. | Act 2, slide 7. |
| 11 | 0:52.9 | 15:57.3–16:00.1 | "Yo diría… **5 minutos**." | Bottom rung of the ladder. | Slide 8 (5 min / 0.5 días / 3 meses). |
| 12 | 0:55.7 | 17:31.1–17:35.2 | "Ok, yo no veo pasar esto en menos de **3 meses** y cinco más personas." | Top rung. Snap zoom onto the red "3 meses 5+ personas" on the 2023 slide. | Slide 9: everything → *"≈ minutos"* → **"¿y es verdad?"** |
| 13 | 0:59.8 | 5:52.8–5:54.7 | "No sé quién sí haya hecho una migración de stack." | Sets up the migration pain. | — |
| 14 | 1:01.8 | 5:56.7–6:00.8 | "Quien sí lo haya hecho, lo compadezco y lo abrazo. Es **horrible**." | The funniest version of "migrating hurts". | 🔄 *"Migrar cuesta años"*. |
| 15 | 1:05.8 | Q&A 57:30.0–57:34.9 | "No creo que sea buena idea migrar porque es nuevo." | The advice (answering a question on Airflow → Dagster). The Bellotti *Kill It with Fire* slide is on screen. | The advice survives (5 🔄; 26 "migra todo porque hay IA"). |
| 16 | 1:10.7 | Q&A 58:53.9–59:01.0 | "El plan de migración más corto de una base de datos on-prem a Snowflake es de **3 años**, en este caso." | The *reason*, with his own number ("de chamba tuve que hacer una evaluación"). Kept "en este caso". | 5 🔄: *"eso ya no es cierto"* (Airbnb 6 semanas, Uber 4 meses). |
| 17 | 1:17.8 | 44:56.5–45:01.3 | "Riggan tomó todas las decisiones erróneas al momento de montar su obra. Todas." | The 2023 close begins. | 4 (#4) and 28. |
| 18 | 1:22.6 | 45:07.0–45:08.1 | "Aún así triunfó." | Fast and soft in the audio, but the slide shows the same words at that moment. | — |
| 19 | 1:23.7 | 45:11.8–45:13.0 | "Un data dev," | Subject of the rewrite. The slide is being rewritten in red. | — |
| 20 | 1:24.8 | 45:18.3–45:25.1 | "…puede tomar todas las decisiones erróneas al momento de montar su stack. Y aún así, yo argumento que puede **triunfar**." | The closing line of 2023, with zooms onto the red "stack" and "triunfar". | 28: *"en 2023 sus errores eran caros… hoy te cuesta meses."* |
| 21 | 1:31.6 | Q&A 53:12.3–53:16.0 | "Se sigue manteniendo la idea general del stack." | Context for the cliffhanger (Q&A: does the stack change by industry? Not even in a blood-centrifuge machine). | Slide 6: *"¿Cambió el stack, o cambió otra cosa?"* |
| 22 | 1:35.3 | Q&A 53:42.6–53:48.4 | "Va a ser interesante si esto cambia de raíz, pero no ha cambiado en **40 años**." | The cliffhanger: his most quotable bet, and the one tonight's thesis answers (the stack didn't win, it became invisible). | Acts 2–4. |
| — | 1:41.1 | card | THE DATA PUB · OCTUBRE 2026 / **Tres años después.** | 2026 voice, clearly labelled. Hit. Echoes "40 años". | — |
| — | 1:42.6 | card | THE DATA PUB · OCTUBRE 2026 / **¿Sigue siendo cierto?** (amber) | Last frame; the deck holds it on screen when the video ends. | Hand-off to Carlos live → scorecard. |

### What was trimmed inside a thought (meaning preserved)
- **13 + 14:** dropped the middle clause *"quién no haya hecho una migración de stack"* from the same sentence.
- **17–20:** dropped the critic line (*"hay un crítico que le dice: ni te me acerques"*), *"déjenme modificarlo"*, and the appositives *"uno de nosotros, un ingeniero de datos, cualquier persona que inclusive esté comenzando en esto"*. The subject stays "un data dev", which is exactly what the 2023 slide says in red.
- **21 + 22:** about 26 s apart in the same answer. In between he says the stack *"funciona y se puede modificar con base en las necesidades"*. "Esto" = the general idea of the stack.
- Nothing is reordered within a quote. Clips 15, 16, 21 and 22 come from the Q&A, and the on-screen timestamp shows it.

## Lines for Carlos, right after the video

1. "Ese tipo tan seguro de sí mismo era yo. Hace tres años, en este mismo escenario."
2. "Les dije que el Modern Data Stack era marketing, que DuckDB era un juguete y que migrar cuesta años. Y cerré con que el stack no ha cambiado en 40 años."
3. "Spoiler: algo sí cambió. Pero no fue el stack."
4. "Hoy me toca calificarme en voz alta. Y no todas las salvo."
5. "Y ahora sí: episodio dos."

## For Carlos to eyeball
- **Beat 18, "Aún así triunfó" (1:22.6).** It's quick and quiet. Whisper with context hears "aún así triunfó", and the slide shows it at that moment. Listen once.
- **Beat 10.** He said *"¿Puedes añadirle solo…?"*; the 2023 slide and the deck say *"¿Puedes solo añadirle…?"*. Captions follow the audio.
- **Length is 105 s.** Slide 1 has `time: 100` and the notes say "~2 min". The v1 notes still list the beats correctly (Birdman, Nokia/iPhone, Hadoop/Spark/DuckDB, ejemplo mínimo, marketing). The new items are the migration bit and "40 años".
- **Act 1 TODO.** The "3 años on-prem → Snowflake" number is now on video in his own words (Q&A 58:53, "en este caso"), which partly answers the TODO in the act1 notes.
- **Picture.** The face punch-ins are a 160 px camera panel upscaled about 12×. They're soft by nature (light grain added), so I kept them to short beats.
