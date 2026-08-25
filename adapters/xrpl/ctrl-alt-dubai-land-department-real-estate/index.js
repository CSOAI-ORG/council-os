// adapters/xrpl/ctrl-alt-dubai-land-department-real-estate/index.js — DeFiLlama-style reference adapter.
// Pulls the reference data the GSPC engine needs to MEASURE this instrument.
// This is the OPEN layer: data only, NO signing, NO verdict. The engine (private)
// consumes what this returns; the publisher (separate stage) attaches the result.
// Anyone — including the issuer — may PR a better adapter for their instrument.
export const meta = {
  instrument: "Ctrl Alt / Dubai Land Department real estate",
  category: "real-estate",
  chain: "XRPL",
  xrplIssuer: null,
  addressStatus: "not-located",
};

// Returns reference data for measurement. Honest by construction: if the issuer
// address is not locatable, the adapter reports that rather than inventing data.
export async function reference() {
  if (!meta.xrplIssuer) {
    return { instrument: meta.instrument, status: "no-public-address",
             note: "no independently confirmable XRPL r-address; not measurable from chain yet" };
  }
  // Live read (caller injects an XRPL client / MCP chain-data tool). Kept as a
  // declarative descriptor so the open layer needs no secrets and no signing key.
  return {
    instrument: meta.instrument,
    xrplIssuer: meta.xrplIssuer,
    reads: [
      { method: "account_info", account: meta.xrplIssuer },
      { method: "account_lines", account: meta.xrplIssuer },
      { method: "gateway_balances", account: meta.xrplIssuer },
    ],
    measurementStatus: "UNMEASURED",
  };
}
