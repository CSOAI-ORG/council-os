# PLAYBOOK — how this estate actually gets work done

Standing operational doc. Every rule comes from something that happened in this estate's record,
and cites it. No generic project-management advice. Rules with no incident behind them are marked
**[ASPIRATIONAL]** — a design under test, not a law.

Companions: `HIVE-HARMONY.md` (charter — *why*), `LANES.md` (who holds what),
`HARNESS-FLEET-SPEC.md` (scale). This is the behavioural layer: what an agent does at the keyboard.
Sources are `repo:path`, a commit sha in `councilof-ai`, or a memory file
(`~/.claude/projects/-Users-nicholas/memory/*.md`).

> **The one defect.** Every expensive failure here is the same defect at a different altitude:
> *a claim substituted for the thing itself* — code returns a default instead of refusing; a name
> asserts a property the code lacks; "stored" means RAM on a pod; "shipped" means committed
> somewhere nobody serves; a commit message or a count stands in for the bytes. Every counter that
> has actually held is **structural**, never intentional.

---

## 1. WHAT WORKS

| # | Rule | Proof |
|---|---|---|
| **W1** | **Branch, then land in ONE gated merge.** | `council-os`: 29 commits, 3 of them merges (`b5bdecb`, `60dcbe4`, `63acd37`), **zero `fix:` churn**. `councilof-ai` master the same week: **345 of its last 400 commits are `fix:`**. Same operator, same days — the difference is merge discipline. |
| **W2** | **One worktree per lane; never a shared checkout.** | `git worktree list` in `councilof-ai` shows ten+ live worktrees, one branch each. Memory (`plays-integration-state`): a shared checkout "collides past ~2 agents", leaving plays branches carrying foreign commits. `_alignment:FULL_RUNDOWN_2026-08-25.md` names it the biggest throughput killer — "a sibling lane redeploys every few minutes … and it *rewinds my commits*. That, not the work, is why `/api/fines` won't stay live." |
| **W3** | **Cherry-pick pinned SHAs onto an integration branch, gate once.** | The plays were recovered that way, not by merging (`ca7ba225`, `f245887e`, `2974bf19`, `d16f3d5d`). `61b01fca` landed three verified pieces in one gate run; `addc4139` shows the care — it *dropped* a deletion the cherry-pick had dragged along. |
| **W4** | **Run the full gate chain, and write the incident into the step.** | `deploy.yml`: one-door-guard → no-conflict-markers → install → build:client → prerender → place-aliases → **brand-gate** → **signed-json-guard** → dist-bundle-guard → deploy(×3 aliases) → assert → recheck(120s) → anti-clobber → hold(90s). Every step carries a dated comment naming its failure ("blocks the 2026-08-24 build break"; "Fail this job if that race happens **so we do not ship a green lie**"). Only the deploy steps hold secrets; every gate runs with none. |
| **W5** | **Make the honest answer structural.** | `signed-json-guard.mjs` header: *"a component must be STRUCTURALLY UNABLE to report success on a path it did not complete."* `council-os:ops/live_status_check.py` is the same rule in the spine — the **only** writer of `LIVE`, verdict written together with its evidence, missing evidence fails validation, hand-edited `LIVE` invalid by definition. Prose reminders have not held here; code that cannot express the lie has. |
| **W6** | **A gate that cannot fail is indistinguishable from no gate.** | `crawler-view-gate.mjs` and `no-conflict-markers.mjs` both run `--selftest` in CI *first*, seeding each violation class and asserting the gate fires. |
| **W7** | **Gate at the layer the consumer reads.** | `brand-gate.mjs` moved from linting `client/src` — **219 false positives**, since a redirect must still name the killed route — to scanning **rendered visible text** after prerender. `crawler-view-gate` tests the no-JS view because hydrating is the thing a crawler will not do. |
| **W8** | **Block the assertion, not the disclosure.** | `brand-gate.mjs` carries a `nearAllow` ±90-char window and `allowOn` carve-outs so a retraction page may *discuss* the withdrawn claim: "the point is to block the ASSERTION, not the honest 'this claim was retracted'." A gate that censors the correction makes honesty expensive. |
| **W9** | **Three states — and UNMEASURED is a first-class answer.** | Binding form (`_alignment:ARENA_METHODOLOGY_2026-08-24.md`): *"UNMEASURED never equals 0"* — unmeasured rows leave the denominator, never score 0.0. Applied inward, `MASTER-STACK-INVENTORY.md` grades all 70 artifacts **harvested-verified / catalogued-not-pulled / inferred-unverified** and closes "no merged model in this plan is called good — none has passed the gate yet." Also **UNMEASURABLE ≠ FAILED**: `evidence-smoke.yml` exits 75 when Cloudflare 403s the runner, because "measuring nothing and measuring a failure are different findings." |
| **W10** | **Probe before asserting — in both directions.** | The facts ledger: *"never enshrine a capability negative without a live probe. A tool NAME in the catalog is a claim to TEST, not a fact to assert or dismiss."* Proven both ways in one day (`names-promise-what-code-lacks`): six models named for refusal all complied with an Art 5(1)(c) request; and a tool declared missing existed as a dead stub. |
| **W11** | **Read the fact ledger at session start; do not re-derive.** | The 52 memory files and `_alignment/*_FACTS_LEDGER.md` exist because *"Nick asserts a fact here ONCE; every future session reads it at start and stops re-asking."* The rule that follows: **you do not inherit a sibling agent's capabilities from chat memory** — a different agent in a different environment did that, not you. |
| **W12** | **Fresh-agent rounds, fixed template, one artifact each.** | RALPH rounds run *"fresh worker, round N of 20"* — no chat memory, workspace as memory. Fixed sections: **what I did (with verification evidence) / honest number deltas / what remains / status**, each leaving a file the next worker resumes from. Measured **5 rounds in ~2h45m** (2026-08-24), tightening to 5–25 min; corpus 257 → 585 → 708 → 904 → 1530 in one night. Day-end contract: *open until every incomplete item names a person or a gate.* |
| **W13** | **Stage, don't wire, until the measurement is inspected.** | RALPH r4 set the contract up front — "do NOT wire `/api/model-router` until inspected (next round)"; r5 inspected, validated, wired, verified 200, re-ran the regression sweep. The one time a measurement was wired unread, it was the all-0.0 degenerate router. |
| **W14** | **Verify, read the output, *then* claim — in that order.** | `_alignment:COMMIT_CORRECTION_2026-07-11.md`: *"Do not run `git commit` in the same cell as a verification whose output has not yet been read. Read the assertion's printed result FIRST."* |
| **W15** | **Corrections are assets — log them append-only.** | `CORRECTIONS_LEDGER` entries are **Wrong: / Fix: / Evidence:**, append-only: *"a body that logs its own corrections is one that can be verified."* Published at `/honesty` and `/api/corrections`. The degenerate router artifact was **preserved** as `…DEGENERATE_20260824T0347Z.json`, root-caused and re-measured — not deleted. |
| **W16** | **Every count names its set; never hardcode a live number.** | One canonical `counters.json` + `COUNTER_REGISTRY.md`, because an external audit (2026-08-19) found **three disagreeing public numbers at once** — `llms.txt` 819, `agent.json` 890, live `/api/gspc` 966 — and one metric had carried 8+ values. Cite the API, and use `curl` (`urllib` gets 403'd by Cloudflare). |
| **W17** | **Long jobs run detached under a supervisor, never in the tool session.** | The v3 train died to session reaping, then again to a `/tmp` purge of its venv; fixed with a launchd plist + persistent venv. Same class: `nightly_board.yml` runs "on GitHub's servers while you sleep, **NOT the agent's kernel**." |
| **W18** | **Durability is where the bytes land — two machines or it didn't happen.** | The red-team v2 run, written specifically to store transcripts, was **lost with its pod**, taking the 33-cell hand-labelled gold set — the least reproducible artifact in the pipeline. Rule: fsync each record before the next call, mirror off the worker continuously, grade as a separate phase over stored transcripts. |
| **W19** | **Compute on pods; the laptop is a thin client.** | The Mac died at 19:03 "No space left on device" while the cloud half of the same run completed (`run-on-cloud-not-mac`). Never route bulk data through it: pod→pod direct measured **~37 MB/s vs 0.75 MB/s via the Mac — 50×**. GPU is the exception, not the rule — deterministic grading is CPU + I/O (`HARNESS-FLEET-SPEC`) — and key custody is "HSM/MPC, **not a laptop**." |
| **W20** | **Publish the honest negative with a reproduce command.** | `_alignment:BASELINE_VS_GATE_FINDING_2026-07-12.md` ships the win (0/15 → 15/15, "the care-floor gate is load-bearing, not decorative") *and* the limit ("this does NOT claim to beat GPT/Claude's built-in safety") in the same breath. `ROUTER_HONEST_CEILING` is a whole document about stopping. Owner's read: every competitor claims their gate works — publishing where ours doesn't, with the measurement attached, *is* the pitch. |
| **W21** | **Ratchet legacy debt; don't gate it.** | `ts-ratchet.mjs`: 249 type errors across 114 files while `vite build` stays green — "the build being green tells you nothing about whether the types hold." The count may go down, never up. |
| **W22** | **Subagents mine, the main session decides.** | Token-heavy reading is delegated; synthesis and the honesty call stay in one place. `MASTER-STACK-INVENTORY.md` is the shape — a read-only harvest over 18 pods where *"nothing on any pod was started, stopped, or deleted."* Read-only mining parallelises safely; writing does not (W1, F1). |

---

## 2. WHAT FAILS

| # | Failure | The incident |
|---|---|---|
| **F1** | **Counter-push wars** | 2026-08-23→26: **19+ waves**, **115 wave-commits**, **898 commits on 08-25 alone**, **417 `origin/cursor/*` branches**. Two auto-pushing bots byte-pinned each other's files — `reject-335-board` asserted `honest-board-floor.yml` was *exactly 1846 bytes*. Product shipped: none. A push rejection is information; rebase and merge the union. |
| **F2** | **Structure verified, called bytes verified** | The 335 overclaim. `BOARD-RULING.md`: *"`\"signed\": true` … is a **boolean flag, not a signature**"*; the hashes resolve only against a store this repo cannot see. The first ruling (`a27fb15f`, 04:46) measured overlap, pubkey, schema and chain head — all structural — and got it wrong; corrected 05:46 (`d3448085`). |
| **F3** | **Commit messages standing in for bytes** | Commits claiming "ATOMIC restore 335 (75578B)" shipped a **41-byte stub** — the literal string `__LOAD_FROM__/tmp/card_index_content.json` — publicly. The first guard only required ≥50 cards, so "a valid 50-card JSON lie shipped to councilof.ai" (`signed-json-guard.mjs`). |
| **F4** | **Guards built as weapons** | `honest-board-floor` / `reject-335-board` / `protect-verified-335` / `sticky335-land-atomic` each auto-restored its side's number. `BOARD-RULING.md` §2 ordered all removed — yet **both `reject-335-board` and `honest-board-floor` still executed 2026-08-26 05:17**, and `wave11-assemble.yml` is still on master HEAD. A guard encodes doctrine, never a position in a live dispute; removing one means sweeping every branch that can trigger it. |
| **F5** | **"Built" reported as "live"** | `MORNING-EXECUTION.md`: `/gpai-evidence`, `/cra-readiness`, `/financial-axes`, `/distribution-integrity`, `/embed`, `/white-label` and the flagship post all hard-404 — while `PLAYS-LEDGER.md` tags the same items "fuse: **LIVE NOW**". **151 local branches ahead of origin/master.** |
| **F6** | **Catalogue described as built** | `estate-data-sources-noaa-nvidia` exists because a data-source catalogue was reported as a working integration. `FREE_COMPUTE_REGISTRY`: ~70 catalogued, **~30 genuinely usable**. The standing honesty pass is "for the 313 MCP methods, mark each REAL (server responds) vs CATALOG-ONLY". |
| **F7** | **Trusting a name over the artifact** | Pod `kimi-k2-lora-train`: *"**EMPTY.** Despite the name … burning $1.39/hr for nothing"* ≈ $33/day. Six models named for refusal that don't refuse. `deploy_refusal_models.sh` orchestrates Modelfiles **that do not exist** — it has never run. |
| **F8** | **The no-op gate — looked like it ran, didn't** | Named as a family, **≥3 recurrences**: the retrain-gate stub (C-14); "TRAIN ran, DEPLOY didn't" (C-21); and `pgrep -f` over SSH **matching its own argv**, producing a fake "ALIVE ✓" for a loop that had stopped. Prove liveness by fresh bytes on disk, never by a log line. |
| **F9** | **Scoring a non-answer instead of refusing** | A failed API call scored 0.0 → vendors publicly "scored zero on governance" having never been run. `fcc.gov` HTTP 403 recorded 0% on all 5 predicates. **2,215 ledger records scored a page nobody read.** A EUR-Lex monitor reported "no updates" through **240 SSL failures over 75 days**. Corollary: *a clean 0/N sweep is a bug, never a result* — max_tokens=3 had starved the judge. |
| **F10** | **Reading an instrument artifact as a result** | The "best model at 0.938" was inflated ~0.25 because it **echoed the axis labels the judge grepped for**; retired as an artifact, honest baseline 0.762. Run a discrimination/control test on the judge first. |
| **F11** | **Committing before reading the verification** | `d5bb640b` claimed session scoping made lockdown per-caller; the smoke test had printed **SESSION SCOPING: FAIL**. Pushed before the output was read. |
| **F12** | **Working in the wrong repo, or the wrong copy** | ~**50% of a two-day budget** went into `csoai-org-v2` and `csoai-dashboard` while the canonical repo had zero commits for 17 days (`canonical-csoai-site-repo`). Round-scale version: "my first edit hit the non-served `agui/` copy." |
| **F13** | **Deploy clobber and queue starvation** | A direct `wrangler pages deploy` from an ungoverned lane overwrites the gated CI build — "that is how an ungated 17-axis `/api/gspc` and a de-branded regression shipped" (`drift-guard.mjs`). Live: good deploy 11:19 → green 11:25 → **clobbered 11:51 → red 90 minutes, nobody acted**. Separately, deploys are serialised by design, so at 898 commits/day the queue never drains — *"a master deploy is reportedly blocked by GHA starvation"* (`E2E-TEST-REPORT.md`). And **two repos must never deploy one Pages project**: that clobbered the `did:web` trust root. |
| **F14** | **Shipping a green lie** | 2026-08-22: deploy went green (apex 212889); a Vite-only writer flipped the production alias ~3 min later. `/` is no-cache so the homepage went thin while `/os/` **stayed fat on a week-long cache and hid the clobber**. Hence assert → 120s recheck → anti-clobber → 90s hold. |
| **F15** | **Missing the fourth wiring** | A new page needs route + title map + prerender list + **`PRIMARY_PATHS`**. All **6 freshly-shipped play pages went live wearing "Reference / archive" banners** because `ArchivedBanner` marks every route absent from `PRIMARY_PATHS`. |
| **F16** | **Self-contradicting artifacts** | `financial-axes.json` tags `ai-economy-index` and `human-labour-index` `MEASURED-INDEX-v0.1` while the same file's `honesty` block says UNMEASURED, "NO rubric and NO data yet" (`E2E-TEST-REPORT.md`). |
| **F17** | **Diagnostics that kill the job** | "My diagnostic 10-step test **KILLED the v3 run at ~90%** (script has no resume)." Adjacent: re-probing a rate-limited host inside its cooldown, and concluding "pod exited" from an SSH timeout when RunPod had merely reassigned the endpoint. |
| **F18** | **Leaving the truth gates red** | Last 40 runs: `Claims E2E (live truth check)` failed 5×, `Council OS E2E` 5×, `crawler-view-gate` 3×. A red honesty gate nobody drains stops being an adjudicator and becomes noise. |
| **F19** | **Stale operating doc** | `councilof-ai:CLAUDE.md`, stamped **2026-06-25**, still says the repo deploys to **Vercel** and the hero CTA is "Get certified". Vercel returns **402 DEPLOYMENT_DISABLED**; `deploy.yml` ships to Cloudflare Pages; doctrine is *measurement, not certification*. Memory stayed current; the in-repo doc did not. |

---

## 3. THE ESCALATION LADDER

As executed in `BOARD-RULING.md` — the only path that has actually ended a dispute here.

1. **Measure — bytes, not structure.** Counts, schema matches, overlap and boolean flags do not
   close a dispute (F2).
2. **If it cannot be verified, freeze at the verifiable floor and say so.** Not the larger number,
   and not the smaller one as a rhetorical hedge — whatever actually verifies. *"Whatever number
   actually verifies becomes the board."* Publish "could not verify" as the finding.
3. **Still disputed → file `RULING-REQUEST-<topic>.md` on the trunk**: both positions, the
   measurement, what is asked. Only the owner rules; the ruling lands as a `BOARD-RULING` file and
   supersedes loudly.
4. **Freeze the contested path.** Neither side pushes; the passive gate holds the last verified
   state; every later change is a PR against the gate. **No bot fights** — remove write permission
   from the dispute rather than building a better bot.

Gates are global: no lane routes around brand-gate, signed-json-guard, banned-strings, or
`live_status_check`.

---

## 4. THE OPERATING SHAPE

| Actor | Owns | Never |
|---|---|---|
| **Owner (Nick)** | Rulings; credentials and key custody; spend; anything sent or published in the estate's name; counsel gates | Is not a reviewer of routine diffs — don't queue behind him for what the gates settle |
| **Main session** | Decisions, the honesty call before any claim, trunk landings, owner interface, memory writes | No token-heavy mining itself; no heavy builds on the laptop |
| **Subagents** | Token-heavy mining, isolated builds in worktrees, read-only audits with per-claim evidence | Never write the shared trunk, claim another's lane, or counter-push |
| **Pods / DSH / launchd** | Training, model runs, long harvests, scheduled loops — committing results off the worker continuously | Are never where state lives (W18); a job in the tool session is a job that dies |
| **CI guards** | The only adjudicator that cannot be argued with — brand-gate, signed-json-guard, banned-strings, `live_status_check`, drift-guard, `--selftest` | Must encode doctrine, never a position in a live dispute (F4) |

Owner gates that **more compute does not unlock**: signing-key custody (KMS or MPC), counsel
sign-off before any measured verdict on a named security, and any outbound send. Everything else
proceeds without asking — coverage and UNMEASURED work need neither and run now.

---

## 5. PRE-FLIGHT — before claiming anything

1. **Bytes or structure?** Did I recompute or resolve the content, or did I count entries, match a
   schema, or read a `"signed": true` flag? (F2, F3)
2. **Built, or catalogued?** A live URL with a status code — or a file, a branch, a registry row, a
   plan? (F5, F6)
3. **Did I read memory and the ledgers first?** `memory/`, `_alignment/`, `LANES.md`, before
   re-deriving something already settled — and a recorded honesty ruling outranks my fresh
   re-derivation from counts. (W11, F2)
4. **Am I about to counter-push?** Push rejected, or my change reverts another agent's: stop, pull,
   merge the union, or file a ruling-request. (F1, §3)
5. **Will this run heavy on the owner's laptop?** Builds, training and long harvests go to a pod;
   secrets never do; long jobs go under a supervisor. (W17, W19)
6. **Does the name match the artifact?** Probe it — and don't assert a capability *negative*
   without probing either. (W10, F7)
7. **Did I read the verification output before writing the claim?** (W14, F11)
8. **Is my honesty state on it?** verified / built-untested / not-built; UNMEASURED is never zero
   and never silently upgraded; a clean 0/N is a bug. (W9, F9)
9. **Am I in the served copy of the right repo, and does my count name its set?** (F12, W16)
10. **Did I land it where the deploy can see it — and did the gates go green *and stay* green?**
    (W1, F14, F18)

---

## 6. WHERE THE RECORD CONTRADICTS ITSELF

Flagged, not silently reconciled. Where a later file corrects an earlier one, the later wins.

- **`HIVE-HARMONY.md` §3 cites a superseded ruling.** It states the war ended at "union = 335 …
  the war machinery was deleted." That was the 04:46 ruling; the owner corrected it at 05:46 to a
  **freeze at 150**, with 335 named an overclaim — and the machinery demonstrably still runs (F4).
  §3 should be re-pointed at the corrected `BOARD-RULING.md`.
- **Card count.** `cursor-closed-claude-governs` says "335 settled, respect the sticky-335 state";
  `card-index-war-and-guard`, one day later, says frozen at 150. **150 wins**, independently
  corroborated by the Merkle log built over the 150-card chain. The `MEMORY.md` index line "335
  settled" is stale. Note the guard hard-codes `!== 150`, so it is floor *and* ceiling — settling
  upward requires the PR path, by design.
- **The axis count has moved three times**: 13-of-14 → 16 (reversed the same day) → 22 (14 GSPC +
  8 financial/domain, owner ruling 2026-08-24). The public sweep is **authorized and unexecuted**,
  and must go via the data + re-sign path, never copy edits. Residual conflict:
  `HARNESS-FLEET-SPEC` decomposes the 8 as 5 financial + 3 candidate **UNMEASURED** — so "8
  measured financial axes" may itself be an overclaim. **Open for the owner.** Cite the live API,
  never a remembered number.
- **`PLAYS-LEDGER.md` vs `MORNING-EXECUTION.md`** on what is live (F5). The HTTP evidence wins.
- **`councilof-ai:CLAUDE.md` vs `deploy.yml` and doctrine** (F19). The workflow wins.
- **Deploy path** — "fully GHA-automated" vs "every deploy is a manual wrangler push". Both are
  true: the workflow deploys both Pages projects, while the `csoai-site` project's own Git
  integration is off. The trap is assuming a merge deploys it when the workflow didn't run.
- **Payments.** "Open source, never a card processor" vs live subscription billing on a sibling
  surface, flagged elsewhere as a P0 (money on an overclaim). **This is an open owner decision** —
  do not silently delete a payment link as off-canon, and do not design tiers onto free tooling.
- **[ASPIRATIONAL]** — designs under test, not yet proven here: the serial merge queue at 22 lanes;
  stalled-lane takeover; `RULING-REQUEST-*.md` as a routine step (used once, by the owner
  directly); and `functions-guard.mjs`, which documents a real incident but is **wired to nothing**.
