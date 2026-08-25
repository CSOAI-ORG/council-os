# Council of AI — measurement methodology

*Public methodology statement. Version 0.1, 2026-08-25.*

Council of AI is an independent measurement body. We measure AI systems (and, on the
financial axes, tokenized assets) against the rules that govern them, sign the result
(Ed25519 over RFC 8785 canonical JSON), and publish what we cannot yet measure. We do
not certify; determination stays with authorities. Scores are never sold. This document
states, in public, exactly how a number becomes a signed verdict — the discipline the
competitive field does not disclose.

## 1. Deterministic grading — no model judges another

Every score is produced by a deterministic predicate against a frozen gold label. No LLM
is used as a judge of another model's output. An answer that cannot be parsed into the
graded form is counted **incorrect**, never silently dropped. This is a design rule, not
an aspiration: a component must be *structurally unable* to report success on a path it
did not complete.

## 2. Confidence intervals — Wilson score, always

For every proportion metric (accuracy, pass-rate) we report a **Wilson score 95%
interval**, not a Wald interval. Wilson is the de-facto standard for eval proportions
precisely because it does not fail near 0 and 1 where Wald produces impossible bounds.
Reference: E. B. Wilson (1927), "Probable Inference, the Law of Succession, and
Statistical Inference," *JASA* 22(158). Nothing below n≥30 is quoted.

## 3. Separation — a deliberately conservative anti-overclaiming rule

We declare a **leader** only when its Wilson interval does **not** overlap the fleet
mean (`stat_suite.separated_leaders`). When the leader's interval contains the fleet
mean, we report **TIE — statistically indistinguishable**, never a win. Worked example
(the jail axis, from live aggregates): 42/71 computes to **TIE** — the leader's edge is
not separated from the field, so the public grammar honestly reports it as unresolved.

**We state plainly that this rule is deliberately conservative.** Overlapping confidence
intervals do not, by themselves, prove non-significance — two estimates can overlap yet
differ under a paired test. Our overlap-with-fleet-mean rule errs toward *not*
overclaiming a leader, which is the honest direction for a body whose product is trust.
It answers the question "is this a proven leader versus the whole field," and it is
audit-friendly by construction.

## 4. Head-to-head — paired McNemar for leader-vs-runner-up

For a specific "does A beat B" claim (as opposed to "is A separated from the field"), the
field standard is a **paired McNemar test** on question-level differences, not a
comparison of population summaries — see E. Miller, "Adding Error Bars to Evals"
(arXiv:2411.00640, Anthropic, 2024), recommendation 4. Where we make a head-to-head
leader-vs-runner-up claim, it is backed by a paired McNemar test at α=0.05, complementing
(not replacing) the conservative fleet-mean separation rule above. Miller documents that
clustered standard errors can be >3× naive ones; we compute clustered errors where
questions come in related groups (recommendation 2).

## 5. Three-state verdicts — UNMEASURED is a first-class answer

Every cell is **pass / fail / UNMEASURED**. UNMEASURED is reported, never hidden — an
absent measurement is a stated fact, not a blank. This is why the public board reads, and
will keep reading, an honest count (e.g. "13 measured of 14 quotable") until a further
axis actually separates under the rules above.

## 6. Recomputability and corrections

Every number is recomputable from its published rows. Corrections are published, never
silently edited (append-only ledger, signed). A wrong signed measurement is publicly
refutable forever — reputational slashability is the discipline.

## 7. Where we sit versus the field (why this document exists)

Alignment with published best practice: NIST AI RMF **MEASURE** function (uncertainty
measurement + structured reporting), Stanford HELM (multi-metric holistic reporting),
and Miller (2024) for eval statistics. Notably, the most-cited industry leaderboard
(MLPerf/MLCommons) reports point estimates with **no** confidence intervals or
significance testing on rankings — the exact practice Miller critiques. None of the
named on-chain rating/attestation players (Moody's TIE, S&P on-chain SSAs, Chainlink
ACE, Credora/RedStone, Particula) publicly discloses confidence-interval methodology,
statistical-separation testing, or third-party audit of the *statistics* behind their
scores. **Unsolicited + statistically-governed + cryptographically-signed is a
combination none of them offers.** We cannot out-brand Moody's; we out-rigor and
out-independence them, in public.

## 8. Governance direction (stated, not yet claimed)

- Pursuing **ISO/IEC 42001** certification of the internal evaluation-management system
  (process governance) — a third-party-audited credential, marked *in progress*, never
  asserted before earned.
- Voluntarily mapping to **IOSCO's CRA Code of Conduct Fundamentals** vocabulary as
  governance language, while remaining explicitly **not** an ESMA/SEC-registered credit
  rating agency: our outputs are compliance/measurement attestations, never credit
  ratings.

## References
- E. B. Wilson (1927), *JASA* 22(158). · E. Miller (2024), arXiv:2411.00640.
- NIST AI RMF 1.0 (MEASURE). · Stanford HELM. · ISO/IEC 42001:2023; 42005:2025.
- IOSCO CRA Code of Conduct Fundamentals (rev. 2015); Crypto/Digital-Asset Policy
  Recommendations (2023).
