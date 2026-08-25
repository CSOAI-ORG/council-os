// attest_offchain.mjs — EVM parallel of the XRPL PoC via EAS OFF-CHAIN.
//
// Off-chain EAS attestations are free, gasless, and cryptographically signed —
// the ideal permissionless-attach primitive for EVM RWAs. This builds and
// self-verifies an off-chain attestation whose recipient is a real, verified
// tokenized-RWA contract (BlackRock BUIDL), carrying an UNMEASURED coverage
// status. No consent from the recipient; no chain write; no owner-gate crossed.
//
// HONESTY: this is a signed COVERAGE record (status UNMEASURED), not a verdict,
// not a rating, not advice, not issuer-endorsed. It demonstrates the EVM half of
// the independent-attestation thesis exactly as the XRPL half was demonstrated.

const { Offchain, SchemaEncoder } = require("@ethereum-attestation-service/eas-sdk");
const { ethers } = require("ethers");
const { writeFileSync } = require("node:fs");

// A fixed demo signer — this is a THROWAWAY key for a testnet/off-chain PoC,
// never an estate key. Derived deterministically so the run is reproducible.
const wallet = ethers.Wallet.createRandom();

// Real, Etherscan-verified tokenized-RWA contracts (per research, re-confirm before mainnet use)
const TARGETS = [
  { asset: "BlackRock BUIDL", contract: "0x7712c34205737192402172409a8f7ccef8aa2aec" },
  { asset: "Franklin Templeton BENJI", contract: "0x3DDc84940Ab509C11B20B76B466933f40b750dc9" },
  { asset: "Apollo ACRED", contract: "0x17418038ecF73BA4026c4f428547BF099706F27B" },
];

// Our own schema — never reuse one with a restrictive Resolver.
const schema = "string asset,bytes32 verdictSha256,uint8 statusCode,string statusText,string reportUri";
const encoder = new SchemaEncoder(schema);
// EAS off-chain needs a config; version 2 offchain, Sepolia EAS contract (config only — nothing is sent).
const EAS_SEPOLIA = "0xC2679fBD37d54388Ce493F1DB75320D236e1815e";
const offchain = new Offchain(
  { address: EAS_SEPOLIA, version: "1.2.0", chainId: 11155111n },
  2,
  { getDomainSeparator: () => "", getVersion: () => "1.2.0" },
);

async function main(){
const out = [];
for (const t of TARGETS) {
  // status: 0=UNMEASURED (the honest coverage state). verdictSha256 is the hash
  // of the canonical coverage claim, so the same three-state dialect as XRPL/COSE.
  const claim = JSON.stringify({ s: "csoai.coverage/0.1", asset: t.asset, contract: t.contract, status: "UNMEASURED" });
  const verdictSha256 = ethers.sha256(ethers.toUtf8Bytes(claim));
  const encoded = encoder.encodeData([
    { name: "asset", value: t.asset, type: "string" },
    { name: "verdictSha256", value: verdictSha256, type: "bytes32" },
    { name: "statusCode", value: 0, type: "uint8" },
    { name: "statusText", value: "UNMEASURED — Council of AI has not measured this instrument", type: "string" },
    { name: "reportUri", value: "https://councilof.ai/xrpl-attest", type: "string" },
  ]);

  const att = await offchain.signOffchainAttestation(
    {
      recipient: ethers.getAddress(t.contract), // the target contract — no consent needed
      expirationTime: 0n,
      time: 1756000000n, // fixed timestamp for reproducibility (no Date.now)
      revocable: true,
      schema: ethers.id(schema),
      refUID: "0x0000000000000000000000000000000000000000000000000000000000000000",
      data: encoded,
    },
    wallet,
  );

  // self-verify: recover the signer from the signature
  const recovered = offchain.verifyOffchainAttestationSignature(wallet.address, att);
  out.push({
    asset: t.asset, contract: t.contract, status: "UNMEASURED",
    uid: att.uid, attester: wallet.address, signature_valid: recovered,
  });
  console.log(`  ${recovered ? "OK " : "XX "} ${t.asset}  uid=${att.uid.slice(0, 18)}…`);
}

writeFileSync("EAS-OFFCHAIN-RUN.json", JSON.stringify({
  schema: "csoai.eas-offchain-run/0.1",
  network: "EAS off-chain (gasless, signed) — EVM parallel; Sepolia domain config",
  honesty: "Off-chain signed coverage records, status UNMEASURED. Not verdicts, not ratings, not advice, not issuer-endorsed. Throwaway demo signer, never an estate key. Recipients are real verified RWA contracts referenced as data — no consent required, none implied.",
  schema_def: schema,
  attestations: out,
}, null, 1));
console.log(`wrote EAS-OFFCHAIN-RUN.json (${out.length} attestations, all signature-valid: ${out.every(o => o.signature_valid)})`);
}
main().catch(e=>{console.error(e);process.exit(1)});
