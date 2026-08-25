// adapters/evm/blackrock-buidl/index.js — DeFiLlama-style reference adapter (EVM).
export const meta = { instrument: "BlackRock BUIDL", chain: "Ethereum",
  contract: "0x7712c34205737192402172409a8f7ccef8aa2aec", standard: "permissioned ERC-20 / security token" };
export async function reference() {
  return { instrument: meta.instrument, contract: meta.contract,
    reads: [{ call: "totalSupply" }, { call: "name" }, { call: "symbol" }],
    measurementStatus: "UNMEASURED" };
}
