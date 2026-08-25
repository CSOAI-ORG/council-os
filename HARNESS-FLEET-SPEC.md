# HARNESS-FLEET-SPEC — 22 axes, N lanes, 24/7, gate-governed

The blueprint to turn one DSH harness (proven: ~6 coherent commits/hour) into a
22-lane fleet running 24/7 on owned/cheap compute, without multiplying mistakes.

## The unit: one axis = one lane = one branch = one worker

| # | Lane (axis) | Family | Pod class | Why |
|---|---|---|---|---|
| 1 | governance | GSPC | CPU | deterministic grading |
| 2 | safety | GSPC | CPU | deterministic |
| 3 | provenance | GSPC | CPU | deterministic |
| 4 | continuity | GSPC | CPU | deterministic |
| 5 | conformance | GSPC | CPU | deterministic |
| 6 | openness | GSPC | CPU | deterministic |
| 7 | machinery-conformity | GSPC | CPU | deterministic |
| 8 | care | GSPC | CPU | deterministic |
| 9 | cross-reality | GSPC | CPU | deterministic |
| 10 | detector-interop | GSPC | CPU | deterministic |
| 11 | art5-safeguard | GSPC | CPU | deterministic |
| 12 | swarm | GSPC | GPU | multi-agent sim may need model runs |
| 13 | affect | GSPC | CPU | deterministic |
| 14 | jail | GSPC | GPU | refusal probing over model fleet |
| 15 | provenance-controls | financial | CPU | on-chain fact reads (I/O) |
| 16 | reserve-attestation | financial | CPU | disclosure checks |
| 17 | regulatory-framework | financial | CPU | crosswalk lookup |
| 18 | distribution-integrity | financial | CPU | RWA.xyz + chain reads |
| 19 | custody-disclosure | financial | CPU | disclosure checks |
| 20 | ai-economy-index | candidate | CPU | UNMEASURED — rubric TODO |
| 21 | human-labour-index | candidate | CPU | UNMEASURED — rubric TODO |
| 22 | humanoid-labour-index | candidate | CPU | UNMEASURED — rubric TODO |

**GPU is the exception, not the rule.** Deterministic grading ("no model judges
another") is CPU + I/O. Only swarm/jail (model-fleet runs) need GPU. So the fleet
is mostly Oracle free-tier + cheap RunPod CPU pods, with 2 GPU pods on demand.

## Each lane's 24/7 loop

```
while true:
  pull lane/<axis> + main
  read gold bank (frozen instrument, HF)              # durable source
  run harness (deterministic grader)                  # CPU
  [if model-based axis] run specialist on GPU pod
  compute separation via stat_suite.separated_leaders # Wilson/McNemar, no overclaim
  sign board delta (scoped key via ANVIL/cb-mpc)      # NEVER estate root
  commit to lane/<axis>; open merge request
  sleep(interval)
```

## Coordination substrate (the thing that stops chaos at 22 writers)

1. **Branch-per-lane.** No lane writes `main` directly. `lane/<axis>` only.
2. **Merge queue.** One serial merger drains lane MRs into `main`, running on each:
   `brand-gate.mjs` + `signed-json-guard.mjs` + `live_status_check.py`. A lane that
   fails a gate is bounced, not merged. This is what makes card-index-war-×22 impossible.
3. **drift-guard** watches production; if a merge or an external push reverts a live
   surface, it restores from the last gate-passed state and files a correction.
4. **The registry is the source of truth** — `council-os/registry/spine.json`; only
   `live_status_check.py` writes LIVE, with evidence. Hand-edited LIVE is invalid.

## Supervisor / queue

- Reads the task list: `CURSOR-JOBS.md` + the next-300-moves + `LIVE-GAP-AUDIT.md`.
- Hands each lane its next move; lane claims it, ships through the gates, reports.
- Idle lanes pull the next unclaimed axis-improvement or gap-fill.
- Emits a heartbeat to the board so `/os` shows the fleet honestly (OFFLINE is a
  first-class state — never a fabricated fleet, per SovereignTown's own rule).

## The FOUR HARD CONSTRAINTS (violations = the failure modes we already hit)

1. **Durability is where bytes land.** Pods are ephemeral — the v2 run was lost WITH
   its pod. Every lane commits to git/HF continuously; NOTHING trusted on pod-local
   paths (`/workspace`, `/root` wipe on reboot). Two machines or it didn't happen.
2. **The governor does not scale with compute.** brand-gate / signed-json-guard /
   counsel-gate / key-gate throttle *mistakes*, and they're doctrine-bound. 22 lanes
   at speed = 22× chances to overclaim; the gates keep honesty flat as output grows.
3. **Collision is real at 22 writers** — branch-per-lane + merge queue is mandatory.
4. **Cost is a dial.** Oracle free-tier + cheap CPU for the 20 deterministic lanes;
   GPU only for swarm/jail, on demand. Never leave GPU pods idle-billing.

## Owner gates that DON'T unlock by scaling compute
- **Signing key**: AWS KMS (both curves) OR cb-mpc-on-Oracle (owned/sovereign). The
  harness committed the KMS client — "gated only on the owner's key/API-key."
- **Counsel sign-off**: the committed legal brief → counsel, before ANY mainnet
  verdict on a named security. Coverage/UNMEASURED needs neither and runs now.

## Bring-up order (don't light all 22 at once)
1. Merge queue + gates on `main` first (the governor before the fleet).
2. One financial lane 24/7 on Oracle free-tier as the pattern (coverage, UNMEASURED).
3. Add lanes in fours, watching the merge queue stay green.
4. GPU lanes (swarm/jail) last, on-demand pods.
5. Candidate index lanes (20-22) only once a deterministic rubric exists — never
   claim an index before it's measured.
