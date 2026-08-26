# On-chain instrument coverage — what the financial axes may actually stand on

**Signed artifact:** [`COVERAGE.json`](COVERAGE.json) · **Signature:** [`COVERAGE.sig.json`](COVERAGE.sig.json)
**Built:** 2026-08-26 · **Regenerate:** `python3 economy/build_coverage.py > economy/COVERAGE.json`
**Verify (stranger, offline):** `python3 economy/verify_coverage.py`

This is the evidence layer the 8 financial/domain axes of [ADR-001](../ADR-001-axis-count.md)
cite. It does not touch the signed board or `functions/api/gspc.ts` — that is a
separate lane. It states what coverage exists, what does not, and where the line
sits.

---

## The coverage claim — and nothing beyond it

> Council of AI has attached signed, independently re-verifiable coverage records
> to the XRP Ledger for **6 tokenized real-world-asset issuers**, and has measured
> **deterministic on-chain control facts** for those same 6. The attestation
> transactions are on **XRPL DEVNET**; the issuer accounts and the control facts
> are read from **XRPL MAINNET**. **Nothing is attested on any Ethereum chain.**
> No risk verdict, rating, score, ranking or opinion on any named instrument has
> been produced, and none may be cited.

Every clause is re-derivable by running the two commands at the top of this file.

**XRPL mainnet is PLANNED, not live.** No mainnet write has ever been made. The
mainnet ledger is *read* (issuer accounts, control flags, declared domains); the
attestations are *written* to devnet.

**We attest, never tokenize.** Nothing here mints, transfers, holds, prices or
represents a security. `gspc_measurement.bridge` maps a card into the
ERC-3643/ONCHAINID claim shape and its `mint`/`transfer` raise by construction.

---

## 1. The 16-instrument XRPL registry, audited against the live chain

Every row below was re-probed on 2026-08-26: the mainnet issuer account was
re-read, and each recorded devnet attestation transaction was re-fetched and
required to come back `validated: true`.

| # | Instrument | Category | Issuer (XRPL mainnet) | State | Evidence |
|---|---|---|---|---|---|
| 1 | Ondo OUSG | treasury | `rHuiXXjHLpMP8ZE9sSQU5aADQVWDwv6h5p` | **VERIFIED** | mainnet acct live (`ondo.finance`); coverage tx `1CA61A8A…` ledger 4764399 validated; control-facts tx `CD26E02B…` ledger 4766104 validated; flags reproduce with **zero drift** |
| 2 | Ripple USD (RLUSD) | stablecoin | `rMxCKbEDwqr76QuheSUMdEGf4B9xJ8m5De` | **VERIFIED** | mainnet acct live (`https://ripple.com/`); `FEA76FB2…` ledger 4764396; `770A7C8B…` ledger 4766101; zero drift |
| 3 | Archax × abrdn USD Liquidity Fund | institutional-fund | `rKCu4CucpepQ6N89c8T5GuX2jkxzCST18Q` | **VERIFIED** | mainnet acct live (`archax.com`); `18E36DCE…` ledger 4764405; `F186ADA1…` ledger 4766112; zero drift |
| 4 | OpenEden TBILL (TBL) | treasury | `rJNE2NNz83GJYtWVLwMvchDWEon3huWnFn` | **VERIFIED** | mainnet acct live (`openeden.com`); `AAA98FFB…` ledger 4764402; `7144FD1F…` ledger 4766108; zero drift |
| 5 | Braza Bank USDB | stablecoin | `rB3y9EPnq1ZrZP3aXgfyfdXQThzdXMrLMc` | **VERIFIED** | mainnet acct live (`tokens.brazacripto.com.br`); `134368CE…` ledger 4764408; `404DBC29…` ledger 4766115; zero drift |
| 6 | Braza Bank BBRL | stablecoin | `rH5CJsqvNqZGxrMyGaqLEoMWRYcVTAPZMt` | **VERIFIED** | mainnet acct live (`tokens.brazacripto.com.br`); `FD4BDF36…` ledger 4764410; `D0B72B73…` ledger 4766118; zero drift |
| 7 | Aviva Investors USD Liquidity Fund | institutional-fund | — | **NOT-BUILT** | no public r-address independently locatable; never attested |
| 8 | Guggenheim Digital Commercial Paper | corporate-paper | — | **NOT-BUILT** | as above |
| 9 | Société Générale-FORGE EURCV | stablecoin | — | **NOT-BUILT** | as above |
| 10 | Ctrl Alt / Dubai Land Department | real-estate | — | **NOT-BUILT** | as above |
| 11 | SBI START tokenized bond | corporate-bond | — | **NOT-BUILT** | as above |
| 12 | Justoken JMWH | commodity | — | **NOT-BUILT** | as above |
| 13 | Ctrl Alt / Billiton diamonds | commodity | — | **NOT-BUILT** | as above |
| 14 | GateHub XAU | commodity | — | **NOT-BUILT** | as above |
| 15 | Schuman Financial EURoP | stablecoin | — | **NOT-BUILT** | as above |
| 16 | Kyobo Life tokenized govt-bond pilot | government-bond | — | **NOT-BUILT** | as above |

