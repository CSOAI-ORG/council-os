# regwatch — live-regulation cross-reference on free official feeds

Track the regulations that govern the systems we measure, using **free,
official, no-API-key feeds**, and detect when a regulation's text changes by
**SHA-256-diffing** it against a stored hash.

## The approach

1. **Poll free official feeds.** Government publishers already expose the
   authoritative text over open HTTP/REST/SPARQL — no vendor in between, no key.
2. **SHA-256 each regulation's text.** Hash the fetched body. This is the
   **same SHA-256 primitive the attestation core uses** (there over the frozen
   instrument), here applied to regulation-tracking. One primitive, two jobs.
3. **Diff against the stored hash** in `state.json`. Same hash → `UNCHANGED`.
   Different hash → `CHANGED`. Never-seen URL → `NEW`.
4. **Surface a word-level diff** so a human sees *what* moved, not just *that*
   something moved.

### Three-state, never a false "unchanged"

A fetch that fails is **`UNKNOWN`**, never `UNCHANGED`. Reporting "no change"
because we could not reach the server would be a silent false negative — the
estate's recurring defect class. If we did not read the text, we do not claim
it is the same. (Same discipline as `ops/live_status_check.py`, which is unable
to report LIVE on a path it did not complete.)

## Free feeds (no API key)

| feed | what | access |
|------|------|--------|
| **EUR-Lex CELLAR** | EU legal corpus, ~2.7M works, updates within hours | SPARQL endpoint + REST content negotiation |
| **FederalRegister.gov** | US Federal Register documents (rules, proposed rules, notices) | REST API, JSON, no key |
| **eCFR** | US Code of Federal Regulations, current & historical | public REST API, no key |
| **regulations.gov** | US rulemaking dockets & public comments | REST API (free key; `DEMO_KEY` for light use) |
| **IOSCO** | international securities-regulator publications | publications feed |
| **BIS** | Bank for International Settlements publications | publications feed / RSS |

See `feeds.json` for the machine-readable registry.

### Paid RegTech — reserved for gap jurisdictions only

Commercial RegTech (Thomson Reuters Regulatory Intelligence, Corlytics, and
similar) is **reserved only for jurisdictions the free feeds do not cover**. It
is a gap-filler, never the backbone. The backbone is free and official so the
tracking itself carries no vendor dependency.

## Files

- `README.md` — this document.
- `feeds.json` — machine-readable feed registry: name, url, format, auth,
  cadence, jurisdiction, coverage.
- `watch.py` — stdlib-only prototype. Given a URL it fetches (urllib, with a
  User-Agent), SHA-256s the body, compares to the stored hash in `state.json`,
  and reports `CHANGED` / `UNCHANGED` / `NEW` / `UNKNOWN`.

## Running

The committed run does **not** hit live endpoints (they may rate-limit and need
polite scheduling). Prove the diff logic offline instead:

```
python3 regwatch/watch.py --selftest
```

The self-test hashes local fixture strings and proves all three transitions:
unchanged (same bytes), changed (different bytes), and unknown (fetch failure
never collapses to "unchanged").

A real poll, when you choose to run one, is:

```
python3 regwatch/watch.py --url "https://www.federalregister.gov/api/v1/documents.json?per_page=1"
```

It stores the hash in `regwatch/state.json` on first sight (`NEW`) and reports
`CHANGED` / `UNCHANGED` on later runs. Be a polite client: low frequency,
honest User-Agent.
