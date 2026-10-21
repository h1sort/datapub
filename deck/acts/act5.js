// Acts 5 + 6 (slides 24–29): valor real vs. hype, predictions, close. See CONTRACT.md.
Deck.css(`
.a5-list { list-style: none; margin: 0; padding: 0; }
.a5-list li { display: grid; grid-template-columns: 110px 1fr; align-items: baseline; padding: 22px 0; border-top: 2px solid var(--hair); }
.a5-list li:last-child { border-bottom: 2px solid var(--hair); }
.a5-list .n { font-family: var(--mono); font-size: 24px; letter-spacing: 0.2em; color: var(--accent); }
.a5-list .tx { font-size: 42px; line-height: 1.2; letter-spacing: -0.01em; }
.a5-list .tx small { display: block; margin-top: 8px; font-family: var(--mono); font-size: 24px; letter-spacing: 0.06em; color: var(--dim); }
.a5-head { margin-bottom: 36px; }
.a5-head .t-label { margin-bottom: 18px; }
.a5-head h2 { margin: 0; font-size: 84px; font-weight: 500; letter-spacing: -0.025em; line-height: 1.05; }

/* 25: horror story */
#s-no-todo-llm { padding-top: 96px; }
#s-no-todo-llm .trail { position: absolute; left: 120px; right: 120px; top: 96px; display: flex; gap: 20px; flex-wrap: wrap; }
#s-no-todo-llm .stagebox { position: absolute; left: 120px; right: 120px; top: 190px; bottom: 150px; display: flex; flex-direction: column; justify-content: center; }
#s-no-todo-llm .panel { position: absolute; inset: 0; display: flex; flex-direction: column; justify-content: center; }
#s-no-todo-llm .big { font-size: 280px; font-weight: 500; letter-spacing: -0.045em; line-height: 0.95; margin: 0; }
#s-no-todo-llm .big.xl { font-size: 340px; }
#s-no-todo-llm .big.md { font-size: 200px; }
#s-no-todo-llm .cap { font-size: 44px; color: var(--dim); margin-top: 28px; line-height: 1.25; max-width: 1400px; }
#s-no-todo-llm .cap b { color: var(--fg); font-weight: 500; }
#s-no-todo-llm .two { display: grid; grid-template-columns: 1fr 1fr; gap: 80px; align-items: end; }
#s-no-todo-llm .pun { font-size: 120px; font-weight: 500; letter-spacing: -0.035em; line-height: 1.02; margin: 0; }
#s-no-todo-llm .bench { display: flex; gap: 56px; margin-top: 48px; align-items: baseline; font-family: var(--mono); }
#s-no-todo-llm .bench .v { font-size: 64px; }
#s-no-todo-llm .bench .k { font-size: 22px; letter-spacing: 0.22em; text-transform: uppercase; color: var(--dim); display: block; margin-bottom: 8px; }
#s-no-todo-llm .src { position: absolute; left: 0; bottom: 0; }

/* 27: predictions */
#s-predicciones-2029 .a5-list .tx { font-size: 36px; line-height: 1.22; }
#s-predicciones-2029 .a5-list li { padding: 17px 0; }
#s-predicciones-2029 .a5-list .tx small { font-size: 22px; margin-top: 6px; }
#s-predicciones-2029 .a5-head h2 { font-size: 64px; }
#s-predicciones-2029 .a5-head { margin-bottom: 20px; }
#s-predicciones-2029 .vf { position: absolute; inset: 40px; pointer-events: none; }
#s-predicciones-2029 .vf i { position: absolute; width: 90px; height: 90px; border: 0 solid var(--accent); }
#s-predicciones-2029 .vf i:nth-child(1) { left: 0; top: 0; border-width: 4px 0 0 4px; }
#s-predicciones-2029 .vf i:nth-child(2) { right: 0; top: 0; border-width: 4px 4px 0 0; }
#s-predicciones-2029 .vf i:nth-child(3) { left: 0; bottom: 0; border-width: 0 0 4px 4px; }
#s-predicciones-2029 .vf i:nth-child(4) { right: 0; bottom: 0; border-width: 0 4px 4px 0; }
#s-predicciones-2029 .shotlbl { position: absolute; right: 120px; top: 96px; }
#s-predicciones-2029 .shotlbl span { display: inline-block; background: #000; border: 2px solid var(--accent); border-radius: 999px; padding: 14px 36px;
   font-family: var(--mono); font-size: 32px; letter-spacing: 0.25em; text-transform: uppercase; color: var(--accent); }
#s-predicciones-2029[data-at="6"] .a5-list > li { opacity: 1 !important; } /* room photo: all five bright */
#s-predicciones-2029 .a5-list { transition: opacity 0.5s var(--ease); }

/* 28: closing */
#s-cierre-birdman .ln1, #s-cierre-birdman .ln2 { font-size: 64px; line-height: 1.18; letter-spacing: -0.015em; max-width: 1500px; margin: 0; font-weight: 400; transition: opacity .5s var(--ease), color .5s; }
#s-cierre-birdman .ln3 { font-size: 112px; line-height: 1.04; letter-spacing: -0.03em; font-weight: 500; max-width: 1600px; margin: 0; }
#s-cierre-birdman .gap { height: 56px; }
#s-cierre-birdman[data-at="1"] .ln1 { opacity: 0.65; }
#s-cierre-birdman[data-at="2"] .ln1, #s-cierre-birdman[data-at="2"] .ln2 { opacity: 0.55; }
#s-cierre-birdman .yr { font-family: var(--mono); font-size: 24px; letter-spacing: 0.3em; color: var(--accent); display: block; margin-bottom: 14px; }

/* 29: thanks */
/* same 2×2 QR grid as who_is_this_dude, for the back of the room */
#s-gracias .qrs { position: absolute; right: var(--pad-x); top: var(--pad-y); display: grid; grid-template-columns: repeat(2, 360px); gap: 24px 40px; }
#s-gracias .qr { text-align: center; }
#s-gracias .qr .tile { width: 360px; height: 360px; padding: 22px; border-radius: 20px; background: #fff; }
#s-gracias .qr img { width: 100%; height: 100%; display: block; image-rendering: pixelated; }
#s-gracias .qr .u { margin-top: 12px; font-family: var(--mono); font-size: 26px; color: var(--fg); }
#s-gracias .url { font-family: var(--mono); font-size: 52px; letter-spacing: 0.01em; margin-top: 36px; }
#s-gracias .who { margin-top: 56px; line-height: 1.5; }
`);

