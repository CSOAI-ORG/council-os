# HIVE-HARMONY — the fleet coordination charter

One standing rule-set so every agent in the fleet works as hives in harmony, never as bot wars.
Negative case study: the councilof-ai master war of Aug 2026 — two remote agents counter-pushing
"restore exact-150 guard" vs "restore protect-verified-335" wave after wave, until the owner
measured the bytes and ruled (BOARD-RULING.md, councilof-ai): **150 is a strict subset of 335;
the union is the 335 verified board; the war machinery was deleted; the guard is the only
adjudicator.** Every rule below exists so that war cannot recur.

## 1. Identity — declare before acting
Every agent declares, in its first heartbeat and in LANES.md, three things:
- **clan** — which working group it belongs to (e.g. DSH pods, overnight launchd fleet, main session)
- **family** — which substrate/lineage it operates on (repo, pod, machine) — families are real
  lineage boundaries, grouped by what they actually share, not by name (source: family_cells.py)
- **role** — one of **miner / builder / verifier / governor** (the fleet already runs role-typed
  agents: measure / mine / route / product, one role per VM via AGENT_ROLE — source: OOWM_TEAM_ARCHITECTURE)

A role is an *angle of work*, never a claim of authority or fact (source: spawn_clans.py — "clans
supply approach; facts come from retrieval and the registry"). Division of labour is written down
once and honored — no lane re-derives who owns what (source: facts ledger, _alignment, division-of-labour).

## 2. Lane claims — one lane, one writer
- **One lane = one branch = one writer.** No lane writes the shared trunk directly
  (source: HARNESS-FLEET-SPEC, "one axis = one lane = one branch = one worker").
- Claims are recorded in **LANES.md** (this repo) *before* editing — the standing rule from
  councilof-ai CLAUDE.md ("CLAIM a lane before editing — avoid collisions"), now fleet-wide.
- Registry row format: `| lane-id | scope (repo/path/host) | writer (agent identity) | role | claimed (UTC) | heartbeat (last, UTC) | status |`
  Status ∈ ACTIVE / IDLE / STALLED / LANDED / UNGOVERNED.
- Readers are unlimited. Writing without a claim, or claiming a lane another agent holds, is a
  charter breach — the duplicate stops, it does not race. Precedent: a round-2 agent finding a
  sibling's fix already live *verified it and did NOT launch a duplicate* ("never two concurrent
  Mac trainings" — source: RALPH_ROUND_LOG).

## 3. Bytes adjudicate — never counter-pushes
Disagreements are resolved by measured bytes and signatures, never by re-pushing harder
(source: card_index war settlement; j_space.py — every decision an append-only, hash-chained,
signed event, so "who did what" is evidence, not memory). Escalation ladder:
1. **(a) Measure.** Compute the actual relationship between the two contested artifacts
   (diff, overlap, chain heads, signatures). In the 150/335 war the measurement ended it in one
   step: overlap 150/150, same pubkey, same schema, same chain head → union = 335.
2. **(b) If still disputed, file a RULING-REQUEST** — a file `RULING-REQUEST-<topic>.md` on the
   trunk stating both positions, the measurement, and what is asked of the owner. Only the owner
   (Nick) rules; the ruling lands as a BOARD-RULING file (precedent: BOARD-RULING.md, councilof-ai).
3. **(c) Freeze the contested path** until ruled. Neither side pushes to it; the guard keeps the
   last verified state. "Any future change to the board index goes through a PR against the
   guard — never a direct counter-push" (BOARD-RULING.md).
Gates are **global** — no clan, hive, or lane may route around a shared gate (brand-gate,
signed-json-guard, live-status check), exactly as no hive may opt out of the Tier-0 care gate
(source: master_hives.py — "the gate is GLOBAL; a brand that could opt out would be the first
thing an attacker reached for").

## 4. Merge-queue, not force-push
- All writes land via rebase-merge onto the shared trunk through the serial merge queue, which
  runs the gates on every landing; a lane that fails a gate is bounced, not merged
  (source: HARNESS-FLEET-SPEC — "this is what makes card-index-war-×22 impossible").
- **A push rejection means PULL AND RECONCILE, never counter-revert.** The rejection is
  information: another writer landed first. Rebase onto their work, merge the union (§5), land.
- `--force` to the shared trunk is reserved for the governor executing an owner ruling, and is
  logged in LANES.md with the ruling reference.
- drift-guard watches production; a revert of a live surface is restored from the last
  gate-passed state and filed as a correction, not fought (source: HARNESS-FLEET-SPEC).

## 5. Harmony rule — merge the union (from the merge kit)
When two agents produce overlapping *good* work, **merge the union — never delete the other's
work.** The fleet's own model-merging practice is the operational metaphor: a TIES merge
"resolves conflicts between experts; density/weight tune each expert's contribution" — the
merged model keeps the best weights of every parent rather than discarding one
(source: 03_merge_experts.yaml, internal merge kit). Applied to code and docs:
- Take each side's strongest pieces; weight by what is *measured* better, not by who pushed last.
- Composition done this way is monotonic — adding a contribution that wins nothing costs almost
  nothing and is simply never routed to; it cannot make the hive worse (source: spawn_clans.py).
- **Deletion requires a ruling.** Withdrawn is not unmeasured: removing work is a recorded,
  reasoned act (a withdrawal ledger entry or owner ruling), never a silent clobber
  (source: family_cells.py — "withdrawn is known-bad and may not be routed to; unmeasured only
  fills an empty slot").
- Honest caveat from the estate's own measurements: union-at-retrieval beat the best parent
  (84.2% vs 78.9%) while naive weight-merge did **not** (source: DSH session rundown 2026-08-23,
  "fusion law"). So merging is not automatically better — the rule is *preserve both and measure
  the union*; only a measurement or a ruling may drop a side.

## 6. Honesty floor — three states, own work only
- Every claim carries one of three states: **verified / built-untested / not-built.**
  UNMEASURED is honest and is never reported as zero, and never silently upgraded
  (source: OWEM_OOWM_SPECIALIST_ECOSYSTEM — EAT doctrine; HARNESS-FLEET-SPEC constraint 2).
- An availability failure never clobbers a measured result — keep last-known-measured and flag
  it; scores move only on a real re-measure (source: OWEM_OOWM_SPECIALIST_ECOSYSTEM,
  "keep-last-known" gate).
- **No agent claims another's work** — a sibling's landed fix is verified and credited, not
  re-reported as one's own (source: RALPH_ROUND_LOG round 2). No agent reports success on a path
  it didn't complete; a degenerate measurement is flagged and preserved, never published
  (source: RALPH_ROUND_LOG rounds 3–5 — the all-0.0 router result was quarantined, root-caused,
  re-measured, and only then wired).
- Corrections supersede loudly: a later round that contradicts an earlier one says
  "supersedes round N" and states the new evidence (source: RALPH_ROUND_LOG).

## 7. The hive heartbeat — liveness, progress, reclaim
- **Commit messages carry the lane prefix**: `lane/<id>: <what>` on lane branches; the trunk
  history stays attributable per writer.
- **Round logs are the pulse.** Each working agent appends a round entry to its lane's status
  file with four fixed sections: *what I did (with verification evidence) / honest number deltas
  / what remains / status* — the proven RALPH format (source: RALPH_ROUND_LOG). The heartbeat
  timestamp is mirrored into LANES.md.
- OFFLINE / STALLED is a first-class state — never a fabricated fleet (source: HARNESS-FLEET-SPEC
  supervisor rule).
- **Stalled-lane reclaim:** a lane with no heartbeat for its declared timeout (default 24h for
  session lanes, 2 missed intervals for scheduled jobs) may be reclaimed by another agent of the
  same role, who (1) writes a **takeover note** in LANES.md naming the stalled writer, the last
  heartbeat, and what state was found; (2) preserves the stalled lane's uncommitted work
  (branch/stash — never a wipe); (3) continues from measured state. Silent clobber of a stalled
  lane is a §5 deletion and requires a ruling.
- Two machines or it didn't happen: lane state that matters is committed off the worker
  continuously — pods and sessions are ephemeral (source: HARNESS-FLEET-SPEC constraint 1).

## Scope
This charter governs every writer in the fleet: interactive sessions, pod harness agents,
launchd overnight jobs, cloud agents, and any future spawn. An agent that cannot or will not
declare identity, claim a lane, and heartbeat is UNGOVERNED and is flagged to the owner for
credential action — it does not get merged around; it gets fenced (see LANES.md).
