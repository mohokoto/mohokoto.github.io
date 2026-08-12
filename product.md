# Product Philosophy

## Status

This document defines the long-term product philosophy and core design
principles for `mohokoto`. It sits above `SPEC.md` in scope: `SPEC.md`
describes the current, initial implementation (a static personal
homepage); this document describes what that homepage is the first
environment for.

Not everything below is equally settled. Sections are written as clearly
as possible, but implementation specifics (algorithms, models, schemas,
libraries) are deliberately excluded — see [Out of scope](#out-of-scope).

## Product positioning

This product is not a personal homepage or a blog.

> A personal knowledge management system that accumulates, refines, and
> organizes an individual's knowledge — and whose organizing structure
> itself evolves over time.

The personal homepage (as specified in `SPEC.md`) is the first real
usage environment for this system, not the system itself. The site can
and will ship, and be useful, well before the full system described here
exists.

## Core model

The system distinguishes different kinds of things a user works with.
Only two are defined now — the model is deliberately not closed to
others; see "Open categories" below.

- **Projects** — things being built. A Project has its own lifecycle
  (started, in progress, shipped or archived), independent of any Topic.
- **Notes** — the atomic unit of written content: what the user actually
  writes, across whatever range of subjects. Notes are organized by
  Topics, and Topics are structured by an evolving Taxonomy (see
  Evolving taxonomy, below). Topics and Taxonomy are not themselves a
  kind of thing the user creates the way Projects and Notes are — they
  are the organizing structure Notes are placed into, and that
  structure is what evolves.

A Project may relate to one or more Notes, but Projects and Notes remain
distinct: a Project is a bounded thing being built; a Note is a piece of
writing organized by an evolving topic structure, not necessarily tied
to any project.

### Open categories

Projects and Notes are the only categories this document requires.
Whether other peer categories exist — and what they would be called — is
explicitly undecided. This list is not exhaustive and should not be
treated as a closed set the product is forced into.

## AI philosophy

AI does not decide knowledge on the user's behalf, and does not replace
the user as author.

AI helps the user do better what they are already trying to do. Typical
interactions:

- Refine
- Polish / proofread
- Title suggestion
- Organize
- Local, selection-scoped refinement

The governing principle is **author-preserving intervention**: what the
user finds useful matters more than what the AI is technically capable
of doing. AI capability is not the goal; usefulness to the author's own
intent is.

## Evolving taxonomy

Topics are not a static classification. Over time, the taxonomy that
organizes them can evolve through:

- Split
- Merge
- Move
- Rename
- Archive
- New topic creation

Taxonomy evolution — the fact that the organizing structure itself
changes, and that this change is a first-class, visible part of the
system — is the product's core differentiator. It is not a background
maintenance feature.

## Evolution signals

Taxonomy evolution is not triggered by a single metric. At least three
qualitatively distinct kinds of signal are considered separately:

1. **Semantic pressure** — content that is semantically close but
   organized apart, or semantically distant but organized together.
   Typically expressible through embedding/vector-based signals, though
   the exact method is not decided (see [Out of scope](#out-of-scope)).
2. **Structural / MECE pressure** — how well the current taxonomy
   partitions the knowledge space along consistent axes. This considers,
   separately:
   - Mutual exclusivity
   - Collective exhaustiveness
   - Consistency of the classification axis
   MECE here is a *pressure* the system reasons about, not a strict
   mathematical property the taxonomy is forced to satisfy at all times.
3. **Temporal persistence** — whether a pattern holds up over time, as
   opposed to being a short-lived fluctuation.

These three are kept conceptually distinct from each other. They are not
collapsed into a single blended score. How each is computed, and how
they are combined into an actual proposal, is an algorithm-level decision
deferred to future implementation-design discussion (tracked as GitHub
Issues, not a separate design document).

## Human authority

AI may propose taxonomy evolution. It never finalizes it automatically.

```text
system detects pressure
→ proposes change
→ user accepts / rejects / modifies
→ taxonomy evolves
```

Final authority always rests with the user. The user's response to a
proposal — accept, reject, or modify — is itself a signal worth
preserving, since it is expected to inform future personalization and
proposal quality. How that signal is stored and used is not decided here.

## Temporal visualization

Taxonomy evolution is not just a change log. When the user moves along a
time axis, they should be able to see topics being created, splitting,
merging, moving, and being archived, with continuity preserved across
those transitions — not as disconnected snapshots.

This visualization is treated as a core part of the product experience,
not an administrative or debugging feature. Its concrete implementation
(library, visual language, interaction model) is not decided here.

## Relationship to SPEC.md

```text
product.md        (why — long-term philosophy, this document)
    ↓
invariants.md      (what must always hold, regardless of implementation)
    ↓
SPEC.md            (what must be built — required behavior, technology-agnostic)
    ↓
ARCHITECTURE.md    (what's actually built, right now — normative, not a plan)
    ↓
implementation
```

`SPEC.md` currently specifies a static personal homepage (V0) plus a
Notes authoring/publishing system (V1, implemented — see
`ARCHITECTURE.md` for what was actually built, including its
server-side component). That scope is intentionally narrow — it covers
writing and publishing Notes, not the Topics/Taxonomy/AI system this
document describes — and is not superseded by this document. It
describes the first phase(s) of the system described here, not the
whole of it. Later phases (informed by this document and by
`invariants.md`) — Topics, Taxonomy evolution, AI-assisted authoring —
will require their own spec work, likely including a design phase, and
remain out of scope for now.

## Out of scope

The following are explicitly not decided by this document and are left
for future implementation-design discussion, tracked as GitHub Issues
rather than a separate design document:

- Database schema
- API design
- Frontend architecture
- Embedding model
- LLM provider
- Taxonomy evolution algorithm (exact signal computation and thresholds)
- Visualization library

Where this document describes specific signal types or interaction
patterns, it is describing the shape of the problem the system must
address, not an implementation.
