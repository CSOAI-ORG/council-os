# ADR-002 — The live board is public-read, free forever

**Status:** ACCEPTED · **Date:** 2026-08-26 · **Decider:** Nick Templeman (owner)

## Ruling

> **Public read. No gate, no login, no key, forever.**
> Gate **writes**. Gate **telemetry ingestion**. Gate a **high-volume API tier** later
> if load demands it. The read is never gated.

## Context

`apps/live-board/` renders `apps/live-core/`'s signed verdicts over SSE. It was built
loopback-only and exposed nothing; the agent that built it named public-read-vs-gated as
the decision everything else hangs off, observing that **gating a citation surface
defeats its purpose.**

That is the whole strategy. The permissionless-measurement thesis, the LMArena precedent
(free public leaderboard → became the reference the industry cites → *then* monetised the
private tier), and the acquisition case (a signed measurement history an incumbent cannot
retroactively manufacture) all collapse if a reader must authenticate to see the board.

You cannot become the thing the industry cites from behind a login.

## Consequences — what must exist before it goes public

Public-read is the ruling; it is not a licence to expose an unhardened service. Required
first, all currently NOT-BUILT:

1. **Rate limiting.** Today each SSE connection holds a process polling SQLite every
   250ms with **no cap anywhere**. A public endpoint without a cap is a denial-of-service
   waiting to be discovered.
2. **TLS**, and a decision on where it runs — `live-core`'s state currently dies with the
   pod, which is not an acceptable home for a citation surface.
3. **Concurrent-viewer testing.** Every verification run so far used one client at a time.
4. **Read-only enforcement at the edge**, so "public read" cannot silently become
   "public write" through a mis-scoped route.

## What is deliberately NOT gated

- The board itself, the per-cell verdicts, the skips view (*"we looked and nothing
  changed"* is part of the product), the card digests, and the public key needed to
  verify a card offline.
- A reader must be able to check us **without trusting us and without asking us**. That
  is the moat, not a feature.

## The rule this encodes

Free-forever verification is not generosity, it is the product's integrity claim made
operational. Anything that would require a reader to identify themselves before they can
check a measurement is, by construction, a weaker measurement.
