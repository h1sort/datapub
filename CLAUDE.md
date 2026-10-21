# datapub — Carlos Haro's talks at The Data Pub

Current talk: **Post-AI Data Stack** (Oct 21, 2026). Read `PLAN.md` first; it is the source of truth for structure, timing and phases.

## Working rules
- Work phase by phase as listed in `PLAN.md` §2. Don't start a phase before the previous one is shippable.
- The deck never depends on a demo or video: every [D#]/[M] slot keeps a static fallback. Later phases replace fallbacks; they never add slides.
- Slide text is in Spanish. Code, file names and commit messages in English.
- Every number on a slide needs a source in `PLAN.md` §6, or it gets cut.
- ≤ 6 proper nouns (tools, vendors) per act.
- Never commit video. `montage/src/` is gitignored; keep outputs ≤ 30 MB.

## Lessons from Carlos's previous talks (apply them)
- He over-scopes and the ending gets rushed. The last 5 slides are protected; cut from Act 3 instead.
- His best moment is a confident wrong answer built on real data, then fixed.
- Live demos have failed on quotas, network and missing files. Scripted `make` targets + recorded backups only.

## Publishing to h1sort.com/datapub
The site (`~/Code/h1sort-website`, Astro + Worker static assets) holds a generated public copy in `public/datapub/`. Never edit the deck there.
1. Commit and push the deck here first.
2. In the site repo: `git checkout main && git pull`, new branch, then `~/Code/datapub/deck/tools/public-build.py public/datapub` (strips speaker notes; fails if any remain). `npm ci && npm run build`.
3. Smoke test: `npx wrangler dev --port 8799`; `/datapub` → 307, `/datapub/` → 200, other decks still 200. Stop it by PID, not `pkill -f`.
4. Commit only `public/datapub` (plus `astro.config.mjs` / `public/llms.txt` if changed). Any branch push deploys production; open the PR and merge it the same day.
5. The recap video is a static asset (Workers limit: 25 MiB per file). If a re-edit goes over, move it to R2 and pass `--video-url`. R2 isn't enabled on the account yet.
