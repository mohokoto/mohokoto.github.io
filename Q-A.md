# Q/A (Subsystem)

① Regulates the elements (content model), relationships (Q↔Q relation
storage and reverse lookup), and behavior (create/save/delete) of the
Q/A object.
② Applies to the Q/A object only.
③ Does not cover the Note subsystem itself, the V0 static site, or any
global-scope norm (`ARCHITECTURE.md`/`RELATIONS.md`/`BEHAVIOR.md`). How
a Note draws on Q/A is a Notes-subsystem concern (`NOTES.md`'s Sources
section); the cross-object workflow of moving from Q/A exploration to
Note authoring is a `BEHAVIOR.md` concern once written. The routes
exposed for Q/A are inventoried in `ARCHITECTURE.md` (Global/Elements);
this document covers what using them does.

## Purpose

Enable mohokoto to record personal inquiry (a question and its current
answer) directly, independent of whether it is ever composed into a
Note, and to preserve relationships between related pieces of inquiry
over time.

## Scope

- Same single-author, same-authentication constraint as Notes.
- A Q/A has no publication or visibility state of its own — it is never
  directly visible to a visitor. Only content a Note deliberately
  composes from it, and that Note publishes, becomes public.

## Content model

A Q/A has at minimum a question and an answer, and its relationships to
other Q/A's. Neither the question nor the answer is required to be
complete for a Q/A to exist — a bare label is sufficient, so a recalled
interest can be captured the moment it comes to mind rather than
requiring it be worked into a proper question first. In practice,
`POST /qa` requires a non-empty `question` (≥1 character after trim,
same shape as a Note's title) — `answer` is not required.

## Relations

A relation is one entry per pair, not one per direction: a single
relation, authored once by whichever side added it, is shown on both
ends. It does not mean each side gets to independently author its own
note about the other. Even a directional relation (e.g., cause →
effect) has two readings that are coupled, not two arbitrary free
texts, and there's no way to derive one direction's phrasing from the
other's without relation types, which this subsystem deliberately
defers.

**Outgoing and incoming.** `GET /qa` includes each item's `relations`
alongside `question`/`savedAt`/`answered`. The Editor computes a Q/A's
*incoming* relations client-side by filtering the full Q/A list for any
item whose `relations` contains the current Q/A's id, and renders it as
a second, read-only list below the editable outgoing one. Both lists
are clickable through to the target's own edit page (mohokoto.github.io#21
— outgoing's link-ification was deliberately excluded from #16's scope
and deferred to this workflow-design issue).

**Which Q/A's the list itself surfaces relation counts for.** `GET /qa`'s
list page (not just the editor) shows each Q/A's total relation count —
outgoing plus incoming, computed client-side the same way the editor's
incoming section is. Outgoing alone would show 0 for a Q/A that's
heavily referenced but rarely references anything itself, defeating a
count meant to surface graph structure while scanning the list
(mohokoto.github.io#21).

**Which Notes cite a Q/A.** The Editor also derives, read-only, every
Note whose `sources` reference this Q/A's id — by scanning `GET /notes`
(which includes `sources` per item, see `NOTES.md`), the same
"nothing's stored on this side, derive it from the other side" shape as
incoming relations. Rendered as a third section, linking through to
each citing Note's edit page (mohokoto.github.io#21, closing a gap #15
found: Q/A had no way to see which Notes drew on it).

**Preventing duplicate pairs.** The target-select dropdown excludes a
Q/A both when this Q/A already relates to it *and* when it already
relates to this Q/A, so the same pair can't be created from both sides.
This client-side check runs against the Editor's load-time snapshot, so
`PUT /qa/:id` also checks every newly-added relation's target against
the target's *current* stored `relations` and rejects with 409 if the
target already relates back — closing the stale-client-cache gap the
dropdown alone can't. It does not close every race: two genuinely
concurrent `PUT` requests for both sides of a pair could each still
pass and both write, recreating a duplicate. Not worth closing at this
tool's single-user scale, but not airtight either. Only new relations
are checked; a pair already in both states from before this check
existed is left alone until someone removes one side by hand.

**Deletion asymmetry.** Deleting Q/A A (which stored a relation to B)
leaves B's outgoing `relations` untouched, but B's own file never had a
record of A pointing at it, so B's incoming list simply no longer
includes A — no "(deleted)" stub, because nothing was stored on B's
side to leave one. This is inherent to one-sided storage, not a gap: an
outgoing relation on the referencing side itself keeps the dead `q_id`
and renders it unresolved, because that side does have something
concretely stored to render as a stub.

## State transitions

Q/A has no `status` field and no publish state at all — its state
space is just whether it exists.

| From | Action (endpoint) | To | `content-drafts` |
|---|---|---|---|
| (none) | Create (`POST /qa`) | exists | file created. `question` required, `answer` is not |
| exists | Save (`PUT /qa/:id`) | exists | commit only if `question`/`answer`/`relations` actually changed. A blank `question` in the request falls back to the existing value rather than being written |
| exists | Delete (`DELETE /qa/:id`) | *(gone)* | file deleted. Neither other Q/A's `relations` nor any Note's `sources` that reference this id are touched — the reference becomes dangling, rendered as unresolved rather than erroring. A Q/A's `relations` keep only the `note` text; a Note's `sources` keep the full snapshotted question/answer text |

Adding or removing a relation isn't a separate action — it's a change
to the `relations` field, saved through the same PUT as everything
else. The list page derives whether a Q/A is "unanswered" from `answer`
being empty on every request rather than storing that as its own field.
