// adapters/evm/franklin-templeton-benji/index.js — DeFiLlama-style reference adapter (EVM).
export const meta = { instrument: "Franklin Templeton BENJI", chain: "Ethereum",
  contract: "0x3DDc84940Ab509C11B20B76B466933f40b750dc9", standard: "permissioned ERC-20 / security token" };
export async function reference() {
  return { instrument: meta.instrument, contract: meta.contract,
    reads: [{ call: "totalSupply" }, { call: "name" }, { call: "symbol" }],
    measurementStatus: "UNMEASURED" };
}
