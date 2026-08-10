# Invariants

This document lists properties the system must preserve regardless of
how it is implemented. It complements [`product.md`](product.md), which
explains *why* these matter, and sits above [`SPEC.md`](SPEC.md), which
describes what is actually being built right now.

An invariant here is a principle judged core to the product, not a
feature that happens to be planned. Unimplemented features are not
promoted to invariants just because they are described in `product.md`;
only the constraints those features must satisfy, whenever and however
they are eventually built, are listed here.

## Taxonomy

- **Topic identity survives evolution.** When a topic splits, merges,
  moves, is renamed, or is archived, its identity and lineage must
  remain traceable. A renamed topic is not a new, unrelated topic; a
  merged topic's history is not discarded.
- **Evolution preserves lineage, not just a log.** It is not sufficient
  to record that a change happened; the relationship between the
  taxonomy before and after the change must be reconstructible.
- **Projects and Notes remain distinct concepts.** They must not be
  collapsed into a single taxonomy or treated as interchangeable, even
  when a Project relates closely to one or more Notes.
- **Semantic and structural evidence are kept conceptually separate.**
  Semantic-similarity signals and structural/MECE signals must not be
  merged into a single undifferentiated score before being reasoned
  about. (How each is computed is not an invariant — see `product.md`'s
  "Out of scope".)
- **Evolution must account for temporal persistence.** A signal that is
  momentary should be treated differently from one that persists over
  time; the system must not treat every fluctuation as grounds for
  evolving the taxonomy.
- **Taxonomy evolution must be observable with temporal continuity.** The
  system must be able to express how the taxonomy changed over time —
  topics being created, splitting, merging, moving, being archived — in
  a form that preserves continuity between states, not as disconnected,
  unrelated point-in-time snapshots. This constrains *how* evolution
  over time is expressed, whenever it is expressed; it does not mandate
  a specific visualization technology, and it does not require this
  capability to exist in the current static-site phase (`SPEC.md`) — see
  "Scope of these invariants" below.

## AI and human authority

- **AI-proposed taxonomy changes are never authoritative on their own.**
  A proposal only becomes part of the taxonomy after explicit user
  acceptance (or user modification followed by acceptance).
- **AI intervention is author-preserving by default.** AI assists work
  the user is already doing; it does not make editorial or organizational
  decisions on the user's behalf without the user's review.
- **The user's response to a proposal is preserved, not discarded.**
  Acceptance, rejection, and modification of AI proposals are retained
  as signal, not thrown away once acted on. (How this signal is used is
  not an invariant — that is a design/algorithm decision.)

## Explicitly not invariants (yet)

The following are described in `product.md` as intended product
direction but are not promoted to invariant status, because they are
unimplemented features rather than constraints on implementation:

- The specific form, technology, or interaction model of any view into
  taxonomy evolution (e.g. a particular visualization library, timeline
  UI, or graph layout). Note this is narrower than it may first look:
  that such a view must be *possible in principle* is covered by the
  continuity invariant above; only its concrete realization is excluded
  here.
- That any specific number or set of evolution-signal types (beyond
  "more than one, kept distinct") is fixed.
- Any specific technology, algorithm, schema, or provider.

If and when these become load-bearing product commitments rather than
current intentions, they should be reconsidered for promotion here.

## Scope of these invariants

These invariants describe the system `product.md` is building toward,
not a checklist every current build must already satisfy. The present
implementation (`SPEC.md`, a static personal homepage) does not yet
implement taxonomy, evolution, or AI features at all, and is not in
violation of any invariant above by simply not having built that far
yet. An invariant is violated by building something that works *against*
it (e.g. discarding lineage on merge), not by a feature not existing
yet.
