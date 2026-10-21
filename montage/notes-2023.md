# Notas de la grabación de julio 2023 (The Data Pub)

Fuente: `montage/src/2023.mp4` (640x360, 66 min, no se commitea). Transcripción con mlx-whisper large-v3-turbo (es), en `montage/work/` (gitignored). Los timestamps son mm:ss del video. Whisper deforma nombres: "DogDB/DocDB" = DuckDB, "Regan/Rigging" = Riggan, "Mike Scheiner" = Mike Shiner, "Haduk" = Hadoop. Los primeros ~3 min son música/pre-roll; la charla empieza en 3:08. La charla se llama "Modern Data Stack, o la virtud inesperada de la ignorancia" (3:58–4:02). Slide del título: pájaro de Birdman con el logo de Postgres y de DuckDB como cabezas.

## 1. Hot takes de 2023 (pandas, perros, Santos)

**No aparecen en esta grabación.** Se buscó "pandas", "perro(s)", "santos" y "hot take" en toda la transcripción (sin resultados). Lo más cercano a una opinión: "la realidad que nadie les va a decir, y yo sí, y esta es mi opinión, es que esto es marketing" (43:06–43:11) y "no creo que sea buena idea migrar porque es nuevo" (57:23–57:35). El PLAN.md §3 slide 3 ("Hot takes callback: pandas, perros, Santos") debe venir de otra charla o de la memoria de Carlos; no hay cita verificable aquí. Sugerencia: confirmar con Carlos o quitar la referencia a la grabación.

## 2. Ejemplo mínimo: métricas A y B

Slide "Un ejemplo mínimo" (desde ~13:07). Sitio de gestión de proyectos tipo Linear ("el sitio es Linear", 13:44).

- Hablado (13:21–13:41): "Busca calcular dos métricas solamente. La primera métrica es la **frecuencia promedio en días de los que un cliente está usando el producto en el último año**. La frecuencia simplemente, si yo lo uso diario, mi frecuencia es de 1. La segunda es **cuántas veces un cliente ha visitado la página de documentación del producto**."
- Texto en el slide (visible en `assets/2023/stills/04-anadirle.jpg`): "A. Frecuencia promedio en días de los clientes suscritos en el último año. B. Cuántas veces un cliente ha visitado la página de documentación del producto."
- Pregunta: "¿Cuánto tiempo te toma calcular estas dos métricas?" (14:04). Tira de Skate: "¿Puedes solo añadirle…? Porque responder tu pregunta puede ser fácil o muy, muy difícil" (15:17–15:24; slide: "¿Puedes solo añadirle ... ? / Porque responder tu pregunta puede ser fácil. / O muy, muy difícil.").
- Estimaciones habladas: A y B en el modelo semántico: "yo diría 5 minutos" (15:57; ya hay tablero, "esperar a que el café se caliente"); sin capa visual: "más o menos un día" (16:27); A en el modelo semántico y B en datos limpios: A "mediodía", B "una semanita y dos personas" (17:00–17:06); B en el sistema fuente: "no veo pasar esto en menos de tres meses y cinco más personas" (17:30–17:34). Slide final: "A aquí 0.5 días", "B aquí 3 meses, 5+ personas".
- Remate: "¿Cuánto tiempo te toma? Depende. Soy economista, entonces tenía que decirlo" (17:50–17:58).
- Viñeta del comic (14:17–14:39): "simplemente checa si está en un parque nacional" → "ok, rápido" / "necesito que diga si la foto es de un pájaro" → "voy a necesitar un equipo de investigación y 5 años".

## 3. Birdman, Riggan y Mike

- 8:01 "Tercero, cine." 8:16 "Esta película se llama Birdman… se ganó cuatro estatuillas (mejor película, fotografía, guión original, director) … Alejandro González Iñárritu, orgullosamente mexicano."
- 9:04–9:17 "Quiero presentarles dos personajes de la película. El primero es **Riggan Thomson**: piensen qué hubiera pasado si Robert Downey Jr. hubiera dicho 'ya no quiero seguir haciendo Iron Man' y me hubiera gustado hacer algo más de arte."
- 9:50 "Riggan tiene gran promesa y fama en papeles de juguete o papeles poco serios. No tienen ningún tipo de garantía de éxito ni años de carrera por delante."
- 10:01 "¿Quién es su contraparte? **Mike Shiner** [sic: Scheiner en la transcripción]… un actor de método, puritano… tiene garantía de calidad: tú le subes a un escenario y te va a dar lo mejor… El problema es que tiene una gran complejidad. Es un tipo con muchísimos vicios." 10:37 "estos cuates se enfrentan una y otra vez. A veces en calzones."
- 10:57–11:13 "el actual escenario es muy similar a cómo se enfrentan estos dos papeles. De un lado Riggan, su carita tiene DuckDB enfrente, y al otro lado Mike Shiner, con Spark." 11:20 Dagster vs Airflow, Rill vs Power BI. 11:49 "años, décadas de garantía de entrega. Gran complejidad" (Airflow: "no aparece su DAG en el DAG bag"). 12:06 "Modern Data Stack, ¿qué lado escogemos?"
- 20:10–20:26 vuelve a la obra de Raymond Carver: "What do we talk about when we talk about love?" → "…about modern?". 31:25 "podemos ponerlo en Riggan y en Mike otra vez… no".
- Cierre (43:23–45:25): "¿se acuerdan de nuestros buenos amigos, Riggan y Mike? … no se caen muy bien, uno es un actor de método y el otro un actor farandulero… pero actúan en la misma obra." 44:55 "Riggan tomó todas las decisiones erróneas al momento de montar su obra. Todas. Inclusive hay un crítico que le dice 'ni te me acerques'. Aun así triunfó." Slide: "Riggan tomó todas las decisiones erróneas al momento de montar su obra. Aun así, triunfó…" (con "Un data dev puede tomar… stack… triunfar" escrito encima en rojo).

