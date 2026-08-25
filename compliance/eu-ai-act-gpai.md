# EU AI Act — GPAI exposure map (Council of AI attestation engine)

Pack date: **2026-08-25**. Status: **template — model rows are TODO**, do not
invent which models the engine uses.

## The deadline that bites

**2026-08-02 — GPAI enforcement powers went live.** From this date the EU AI
Office can exercise its supervision and enforcement powers over general-purpose
AI (GPAI) models:

- **Request documentation** (technical documentation, training-data summary,
  copyright policy, and — for models with systemic risk — model evaluations and
  adversarial-testing records).
- **Conduct or require evaluations** of a model.
- **Request mitigations, restrict, or withdraw** a model from the EU market.
- **Fines up to €15,000,000 or 3% of total worldwide annual turnover**, whichever
  is higher, for GPAI-provider infringements.

### Why this is *our* exposure, not only the model vendor's

The AI Office's primary target is the **GPAI provider**. But **any GPAI model
embedded in our attestation engine that touches EU users** creates
**vendor-compliance exposure in OUR posture**: if a vendor's model is restricted,
mitigations are imposed, or its documentation/Code-of-Practice status lapses, the
part of our engine that depends on it can be disrupted or non-conformant. We must
know, per component, which model we depend on and whether it is EU-exposed.

**TODO(owner):** confirm whether Council OS itself is (a) only a *downstream
deployer* of third-party GPAI, or (b) also fine-tunes/modifies a model such that
it could be treated as a GPAI provider in its own right. The answer changes which
obligations attach to us directly.

## Model-map table (fill the rows)

One row per engine component that invokes a model. Leave a row as TODO until the
actual model is confirmed — **do not guess the model or vendor.**

| Engine component | GPAI model used | Vendor | EU exposure (Y/N) | Code-of-Practice status | Portability fallback |
|---|---|---|---|---|---|
| _e.g. harness / grader lane_ | TODO | TODO | TODO | TODO | TODO |
| _e.g. specialist model lane_ | TODO | TODO | TODO | TODO | TODO |
| _e.g. summarization / report gen_ | TODO | TODO | TODO | TODO | TODO |
| _e.g. MCP server tool calls_ | TODO | TODO | TODO | TODO | TODO |
| _e.g. frontend copilot (AG-UI)_ | TODO | TODO | TODO | TODO | TODO |

Column definitions:

- **Engine component** — the specific place in the tree that calls a model
  (`engine/`, `mcp-server/`, `adapters/`, frontend copilot, etc.). Note: the
  spine doctrine is **"no model judges another"** — the deterministic grader must
  stay model-free; a model appearing in a *grading* row is a red flag to
  investigate, not fill in.
- **GPAI model used** — exact model id/version.
- **Vendor** — the GPAI provider responsible under the Act.
- **EU exposure (Y/N)** — does this component serve or process data for EU users?
  If Y, vendor restrictions propagate to us.
- **Code-of-Practice status** — has the vendor signed the GPAI Code of Practice,
  and is documentation/copyright-policy available? (Signing is voluntary but is
  the presumption-of-conformity path.) TODO per vendor.
- **Portability fallback** — the *other* model/vendor this component can switch
  to, and how fast. Empty = single point of failure.

## The rule: build for model portability

**Design so that one vendor restriction cannot halt the product.**

- **Every model-calling component must have at least one named fallback** in the
  table above. A component with no fallback is a compliance *and* availability
  single point of failure — the AI Office restricting or withdrawing that one
  model would stop that feature.
- Prefer an **abstraction layer** (provider-agnostic interface) so swapping a
  model is a config change, not a code rewrite. This also matches the repo's
  existing "bind, don't migrate" and adapter-pattern design.
- **Keep grading deterministic and model-free** (spine doctrine): the more of the
  pipeline that is deterministic, the smaller the GPAI-exposed surface, and the
  smaller our AI Act footprint.
- **Record the vendor's documentation location** (technical docs, training-data
  summary, evaluation records for systemic-risk models) so that if the AI Office
  asks us — as a deployer — where our upstream model's docs are, we can answer.

## Owner / counsel actions

- **TODO(owner):** populate every row of the model-map table with real models.
- **TODO(owner):** ensure each row has a working portability fallback.
- **TODO(counsel):** confirm our classification (deployer vs. provider) and
  whether any component touches "high-risk" use cases under the Act (separate
  obligations from GPAI).
- **TODO(owner):** wire a check that fails CI if a new model-calling code path is
  added without a corresponding row here.

## Sources to re-verify (do not cite from memory)

The dates and figures above (2026-08-02 enforcement powers; €15M / 3% turnover)
should be re-confirmed against the official Regulation (EU) 2024/1689 text and the
AI Office's published guidance before external use. **TODO:** attach dated links.
