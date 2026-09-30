# Team workflow (5 people, each with their own AI assistant)

New here? Read `docs/TEAM_GUIDE.md` once. This file is the short command reference.

Your AI accounts don't share memory, so **the repo is the only shared brain**: `AGENTS.md`,
`ROADMAP.md`, `docs/PROGRESS.md`, and the graphify graph.

## One-time setup
```bash
git clone <repo-url> && cd LucidForm
python -m venv .venv && .venv/Scripts/pip install -r requirements.txt    # POSIX: .venv/bin/pip
cp .env.example .env              # add GEMINI_API_KEY for live runs only
.venv/Scripts/python -m pytest    # expect all green, offline

pip install uv && uv tool install graphifyy
graphify install --project        # registers the /graphify skill for this repo
graphify hook install             # rebuilds the graph on every commit (AST only, free)
git config alias.gpull '!git pull && graphify update .'
```

## Per phase
```bash
git switch main && git gpull
git switch -c phase-9-hindi               # branch name matches the ROADMAP row
# ...work, committing small and often...
.venv/Scripts/python -m pytest            # must be green
# append an entry to docs/PROGRESS.md
git push -u origin phase-9-hindi          # open a PR; someone else reviews and merges
```
- Claim the phase in `ROADMAP.md` first.
- After a merge: `git switch main && git gpull`, then `git rebase main` on your branch.
- `graph.json` conflicts resolve themselves (graphify merge driver). In `PROGRESS.md`, keep both entries.
- No AI co-author lines in commits.

## Handing off to another AI
"Read AGENTS.md, the last two entries of docs/PROGRESS.md, and graphify-out/GRAPH_REPORT.md,
then continue phase N." That is enough context to carry on.
