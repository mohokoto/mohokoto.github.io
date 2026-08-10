# 0001: Adopt evolving taxonomy as the core organizing model

## Status

Accepted

## Context

A personal knowledge system needs some way to organize Topics. The
default, low-effort option is a static classification the user sets up
once (folders, tags, a fixed category list) and maintains manually as
things drift out of date.

That default was considered and rejected. A static taxonomy degrades
predictably: as the volume and range of accumulated knowledge grows, the
original categories stop fitting, and either the user manually
reorganizes (rare, effortful, usually deferred indefinitely) or the
taxonomy silently stops reflecting how the knowledge is actually
structured.

## Decision

The taxonomy is treated as something that evolves — through split,
merge, move, rename, archive, and creation — as a first-class, visible
part of the product, rather than as manual maintenance the user is
expected to perform out of band.

## Consequences

- The system needs a way to detect when the current taxonomy is under
  pressure (see [0002](0002-semantic-plus-structural-signal-combination.md)),
  which a static-taxonomy design would not have needed.
- Evolution must preserve topic identity/lineage across changes (see
  `invariants.md`), which is more implementation work than treating each
  reorganization as a fresh start.
- This is the product's core differentiator, not an incidental feature —
  see `product.md`'s "Evolving taxonomy" section.