**Nothing has gone stale.** Zero rows are STALE and zero are UNRESOLVABLE. XRPL
devnet has not reset since 2026-08-25, all 12 attestation transactions are still
validated on the ledger, and every recorded control flag still matches the live
mainnet account root exactly.

The honest headline is therefore not decay but **scope**: the registry names 16
instruments and covers **6**. Ten were never attested because no public issuer
address could be independently confirmed, and nothing was invented to close the
gap. `REGISTRY.json` already said so; this audit confirms it against the chain
rather than taking its word.

### The capability PoC also still verifies

`verify.py` — the stranger checker that trusts nothing local except the claim
under test — was re-run today and passed. It re-fetches both PoC transactions
from public devnet, re-derives the evidence digest from the **live** signed card
index at `councilof.ai/signed/card_index.json`, and checks the Ed25519 signature:

```
VALID — both attaches verified from public ledger + live signed index alone:
  memo tx        BC767FEF6497832908B2D208101E361C58A6C0B617C5D94419F9274826A77464
  credential tx  958BA25801A068AEA1507FC1649A862C33D59A1D715924794D98D2C66254DC4B
  evidence       card 82994353b8f94337… re-hashed from https://councilof.ai/signed/card_index.json
  signer         cose-interop-1 (25456441b9869087…)
```

### What "measured" means for the 6, precisely

Measured (deterministic, re-checkable by anyone, no model judges anything):
account-root control flags — `RequireAuth`, `NoFreeze`, `GlobalFreeze`,
`DefaultRipple`, `DisallowXRP`, `RequireDest` — plus the declared identity
`Domain`. From these, three mechanical disclosures: whether allowlisting is
enforced, whether the issuer retains freeze capability, whether an identity
domain is declared.

**Not measured, and not claimable:** risk, creditworthiness, solvency, reserve
adequacy, redemption terms, or any aggregate opinion. `measure_financial.py`
refuses to emit one; `risk_verdict` is hard-coded `UNMEASURED`.

---

## 2. The Ethereum / EAS side: **NOT-BUILT**

The estate's research settled on EAS as the registry — no own chain — with
ERC-3643/ONCHAINID as the tokenization bridge. That decision is sound and the
bridge code exists. **The EAS registry itself does not.**

Probed read-only on 2026-08-26 across **Ethereum mainnet** (block 25,838,926),
**Sepolia** (11,570,437) and **Base** (50,476,212). Nothing was sent, signed or
spent. Cross-checked with two independent implementations — an `ethers`-based
probe and the stdlib `eth_call` probe inside `build_coverage.py` — which agree
exactly.

| Question | Answer |
|---|---|
| Is the CSOAI coverage schema registered in the EAS SchemaRegistry? | **No** — on none of the three chains, under **none** of three candidate UIDs |
| Do the 3 recorded attestation UIDs exist on chain? | **No** — `NOT ON CHAIN` on all three chains |
| Has the recorded attester `0xbFB4…a5Bc` ever transacted? | **No** — nonce 0, balance 0, on all three chains |
| Is there estate code that talks to EAS? | **No** — `anchor.py` backends: `dryrun` implemented, `xrpl` **NOT-BUILT**, `eas` **NOT-BUILT**. Zero network calls to EAS anywhere in the tree |
| Are the 3 named RWA contracts real? | **Yes** — BUIDL (703 bytes), BENJI (708), ACRED (170) all have deployed code on Ethereum mainnet. This is the *only* verified EVM fact we hold |

### Two defects in the existing EAS artifact — report, don't paper over

`eas/EAS-OFFCHAIN-RUN.json` cannot be treated as evidence, for two independent
reasons found by re-running the script rather than reading it:

