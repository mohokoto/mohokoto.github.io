# Surface (Global)

① Regulates presentation-layer norms — how UI is structured across
pages, and how runtime-assembled UI components must initialize —
independent of backend/domain concerns.
② Applies system-wide, to any page or component in the Editor UI.
③ Does not cover domain object structure (`ARCHITECTURE.md`),
relationships between objects (`RELATIONS.md`), domain/cross-object
behavior (`BEHAVIOR.md`), or subsystem-specific content models
(`SITE.md`/`NOTES.md`/`Q-A.md`).

Not yet split into subsystem-scoped documents (e.g. a semantics/markup
split) — everything Surface-level currently lives here. If an
independent authority boundary is genuinely needed later, split into
`SURFACE_SEMANTICS.md`/`SURFACE_UI.md`-style documents; norms that are
Surface-Global (apply across whatever the split becomes) stay in this
file even after a split, the same way `RELATIONS.md`/`BEHAVIOR.md`
stayed Global once `SITE.md`/`NOTES.md`/`Q-A.md` were split out from
them.

## List rows: fixed two-tier structure

A list row (Note list, Q/A list) always has its title on its own
full-width line, truncated with an ellipsis rather than wrapped, and
its metadata (status/relation-count/timestamp) on a second line below,
itself wrapping if it has several items. This is not a responsive
fallback that only matters on narrow viewports — it's the row's only
layout, regardless of screen width. A single flex row that tries to
fit title and metadata on one line and depends on wrapping to recover
breaks differently depending on title length and script, and
"differently" sometimes means "not visibly at all" (mohokoto.github.io#24
— a title that wrapped internally onto several lines still left
metadata floating beside it rather than dropping below, on a list row
that had never actually overflowed).

## Persistent navigation

Every page's shared header includes navigation to both the Notes and
Q/A lists, regardless of which one is the current page or which is the
main screen (`/`). A page never has to be the site's home to be
reachable — navigation between the two top-level areas does not depend
on knowing a direct URL (mohokoto.github.io#22 — found live: neither a
persistent nav nor any link to the other area existed before this).

## Page initialization lifecycle contract

A page region containing a runtime-JS-assembled UI component (currently:
EasyMDE replacing a plain `<textarea>` with a toolbar+editor) must not
be shown to the user until that component has finished initializing.
Getting this wrong doesn't fail loudly — it fails as a sequence of
increasingly subtle live-only symptoms, all traced to the same root
cause in mohokoto.github.io#28:

1. **Don't guess the component's eventual size to reserve space.** A
   plain `<textarea>`'s default height doesn't match what EasyMDE
   renders (toolbar + ~300px content area), so anything below it
   visibly shifts once EasyMDE swaps in — and the "fix" of giving the
   textarea a hardcoded matching `min-height` doesn't work anyway: the
   component may hide the original element and build an entirely
   separate DOM structure, which the original element's own sizing has
   no bearing on.
2. **Hide the whole region until the component is done, not just until
   it's "probably done."** Wrap the region in a container that starts
   hidden and reveal it only after construction (and any of the
   component's own post-construction settling, e.g. `refresh()`) has
   actually run — not merely scheduled to run soon.
3. **Hide with `visibility: hidden`, never `display: none`, for
   anything that needs to measure real layout during initialization.**
   `display: none` removes the element from the layout tree entirely —
   width/height read as zero — which is exactly wrong for a component
   (or supporting code, e.g. this project's own toolbar-overflow
   calculation) that measures its container to lay itself out.
   `visibility: hidden` keeps real, non-zero geometry available the
   whole time and only suppresses painting, so measurement-dependent
   initialization succeeds on the first attempt instead of needing a
   later correction.
4. **Reveal is the last step, strictly after every other init step in
   the same sequence — not merely placed near them.** Any
   post-construction settling (`refresh()`, layout-dependent
   adjustments) runs first, so if it causes any internal re-render,
   that happens while still unpainted; removing the hidden state is the
   final line, the consequence of initialization completing rather than
   a step interleaved with it.

This isn't specific to EasyMDE - it applies to any future component
with the same shape of requirement (needs real layout to initialize,
assembles itself into the DOM at runtime rather than existing fully
formed in the server-rendered HTML).
