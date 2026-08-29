# compliance — Council of AI attestation engine, EU-readiness pack

Pack date: **2026-08-25**. Owner: CSOAI Ltd (UK #16939677). This directory is a
readiness pack, not a legal opinion. Every item that needs counsel or an owner
decision is marked **TODO** rather than asserted.

## What this engine is (and is not)

Council OS signs **opinions / measurements ABOUT assets and AI systems**. It is a
**pure attestor**:

- **No token issuance** — the engine never mints ownership or a security. The
  `tokenization/` tree is a *bound reference* (ERC-3643 T-REX) for integration
  contracts only; issuance, if ever, is via a regulated partner
  (Securitize / Tokeny / Archax / Ownera), never in this tree.
- **No custody** — we hold no client assets, funds, or private keys on behalf of
  a third party. The only keys we hold are our own Ed25519 signing keys used to
  sign attestations.
- **No synthetic exposure** — no derivatives, no leverage, no financial product
  is created, offered, or referenced as investable by this engine.

We measure AI systems against the rules that govern them, sign the result
(Ed25519 over CPython json.dumps of body — not RFC 8785; JCS is catalog-only),
and publish what we cannot yet measure.
**Not a certifier. Scores are never sold. Regulators free forever.**

## Why the posture matters for U.S. securities framing

The SEC's January-2026 staff statement on tokenized securities sets out a
taxonomy for tokenized instruments (issuance, custody, secondary trading of
tokenized securities). A pure attestor that issues no token, custodies nothing,
and creates no synthetic exposure sits **outside** that taxonomy: there is no
security being tokenized, offered, or held. This is not legal advice — it is the
posture we assert and must keep true by construction.

- The staff statement is **staff-level guidance, not a rule or Commission
  action** — it can shift. Treat this section as a living claim, re-checked when
  the SEC acts. **TODO(counsel):** confirm current status of the Jan-2026 staff
  statement and whether any Commission-level action has superseded it.

### The differentiator: unsolicited + permissionless

Our attestations are **unsolicited and permissionless** — we measure a system
whether or not its operator asks us to, and no operator pays for or gates the
measurement. This is the structural opposite of a paid rating relationship. It
is the moat *and* the compliance safety property: there is no issuer on the other
side of a transaction with us.

## Credit-rating / NRSRO hygiene (naming discipline)

The engine's outputs are **compliance / measurement attestations**. They are
**not** credit ratings, and must never be described as such — internally, in
marketing, in the UI, or in machine surfaces.

- **Never** call an output a "credit rating," "rating," "grade," or
  "creditworthiness" assessment. Use "**compliance attestation**" or
  "**measurement attestation**."
- The model is **demonstrably not issuer-paid**: attestations are unsolicited and
  permissionless, and **scores are never sold** (repo doctrine). This is the
  factual basis for staying clear of NRSRO / credit-rating-agency regimes
  (e.g., U.S. NRSRO rules, EU CRA Regulation (EC) No 1060/2009).
- **TODO(counsel):** a formal naming-and-scope memo confirming outputs fall
  outside credit-rating-agency definitions in each target jurisdiction (US, EU,
  UK). Until then this is an asserted posture, not a cleared one.

## The dated obligations that bite in weeks

| Obligation | Date | Doc |
|---|---|---|
| EU AI Act — GPAI enforcement powers live | **2026-08-02** | [eu-ai-act-gpai.md](eu-ai-act-gpai.md) |
| CRA — notified-body provisions apply | **2026-06-11** | [cra-sbom-workflow.md](cra-sbom-workflow.md) |
| CRA — vuln/incident reporting to ENISA applies | **2026-09-11** | [cra-sbom-workflow.md](cra-sbom-workflow.md) |
| CRA — full conformity obligations apply | **2027-12-11** | [cra-sbom-workflow.md](cra-sbom-workflow.md) |
| xrpl.js supply-chain hygiene (CVE-2025-32965, patched) | ongoing | [xrpl-js-hygiene.md](xrpl-js-hygiene.md) |

Machine-readable version for dashboards: [deadlines.json](deadlines.json).

## Files in this pack

- **[README.md](README.md)** — this posture overview.
- **[eu-ai-act-gpai.md](eu-ai-act-gpai.md)** — GPAI model-map template + portability rule.
- **[cra-sbom-workflow.md](cra-sbom-workflow.md)** — SBOM generation + ENISA 24h/72h/14-day runbook.
- **[xrpl-js-hygiene.md](xrpl-js-hygiene.md)** — dependency pinning + SCA note.
- **[deadlines.json](deadlines.json)** — machine-readable dated obligations.

## How to keep this honest

Same rule as the spine: a status we cannot evidence is not a status. Where a
claim needs counsel, it stays **TODO(counsel)**; where it needs an owner
decision, **TODO(owner)**. Do not upgrade a TODO to a green claim without the
evidence next to it.