## 4. Línea de cierre exacta

45:07–45:25: "déjenme modificarlo: un data dev, uno de nosotros, un ingeniero de datos, cualquier persona que inclusive esté comenzando en esto **puede tomar todas las decisiones erróneas al momento de montar su stack, y aún así, yo argumento, puede triunfar.** Muchas gracias." (aplausos 45:25). Antes (44:00–44:17): "a pesar de que son términos de marketing… a pesar de que es complejo realmente evaluar un cambio de stack, sí hay una virtud inesperada de no conocerlo a fondo, o de poderlo tratar por primera vez." Luego Q&A hasta ~62:00.

## Otros momentos útiles

- Título/charla: 3:56–4:04. Slide con DuckDB: 3:56 "el de enfrente es DuckDB".
- Primera versión de la charla (4:07–4:32): compresión Postgres vs DuckDB "21 GB contra 1.7 GB"; query "Postgres corre en 6 minutos, DuckDB en 1.87 segundos".
- Nokia (21:38–21:57): "este celularcito, en 2016 [slide dice 2006], es el Nokia N95, 5 megapíxeles… el siguiente, el iPhone primera generación, 2 megapíxeles… el primer Android, el HTC, 3.15 megapíxeles". 22:19 "lo moderno no es lo más avanzado". Sesgo 2 (autos, QWERTY, bash/teletype): 22:33–25:50, conclusión 25:49 "la ingeniería y el diseño no progresan de forma lineal, progresan en ciclos".
- Retadores (30:58–34:04): Google 2003 "SQL doesn't scale" → Hadoop (2006) vs Oracle/Teradata/IBM ("el CEO de Oracle… se compró una isla") 31:08–31:51; "¿alguien usa Hadoop?… luego vino Spark" 31:58–32:09 (Matei Zaharia, Databricks); "Hadoop salió en 2006, Spark en 2014" 34:50; Hannes Mühleisen propuso DuckDB, "un sistema de un solo nodo" 33:36–33:44; "ahora el establecido es Spark, y quien viene como challenger… es DuckDB" 33:54–34:03.
- Pregunta del millón (34:23–35:44): "¿qué hubiera pasado si hubiéramos migrado a Hadoop en cuanto salió?… o por ignorancia o por análisis nos hubiéramos ahorrado un salto en un stack". Cita de Kill It with Fire (Marianne Bellotti), 36:10: "debes evitar migrar a una nueva tecnología simplemente porque es nueva; esa es la razón equivocada". "Depende" 36:39.
- Marketing (42:06–43:20): Amit Prakash, "¿qué hace que un software sea parte del MDS?" (easy to try/deploy, massive scalability, composable). "La realidad que nadie les va a decir… esto es marketing" 43:06–43:11; sello MARKETING en el slide desde ~43:12. DuckDB y MotherDuck (Jordan Tigani) no aparecen en moderndatastack.xyz: 43:19–43:52.
- Q&A: "el plan de migración más corto de una base de datos on-prem a Snowflake es de 3 años" (58:49–59:00; de chamba, lo evaluó él). Uber/Netflix migraron y regresaron (48:05–48:19). Se presenta como economista ("Soy economista", 17:54).

## Recap v2 (oct 2026)

Beat sheet, cortes y líneas en vivo: `montage/RECAP.md`. Momentos nuevos que v1 no usaba: "no sé quién sí haya hecho una migración de stack… lo compadezco y lo abrazo, es horrible" (5:52–6:00), "y que no sabemos si puede hacer algo en producción" (34:00), Q&A "no creo que sea buena idea migrar porque es nuevo" (57:30), "el plan de migración más corto… a Snowflake es de 3 años, en este caso" (58:53) y el cierre del Q&A "va a ser interesante si esto cambia de raíz, pero no ha cambiado en 40 años" (53:42). Timestamps por palabra: `montage/words.tsv` (whisper con contexto + envolvente de audio; los tiempos de whisper derivan hasta ~0.4 s aquí).

## Cómo se encontraron los cues

`uvx --from mlx-whisper mlx_whisper audio.wav --model mlx-community/whisper-large-v3-turbo --language es --condition-on-previous-text False`. La corrida única sobre los 66 min alucina ("¡Suscríbete al canal!", "bla bla…") en la música y en el tramo 38:38–45:27; se re-transcribieron por partes (0–21:30 y 38:00–fin) con `--condition-on-previous-text False`. Reconstruir el corte: `montage/make.sh` (lee `montage/cues.tsv`).
