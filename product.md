# Product Vision (non-authority)

**This is not an authority document.** It does not constrain the
current implementation, and nothing here is required to be built.
`ARCHITECTURE.md`/`RELATIONS.md`/`BEHAVIOR.md`/`SITE.md`/`NOTES.md`/
`Q-A.md` are the authority documents; the #18 audit's "current
implementation constraining norm" test does not apply here.

This document preserves content that has no other durable record —
unimplemented product vision, an unimplemented category, and the
rationale behind past decisions — so it isn't lost when a page
happens not to reference it. It is not itself updated as vision
evolves: new product-vision discussion belongs in a GitHub Issue. If
and when something described here is actually built, its authoritative
content moves out to the relevant authority document above, and this
page is trimmed accordingly.

## Product positioning

This product is not meant to be a personal homepage or a blog:

> A personal knowledge management system that accumulates, refines, and
> organizes an individual's knowledge — and whose organizing structure
> itself evolves over time.

The current site (see `SITE.md`/`NOTES.md`/`Q-A.md`) is the first real
usage environment for this vision, not the vision realized — it ships
and is useful well before the rest of what's described here exists.

## AI philosophy

AI does not decide knowledge on the user's behalf, and does not replace
the user as author.

AI helps the user do better what they are already trying to do. Typical
interactions: refine; polish/proofread; title suggestion; organize;
local, selection-scoped refinement.

The governing principle is **author-preserving intervention**: what the
user finds useful matters more than what the AI is technically capable
of doing. AI capability is not the goal; usefulness to the author's own
intent is.

**AI and human authority.** AI is never the source of truth for
personal knowledge. It can organize, connect, infer, and resurface —
but authority over what the individual actually knows or believes
always rests with the individual, not the AI. AI intervention is
author-preserving by default: AI assists work the user is already
doing; it does not make editorial or organizational decisions on the
user's behalf without the user's review. The user's response to any AI
proposal is preserved, not discarded — acceptance, rejection, and
modification are retained as signal, not thrown away once acted on.

No AI-assisted feature exists in the current implementation — this
entire section describes intent for a not-yet-built capability.

## Project (unimplemented category)

A Project is a thing being built, with its own lifecycle (started, in
progress, shipped or archived), independent of any Topic or Note. A
Project may relate to one or more Notes, but Projects and Notes remain
distinct: a Project is a bounded thing being built; a Note is a piece
of writing, not necessarily tied to any project. They must not be
collapsed into a single structure or treated as interchangeable, even
when closely related.

Project, Q/A, and Note are not meant to be a closed set — whether other
peer categories exist, and what they'd be called, is undecided. Q/A and
Note have since been built (see `ARCHITECTURE.md`); Project has not.

No Project object, route, or storage exists in the current
implementation.

## On the name "Note"

Conceptually the Note category is a composed, publishable document —
"Article" or "Document" would describe it more precisely, and the
mohokoto.github.io#12 discussion that introduced Q/A called it
"Article" throughout. The name "Note" was kept instead of renaming to
match. Measured the cost of renaming: 206 identifier occurrences across
the codebase is the small part — the real cost is published URL
stability (`/notes/{slug}/`), storage layout across two repositories,
the `notes-published` repository name, and the sync workflow. All of
that would need to move or redirect for a rename, none of it for
keeping the name and stating the conceptual definition explicitly
instead (see `ARCHITECTURE.md`'s "What a Note and a Q/A each are").

## Taxonomy (unimplemented)

Notes are meant to be organized by Topics, and Topics structured by
this evolving taxonomy — Topics and Taxonomy aren't a kind of thing the
user creates the way Notes are; they're the organizing structure Notes
would be placed into. Topics are not a static classification. Over
time, the taxonomy that organizes them can evolve through split, merge,
move, rename, archive, and new topic creation. Taxonomy evolution — the
fact that the
organizing structure itself changes, and that this change is a
first-class, visible part of the system — is meant to be the product's
core differentiator, not a background maintenance feature.

**Evolution signals.** Taxonomy evolution is not meant to be triggered
by a single metric. At least three qualitatively distinct kinds of
signal are meant to be considered separately: semantic pressure
(content that is semantically close but organized apart, or distant but
organized together); structural/MECE pressure (mutual exclusivity,
collective exhaustiveness, and consistency of the classification axis
— a pressure the system reasons about, not a strict property the
taxonomy is forced to satisfy at all times); and temporal persistence
(whether a pattern holds up over time, as opposed to a short-lived
fluctuation). These three are meant to be kept conceptually distinct,
not collapsed into a single blended score.

**Human authority.** AI would be able to propose taxonomy evolution but
never finalize it automatically — final authority always rests with
the user, and the user's accept/reject/modify response would itself be
signal worth preserving.

**Temporal visualization.** Taxonomy evolution is meant to be more than
a change log: moving along a time axis should show topics being
created, splitting, merging, moving, and being archived, with
continuity preserved across those transitions, not disconnected
snapshots.

**Constraints this would need to satisfy, if built** (currently
recorded only here — not enforced by anything, since nothing is built):
topic identity and lineage must remain traceable across evolution (a
renamed topic is not a new, unrelated one; a merged topic's history is
not discarded); it is not sufficient to record that a change happened —
the relationship between the taxonomy before and after the change must
be reconstructible; semantic-similarity signals and structural/MECE
signals must not be merged into a single undifferentiated score before
being reasoned about; a momentary signal must be treated differently
from one that persists over time; AI-proposed taxonomy changes are
never authoritative on their own — a proposal only becomes part of the
taxonomy after explicit user acceptance (or user modification followed
by acceptance); taxonomy evolution must be observable with temporal
continuity — the system must be able to express how the taxonomy
changed over time in a form that preserves continuity between states,
not as disconnected, unrelated point-in-time snapshots.

See `decisions/0001–0003` for the rejected alternatives and reasoning
behind these choices.

## Out of scope

Not decided anywhere in this project yet, left for future
implementation-design discussion if this category is ever built:
database schema, API design, frontend architecture, embedding model,
LLM provider, taxonomy evolution algorithm (exact signal computation
and thresholds), visualization library.
