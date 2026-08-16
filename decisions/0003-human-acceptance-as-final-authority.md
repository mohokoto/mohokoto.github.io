# 0003: Human acceptance as final authority for taxonomy evolution

## Status

Accepted

## Context

Given the system can detect pressure and propose taxonomy changes (see
[0001](0001-evolving-taxonomy-as-core-model.md) and
[0002](0002-semantic-plus-structural-signal-combination.md)), it could
either apply high-confidence proposals automatically, or always route
proposals through the user before they take effect.

Automatic application was considered and rejected as the default. A
taxonomy is how the user makes sense of their own knowledge; an
automatic reorganization the user did not review — even a well-reasoned
one — risks eroding the sense that the structure is theirs, which
undermines the "author-preserving" AI philosophy the rest of the product
is built on (see `product.md`'s "AI philosophy").

## Decision

AI may detect pressure and propose taxonomy evolution, but a proposal
only becomes part of the authoritative taxonomy after the user accepts
it (with or without modification). This applies uniformly, independent
of how confident the underlying signal is.

## Consequences

- Every evolution event has an explicit human decision point, which adds
  interaction cost the automatic-application design would not have.
- The user's accept/reject/modify response becomes a signal the system
  can use later (for personalization or proposal quality), rather than
  being discarded — recorded in `product.md`'s Taxonomy section.
- This does not preclude a future design where sufficiently trusted
  proposal types require less friction (e.g. lighter-weight confirmation)
  — it precludes the taxonomy becoming authoritative for a change the
  user never saw. That distinction is left for future implementation-
  design discussion, tracked as a GitHub Issue rather than a separate
  design document.
