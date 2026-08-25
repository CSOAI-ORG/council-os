# xrpl.js — dependency pinning + supply-chain hygiene

Pack date: **2026-08-25**. Severity: **routine hygiene — the CVE is already
patched upstream.** This note exists so the fix stays pinned and does not
regress.

## Current state in this repo

- As of this pack date, **no `package.json` in the tree pins `xrpl`** (checked:
  the only `package.json` with dependencies is `tokenization/erc3643-t-rex`, and
  `publishers/` is a README placeholder). xrpl.js is the **intended** publisher
  library for the XRPL Memo + XLS-70 attestation-attach stage described in
  `MONOREPO.md`, not yet a wired dependency.
- **Action:** when the XRPL publisher stage is wired, pin xrpl.js correctly from
  the first commit (below), so the compromised range is never reachable.

## The vulnerability (context, already resolved)

- **CVE-2025-32965** — a supply-chain compromise of the `xrpl` npm package.
- **Compromised versions: 4.2.1, 4.2.2, 4.2.3, 4.2.4, and 2.14.2.**
- **Fixed in 4.2.5 and 2.14.3.** Current stable line is **5.x**.
- Treat as **routine hygiene**: the fix is published; the job is to pin at or
  above the fix and never let a lockfile drift back into the bad range.

## The pinning rule

- Pin xrpl.js to **≥ 4.2.5**, and prefer the **current 5.x** stable line for new
  work.
- **Never** allow a resolved version in the compromised range
  (`4.2.1`–`4.2.4`, `2.14.2`). Verify the *resolved* version in the lockfile, not
  just the declared range.
- Example (adjust to the real target version at wiring time):

```jsonc
// package.json — when the XRPL publisher stage is added
{
  "dependencies": {
    "xrpl": "^5"          // current stable line; or ">=4.2.5" if held on 4.x
  }
}
```

```bash
# verify the resolved version never sits in the bad range
npm ls xrpl
```

## Software-composition analysis (SCA)

Fold this into the same SCA gate described in
[cra-sbom-workflow.md](cra-sbom-workflow.md):

- Run `npm audit --audit-level=high` in CI for any package that adds xrpl.js.
- Include xrpl.js in the CycloneDX SBOM so an SBOM-aware scanner
  (Grype / Trivy / OSV-Scanner) flags any future advisory automatically.
- **TODO(owner):** add a CI check that fails if `npm ls xrpl` resolves into the
  compromised range.

## npm account-security changes to plan for

The npm registry is tightening publish security on a timeline that affects how we
consume and (if ever) publish packages:

- **From ~August 2026:** changes to **npm 2FA / granular access tokens** — token
  lifetimes and 2FA-on-publish requirements tighten. Ensure any automation token
  used in CI is a current granular token with least privilege and a short
  lifetime.
- **From ~January 2027:** a move toward **direct/trusted publishing** (reducing
  reliance on long-lived tokens, favoring OIDC-style trusted publishing from CI).

Actions:

- **TODO(owner):** audit any npm tokens in CI/secrets; rotate to short-lived
  granular tokens; enable 2FA-on-publish for any account that can publish.
- **TODO(owner):** if/when we publish any package (e.g. a client SDK for the
  attestation engine), plan for trusted/direct publishing from CI rather than a
  stored token.
- **TODO:** re-verify the exact npm dates and mechanics against npm's official
  changelog before relying on them — attach dated links.

## One-line summary

xrpl.js CVE-2025-32965 is already fixed upstream; our job is to **pin ≥ 4.2.5 /
current 5.x from the first commit that adds it, verify the resolved version, and
keep an SCA gate + least-privilege npm tokens in place.**
