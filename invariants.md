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

## Preservation value

> The value of preserved information is judged not by whether it can be
> regenerated, but by how uniquely it preserves value arising from the
> individual's experience, judgment, taste, context, or personal
> circumstances and activity.

This is the single governing invariant beneath every other one in this
document. Taxonomy and AI/human authority (below) describe how
preserved knowledge is organized and by whom; Originality and
provenance, Context and relationships, and Change over time (also
below) describe what must not be lost about it. This section describes
something upstream of all of that: what earns preservation in the
first place (mohokoto.github.io#12).

Two direct implications, not independent invariants in their own right
— restatements of the principle above, not additional constraints
beside it:

- **Personal value is required, not incidental.** Stored information
  must carry value arising from the individual's own experience,
  judgment, taste, context, or circumstances and activity — not merely
  value a generic LLM response could already supply.
- **Regeneratability is not, on its own, a reason to keep something.**
  General knowledge easily re-obtained by asking an LLM again is not,
  by itself, grounds for long-term preservation.

Two boundary clarifications on "personal value":

- It is not limited to reflective content (experience, judgment,
  taste). Reference information that only carries meaning because of
  the individual's own circumstances or activity — a project's server
  IP, a contract's expiry date — qualifies too.
- This does not mean "anything connected to the person" qualifies. The
  test is still uniqueness of preservation value, not personal
  relevance in general.

## Originality and provenance

- **What the individual actually experienced or thought must remain
  distinguishable from what an LLM generated or inferred.** An LLM's
  interpretation must not overwrite the individual's own memory or
  judgment — refining, summarizing, or reorganizing content must not
  destroy the ability to tell which parts were authored by the person
  versus produced by the LLM.

## Context and relationships

- **What something is about is not sufficient on its own.** Why it
  mattered, or what question it arose from, should not be lost
  wherever that context is available.
- **When a knowledge object's value comes from its relationship to
  other objects, that relationship must be preserved** — in
  particular, lineage such as question → derived question → insight →
  topic → experience.

## Change over time

- **A changed judgment does not silently overwrite the earlier one.**
  When the user's thinking changes, "I used to think X, now I think Y"
  is itself knowledge worth preserving, not noise to be discarded in
  favor of the current view.

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

- **AI is never the source of truth for personal knowledge.** It can
  organize, connect, infer, and resurface — but authority over what the
  individual actually knows or believes always rests with the
  individual, not the AI.
- **AI-proposed taxonomy changes are never authoritative on their own**
  (a specific instance of the constraint above, for taxonomy). A
  proposal only becomes part of the taxonomy after explicit user
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

Not every invariant above is exempt from the present implementation in
the same way.

**Preservation value, Originality and provenance, Context and
relationships, and Change over time** govern any knowledge the system
stores, including what is already built. The current V1 Note/CMS
structure is in scope for these starting now, not only once some
future phase ships — mohokoto.github.io#12 is the active review of
exactly how the present implementation holds up against them (an
already-shipped example under review there: whether Delete's silent,
unrecoverable-from-the-app removal of a Note works against Change over
time).

**Taxonomy, and the taxonomy-specific bullet of AI and human
authority,** are different: they describe the system `product.md` is
building toward, not a checklist the current build must already
satisfy. The present implementation does not yet implement taxonomy,
evolution, or topic-proposal AI features at all, and is not in
violation of those invariants by simply not having built that far yet.

Either way, an invariant is violated by building something that works
*against* it (e.g. discarding lineage on merge), not by a feature not
existing yet.
