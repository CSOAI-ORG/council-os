# STATE OF THE ESTATE — probed 2026-08-26

**Read this first, before any other ledger.** Every line carries a state tag proved in the
2026-08-26 probe run. `DSH-ALIGNMENT-BRIEF.md:13` pointed here at a file that did not exist; this is it.

Tags: **VERIFIED-LIVE** (a command returned the evidence shown) · **EXISTS-UNVERIFIED** (artifact
present, not exercised) · **CLAIMED-ONLY** (a doc asserts it, no artifact found) · **NOT-BUILT** (searched, absent).
Counts: 71 VERIFIED-LIVE · 14 EXISTS-UNVERIFIED · 13 CLAIMED-ONLY · 9 NOT-BUILT.

---

## 1. THE ONE-SCREEN ANSWER

The estate is a **measurement and attestation stack that works, attached to a delivery pipeline that
mostly does not.** councilof.ai serves a live signed 14-axis board (`/api/gspc`, 200, 26,236 b), a
191-server Council OS gateway answers on the 3090 pod behind an SSH tunnel (191 mounted / 184
runnable), a 103,286-chunk estate RAG is built, and the model harvest is durable on HF (171 files,
private). All VERIFIED-LIVE today.

What does not work is **landing**. 29 PRs sit open on councilof-ai. Four repos hold real committed
work on branches with **no upstream at all**. Two shipped surfaces are running dead (`/first-fine-watch/`
returns 200 while its `/api/fines` returns 404; `/api/specialists` 404 with its source commit
unreachable). The self-improving fix_loop — the estate's one genuine learning mechanism, with a real
+2.5 held-out promote on 2026-08-14 — has **not run a successful iteration in 10 days** and has no
cron and no live process.

**The single biggest gap: the estate measures honestly and builds constantly, but has no merge
discipline.** Nine parallel DSH lanes independently built five competing "living connections
databases" in five repos on the same day, and roughly half of all committed work in those sessions
was never pushed anywhere. Nothing is missing because it was hard. It is missing because it was
never merged.

---

## 2. LIVE SURFACES

| Surface | URL / endpoint | State | Evidence (this run) |
|---|---|---|---|
| Front site | `https://councilof.ai/` | VERIFIED-LIVE | 200, 238,638 b |
| Board API | `/api/gspc` | VERIFIED-LIVE | 200, 26,236 b, `csoai.gspc-axes/0.5`, `axes[]` len **14**, DOI `10.5281/zenodo.21991104` |
| Board lobby | `/?lobby=board` | VERIFIED-LIVE | 200, 238,638 b |
| Health | `/api/health` | VERIFIED-LIVE | 200, 215 b |
| Products | `/products/` | VERIFIED-LIVE | 308 → 200 (bare `/products` is a redirect, not a page) |
| GPAI evidence | `/gpai-evidence/` | VERIFIED-LIVE | 308 → 200 |
| Honesty | `/honesty/` | VERIFIED-LIVE | 308 → 200 |
| Regulator findings | `/regulator-findings/` | VERIFIED-LIVE | 308 → 200 |
| OG cards | `/api/og` | VERIFIED-LIVE | 200 (a DSH session found it returning **0 bytes**; status only re-checked here) |
| Receipts | `/api/receipts/latest` | VERIFIED-LIVE | 200 |
| **Specialists API** | `/api/specialists` | **NOT-BUILT (lost)** | **404** — source commit `5f0f8ab9` unreachable after a sibling reset; file absent from HEAD and disk |
| **Fines API** | `/api/fines` | **NOT-BUILT (lost)** | **404** — while `/first-fine-watch/` returns **200**. A live page with a dead back end. |
| Axes (bare) | `/axes` | NOT-BUILT | 404, 1,258 b — the axes live at `/api/gspc` |
| Board (bare) | `/api/board` | NOT-BUILT | 404 `{"error":"not_found"}` |
| Apex | `https://csoai.org/` | VERIFIED-LIVE | 200 |
| Verify pages | `https://csoai-verify.pages.dev/axes` | VERIFIED-LIVE | 200 |
| Signed-cards site | `https://csoai-sovereign.pages.dev/` | VERIFIED-LIVE | 200 |
| **Parallel 2nd site** | `https://csoai-gspc.pages.dev/` | VERIFIED-LIVE | 200 — built from `~/.grokbot/csoai-site-main`, **never merged into councilof-ai** |
| Frameworks feed | `https://frameworks-drum.pages.dev/` | VERIFIED-LIVE | 200 |
| Outreach audit | `csoai-org.github.io/cibola/docs/OUTREACH-AUDIT-2026-08-25.md` | VERIFIED-LIVE | 200 |
| PyPI packages | `sovos-router`, `sovos-invariants`, `sovos-city` | VERIFIED-LIVE | 200 each on `pypi.org/pypi/<name>/json` |

