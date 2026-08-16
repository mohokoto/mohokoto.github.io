# Behavior (Global)

① Regulates system-wide behavior — what the system or an AI feature may
or may not do when acting on stored content, and cross-object workflows
that span multiple subsystems.
② Applies system-wide, to any action on any currently implemented
object type, and to any workflow that spans more than one subsystem.
③ Does not define what an object *is* (`ARCHITECTURE.md`) or how
objects relate to each other (`RELATIONS.md`), or subsystem-internal
behavior confined to one object type (`NOTES.md`/`Q-A.md`'s own state
transitions).

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

## Cross-object workflow (not yet written)

How a user moves from exploring Q/A and their relations to composing a
Note that draws on several of them is a Global/Behavior norm once
designed — it spans the Q/A and Notes subsystems and isn't confined to
either. Not yet designed (mohokoto.github.io#15 audited the current gap
without designing a replacement); this section is populated once that
design work concludes.
