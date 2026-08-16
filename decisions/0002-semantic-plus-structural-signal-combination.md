# 0002: Keep semantic and structural/MECE pressure as separate evolution signals

## Status

Accepted

## Context

Once taxonomy evolution is the model (see
[0001](0001-evolving-taxonomy-as-core-model.md)), something has to decide
*when* evolution is warranted. The simplest approach is a single blended
score — for example, purely embedding-based semantic similarity — that
triggers a proposal above some threshold.

A single-signal approach was considered and rejected. Semantic similarity
alone can justify merging two topics that are "about similar things" but
serve different organizational purposes for the user (a MECE / structural
concern), and structural analysis alone can justify a change that
contradicts how the content actually reads (a semantic concern). Neither
signal alone is a reliable trigger on its own, and blending them into one
number early hides which concern is actually driving a given proposal —
which matters when the user has to evaluate and decide on it.

## Decision

At least three distinct signal categories are reasoned about separately,
not pre-merged: semantic pressure, structural/MECE pressure, and temporal
persistence (whether a pressure holds up over time rather than being
momentary). See `product.md`'s "Evolution signals" section for what each
covers.

## Consequences

- Proposals to the user can be explained in terms of which signal(s)
  motivated them, rather than an opaque score.
- This is a *conceptual* commitment, not an algorithm. The exact
  computation for each signal, and how they are combined into an actual
  proposal, is deliberately left to future implementation-design
  discussion (tracked as a GitHub Issue, not a separate design
  document) — see `product.md`'s "Out of scope".
- `product.md`'s Taxonomy section records the narrower, durable version
  of this decision: semantic and structural evidence must be kept
  conceptually distinct, regardless of how each is eventually computed.