---

## 3. THE FLEET

**RunPod — 20 pods, 8 RUNNING, 12 EXITED** (VERIFIED-LIVE, `runpodctl pod list`). Running: one RTX 3090,
three A100 (PCIe ×2, SXM ×1), four 0-GPU shells (`oowm-agent-*`, `*-volume-sink-cpu`). Names are in
`runpodctl pod list`; several carry banned strings so they are referenced by ID here.

| Reach | Detail | State |
|---|---|---|
| **The one pod that matters** | `root@194.26.196.156 -p 12473` (ID `fpowppss5ngtkw`, RTX 3090 24,576 MiB, host `19cc1e29bc9d`) | VERIFIED-LIVE — SSH'd, carries gspc-os, fix_loop, RAG, gateway |
| Gateway tunnel | `ssh -L 8090:127.0.0.1:8090` → pod uvicorn pid 58510 | VERIFIED-LIVE — `/health` `{"status":"ok","servers_mounted":191,"servers_runnable":184}` |
| Pod DSH tunnel | `ssh -L 3081:127.0.0.1:3080` → pod node pid 53816 | VERIFIED-LIVE but **EMPTY** — 200, `workspace.list` returns **0 workspaces, 0 sessions** |
| **Local DSH** | `http://127.0.0.1:3090`, node pid 40210, launchd `com.meok.dsh-local` | VERIFIED-LIVE — 1 workspace (`/Users/nicholas`), **23 sessions** |
| Oracle micro-2 | `ubuntu@141.147.73.85`, host `sov33-owem-micro2` | VERIFIED-LIVE — `up 23 days, 19:16` |
| **Oracle (other)** | `ubuntu@145.241.232.16` | **DOWN** — "Connection timed out during banner exchange" |
| Ollama tunnel (pod) | `:11439` → pod `:11434` | **DEAD** — HTTP **000** |
| Ollama tunnel (Oracle) | `:11436` → `145.241.232.16:11434` | **DEAD** — HTTP **000** (its host is down) |
| Ollama (local) | `:11434` | VERIFIED-LIVE but empty — `models: 0` |

Revive local DSH: `launchctl kickstart -k gui/$(id -u)/com.meok.dsh-local`.

---

## 4. CODE & REPOS

**`CSOAI-ORG` holds 668 repos** (VERIFIED-LIVE, `gh repo list CSOAI-ORG --limit 1000 --json name --jq length`).

| Repo | What it IS | State | The ONE command |
|---|---|---|---|
| **councilof-ai** `/Users/nicholas/clawd/councilof-ai` | The live front end. HEAD `45ad8424` on `master`. **29 open PRs.** | VERIFIED-LIVE | `npm run deploy:prod` (build:client → prerender → brand-gate + signed-json-guard → wrangler). Restore after clobber: `gh workflow run deploy.yml --ref master` |
| **gspc-os** `CSOAI-ORG/gspc-os` (PRIVATE, 215 MB) | The 191-server monorepo. **Pod-only** at `/workspace/codebases/gspc-os`, HEAD `32138f0d` on `main`, clean tree, 1.3 GB, `servers/` = 191 dirs. **No local checkout exists.** | VERIFIED-LIVE (on pod) | Already running: `uvicorn gateway:app --host 127.0.0.1 --port 8090` from `apps/gspc-os-gateway`. Probe: `curl 127.0.0.1:8090/health` |
| **council-os** `/Users/nicholas/clawd/council-os` (PUBLIC) | The ledgers — and this file. 233 files, 62 code, 40 md. **`measure/`, `mcp-server/`, `os/`, `trust/` are EMPTY directories.** `MONOREPO.md` calls itself a "(build-plan structure)". | EXISTS-UNVERIFIED as a system; VERIFIED-LIVE as a ledger | `git -C /Users/nicholas/clawd/council-os log --oneline -5` |
| **csoai-static-deploy2** `/Users/nicholas/clawd/csoai-static-deploy2` | The harness workspace, 9.6 GB, signed cards + evidence. On `feat/sandbox-arena-seam`, HEAD `97a6b119`, **NO UPSTREAM**. | EXISTS-UNVERIFIED | `git -C … push -u https-origin feat/sandbox-arena-seam` (nothing is pushed today) |

