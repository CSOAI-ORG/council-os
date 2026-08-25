# Authoring a Council OS adapter

An adapter is the OPEN, data-only description of how to pull reference data for one
tokenized-RWA instrument. It never signs, never issues a verdict, never touches a key.

## To add one
1. Create `adapters/<chain>/<asset-slug>/index.js`.
2. Export `meta` (instrument, category, chain, issuer address/contract, addressStatus).
3. Export `async reference()` returning the reads the engine needs — or, if no public
   address is confirmable, `{ status: "no-public-address" }`. **Never invent an address
   or a value to fill a gap** — honesty is the product; an unmeasurable instrument is
   reported as such.
4. `measurementStatus` is always `UNMEASURED` in the open layer. Only the private
   engine, after a real GSPC run, produces anything else.

## Rule
Adapters are opinion-free reference plumbing. The verdict/signature is a separate,
later stage (`/engine` + `/publishers`). Issuers may PR an adapter for their own
instrument; a PR that asserts a verdict, a rating, or ownership is rejected.
