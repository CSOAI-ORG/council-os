# LANES — the live lane registry (HIVE-HARMONY §2)

One lane = one writer. Claim here BEFORE editing; heartbeat here while working; mark LANDED when
done. Readers unlimited. Format:

`| lane-id | scope (repo/path/host) | writer (agent identity) | role | claimed (UTC) | heartbeat (UTC) | status |`

Status ∈ ACTIVE / IDLE / STALLED / LANDED / UNGOVERNED. A stalled lane is reclaimed only with a
takeover note appended below the table (HIVE-HARMONY §7) — never a silent clobber.

## Registry

| lane-id | scope | writer | role | claimed | heartbeat | status |
|---|---|---|---|---|---|---|
| councilof-master | councilof-ai `master` (trunk + deploy) | Claude main session (Mac) | governor | 2026-08-25 | 2026-08-26 | ACTIVE |
| dsh-bench-3090 | RunPod `sov-repull-20260808` (3090: bench :11435, banks-all, router measures) | pod harness agent | verifier | 2026-08-23 | 2026-08-24 | ACTIVE |
| dsh-mine-03 | RunPod `oowm-agent-03-mine` (CPU VM, AGENT_ROLE=mine) | pod harness agent | miner | 2026-08-24 | 2026-08-24 | IDLE |
| oowm-measure-01 | RunPod `oowm-agent-01` (CPU VM, AGENT_ROLE=measure, estate heartbeat proven) | pod harness agent | verifier | 2026-08-24 | 2026-08-24 | IDLE |
| oowm-measure-02 | RunPod `oowm-agent-02-measure` (CPU VM) | pod harness agent | verifier | 2026-08-24 | 2026-08-24 | IDLE |
| oowm-gateway | hub pod :8899 (`/oowm/chat` `/oowm/clusters` `/mcp` `/a2a`) + `councilof-ai/harness/owem/` | gateway coordinator | builder | 2026-08-24 | 2026-08-24 | ACTIVE |
| axis-loop-gpu | GPU pod `/workspace/axis_loop.sh` (10-min living re-measure, mirrors register to offline index) | axis measurement worker | verifier | 2026-08-24 | 2026-08-24 | ACTIVE |
| overnight-fleet | Mac launchd `com.meok.*` (~95 jobs: eat loops, sim-world, watchdogs, tunnels, backups) + overnight/train/backup siblings | scheduled fleet | miner/builder | standing | continuous | ACTIVE |
| jeeves-overnight | Mac overnight driver (distill → sync → train → eval; RALPH round logs in `_alignment/`) | JEEVES lane | builder | 2026-08-23 | 2026-08-24 | IDLE |
| dsh-mcp-bridge | council-os `bridges/dsh-mcp` (harness as MCP stdio tools) | main session | builder | 2026-08-25 | 2026-08-26 | LANDED (`b5bdecb`) |
| cursor-cloud | Cursor cloud agents pushing to councilof-ai remotes | (unidentified remote agents) | — | never claimed | unknown | **UNGOVERNED** |

## Flags

- **cursor-cloud — UNGOVERNED, fenced.** These are the writers behind the 150-vs-335 counter-push
  war on councilof-ai master (settled by BOARD-RULING.md: 150 ⊂ 335, union = 335). They do not
  declare identity, claim lanes, or heartbeat. Per HIVE-HARMONY (Scope): flagged for **owner
  credential revoke**; until revoked, `signed-json-guard` + drift-guard fence their pushes —
  nobody counter-pushes them.
- **dsh-bench-3090 caveat:** SSH endpoints on live pods drift (ports change on resume) — verify
  via the RunPod API before declaring a pod-lane STALLED; an unreachable stale port is not a
  dead writer.
- Heartbeats above are seeded from the last verified evidence (round logs, pod probes,
  commit `b5bdecb`) at charter creation, 2026-08-26. Each writer refreshes its own row on its
  next round.

## Takeover notes

_(none yet — reclaim format: date, lane-id, stalled writer, last heartbeat, state found,
work preserved where, new writer)_
