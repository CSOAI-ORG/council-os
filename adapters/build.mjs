// adapters/build.mjs — run every adapter's reference(), emit adapters-manifest.json.
// Proves the open layer is coherent: each adapter either yields reads or honestly
// declares no-public-address. No signing, no network — pure descriptor assembly.
import { readdirSync, statSync, writeFileSync } from "node:fs";
import { join } from "node:path";
const out = [];
for (const chain of ["xrpl", "evm"]) {
  const base = join("adapters", chain);
  for (const slug of readdirSync(base)) {
    const p = join(base, slug);
    if (!statSync(p).isDirectory()) continue;
    try {
      const m = await import("./" + join(chain, slug, "index.js").replaceAll("\\", "/"));
      out.push({ chain, slug, meta: m.meta, reference: await m.reference() });
    } catch (e) { out.push({ chain, slug, error: String(e).slice(0, 80) }); }
  }
}
writeFileSync("adapters/adapters-manifest.json", JSON.stringify(out, null, 1));
const ok = out.filter(a => !a.error).length, gaps = out.filter(a => a.reference?.status === "no-public-address").length;
console.log(`adapters: ${out.length} total, ${ok} loaded, ${gaps} honestly no-public-address`);