const LI = (n, tx, sm, step) => `<li data-step="${step}"><span class="n">${n}</span><span class="tx">${tx}${sm ? `<small>${sm}</small>` : ''}</span></li>`;

Deck.act(5, 'Acto 5 · Valor real vs. hype', [
  {
    id: 'valor-real',
    title: 'Aporta valor real',
    time: 60,
    class: 'middle',
    particles: { shape: 'grid', opacity: 0.16 },
    html: `
      <div class="a5-head"><div class="t-label">Acto 5 · cinco señales</div><h2>Aporta <em>valor real</em></h2></div>
      <ul class="a5-list focus-last">
        ${LI('01', 'Definiciones con <em>dueño</em> y versión', 'capa semántica', 1)}
        ${LI('02', 'Herramientas que <em>cualquier agente</em> puede operar', 'APIs · MCP', 2)}
        ${LI('03', 'Evals que leen <em>trazas</em>, no solo respuestas', '', 3)}
        ${LI('04', 'Formatos <em>abiertos</em> + DuckDB', '', 4)}
        ${LI('05', 'Clasificadores <em>tipados</em> cuando la pregunta es un juicio, no un texto', 'Jev', 5)}
      </ul>`,
    notes: `
      <p>Ok, ya les conté qué cambió. Ahora la pregunta incómoda: ¿qué de todo este ruido sí vale la pena? Yo me fijo en cinco cosas, y ninguna es un modelo nuevo.</p>
      <p>Uno: definiciones con dueño y versión. Es lo de la métrica A: si nadie es dueño de qué es "suscrito", el agente inventa. Dos: herramientas que cualquier agente pueda operar, o sea APIs, MCP, lo aburrido. Tres: evals que leen las trazas, no solo la respuesta final, porque una respuesta correcta por la razón equivocada es una bomba de tiempo.</p>
      <p>Cuatro: formatos abiertos y DuckDB. Si tus datos están en un formato que cualquier herramienta lee, no te casas con nadie. Y cinco, que es la que me tiene obsesionado esta semana: clasificadores tipados cuando la pregunta es un juicio y no un texto. Y para esa les voy a contar una historia de terror.</p>
      <p class="dir">[Un click por cada punto. En el cinco, esperar un segundo antes de pasar.]</p>`,
  },
  {
    id: 'no-todo-llm',
    title: 'No todo necesita un LLM',
    time: 100,
    class: '',
    steps: 5,
    particles: [{ shape: 'swarm', opacity: 0.18 }, { shape: 'swarm', opacity: 0.18 }, { shape: 'swarm', opacity: 0.18 }, { shape: 'swarm', opacity: 0.18 }, { shape: 'swarm', opacity: 0.18 }, { shape: 'swarm', opacity: 0.18 }],
    html: `
      <div class="trail">
        <span class="chip" data-step="2">250 mil títulos</span>
        <span class="chip" data-step="3">NULL · reintento / 30 min</span>
        <span class="chip" data-step="4">2 semanas</span>
        <span class="chip" data-step="5">tokens · créditos</span>
      </div>
      <div class="stagebox">
        <div class="panel" data-step-only="0">
          <div class="t-label" style="margin-bottom:28px">Una historia de terror · Snowflake AI_CLASSIFY</div>
          <h2 class="t-hero" style="font-size:150px">No todo necesita <em>un LLM</em></h2>
        </div>
        <div class="panel" data-step-only="1">
          <p class="big xl">~250 mil</p>
          <p class="cap"><b>títulos de puesto</b> por clasificar en persona y función.</p>
        </div>
        <div class="panel" data-step-only="2">
          <p class="big xl"><em>NULL</em></p>
          <p class="cap">Un bug devuelve vacíos. El reintento <b>los manda otra vez al modelo, cada 30 minutos</b>. En dev.</p>
        </div>
        <div class="panel" data-step-only="3">
          <p class="big xl">2 semanas</p>
          <p class="cap">Reintentando <b>cada 30 minutos</b>. En un ambiente de dev.</p>
        </div>
        <div class="panel" data-step-only="4">
          <p class="big md">~44 mil millones</p>
          <p class="cap" style="margin-top:8px;font-size:56px"><b>de tokens</b></p>
          <p class="big md" style="margin-top:40px"><em>~61,600</em></p>
          <p class="cap" style="margin-top:8px;font-size:56px"><b>créditos</b></p>
        </div>
        <div class="panel" data-step-only="5">
          <p class="pun">Un clasificador tipado hace <em>casi</em> el mismo trabajo por <em>centavos</em>.</p>
          <div class="bench">
            <span><span class="k">4 mil títulos · Jev</span><span class="v accent">$0.16</span></span>
            <span><span class="k">el LLM</span><span class="v">$11–21</span></span>
            <span><span class="k">coinciden (persona)</span><span class="v">88%</span></span>
          </div>
        </div>
      </div>
      <div class="cite foot" style="left:120px">ASTRONOMER · "WHAT JEV WILL DO TO DATA ENGINEERING" · SEP 2026</div>`,
    notes: `
      <p>Esta es una historia real, de gente de Astronomer, y me la robo porque es perfecta. Tenían que clasificar unos 250 mil títulos de puesto: persona y función. Fueron directo al LLM con AI_CLASSIFY de Snowflake.</p>
      <p>Un bug hizo que el modelo regresara NULL en algunas etiquetas. Y el código de reintento, muy servicial, mandaba cada NULL de vuelta al modelo cada media hora. En un ambiente de dev. Durante dos semanas.</p>
      <p>El resultado: unos 44 mil millones de tokens, como 61,600 créditos. Ojo, no les voy a decir pesos ni dólares, porque el artículo mismo no cuadra entre créditos y dólares; los tokens y los créditos sí están medidos.</p>
      <p>Y el remate: esa pregunta no era un texto, era un juicio con etiquetas fijas. Un clasificador tipado, Jev en su benchmark, hizo 4 mil títulos por 16 centavos de dólar; el LLM, entre 11 y 21 dólares. No es idéntico: coincidieron en 88% de las personas, y donde no coincidieron, las reglas escritas casi siempre le dieron la razón a Jev. Ahí está el punto: no todo necesita un LLM. Ahora, ¿quién te vende lo contrario?</p>
      <p class="dir">[Un click por número. Dejar que el silencio haga el trabajo en "2 semanas".]</p>`,
  },
  {
    id: 'vive-del-hype',
    title: 'Vive del hype',
    time: 60,
    class: 'middle',
    particles: { shape: 'scatter', opacity: 0.2 },
    html: `
      <div class="a5-head"><div class="t-label">Acto 5 · desconfía cuando…</div><h2>Vive del <em>hype</em></h2></div>
      <ul class="a5-list focus-last">
        ${LI('01', 'Un proveedor quiere que uses <em>su</em> agente', '', 1)}
        ${LI('02', 'Agentes conectados a datos crudos, <em>sin definiciones</em>', '', 2)}
        ${LI('03', '"Migra todo, <em>ahora hay IA</em>"', '', 3)}
        ${LI('04', 'Zombie reviews: <em>todos aprueban, nadie lee</em>', 'Gergely Orosz · LDX3 2026', 4)}
        ${LI('05', 'Su gemelo de datos: <em>zombie dashboards</em>', '', 5)}
      </ul>`,
    notes: `
      <p>Del otro lado está lo que vive del hype. Cuatro señales. Primera: el proveedor que quiere que uses su agente, y solo el suyo. Segunda: agentes pegados a datos crudos, sin definiciones; ya vimos qué pasa, dos respuestas seguras y distintas.</p>
      <p>Tercera: "migra todo porque ahora hay IA". Yo sigo creyendo lo de 2023: no migres por novedad. Cambió el costo de migrar, no la razón para hacerlo.</p>
      <p>Y la cuarta me la dejó Gergely Orosz: las zombie reviews. El código lo escribe un agente, lo "revisa" otro, y el humano le da aprobar sin leer. Todos aprueban, nadie lee. Y tiene un gemelo que conozco muy bien de la banca: los zombie dashboards. Alguien los hizo, todos los abren, nadie sabe de dónde sale el número.</p>
      <p>Bueno, ya que estamos en la zona de apuestas, hagamos unas.</p>
      <p class="dir">[Sonreír en "zombie dashboards": reconocimiento en la sala.]</p>`,
  },
  {
    id: 'predicciones-2029',
    title: 'Predicciones para el episodio 3 (2029)',
    time: 80,
    class: 'middle',
    particles: { shape: 'grid', opacity: 0.18 },
    html: `
      <div class="a5-head"><div class="t-label">Episodio 3 · 2029 · manos arriba</div><h2>Predicciones para <em>2029</em></h2></div>
      <ul class="a5-list focus-last">
        ${LI('01', 'Aprender un lenguaje de programación seguirá siendo útil.', 'ref: Gergely Orosz · LDX3 2026', 1)}
        ${LI('02', 'Todos van a necesitar habilidades de ingeniería y ciencia de datos.', 'ref: swyx', 2)}
        ${LI('03', 'La IA frenará temporalmente la contratación de talento nuevo, y se ajustará cuando quede claro que ser AI-native es una habilidad profunda.', 'ref: Gergely Orosz · LDX3 2026', 3)}
        ${LI('04', 'Los roles se reorganizan por arquetipo, no por función.', 'ref: Boris Cherny', 4)}
        ${LI('05', 'Democratización de stacks: competencia feroz y proveedores de datos convertidos en commodity.', '', 5)}
      </ul>
      <div data-step="6"><div class="vf"><i></i><i></i><i></i><i></i></div><div class="shotlbl"><span>Foto del público</span></div></div>`,
    notes: `
      <p>Les propongo un trato: cinco apuestas para el episodio 3, en 2029. Después de cada una levantan la mano si creen que sí, y en 2029 les calificamos a todos, incluido yo.</p>
      <p>Una: aprender un lenguaje de programación seguirá siendo útil. Gergely lo dice: los patrones viejos se redescubren y las palabras correctas hacen que el agente escriba mejor código. Dos: todos van a necesitar habilidades de ingeniería y ciencia de datos; swyx escribió hace dos días que los data engineers valen más que los AI engineers.</p>
      <p>Tres: la IA frenará la contratación de gente nueva, y se ajustará cuando quede claro que ser AI-native es una habilidad profunda. Cuatro: los roles se reorganizan por arquetipo, no por función; Boris Cherny habla de cinco. Cinco: democratización de stacks, competencia feroz y proveedores de datos como commodity.</p>
      <p class="dir">[Manos arriba después de cada predicción; contar en voz alta. Al final: levantar el celular y tomar la foto del público. Esa foto se califica en 2029.]</p>`,
  },
]);