1. **It is not reproducible.** `attest_offchain.cjs` calls
   `ethers.Wallet.createRandom()` at module scope, so every run signs under a
   brand-new throwaway key and emits brand-new UIDs. Re-run today produced
   `0x2b10dfba…`, `0xb5c0b8e6…`, `0xacdc266a…` — none matching the stored
   `0xcf86775d…`, `0xb09437ab…`, `0xa39a6ebd…`. The file's own comment, *"Derived
   deterministically so the run is reproducible"*, is false.

2. **It is not verifiable by anyone, including us.** The artifact stores only
   `{uid, attester, signature_valid: true}`. It stores **no signature**, no signed
   message and no domain separator, and the signing key was never persisted. A
   stranger has nothing to check. `signature_valid: true` is a claim about a
   computation that happened once in a process that has since exited.

A third, smaller issue: the schema UID written into those attestations is
`ethers.id(schema)`. EAS derives a schema UID as
`keccak256(abi.encodePacked(schema, resolver, revocable))`. The UID in the
artifact therefore does not correspond to any schema EAS could ever resolve. All
three candidate UIDs were probed anyway, so "not registered" is not an artefact
of looking in the wrong place.

**Verdict: the Ethereum side is NOT-BUILT.** Not weakly built — absent. It is
recorded that way in `COVERAGE.json` rather than as UNTESTED, because UNTESTED
would imply a proof that merely lacks confirmation.

### The smallest real first step

An **EAS off-chain EIP-712 attestation, done properly** — gas-free, no chain
write, no owner gate crossed. Three changes make it real:

1. **A persistent signer.** Replace `Wallet.createRandom()` with the MPC custody
   in `apps/signing-custody` (which already produces stock signatures over
   arbitrary bytes) or, failing that, a stored scoped key like `cose-interop-1`.
   The attester address must be stable and publishable.
2. **Store the whole attestation.** Persist the full signed object — `domain`,
   `types`, `message`, `signature` — not a boolean. Ship a `verify_eas.js` that
   recovers the signer from the stored bytes, the way `verify.py` does for XRPL.
3. **Use a real schema UID.** Derive it as EAS does. Registering the schema
   on-chain is a separate, **owner-gated** step that costs gas; the off-chain
   attestation does not require it to be verifiable, only to be *discoverable* on
   easscan.

None of that was done here, because step 3's on-chain half is owner-gated and
steps 1–2 belong to whoever owns the EAS lane. This document's job is to say the
gap exists and size it.

---

## 3. What the axes may claim — and what must stay UNMEASURED

### Eligible to be MEASURED

| Axis family | Population | Basis |
|---|---|---|
| On-chain provenance / issuer-control disclosure | **6 XRPL mainnet RWA issuers** | Deterministic account-root flags + declared `Domain`, re-read from XRPL mainnet at build time, zero drift, signed |

That is the whole list. One axis family, six instruments, one chain, devnet
carrier.

### Must stay UNMEASURED — message to the board lane

1. **Any risk / creditworthiness / solvency axis on a named instrument.** Counsel
   gate. Never "credit rating". `measure_financial.py` already refuses to emit one
   and the refusal must survive into the board.
2. **Any EVM / Ethereum-side coverage axis.** Nothing exists on any EVM chain. An
   axis backed by `EAS-OFFCHAIN-RUN.json` would be backed by an unverifiable file.
3. **Reserve adequacy, redemption terms, off-chain disclosure quality.** Nothing
   in this file measures them.
4. **The 10 XRPL instruments with no locatable issuer address.** They are named in
   the coverage universe and measured by nothing.

If the 8 financial/domain axes need broader coverage than one axis family over
six instruments, the honest move is to leave the remainder UNMEASURED in the
signed payload rather than widen the claim. Per ADR-001: *a public count must be
backed by the signed artifact it claims to summarise.*

---

## 4. Signing — and the ANVIL boundary

`COVERAGE.json` is signed by a **3-party threshold Ed25519 key** held in the MPC
custody on the owner's own Oracle host (`oracle-micro-2`, 141.147.73.85,
uk-london-1). The key was created by a distributed key generation inside the
custody: no private scalar was ever assembled on any machine, and signing
requires all three 242-byte shares.

**The existing estate signing key was not used, not read, not copied and not
derived from.** `coverage-onchain-2026` is a new key with its own public key,
published here *alongside* — never replacing — any existing one, per the
append-only rule.

Nothing secret crossed the wire in either direction: the digest went up, the
public key and signature came back. No credential was placed on any pod.

```
keyid       sha256:51f8b46406225a19911dc775bc26cfc0ba9f738f0d50f1b7e24c68effee90b20
public key  ff6a11a75668960e47b319056e1b8ef71af27e5d6b4b8f0f35dbedcff0b941e9
payload     d5d439bbe27a9bfb922a336272a9a71949878ff5400c6311862fa27b22314667
```

