# EU Cyber Resilience Act (CRA) — SBOM + vuln-reporting readiness

Pack date: **2026-08-25**. Regulation: (EU) 2024/2847 (Cyber Resilience Act).

## Why the CRA applies to us

A **white-labeled or licensed attestation engine sold into the EU** is a
**"product with digital elements"** under the CRA. That triggers two families of
obligation the engine must be ready for:

1. **A software bill of materials (SBOM)** — the manufacturer must identify and
   document the components and dependencies of the product.
2. **A vulnerability- and incident-reporting workflow** — actively exploited
   vulnerabilities and severe incidents must be reported to ENISA (and the
   relevant CSIRT) on tight clocks.

The engine offered **free / permissionless as a reference layer** is a weaker
CRA nexus than the **licensed/enterprise/white-label** distribution. The
white-label path is the one that clearly makes us a "manufacturer placing a
product on the EU market." **TODO(counsel):** confirm which distribution modes
cross the CRA threshold and whether any open-source-steward carve-out applies.

## The dates that bite

| CRA milestone | Date | What it means for us |
|---|---|---|
| Notified-body / conformity-assessment provisions apply | **2026-06-11** | The framework for conformity assessment is live; relevant if the engine is later classified "important"/"critical." |
| **Vulnerability- and incident-reporting obligations apply** | **2026-09-11** | The 24h / 72h / 14-day ENISA reporting clocks are **live** — the runbook below must be operational by this date. |
| Full conformity obligations apply | **2027-12-11** | CE marking, full essential-requirement conformity, and documentation obligations in force. |

**Primary near-term target: have the reporting runbook operational by
2026-09-11.**

## Part 1 — SBOM generation approach

Standardize on **CycloneDX** (widely accepted machine-readable SBOM format;
satisfies "identify and document components and dependencies"). Generate an SBOM
per shipped artifact, store it in the release, and regenerate on every dependency
change.

### JavaScript / TypeScript (the `tokenization/`, `mcp-server/`, frontend trees)

```bash
# CycloneDX SBOM from an npm project
npx @cyclonedx/cyclonedx-npm --output-format JSON \
    --output-file sbom.cdx.json

# (run inside each package dir that has its own package-lock.json)
```

### Python (the `engine/`, `ops/`, `adapters/` tooling)

```bash
# CycloneDX SBOM from the active Python environment / requirements
pip install cyclonedx-bom
cyclonedx-py environment  -o sbom-py.cdx.json      # from installed env
cyclonedx-py requirements requirements.txt -o sbom-py.cdx.json  # from a lockfile
```

### Aggregate + attach

- Generate one SBOM per language/package, then keep them together per release
  (e.g. `release/<version>/sbom/*.cdx.json`).
- **Sign the SBOM with the same Ed25519 root the engine already uses** so the
  SBOM is itself an attested artifact — consistent with repo doctrine
  ("everything ships signed or does not ship").
- Attach the SBOM to the licensed/white-label deliverable so the downstream
  operator inherits a verifiable component list.

### Software-composition analysis (SCA) — automate it

- Run SCA in CI so a known-vulnerable dependency fails the build. Options that
  consume the CycloneDX SBOM or the lockfiles directly:
  - `npm audit` (and `npm audit --audit-level=high`) for the JS trees.
  - `pip-audit` for the Python trees.
  - An SBOM-aware scanner (e.g. Grype / Trivy / OSV-Scanner) run over the
    generated `*.cdx.json`.
- **TODO(owner):** add an SCA gate to `.github/workflows/ci.yml` that (a) builds
  the SBOM, (b) scans it, (c) fails on high/critical with no accepted-risk note.

## Part 2 — ENISA vulnerability & incident reporting runbook

Applies from **2026-09-11**. Three clocks. All start from the moment the
manufacturer **becomes aware**. Reports go to ENISA via the single reporting
platform, with notification also to the relevant national CSIRT. The trigger is
an **actively exploited vulnerability** in the product, or a **severe incident**
affecting the product's security.

### Roles (assign real people before 2026-09-11)

- **Incident Lead** — owns the clocks, makes the call to report, is the ENISA
  point of contact. **TODO(owner): name.**
- **Engineering On-Call** — confirms the technical facts (is it exploited? which
  component? which CVE/dependency?). **TODO(owner): name / rota.**
- **Counsel / Compliance** — reviews wording of external reports, coordinates
  with any regulated tokenization partner. **TODO(counsel): name.**
- **Comms / Customer** — notifies affected white-label licensees. **TODO(owner).**

### The three windows

| Window | Deadline from awareness | What to submit | Owner |
|---|---|---|---|
| **Early warning** | **within 24 hours** | Initial notification: that an actively exploited vuln / severe incident exists; whether it is believed unlawful/malicious; which member states may be affected. Minimal facts, sent fast. | Incident Lead |
| **Notification** | **within 72 hours** | Updated report: severity and impact assessment, and where available indicators of compromise + any corrective/mitigating measures taken or advised. | Incident Lead + Engineering On-Call |
| **Final report** | **within 14 days** (vuln) / after handling (incident) | Full report: description of the vulnerability/incident, its severity and impact, root cause, and the mitigation/remediation applied. | Incident Lead + Engineering On-Call + Counsel |

Notes on the clocks:

- The 24h/72h windows are the CRA reporting cadence to ENISA; the 14-day final
  report closes out an actively-exploited-vulnerability case. **TODO:** confirm
  the exact wording of each window against the final CRA text + ENISA platform
  guidance and attach dated links — treat the table as operational scaffolding
  to verify, not as the legal text.
- **Also notify** the relevant national CSIRT and, where required, affected
  users/licensees — this is separate from the ENISA filing.

### The runbook (step-by-step when an issue lands)

1. **Detect / receive** — a report arrives (SCA alert, upstream advisory, user
   report, our own finding). Log the **awareness timestamp** — the clocks start
   now.
2. **Triage (Engineering On-Call)** — is it *our* product's issue? Is it
   *actively exploited* or a *severe incident*? Which component/CVE? Check the
   SBOM to see if a vulnerable dependency is actually shipped.
3. **Decide (Incident Lead)** — reportable? If yes, start the 24h clock formally
   and open the incident record.
4. **24h — early warning** to ENISA + CSIRT.
5. **Contain / mitigate (Engineering)** — patch, pin, or disable the affected
   path; prepare licensee guidance.
6. **72h — notification** update to ENISA with severity + IoCs + measures.
7. **Notify affected white-label licensees** with the fix/mitigation.
8. **14 days — final report** with root cause + remediation.
9. **Post-incident** — regenerate + re-sign the SBOM, add an SCA rule so the
   class of issue is caught next time, and record the incident in a register.

### Pre-2026-09-11 checklist

- [ ] **TODO(owner):** register / confirm access to the ENISA single reporting
      platform and identify the relevant national CSIRT contact.
- [ ] **TODO(owner):** assign the four roles above to named people with a rota.
- [ ] **TODO(owner):** stand up the SBOM generation + signing per release.
- [ ] **TODO(owner):** add the SCA gate to CI.
- [ ] **TODO(owner):** create the incident register (where incidents + timestamps
      are logged).
- [ ] **TODO(counsel):** confirm which distribution modes make us a CRA
      "manufacturer" and the precise reporting-window wording.
