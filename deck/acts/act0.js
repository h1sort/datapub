// Act 0 · Cold open (180 s): slides 1-3. See CONTRACT.md.
(() => {
  Particles.fromText('a0-two', '2', { size: 1150, x: 1430, y: 560, step: 4 });

  const STILLS = [
    ['01-birdman.jpg', 'Birdman'],
    ['02-nokia.jpg', 'Nokia 5MP vs iPhone 2MP'],
    ['03-retadores.jpg', 'Hadoop → Spark → DuckDB'],
    ['04-anadirle.jpg', '¿Puedes solo añadirle…?'],
    ['05-marketing.jpg', 'esto es marketing'],
  ];
  const stillsHtml = STILLS.map(([f, cap], i) => `
    <figure class="a0-still" data-k="${i + 1}">
      <div class="frame a0-fr">
        <img src="../assets/2023/stills/${f}" alt="" onerror="this.parentNode.classList.add('noimg');this.remove()">
        <span class="a0-num mono">0${i + 1} / 05</span>
        <span class="a0-cap-in">${cap}</span>
      </div>
      <figcaption class="a0-cap-out">${cap}</figcaption>
    </figure>`).join('');

  Deck.css(`
    #s-cold-open .a0-wait { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; }
    #s-cold-open .a0-video { position: absolute; inset: 0; background: #000; }
    #s-cold-open video { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: contain; background: #000; }
    #s-cold-open .a0-fb { position: absolute; inset: 0; display: none; }
    #s-cold-open.a0-failed .a0-video { display: none; }
    #s-cold-open.a0-failed .a0-fb { display: block; }
    #s-cold-open .a0-head { position: absolute; top: 84px; left: 120px; }
    #s-cold-open .a0-still { position: absolute; left: 360px; top: 150px; width: 1200px; margin: 0;
      opacity: 0; transform: translateY(14px); transition: opacity 0.6s var(--ease), transform 0.6s var(--ease); }
    #s-cold-open .a0-fb[data-n="1"] .a0-still[data-k="1"],
    #s-cold-open .a0-fb[data-n="2"] .a0-still[data-k="2"],
    #s-cold-open .a0-fb[data-n="3"] .a0-still[data-k="3"],
    #s-cold-open .a0-fb[data-n="4"] .a0-still[data-k="4"],
    #s-cold-open .a0-fb[data-n="5"] .a0-still[data-k="5"] { opacity: 1; transform: none; }
    #s-cold-open .a0-fr { position: relative; width: 1200px; height: 675px; }
    #s-cold-open .a0-num { position: absolute; left: 24px; top: 20px; font-size: 20px; letter-spacing: 0.24em; color: var(--dim);
      background: rgba(0,0,0,0.6); padding: 4px 12px; border-radius: 8px; }
    #s-cold-open .a0-cap-in { display: none; }
    #s-cold-open .a0-cap-out { margin-top: 36px; text-align: center; font-size: 56px; letter-spacing: -0.01em; }
    #s-cold-open .a0-fr.noimg { display: flex; align-items: center; justify-content: center; border-color: var(--faint); }
    #s-cold-open .a0-fr.noimg .a0-cap-in { display: block; font-size: 84px; line-height: 1.1; text-align: center; padding: 0 80px; letter-spacing: -0.02em; }
    #s-cold-open .a0-fr.noimg + .a0-cap-out { display: none; }
    #s-cold-open .a0-ticks { position: absolute; left: 0; right: 0; bottom: 120px; display: flex; gap: 14px; justify-content: center; }
    #s-cold-open .a0-ticks i { width: 64px; height: 3px; background: var(--hair); transition: background 0.4s; }
    #s-cold-open .a0-fb[data-n="1"] .a0-ticks i:nth-child(-n+1),
    #s-cold-open .a0-fb[data-n="2"] .a0-ticks i:nth-child(-n+2),
    #s-cold-open .a0-fb[data-n="3"] .a0-ticks i:nth-child(-n+3),
    #s-cold-open .a0-fb[data-n="4"] .a0-ticks i:nth-child(-n+4),
    #s-cold-open .a0-fb[data-n="5"] .a0-ticks i:nth-child(-n+5) { background: var(--accent); }

    #s-title .a0-ep { margin-bottom: 36px; color: var(--accent); font-size: 28px; }
    #s-title .a0-name { font-size: 164px; font-weight: 500; line-height: 0.98; letter-spacing: -0.035em; margin: 0 0 56px; }
    #s-title .a0-q { font-size: 60px; line-height: 1.15; color: var(--fg); margin: 0 0 56px; max-width: 980px; }
    #s-title .a0-by { display: flex; gap: 28px; align-items: center; }
    #s-title .a0-by .bar { width: 64px; height: 2px; background: var(--faint); }

    #s-quien .a0-who-l { position: absolute; left: var(--pad-x); top: var(--pad-y); width: 1180px; }
    #s-quien .a0-name { font-size: 76px; font-weight: 500; letter-spacing: -0.02em; line-height: 1.05; }
    #s-quien .a0-role { font-size: 38px; margin-top: 14px; }
    #s-quien .a0-stats { display: flex; gap: 120px; margin-top: 64px; }
    #s-quien .a0-stats .big { font-size: 128px; font-weight: 500; letter-spacing: -0.03em; line-height: 1; }
    #s-quien .a0-stats .cap { font-size: 32px; color: var(--dim); margin-top: 12px; }
    #s-quien .a0-portrait { position: absolute; right: 150px; top: 150px; width: 440px; height: 440px; border-radius: 50%;
      overflow: hidden; border: var(--stroke) solid var(--faint); box-shadow: 0 0 0 14px #000, 0 0 0 16px var(--hair); }
    #s-quien .a0-portrait img { width: 100%; height: 100%; object-fit: cover; display: block; filter: grayscale(1); }
    #s-quien .a0-qrs { position: absolute; left: var(--pad-x); top: 676px; display: flex; gap: 56px; }
    #s-quien .a0-qr { text-align: center; }
    #s-quien .a0-qr .tile { width: 200px; height: 200px; padding: 16px; border-radius: 16px; background: #fff; }
    #s-quien .a0-qr img { width: 100%; height: 100%; display: block; image-rendering: pixelated; }
    #s-quien .a0-qr .t-label { margin-top: 14px; }
  `);

  Deck.act(0, 'Anteriormente', [
    {
      id: 'cold-open',
      title: '[M] Anteriormente en The Data Pub…',
      time: 100,
      class: 'bleed',
      particles: 'none',
      label: '',
      html: `
        <div class="a0-wait" data-step-hide="1"><span class="t-label">Anteriormente en The Data Pub…</span></div>
        <div class="a0-video" data-step="1">
          <video playsinline preload="auto" poster="../montage/out/poster.jpg" src="../montage/out/anteriormente.mp4"></video>
        </div>
        <div class="a0-fb" data-n="0">
          <div class="a0-head t-label" data-step="1">Anteriormente en The Data Pub… · Julio 2023</div>
          ${stillsHtml}
          <div class="a0-ticks" data-step="1"><i></i><i></i><i></i><i></i><i></i></div>
        </div>`,
      steps: 1,
      notes: `
        <p class="dir">[Pantalla negra. Esperar a que la sala se calle. Un clic: arranca el montaje de ~2 min. Si el video no carga, aparecen 5 stills con su frase, cada ~7 s; hablar encima.]</p>
        <p>Antes de empezar: "anteriormente en The Data Pub". Así como en las series, un recap. Hace tres años, en julio de 2023, estuve en este mismo evento con una plática que se llamaba "Modern Data Stack: la virtud inesperada de la ignorancia".</p>
        <p>Les dejo dos minutos de lo que dije entonces: Birdman, un Nokia contra un iPhone, Hadoop, Spark, DuckDB, y un ejemplo mínimo que nos tomó tres meses. Y, bueno, también la frase que me persigue: "esto es marketing".</p>
        <p>Si sale mal el video, no pasa nada, ya me conocen, se los cuento yo. Lo importante es que me acuerden en 2023 y luego me juzguen.</p>
        <p class="dir">[Al terminar el video: un clic.] Y ahora sí: episodio dos.</p>`,
      onEnter(el, ctx) {
        const st = el._a0 = { failed: false, timer: null, v: el.querySelector('video'), fb: el.querySelector('.a0-fb'), step: 0 };
        const fail = () => {
          if (st.failed) return;
          st.failed = true; el.classList.add('a0-failed');
          if (st.step >= 1) startSeq(el, ctx);
        };
        st.v.addEventListener('error', fail);
        // Missing file: some browsers only report on readyState after a tick.
        setTimeout(() => { if (st.v.error) fail(); }, 400);
      },
      onStep(el, step, ctx) {
        const st = el._a0; if (!st) return;
        st.step = step;
        if (step === 0) {
          stopSeq(el); st.v.pause(); try { st.v.currentTime = 0; } catch (e) {}
          return;
        }
        if (st.failed) { startSeq(el, ctx); return; }
        if (ctx.shot) return;
        const p = st.v.play();
        if (p && p.catch) p.catch(() => { if (!st.v.error) return; });
      },
      onLeave(el) { const st = el._a0; if (st) { stopSeq(el); st.v.pause(); st.step = 0; } },
    },
    {
      id: 'title',
      title: 'Post-AI Data Stack · Episodio 2',
      time: 30,
      class: 'middle',
      particles: [{ shape: 'scatter', opacity: 0.3 }, { shape: 'a0-two', opacity: 0.6 }],
      html: `
        <div class="t-label a0-ep">Episodio 2</div>
        <h1 class="a0-name">Post-AI<br>Data Stack</h1>
        <p class="a0-q" data-step="1">¿Qué cambió en la era de GPT?</p>
        <div class="a0-by t-label" data-step="1"><span>Carlos Haro</span><span class="bar"></span><span>The Data Pub</span><span class="bar"></span><span>21 oct 2026</span></div>`,
      notes: `
        <p class="dir">[Un clic para que aparezca la pregunta y las partículas formen el 2.]</p>
        <p>Bienvenidos al episodio dos. "Post-AI Data Stack". La pregunta de hoy es sencilla: ¿qué cambió en la era de GPT?</p>
        <p>En 2023 la pregunta era qué stack elegir. Hoy les voy a tratar de convencer de que esa pregunta dejó de ser la importante, y de que lo que sí cambió es otra cosa. Ya vamos a llegar.</p>
        <p>Ah, y los puntitos de fondo no son decoración: van a estar con nosotros toda la plática y van a decir cosas.</p>
        <p>Antes de seguir, una pregunta incómoda que seguro varios se hacen: ¿y este quién es?</p>`,
    },
    {
      id: 'quien',
      title: '¿Quién es este tipo?',
      time: 50,
      class: 'middle',
      particles: { shape: 'scatter', opacity: 0.2 },
      html: `
        <div class="a0-who-l">
          <h1 class="t-title">¿Quién es este tipo?</h1>
          <div class="a0-name">Carlos Haro</div>
          <div class="a0-role">Sr. AI Engineer · Santander <span class="dim">· servicios financieros</span></div>
          <div class="a0-stats">
            <div><div class="big">~10</div><div class="cap">años lidiando con datos</div></div>
            <div><div class="big">@h1sort</div><div class="cap">h1sort.com</div></div>
          </div>
        </div>
        <div class="a0-portrait"><img src="../assets/carlos-portrait.jpg" alt="Carlos Haro"></div>
        <div class="a0-qrs">
          <div class="a0-qr"><div class="tile"><img src="../assets/qr-linkedin.svg" alt="QR LinkedIn"></div><div class="t-label">LinkedIn</div></div>
          <div class="a0-qr"><div class="tile"><img src="../assets/qr-x.svg" alt="QR X"></div><div class="t-label">X</div></div>
          <div class="a0-qr"><div class="tile"><img src="../assets/qr-slides.svg" alt="QR slides"></div><div class="t-label">Slides</div></div>
        </div>`,
      notes: `
        <p>Para los que no me conocen: soy Carlos Haro, Sr. AI Engineer en Santander, servicios financieros. Llevo unos diez años lidiando con datos. En todos lados soy @h1sort.</p>
        <p>Hace tres años, cuando di la primera plática aquí, era consultor de datos. En el camino pasé por el SAT, por Bancomext y por una consultora, así que me ha tocado ver los datos desde varios lados de la mesa.</p>
        <p class="dir">[Dejar unos segundos para que escaneen: LinkedIn, X y las slides.]</p>
        <p>Les cuento esto porque lo que sigue es una calificación de mí mismo: voy a revisar qué dije en 2023 y qué tan mal me fue. Así que sí: toca el scorecard.</p>`,
    },
  ]);

  function startSeq(el, ctx) {
    const st = el._a0, fb = st.fb;
    stopSeq(el);
    if (ctx.shot) { fb.dataset.n = '5'; return; }
    let n = 1; fb.dataset.n = '1';
    st.timer = setInterval(() => {
      if (n < 5) { n++; fb.dataset.n = String(n); } else { clearInterval(st.timer); st.timer = null; }
    }, 7000);
  }
  function stopSeq(el) {
    const st = el._a0; if (!st) return;
    if (st.timer) clearInterval(st.timer); st.timer = null;
    st.fb.dataset.n = '0';
  }
})();