### A stranger verifies it offline, with no estate package

Verified in a clean venv containing only `cffi`, `cryptography`, `pip`,
`pycparser` — where `import gspc_measurement`, `import custody`, `import xrpl`
and `import council_os` all raise `ImportError`. The stranger receives three
files and nothing else.

```
VALID -- signed coverage artifact verified from these two files alone.
  file            COVERAGE.json (39279 bytes)
  sha256          d5d439bbe27a9bfb922a336272a9a71949878ff5400c6311862fa27b22314667
  keyid           sha256:51f8b46406225a19911dc775bc26cfc0ba9f738f0d50f1b7e24c68effee90b20
  public key      ff6a11a75668960e47b319056e1b8ef71af27e5d6b4b8f0f35dbedcff0b941e9
  custody         3-party threshold Ed25519 (Coinbase cb-mpc, additive shares), 3 parties
  tamper control  one flipped payload bit was REJECTED
```

Negative controls both reject, which is what makes the positive result mean
something:

```
tampered payload  INVALID: ['digest_mismatch (...)', 'ed25519_invalid']          exit 1
substituted key   INVALID: ['keyid_not_derived_from_public_key (...)',
                            'ed25519_invalid']                                    exit 1
```

Threshold EdDSA does not use RFC 8032's deterministic nonce derivation, but
verification consumes only `R`, `s` and `A` — so a stock verifier is correct and
entirely unaware that MPC was involved.

---

## 5. Re-derivability

`COVERAGE.json` is rebuilt, not edited. `build_coverage.py` uses the Python
standard library only — no estate package, no node, no key, and no code path that
can write to any chain.

```bash
python3 economy/build_coverage.py > economy/COVERAGE.json   # rebuild from live chains
python3 economy/verify_coverage.py                          # check the signature
```

Rebuilding changes `generated_at_utc`, ledger indices, balances and block
numbers, so the file digest moves and **a rebuild invalidates the signature until
it is re-signed**. What must *not* move is `stable_digest_sha256` — a SHA-256
over the (chain, network, instrument, subject, state) view with every volatile
field stripped. If that digest changes, the coverage itself changed.

```
stable_digest_sha256  57dc4e55f0ebae50a163c06752a1a8cbabf7cce233428409cc7d9c8e79085c7c
```

---

## 6. State table

| Item | State |
|---|---|
| 6 XRPL instruments: mainnet issuer accounts live | **VERIFIED** |
| 6 XRPL instruments: coverage attestation txs still validated on devnet | **VERIFIED** |
| 6 XRPL instruments: control-facts attestation txs still validated on devnet | **VERIFIED** |
| 6 XRPL instruments: recorded control flags reproduce against live mainnet | **VERIFIED** (zero drift) |
| 10 XRPL instruments: no locatable public issuer address | **NOT-BUILT** |
| Permissionless-attach PoC (`verify.py`, memo + XLS-70 credential) | **VERIFIED** (re-run today) |
| XRPL mainnet write of any kind | **NOT-BUILT** (owner + counsel gated) |
| EAS schema registered on any EVM chain | **NOT-BUILT** (probed mainnet, Sepolia, Base) |
| Any EAS attestation on chain | **NOT-BUILT** |
| `EAS-OFFCHAIN-RUN.json` reproducible | **NOT-BUILT** (random signer per run — proven by re-run) |
| `EAS-OFFCHAIN-RUN.json` verifiable by a stranger | **NOT-BUILT** (no signature stored) |
| 3 named EVM RWA contracts exist as deployed code | **VERIFIED** (Ethereum mainnet) |
| Estate code path that reaches EAS (`anchor.py` backend `eas`) | **NOT-BUILT** |
| ERC-3643 / ONCHAINID claim bridge refuses to mint | **VERIFIED** (`bridge.py` raises) |
| `COVERAGE.json` signed by 3-party MPC custody | **VERIFIED** |
| Stranger verifies the signature offline with no estate package | **VERIFIED** |
| Tamper + key-substitution negative controls reject | **VERIFIED** |
| Estate signing key touched | **NOT-BUILT** — deliberately (ANVIL) |
| Risk verdict on any named instrument | **NOT-BUILT** — deliberately (counsel) |

---

*Coverage declaration and disclosure measurement only. Not a rating, not a score,
not a ranking, not advice, not an endorsement, not a conformity mark, and not
issuer-endorsed. No instrument named here has consented to or is party to
anything in this file.*