**Repos holding real work on branches with no upstream** (VERIFIED-LIVE, `git rev-list --count @{u}..HEAD`):
`/Users/nicholas/master-harness` (HEAD `07c38f3`, remote is `meok-harness` which **does not resolve** —
`gh` returns "Could not resolve to a Repository", and the remote URL has a **GitHub PAT embedded in
plaintext**) · `/Users/nicholas/clawd/csoai-static-deploy2` · `/Users/nicholas/clawd/kimi-regen`
(**104 unpushed** on `jv-wave8-production`) · `/Users/nicholas/clawd/councilof-ai-monorepo` (**10 unpushed**).
`/Users/nicholas/cibola` is the exception — HEAD `ef06c13` is on `origin/main`.

---

## 5. MODELS & DATA

| Asset | State | Evidence |
|---|---|---|
| **Model harvest** `csoai/model-harvest-20260826` (HF, private) | **VERIFIED-LIVE** | API 200, `private:true`, sha `a6a492013ba1`, **171 files**, 59 `.safetensors`/`.gguf`, lastModified `2026-08-26T04:15:59Z`. Token: `~/.cache/huggingface/token` (`~/.env` HF_TOKEN is dead). `MASTER-STACK-INVENTORY.md` claims a local `~/clawd/model-harvest/` — **that directory does not exist**; HF is the only copy. |
| **fix_loop.py** | **VERIFIED-LIVE (dormant)** | `/workspace/fix_loop.py` on pod, 12,502 b, mtime 2026-08-26 06:04. **No crontab, no running process.** |
| **fix_loop history — 36 runs** | **VERIFIED-LIVE** | 3 PROMOTE, all 2026-08-14: `+1.1` (`…044008Z`, 59 rows), **`+2.5` "PROMOTE ✓ (generalized)"** (`20260814T050423Z`, 35 rows), `+1.8` (`…052727Z`, 24 rows). Then **30 consecutive REVERT / no-change** through 2026-08-16. Then **a 10-day gap**. Then one run on 2026-08-26: **−26.7 REVERT**. |
| **BEST adapter** | **EXISTS-UNVERIFIED** | `/workspace/fix_runs/BEST/` — `adapter_model.safetensors` **8,745,704 b**, `adapter_config.json`, `README.md`, all dated **Aug 14 05:28**. Frozen since. **No `report.json` in BEST** — the +2.5 provenance lives in the run dir, not the adapter. |
| **Estate RAG index** | **VERIFIED-LIVE** | `/rag/stats` → `state:BUILT`, **103,286 chunks**, 1,739 docs, 2,166 files scanned, built `2026-08-26T05:21:58Z`. By source: session 96,349 · alignment 5,176 · knowledge 845 · memory 547 · ledger 254 · log 115. **Retriever is `bm25 (rank_bm25.BM25Okapi) — lexical only, no embeddings.** Pod-only; no local copy. |
| **The "316-pair corpus"** | **NOT-BUILT** | Searched pod and Mac. No 316-row corpus exists. The real artifact is `fix_runs/20260826T060653Z/failures.jsonl` = **318 lines** — the flood-run training set, i.e. the thing that was *refuted*, not an asset. Stop citing it as one. |
| Small training corpora | EXISTS-UNVERIFIED | `/workspace/sovos-repo/training/*.jsonl` — 12 + 12 + 12 + 90 = 126 lines total |
| "Clans" / merged model families | **CLAIMED-ONLY** | Vault: "the 'clans' are prompts, not weights"; **0 trained adapters**. `MASTER-STACK-INVENTORY.md` §5: "no merged model in this plan is called good — none has passed the gate yet." |

---

## 6. SETTLED RULINGS — DO NOT RE-LITIGATE

1. **Board card-index is FROZEN at 150, not 335.** Source: `/Users/nicholas/clawd/councilof-ai/BOARD-RULING.md`
   (VERIFIED-LIVE, read this run). The reason, verbatim: `"signed": true` in each card entry is a
   **boolean flag, not a signature**. Neither the core 150 nor the extra 185 have backing card files in
   the repo; the 185 are benchmark/candidate axes. "Whatever number actually verifies (150, 335, or
   between) becomes the board." *Stale sources that still say 335 — do not follow:*
   `memory/cursor-closed-claude-governs.md`, `memory/MEMORY.md`, `ESTATE-INVENTORY.md`.
   *Live contradiction:* HEAD carries `9b488192 fix: restore exact-150 floors after freeze deleted them`,
   re-adding workflows BOARD-RULING §2 ordered removed. **Owner call needed.**

2. **Corpus-flooding fix_loop is REFUTED, measured.** Source: `memory/fixloop-corpus-flood-refuted.md`,
   confirmed VERIFIED-LIVE against `/workspace/fix_runs/20260826T060653Z/report.json`:
   `mean_before 0.7667 → mean_after 0.4`, unseen-pool **−26.7 pts**, `verdict: REVERT (worse)`,
   `n_failures_captured: 7`, `n_failures_trained: 318`. fix_loop is a targeted error-correction loop,
   **not an instruction-tuner**. Never pass `--extra-train` a general corpus. If failures are too few,
   the honest answer is "base already strong — stop", not manufactured volume.

3. **Cursor is closed; Claude is sole governor of `councilof-ai` master.** Source:
   `memory/cursor-closed-claude-governs.md` (25 Aug 2026). `LANES.md` marks `cursor-cloud` **UNGOVERNED**
   and flags owner credential revoke. *Note: this same memory's "settled at 335" clause was overturned by (1).*

4. **Vercel is dead → Cloudflare.** Source: `memory/vercel-is-dead-use-cloudflare.md` — HTTP **402
   DEPLOYMENT_DISABLED** on every csoai host. `councilof-ai/CLAUDE.md` was refreshed (`45ad8424`) but its
   **lower half still says "wait Vercel checks green"** — a check that can never go green. PR #645 has
   been blocked on exactly this for days.

5. **22 axes supersedes "13 measured of 14".** Source: `memory/canon-22-axes-ruling.md` (commit `2bdbac34`).
   Public surfaces still say 14 — `/api/gspc` returned `axes[]` len 14 this run. The sweep must go via the
   **data + re-sign path**, never copy edits. Residual: `HARNESS-FLEET-SPEC` decomposes the 8 financial
   axes as 5 + 3 **UNMEASURED**, so "8 measured financial" may itself be an overclaim. **Open for the owner.**

6. **Bytes adjudicate, not commit messages.** Source: `memory/card-index-war-and-guard.md` — the
   "ATOMIC restore 335 (75578B)" commits were a **41-byte stub** that deployed publicly.
   `PLAYBOOK.md` F1: 19+ waves, 115 wave-commits, **898 commits on 2026-08-25 alone**, 417 `origin/cursor/*`
   branches, **product shipped: none.** A guard encodes doctrine, never a position in a live dispute.

7. **Standing laws** (each in `memory/`): structurally *unable* to report false success ·
   UNMEASURED ≠ 0, a clean 0/N sweep is a bug · two machines or it didn't happen · cloud not Mac, never
   vast.ai · CSOAI measures, MEOK hosts the model · we attest, never tokenize · legal gates widen only via
   counsel · never hardcode a live count · a new page needs 4 wirings incl. `PRIMARY_PATHS` · names lie, probe the artifact.

---

## 7. WHAT IS ACTUALLY MISSING — ranked, honest

1. **Merge discipline. NOT-BUILT.** 29 open PRs; 4 repos on no-upstream branches; ~a dozen `git commit`
   against 2 `git push` across nine sessions. *Takes:* one owner rule — every lane works in a `git worktree`
   and ships via `gh pr merge`, never in the shared `~/clawd/councilof-ai` tree. The two sessions that did
   this (`6e8c651a`, `bc82a5d4`) landed 8 PRs between them; the ones that didn't lost their work.
2. **A running fix_loop. NOT-BUILT (regressed).** No cron, no process, no successful run since 2026-08-16.
   *Takes:* a launchd/cron trigger on the 3090 pod + diagnosing why only 7 probes fail (the plateau cause is
   **UNDIAGNOSED**, per `memory/fixloop-corpus-flood-refuted.md`).
3. **The two dead APIs behind live pages. NOT-BUILT (lost).** `/api/fines` 404 under a 200 page;
   `/api/specialists` 404 with commit `5f0f8ab9` unreachable. *Takes:* recover from
   `~/clawd/_alignment/enforcement-recovery/` (fines) and from sibling commits `bc4a0816`/`e4fa33a5` (specialists).
4. **One connections database. NOT-BUILT.** Five were built the same day in five repos, each claiming to be
   the single source of truth. *Takes:* pick one, delete four, record the choice here.
5. **The 22-axis public sweep. NOT-BUILT.** Ruled 2026-08-24, public surfaces still say 14.
   *Takes:* wire the jail board into the API data, then re-sign. Not a copy edit.
6. **RAG durability. NOT-BUILT.** 103,286 chunks exist on one destroyable pod. This violates the estate's own
   "two machines or it didn't happen" law. *Takes:* push the index to HF alongside the harvest.
7. **`.well-known/scitt.json` on csoai.org. NOT-BUILT.** 404 on the did:web trust-root domain while
   councilof.ai serves 200 (`ESTATE-INVENTORY.md`). Pages direct-upload serves the SPA shell.
8. **Embeddings for the RAG. NOT-BUILT.** Retriever is BM25 lexical only, self-declared.
9. **CI truth gates green. NOT-BUILT.** `PLAYBOOK.md` F18: last 40 runs — Claims E2E failed 5×,
   Council OS E2E 5×, crawler-view-gate 3×. W21: 249 type errors ratcheted, not gated.

*Security items found in passing, needing owner action:* a live email password appears in plaintext in DSH
session prompts and bash calls (one session stripped it from `/Users/nicholas/cibola` and advised rotation —
**not yet rotated**); and `/Users/nicholas/master-harness`'s git remote embeds a GitHub PAT in cleartext
for a repo that no longer resolves. Rotate both.

---

## 8. THE 23 DSH SESSIONS — did the work land?

Local harness `:3090`, workspace `nicholas`. **7 LANDED · 9 STRANDED or partly lost · 4 ABANDONED · 3 blank ·
2 history unavailable.** Full extracts in `sessions_raw.json` (scratchpad, 137 MB).

| # | Session | What it did | Verdict |
|---|---|---|---|
| 1 | `822bd15c`, `1ccf759a`, `d240408b` | blank — 4 events each, 0 turns | — |
| 2 | `5816e384`, `a3df30b7` | **history unavailable** — DSH returns `internal: history unavailable` | — |
| 3 | `1528005e` | Parse an overnight "Ralph mode" day-plan from the plan docs | **ABANDONED** — 15 reads, 0 writes, the `ralph` call was interrupted |
| 4 | `a24a13b4` | Estate morning alignment + master rundown | **LANDED** — `ef06c13` pushed to `origin/main` (verified on `origin/main` this run); PR #611 MERGED. Also leaked the mail password. |
| 5 | `4da3d961` | Publish 3 packages to PyPI | **LANDED** — all three 200 on PyPI (verified). But `/Users/nicholas/FULL_RUNDOWN_AUDIT_2026-08-26.md` (8,529 b) sits loose in home, in no repo, and kimi-regen is **104 commits unpushed** |
| 6 | `c4fad80f` | Outreach registry + unmeasured-axes declaration | **STRANDED** — **PR #645 still OPEN** (verified), blocked on the dead Vercel check; registry commits unpushed |
| 7 | `cebb597f` | Signed measurement cards → 21 live cards on Pages | **LANDED** — `csoai-verify.pages.dev/axes` 200 (verified). Commits local-only; repo has no upstream |
| 8 | `6632eaf2` | Venue/"living DB" engine + Cursor feed | **ABANDONED / LOST** — claimed `living-db/venue_engine.py`, `venues.sqlite`, 97 venues. **Searched the whole Mac: no `living-db`, no `venue_engine.py`, no `venues.sqlite` anywhere.** The repo path it claimed is not a repo. |
| 9 | `f2e2cbcb` | Frameworks feed + connections register | **STRANDED** — `frameworks-drum.pages.dev` 200 (verified), but `master-harness` commits `1dfdddd`/`e9dd6bc`/`07c38f3` have **no upstream and a remote that does not resolve** |
| 10 | `69031712` | Recover crashed gates back to green | **LANDED** — best-evidenced session: verify-all 13/13, e2e 32/32, 20/20 surfaces 200. Used `git add -A`, which doctrine forbids |
| 11 | `2b2e6128` | Living connections DB, strip a committed password, untrack PII | **LANDED** — `93156e4` pushed; audit doc 200 (verified). **The only session that removed a credential.** |
| 12 | `fd777320` | Knowledge/coordination DB + RWA attest harness | **STRANDED** — `MASTER_KNOWLEDGE_DB.json`, `COORDINATION_DB.json` committed locally in the churned shared tree, never pushed. Ralph interrupted |
| 13 | `3e10ad5f` | First-Fine-Watch enforcement API + corpus | **LOST** — commit `3e5116ac` rewound by a sibling; **`/api/fines` 404 verified** while `/first-fine-watch/` 200. Recovery copy in `~/clawd/_alignment/enforcement-recovery/` |
| 14 | `6e8c651a` | Verifier, payment rail, publish gate | **LANDED** — PRs #653, #658, #674, #676, #766 all merged. Worked in an isolated worktree |
| 15 | `bc82a5d4` | Restore clobbered App.tsx, ship `/regulator-findings` | **LANDED** — PRs #633, #639, #768 merged; `/regulator-findings/` 200 (verified) |
| 16 | `f06c7327` | 36-section single-file Council OS hub | **STRANDED (divergent)** — `csoai-gspc.pages.dev` 200 (verified) but built from `~/.grokbot/csoai-site-main`, **zero touch of councilof-ai**. A whole second site |
| 17 | `f21b99b3` | 13-specialist catapult at `/api/specialists` | **LOST** — **404 verified**; commit `5f0f8ab9` unreachable, file absent from HEAD and disk. Rundown doc did land (`fa4e220`) |
| 18 | `46f913e2` | Expansion M1–M10 axis evals + oversight | **STRANDED** — 11 commits in `master-harness`, unpushed, unresolvable remote. Found `/api/og` returning 0 bytes and **left it unfixed** |
| 19 | `4d644532` | Overnight batch: merge 3 PRs, keep surfaces 200 | **STRANDED** — **PRs #439, #451, #470 all still OPEN (verified)**. 3 finished drafts marked "NOT PUBLISHED" |
| 20 | `90163e0b` | Client roofing site (not CSOAI) | **LANDED** — pushed and deployed, live at 200. Source repo lives in volatile `/tmp/mallett-site` |

**Built and forgotten — recover these first:** (1) PRs **#439 / #451 / #470** — verified merge-ready, never
merged; (2) the **enforcement rail** (`functions/api/fines.ts` + corpus) sitting in
`~/clawd/_alignment/enforcement-recovery/` under a live 200 page; (3) the **`master-harness` tree** —
the M1–M10 axis evals, the estate index, and the only doc that reconciles both workstreams, all behind a
remote that does not resolve and a PAT that should be revoked.

---

*Probed 2026-08-26 by direct curl / ssh / gh / runpodctl. Where this file and any other ledger disagree,
re-probe — do not average them.*
