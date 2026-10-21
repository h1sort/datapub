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
5. The recap video lives in R2: bucket `h1sort-media`, key `datapub/anteriormente.mp4`, served at `https://media.h1sort.com/datapub/anteriormente.mp4` (R2 custom domain; range requests work, which iOS needs). Build with `--video-url https://media.h1sort.com/datapub/anteriormente.mp4`. After a re-edit, re-upload: `npx wrangler r2 object put h1sort-media/datapub/anteriormente.mp4 --file montage/out/anteriormente.mp4 --content-type video/mp4 --cache-control "public, max-age=86400" --remote` (`--remote` is required, or it writes to local dev storage). Cache is 1 day, so use a new key, e.g. `anteriormente-v3.mp4`, for an urgent swap.
