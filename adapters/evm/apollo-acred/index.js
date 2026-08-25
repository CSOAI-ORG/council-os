// adapters/evm/apollo-acred/index.js — DeFiLlama-style reference adapter (EVM).
export const meta = { instrument: "Apollo ACRED", chain: "Ethereum",
  contract: "0x17418038ecF73BA4026c4f428547BF099706F27B", standard: "permissioned ERC-20 / security token" };
export async function reference() {
  return { instrument: meta.instrument, contract: meta.contract,
    reads: [{ call: "totalSupply" }, { call: "name" }, { call: "symbol" }],
    measurementStatus: "UNMEASURED" };
}
