# Relations (Global)

① Regulates the relationships between knowledge objects — why they
exist, what conditions they must satisfy, and what must be preserved
about them.
② Applies system-wide, across all currently implemented object types
(Note, Q/A).
③ Does not define what an object *is* (`ARCHITECTURE.md`), how the
system may act on objects or their relationships over time
(`BEHAVIOR.md`), presentation-layer norms (`SURFACE.md`), or
subsystem-internal relationship mechanics (`NOTES.md`/`Q-A.md`).

## Relationships must be preserved

What something is about is not sufficient on its own — why it mattered,
or what question it arose from, should not be lost wherever that
context is available. When a knowledge object's value comes from its
relationship to other objects, that relationship must be preserved.
This is not limited to any one object type: it is what makes Q/A's
Q↔Q relations (see `Q-A.md`) and a Note's Q/A sources (see `NOTES.md`)
both load-bearing rather than optional metadata.

## Note ↔ Q/A: snapshot, not a live view

A Note may draw on one or more Q/A's, and one Q/A may feed several
Notes — but a Note is not a view onto them. It has its own content, its
own composition, and its own editing, and it takes a snapshot of the
Q/A's it drew on at the time the source was added or refreshed: a
later change to a Q/A does not propagate into the Note, and is pulled
in only when the user decides it should be. Editing a Note likewise
never edits a Q/A back. Q/A is where inquiry lives; a Note is something
the user chose to compose from it. Inquiry that never becomes a Note is
not lesser for it — it is preserved on its own terms.
