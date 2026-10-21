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