Deck.act(6, 'Cierre', [
  {
    id: 'cierre-birdman',
    title: 'Birdman · el criterio',
    time: 90,
    class: 'middle',
    particles: { shape: 'scatter', opacity: 0.3 },
    html: `
      <div class="t-label" style="margin-bottom:44px">Birdman · Riggan · The Data Pub</div>
      <p class="ln1"><span class="yr">2023</span>En 2023 les dije que la ignorancia tenía una virtud inesperada.</p>
      <div class="gap"></div>
      <p class="ln2" data-step="1"><span class="yr">2026</span>En 2026 la ignorancia se cura en una tarde.</p>
      <div class="gap"></div>
      <p class="ln3" data-step="2">Lo que no se cura en una tarde es <em>el criterio.</em></p>`,
    notes: `
      <p>Y vuelvo adonde empecé. En 2023 les hablé de Birdman, de Riggan, que podía tomar todas las decisiones equivocadas y aun así triunfar. Les dije que la ignorancia tenía una virtud inesperada.</p>
      <p>En 2026, la ignorancia se cura en una tarde. Le preguntas a un agente y en minutos entiendes un stack que antes te tomaba meses.</p>
      <p>Y lo que cambió con Riggan es esto: en 2023 sus errores eran caros. Una decisión equivocada de stack te costaba años. Hoy te cuesta meses. Lo que sigue siendo caro es no saber por qué estuvo mal.</p>
      <p>Lo que no se cura en una tarde es el criterio.</p>
      <p class="dir">[Tres clicks, pausa larga antes del último. No correr. Decir la última línea despacio, sin mirar la pantalla.]</p>`,
  },
  {
    id: 'gracias',
    title: 'Gracias',
    time: 30,
    class: 'middle',
    particles: { shape: 'scatter', opacity: 0.3 },
    html: `
      <div>
        <div class="t-label" style="margin-bottom:28px">Post-AI Data Stack · Episodio 2</div>
        <h2 class="t-hero" style="font-size:230px">Gracias</h2>
        <div class="url accent">h1sort.com/datapub</div>
        <div class="who t-small dim">Carlos Haro · The Data Pub · CDMX · 21 oct 2026</div>
      </div>
      <div class="qrs" data-step="1">
        <div class="qr"><div class="tile"><img src="../assets/qr-linkedin.svg" alt="QR LinkedIn"></div><div class="u">linkedin.com/in/h1sort</div></div>
        <div class="qr"><div class="tile"><img src="../assets/qr-x.svg" alt="QR X"></div><div class="u">x.com/h1sort</div></div>
        <div class="qr"><div class="tile"><img src="../assets/qr-github.svg" alt="QR GitHub"></div><div class="u">github.com/h1sort</div></div>
        <div class="qr"><div class="tile"><img src="../assets/qr-slides.svg" alt="QR slides"></div><div class="u">h1sort.com/datapub</div></div>
      </div>`,
    notes: `
      <p>Gracias. De verdad. Esto lo preparé con mucho cariño, y a los que me vieron en 2023 y volvieron: gracias por regresar.</p>
      <p>En h1sort.com/datapub van a encontrar las diapositivas y las fuentes de todo lo que cité. Los QR los llevan ahí, y a mi LinkedIn, X y GitHub. Nos vemos en 2029, con las manos arriba.</p>
      <p>Y ahora sí, preguntas. Las dudas incómodas son las mejores.</p>
      <p class="dir">[Click para mostrar los 4 QR. Dejarlos en pantalla durante todo el Q&A.]</p>`,
  },
]);
