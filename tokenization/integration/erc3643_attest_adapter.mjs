// erc3643_attest_adapter.mjs — the concrete ERC-3643 <-> Council OS attestation seam.
//
// Reads an ERC-3643 (T-REX) token's PUBLIC on-chain surface and returns the exact
// reference data the private /engine needs to measure it — then describes where our
// attestation attaches ALONGSIDE the token (EAS recipient = token contract), never
// inside its transfer logic. This is how we "synergize with T-REX without asking":
// ERC-3643 exposes identity/compliance state publicly; we read it, measure it, and
// attest independently. No issuer opt-in, no permission, no ownership touched.
//
// ERC-3643 public reads (from the T-REX interface, no write access needed):
//   token.identityRegistry()   -> the ONCHAINID registry address
//   token.compliance()         -> the modular compliance contract
//   token.totalSupply(), name(), symbol(), decimals()
//   identityRegistry.isVerified(holder) -> per-holder eligibility (public view)
//
// The engine consumes these to score (e.g. holder-concentration, compliance-module
// set, supply vs. claimed reserve). The verdict is signed and attached via EAS with
// recipient = the token contract. The token issuer is untouched and uninvolved.

export const meta = {
  standard: "ERC-3643 (T-REX)",
  bridged_from: "tokenization/erc3643-t-rex (TokenySolutions/T-REX, GPL-3.0 submodule)",
  boundary: "READ-ONLY public views + independent attestation alongside. NOT issuance, NOT ownership, NOT the transfer-agent role.",
};

// Descriptor the batch runner + MCP tool consume. Kept declarative so the open layer
// needs no key and no write access — pure reference plumbing.
export function erc3643Reference(tokenContract) {
  return {
    standard: "ERC-3643",
    contract: tokenContract,
    public_reads: [
      { call: "name" }, { call: "symbol" }, { call: "decimals" }, { call: "totalSupply" },
      { call: "identityRegistry" }, { call: "compliance" }, { call: "paused" },
    ],
    // what the engine derives (measurement is deterministic, no model judges another)
    measurable_signals: [
      "holder_concentration (from Transfer events / identityRegistry)",
      "compliance_module_set (which restrictions the token enforces)",
      "supply_vs_claimed_reserve (needs an off-chain reserve source — flag if absent)",
      "pause_state / clawback_capability (governance surface)",
    ],
    attach_pattern: {
      rail: "EAS off-chain (free) or on-chain (discoverable on easscan.org)",
      recipient: tokenContract,
      note: "attestation references the contract as DATA; it is not wired into the token's compliance modules, so no issuer cooperation is required and no rights are conferred",
    },
    measurementStatus: "UNMEASURED",
  };
}
