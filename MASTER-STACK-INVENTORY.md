# MASTER STACK INVENTORY — RunPod Fleet Harvest 2026-08-26

Master harvest run 2026-08-26 ~04:00–05:15 UTC. Read-only inventory over SSH + small-file
harvest to `/Users/nicholas/clawd/model-harvest/`. Nothing on any pod was started, stopped,
or deleted. Durability doctrine applies: **a model that exists only on a pod does not exist.**

Honesty states used throughout:
- **harvested-verified** — bytes are on the Mac, sha256 recorded.
- **catalogued-not-pulled** — seen on the pod with exact path + size, not pulled (too big or duplicate).
- **inferred-unverified** — pod unreachable/stopped; contents inferred from names, dates, and sibling pods.

---

## 1. Fleet table (18 pods)

| Pod | Status | GPU | $/hr | Reachable | What's on it |
|---|---|---|---|---|---|
| sov-repull-20260808 | RUNNING | RTX 3090 | 0.22 | yes | **RICH.** sov33-v12 adapter, fix_runs self-improving loop (40+ hourly QLoRA runs + BEST), refusal-lora merged, oowm_merge_v1, mergekit/MoA/RouteLLM/semantic-router repos, p5 train data. Active procs: f2_gen_v2.py (98% CPU, mid-flight — untouched), arena_loop_keeper, measure_chain. |
| sovos-light-master-mine-20260816 | RUNNING | A100 PCIe | 1.39 | yes | **RICH.** sovereign-v3 (617M), csoai-training mlx family (16 adapter sets + 4 fused 0.5B models + cards gguf), jeeves-exec repo with benchmark-results (govbench, oowm_v8, care_gate). /workspace is a 755T network volume. ollama + arena_rounds running. |
| sov-volume-sink-cpu | RUNNING | CPU | 0.06 | yes | **RICH (network volume euro, 2.3P).** sovos-harness repo, sov33-v10/v12 q8 ggufs, sov-minimal 1.9G model, mac-migrate mlx-adapter backups (14 checkpoints), leaderboard/GPQA eval results, offload-dsh mirror of csoai-static-deploy2. |
| kimi-k2-lora-train | RUNNING | A100 SXM | 1.39 | yes | **EMPTY.** Despite the name: no models, no data, no repos. Only dsh-web. GPU at 0 MiB. Burning $1.39/hr for nothing — owner decision to stop. |
| oowm-agent-03-mine | RUNNING | CPU | 0.06 | yes | Empty shell (dsh-web only, 20G disk, nothing in /workspace). |
| oowm-agent-04-route | RUNNING | CPU | 0.06 | yes | Empty shell (nginx + sshd only). |
| oowm-agent-05-product | RUNNING | CPU | 0.06 | yes | Empty shell (nginx + sshd only). |
| sov33-master-takeover-v2-migration | RUNNING | A100 PCIe | 1.19 | **NO — SSH timeout** (104.255.9.187:12820, refused this run and the prior one) | inferred-unverified: sov33 master-takeover v2 migration payload. Billing at $1.19/hr while unreachable — owner should check console/web terminal. |
| overnight-bench-a100-v2 | EXITED (stale ports) | A100 PCIe | 1.19 | no (timeout) | inferred-unverified: overnight benchmark v2 harness. NB: memory says "the v2 run was lost with its pod" — likely already gone. |
| sov-fuel-train-20260804091151 | EXITED | RTX 3090 | 0.22 | — | inferred-unverified: fuel-train family LoRA runs from 2026-08-04. |
| sov-fuel-train-retry0-fuel-train | EXITED | RTX 3090 | 0.22 | — | inferred-unverified: retry of the above. |
| sov33-master-takeover | EXITED | A100 PCIe | 1.19 | — | inferred-unverified: sov33 master takeover v1 artifacts. |
| sov33-master-takeover-v2 | EXITED | A100 PCIe | 1.19 | — | inferred-unverified: sov33 master takeover v2 artifacts. |
| k3-autodeploy-20260824 | EXITED | A100 SXM | 1.59 | — | inferred-unverified: K3 autodeploy lane from 2026-08-24 (recent — may hold fresh state). |
| council-ring-a100-20260818 | EXITED | A100 PCIe | 1.39 | — | inferred-unverified: council-ring experiments. |
| sov-brain-a100-fresh-20260811 | EXITED | A100 PCIe | 1.19 | — | inferred-unverified: sov-brain build from 2026-08-11 (brain_merge_results.json backups exist on sov-repull's .stash). |
| dsh-agent-backend-01 | EXITED | CPU | 0.06 | — | inferred-unverified: DSH backend, likely no model artifacts. |
| oowm-agent-02-measure | EXITED | CPU | 0.06 | — | inferred-unverified: likely empty shell like agents 03/04/05. |

Reachability summary: **7 pods reached and inventoried, 2 running-but-unreachable (timeout), 9 stopped.**

---

## 2. The model census

Base families found (every trained artifact traces to one of these):
- **Qwen2.5-1.5B-Instruct** — the sov33 line (v10/v12) and the fix_runs self-improving loop.
- **Qwen2.5-0.5B-Instruct** — the asi_results c1/c2 LoRAs and the csoai-training mlx family (fused 266M models, cards gguf).
- **Qwen1.5B q4 mlx** — mac-migrate mlx checkpoint line.

### sov-repull-20260808 (RTX 3090)

| Artifact | Path (pod) | Size | Family | Eval evidence | State |
|---|---|---|---|---|---|
| sov33-v12 adapter | /workspace/p5/sov33-v12/adapter/ | 71M | sov33 (Qwen2.5-1.5B) | run.json: 1972 examples, 3 epochs, loss 0.399, dataset "p5-hard-probe (wrong 3x)" | **harvested-verified** |
| fix_runs BEST adapter | /workspace/fix_runs/BEST/ | 8.4M | fix_loop (Qwen2.5-1.5B) | 40+ report.json harvested; promotes: 20260814T050423Z **+2.5 held-out (generalized)**, 20260814T052727Z +1.8, 20260814T044008Z +1.1 | **harvested-verified** |
| fix_runs hourly adapters (~40) | /workspace/fix_runs/2026081*/adapter/ | 8.4M each | fix_loop | each has report.json with PROMOTE/REVERT verdict + per-axis before/after | reports harvested-verified; adapters catalogued-not-pulled (BEST supersedes) |
| refusal-lora merged | /workspace/refusal-lora-repull/merged/model.safetensors | 943M | refusal (1.5B merged) | none found beside it | catalogued-not-pulled |
| oowm_merge_v1 | /workspace/oowm_merge_v1/model.safetensors | 943M | oowm merge | oowm_merge_v1_results.json (on sovos-light, harvested) | catalogued-not-pulled |
| fix_runs 20260814T043155Z fused | /workspace/fix_runs/20260814T043155Z/adapter/model.safetensors | 1.1G | fix_loop fused | report.json harvested | catalogued-not-pulled |
| sov33-v10.q8.gguf | /workspace/.stash/mac-backup/oowm-v8-e2e/p5/ | 267M | sov33 | oowm_v8_benchmark_results.json harvested | catalogued-not-pulled (superseded by v12) |
| lora_c1_final / lora_c2_final | /workspace/sovos-repo/asi_results/adapters/ | 4.2M each | asi (Qwen2.5-0.5B, r=8) | asi_results cycle_1..3_training.jsonl nearby | **harvested-verified** |

### sovos-light-master-mine-20260816 (A100, network volume ca-mtl-3)

| Artifact | Path (pod) | Size | Family | Eval evidence | State |
|---|---|---|---|---|---|
| mlx adapter family (16 sets: v6, v7, jail, jail-knowledge, jail-tool, jail-tool-v2, knowledge, knowledge2, evat-facts, gov, tool, night, 15b, gemma, adapters, adapters2) | /workspace/csoai-training/mlx/mlx/adapters-*/ | 2.9M each (+checkpoints) | csoai mlx (Qwen2.5-0.5B) | trained for the cards/jail/tool line; govbench_results.json + care_gate_eval.json harvested | **harvested-verified** (all 16, incl. checkpoints) |
| jail-tool-fused / jail-tool-v2-fused / tool-fused / merged | /workspace/csoai-training/mlx/mlx/*/model.safetensors | 266M each | csoai mlx fused | — | catalogued-not-pulled |
| qwen2.5-0.5b-cards.gguf | /workspace/csoai-training/mlx/mlx/ | 507M | csoai mlx | — | catalogued-not-pulled |
| sovereign-v3 | /workspace/sovereign-v3/model.safetensors | 617M | sovereign | — (no eval found beside it) | catalogued-not-pulled |
| burn-evac oowm_merge_v1 | /workspace/burn-evac-3090/oowm_merge_v1/model.safetensors | 943M | oowm merge | oowm_merge_v1_results.json **harvested** | catalogued-not-pulled (dupe of sov-repull copy) |
| jeeves-exec asi lora_c1/c2_final | /workspace/jeeves-exec/asi_results/adapters/ | 4.2M each | asi (0.5B) | overnight_results.json, benchmark_results.json harvested | **harvested-verified** |

### sov-volume-sink-cpu (network volume euro, 2.3P — survives pod death)

| Artifact | Path (pod) | Size | Family | Eval evidence | State |
|---|---|---|---|---|---|
| sov33-v12.q8.gguf | /workspace/sovos-harness/oowm-v8-e2e/p7v2/ | 61M | sov33 | dataset_sov33_v12_results/{results,gpqa_results}.json harvested (GPQA diamond acc_norm 0.308) | **harvested-verified** |
| sov33-v10.q8.gguf | /workspace/sovos-harness/oowm-v8-e2e/p5/ | 507M | sov33 | leaderboard_results (BBH etc.) harvested | catalogued-not-pulled |
| sov-minimal-output | /workspace/sovos-harness/csoai-static-deploy2/sov-minimal-output/model.safetensors | 1.9G | sov-minimal | — | catalogued-not-pulled |
| mac-migrate mlx-adapters (14 timestamped checkpoints 08-14→08-16) | /workspace/RAG/mac-migrate/mlx-adapters/ | 17–21M each | mac mlx (qwen1.5b-q4) | — | latest (20260816T080000Z) **harvested-verified**; rest catalogued-not-pulled |
| deploy-staging mlx_adapters incl. `proof` | /workspace/offload-dsh/csoai-static-deploy2/.deploy-staging/mlx_adapters/ | small | mac mlx | — | proof **harvested-verified** |
| qwen1.5b-q4 mlx base | /workspace/RAG/mac-migrate/mlx-models/qwen1.5b-q4/ | 829M | base (public) | n/a | catalogued-not-pulled (re-downloadable) |

### The good ones we're missing (eval evidence exists, bytes were pod-side only)
1. **fix_runs BEST + the +2.5 generalized run** — now harvested. Was the top flight-risk: the only measured self-improving-loop win lived on a $0.22/hr community 3090.
2. **sov33-v12 adapter + q8 gguf** — now harvested (adapter from sov-repull, gguf from the euro volume).
3. **oowm_merge_v1 (943M)** — has a results JSON but the model itself is still only on two pods (sov-repull + sovos-light burn-evac). Not pulled (size); next candidate for HF upload from the pod directly.
4. **sovereign-v3 (617M)** — no eval evidence found next to it; measure before spending bandwidth.

---

## 3. Harvested (bytes now on the Mac)

Location: `/Users/nicholas/clawd/model-harvest/` — 456M, 169 files + sha256 manifest.
Full model-artifact checksums: `/Users/nicholas/clawd/model-harvest/SHA256SUMS.models.txt` (59 entries).
Key artifacts:

| File | Size | sha256 |
|---|---|---|
| sov-repull-20260808/p5/sov33-v12/adapter/adapter_model.safetensors | 71M | 159ca69b946087d87716bfbecfe44ba60613836a21eaa830381f610a5b3434c2 |
| sov-repull-20260808/fix_runs/BEST/adapter_model.safetensors | 8.4M | 34d00cefdec7c6483937df8d9fb4b47438f2db36fd6c69ea829489dbb07171a1 |
| sov-volume-sink-cpu/.../p7v2/sov33-v12.q8.gguf | 61M | b194c00a84763caa62165b4732b038d8aeb6afecd483cae39c1f43f900e0e4b3 |

Also harvested (see SHA256SUMS for the rest):
- All 40+ fix_runs `report.json` verdict files (the loop's measured history).
- All 16 csoai mlx adapter sets with checkpoints (~190M).
- asi lora_c1/c2_final from both sovos-repo and jeeves-exec.
- Eval JSONs: govbench_results, care_gate_eval, oowm_v8_benchmark_results (x2 pods), overnight_results, oowm_merge_v1_results, leaderboard_results (BBH), dataset_sov33_v12_results (GPQA), care_scorer/care_divergence results.
- Training data: train.signed.jsonl (signed corpus, 1.8M), p5_train_chat.jsonl + v11, refusal_sov33_rebuild.jsonl, sov33-unified_latest.jsonl.

**Not yet in git/HF** — the harvest dir is local-only on the Mac. Next durability step: push adapters + eval JSONs to a private HF repo (they are small); the Mac alone is still one machine.

---

## 4. STOPPED pods (unminable right now — need an owner start)

| Pod | $/hr if started | Likely contents (inferred-unverified) | Priority |
|---|---|---|---|
| k3-autodeploy-20260824 | 1.59 | Freshest stopped pod (08-24). K3 autodeploy lane state. | HIGH — most recent, unknown contents |
| sov-brain-a100-fresh-20260811 | 1.19 | sov-brain build; brain_merge results exist in backups elsewhere | MEDIUM |
| sov33-master-takeover / -v2 | 1.19 | sov33 takeover artifacts; v2-migration (running twin) is unreachable so these may hold the only other copy | MEDIUM |
| sov-fuel-train-20260804091151 / retry0 | 0.22 | fuel-train LoRAs from 08-04, likely superseded by sov33-v12 | LOW |
| council-ring-a100-20260818 | 1.39 | council-ring experiments | LOW |
| overnight-bench-a100-v2 | 1.19 | per memory, the v2 run was already lost with its pod | LOW |
| oowm-agent-02-measure, dsh-agent-backend-01 | 0.06 | almost certainly empty shells (agents 03/04/05 are) | SKIP |

Also flag: **sov33-master-takeover-v2-migration is RUNNING at $1.19/hr but SSH-unreachable** (timeout on 104.255.9.187:12820, both this run and the prior attempt). Its bytes are hostage until it answers or is inspected via the RunPod web terminal.

---

## 5. Master-stack merge plan

Two mergeable families, one clean lane each. **Never mix bases.**

### Lane A — the 1.5B sov33 master stack (the real candidate)
- Base: `Qwen/Qwen2.5-1.5B-Instruct`.
- Inputs (all harvested): `sov33-v12` adapter (r=16, loss 0.399, 1972 ex) + `fix_runs/BEST` (the compounding loop's promoted state, +2.5 held-out generalized on 2026-08-14).
- Plan: mergekit (already cloned on sov-repull at `/workspace/mergekit`) — TIES or dare_ties over the two adapters applied to the base; alternatively stack-apply (v12 first, BEST on top) since BEST was trained as a delta on measured failures.
- Optional third input: `refusal-lora-repull/merged` — but per the "names promise what code lacks" rule, PROBE it first; six models named "refusing" don't refuse.
- **Gate before "good" is ever claimed:** the same 9-axis held-out battery the fix_loop reports use (governance, safety, provenance, continuity, conformance, openness, care, mach, art5). Merge passes only if unseen-set mean ≥ max(v12 alone, BEST alone) and no axis regresses >2 pts. Report the number; UNTESTED until measured.

### Lane B — the 0.5B cards/jail/tool stack
- Base: `Qwen/Qwen2.5-0.5B-Instruct`.
- Inputs (all harvested): mlx adapters {v7, jail-knowledge, knowledge2, gov, tool, jail-tool-v2, evat-facts, night} + asi lora_c1/c2_final.
- Note: fused checkpoints (jail-tool-fused, jail-tool-v2-fused, tool-fused) already exist pod-side — the merge may already be done; measure those first before merging again.
- Gate: GovBench (never hand-roll a one-off test) + the jail UNTESTED-enforcement probes.

### Not merge candidates
- `sovereign-v3`, `sov-minimal-output`, `oowm_merge_v1` — different/unknown lineage or already-merged outputs; measure before any further use.
- mac-migrate mlx line — qwen1.5b-q4 mlx base, keep as its own continuity backup lane.

### Order of operations
1. Push `/Users/nicholas/clawd/model-harvest` adapters + evals to private HF (durability: second machine). 
2. Probe refusal-lora merged (GovBench safety axis) from the pod before deciding to include it.
3. Run Lane A merge on the already-running sov-repull 3090 (mergekit is there; adapters are small) — no new pod needed.
4. Gate with the held-out battery; only a measured pass gets the name "master stack".
5. Owner decisions: stop kimi-k2-lora-train (empty, $1.39/hr ≈ $33/day) and the three empty oowm agents unless the mesh needs them; investigate the unreachable v2-migration pod.

---

## 6. Honesty ledger

- **harvested-verified**: sov33-v12 adapter (+tokenizer+run.json), fix_runs/BEST, 40+ fix_runs reports, 16 mlx adapter sets, asi c1/c2 (x2 pods), sov33-v12.q8.gguf, mac-migrate 20260816T080000Z, proof adapter, all listed eval JSONs, signed train data. All sha256'd.
- **catalogued-not-pulled**: refusal-lora merged (943M), oowm_merge_v1 (943M x2), sovereign-v3 (617M), sov-minimal (1.9G), fused 0.5B models (266M x4), cards gguf (507M), sov33-v10 ggufs (267M/507M), 13 older mac-migrate checkpoints, ~39 superseded fix_runs adapters, qwen1.5b-q4 base.
- **inferred-unverified**: everything on the 9 stopped pods and the 2 unreachable ones. No claim is made about their contents beyond names and dates.
- Merged-model quality: **no merged model in this plan is called good — none has passed the gate yet.** The only measured wins on record are fix_loop promotes (+2.5/+1.8/+1.1 held-out) and the benchmark JSONs harvested beside sov33-v12.
