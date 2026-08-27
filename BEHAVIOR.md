# Behavior (Global)

① Regulates system-wide behavior — what the system or an AI feature may
or may not do when acting on stored content, and cross-object workflows
that span multiple subsystems.
② Applies system-wide, to any action on any currently implemented
object type, and to any workflow that spans more than one subsystem.
③ Does not define what an object *is* (`ARCHITECTURE.md`), how objects
relate to each other (`RELATIONS.md`), presentation-layer norms
(`SURFACE.md`), or subsystem-internal behavior confined to one object
type (`NOTES.md`/`Q-A.md`'s own state transitions).

## Change over time

A changed judgment does not silently overwrite the earlier one. When
the user's thinking changes, "I used to think X, now I think Y" is
itself knowledge worth preserving, not noise to be discarded in favor
of the current view. This constrains *silent or automatic* overwriting
and cleanup — the system or an AI feature replacing a past state with a
current one, or discarding it, without the user having made that
specific call. It does not constrain the user's own explicit, confirmed
decision to delete or change their own content: a human deliberately
choosing that something is no longer worth keeping is the exercise of
the user's own authority, not a violation of it.

## Workflow-declaration constraint

Any new GitHub Actions workflow in `mohokoto.github.io` that's
triggerable via `workflow_dispatch` must declare a minimal
`permissions:` block itself. `mohokoto-publish-trigger`'s
`actions:write` grant (see `ARCHITECTURE.md`) doesn't distinguish which
workflow it's dispatching, so a workflow that omits its own
`permissions:` block would run with whatever GitHub's default grants,
not a scoped-down one.

## Cross-object workflow: Q selection → Note creation

Moving from exploring Q/A's and their relations to composing a Note
that draws on several of them spans the Q/A and Notes subsystems, so
the workflow itself lives here rather than in either subsystem's own
document (mohokoto.github.io#15 identified the gap; #20 settled the
underlying Q graph model — cycles allowed, no forced acyclicity; #21
designed and built this workflow for Desktop). Mobile portrait/landscape
are explicitly deferred to a future issue, not covered here.

Selection is scoped to the Q/A list page's own client-side memory —
picking several Q/A's to write from is a one-page task, and navigating
away (including into an individual Q/A's own edit page) resets it.
Nothing about the selection is persisted server-side or across page
loads.

| From | Action | To |
|---|---|---|
| Q/A list, 0 selected | check a Q/A row | 1 selected, selection tray shown |
| N selected | check another row | N+1 selected |
| N selected | uncheck a row | N-1 selected (tray hidden again at 0) |
| N selected (N≥1) | click "Start Note" | new Note created immediately (title = first selected Q/A's question, `sources` = snapshots of every selected Q/A's current content), Note editor opens |
| N selected | leave the Q/A list page | 0 selected | selection is page state; no separate handling needed |

"Start Note" fetches each selected Q/A's full content (the list
response doesn't carry answer text) and calls `POST /notes` once with
the assembled `sources` — see `NOTES.md`'s "Creating from selected
Q/A's" for the Notes-subsystem side of this call.
