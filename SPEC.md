# Personal Website Specification

> This document specifies mohokoto's site requirements in three parts.
> Sections 1–8 below (**V0**) describe the current, initial
> implementation — a static personal homepage — which is implemented
> and live. **Part 2: V1 — Content System** adds requirements for
> writing, editing, and publishing content directly on the site.
> **Part 3: Q/A — Personal Inquiry** adds requirements for recording
> personal inquiry independent of publishing. All three are implemented
> and live — see [`ARCHITECTURE.md`](ARCHITECTURE.md) for what was
> actually built to satisfy them. None of the three describes the full
> long-term product direction — see [`product.md`](product.md) for the
> product philosophy this site is the first environment for, and
> [`invariants.md`](invariants.md) for constraints that must hold
> regardless of implementation.

## 1. Purpose

A personal website for `mohokoto`.

The site provides a simple, durable home for personal information, projects, interests, and links.

## 2. Scope

- Static website
- Hosted on GitHub Pages
- Publicly accessible
- Responsive across desktop and mobile
- Easy to maintain and extend

## 3. Technical Baseline

- HTML5
- CSS3
- JavaScript only when necessary
- No framework required
- No server-side application (for V0 — Part 2: V1 Content System below
  documents a scoped exception for V1 only)
- GitHub Pages deployment
- One curated display web font is permitted as a deliberate, documented
  exception to minimal dependencies (see Design Principles), loaded with
  `display=swap` so it does not block rendering. No other external
  runtime dependencies.

## 4. Site Structure

The initial site should support:

- Home
- About
- Projects
- Links

The exact presentation and content of these sections are intentionally left open.

## 5. Design Principles

- Simple
- Fast
- Readable
- Accessible
- Responsive
- Minimal dependencies (one deliberate exception: a display web font,
  see Technical Baseline)
- Easy to modify

### Visual direction

The site's visual identity draws its mood, palette, and typographic
sensibility from a vintage-glamour editorial moodboard (warm cream
background, deep jewel-tone accents — wine, sage, gold — a large serif
display face, and generous editorial spacing/dividers). Only the tone is
referenced: no illustration, photography, or likeness from the source
moodboard appears on the site.

This is a styling decision, not a structural one — it does not change
Sections 1–4 or 6–8 of this specification.

## 6. Accessibility

The site should:

- Use semantic HTML
- Maintain a logical heading hierarchy
- Support keyboard navigation
- Provide meaningful alternative text for images
- Maintain sufficient contrast
- Respect reduced-motion preferences where applicable

## 7. Deployment

The production site is:

`https://mohokoto.github.io/`

Changes are deployed through the Git repository and GitHub Pages.

## 8. Future Expansion

The specification is intentionally minimal.

Additional sections, features, visual direction, and technical requirements may be added as the site evolves.

---

## Part 2: V1 — Content System

> V1 extends the V0 site above with the ability to write, edit, and
> publish content directly from the site itself. This section documents
> requirements only — data storage format, API design, and specific
> technology choices are deferred to future implementation-design
> discussion, tracked as GitHub Issues rather than a separate design
> document.

### V1.1 Purpose

Enable mohokoto to write, revise, and publish Notes (per `product.md`'s
Core model) directly through the site, without requiring a separate
authoring tool or manual git operations.

### V1.2 Scope

- A single authenticated author (mohokoto only) can create and edit
  content through an in-browser editor on the live site.
- Visitors (unauthenticated) can only view Published content. Draft
  content and the editor itself must not be publicly accessible.
- Topics and Taxonomy (per `product.md`) are explicitly out of scope
  for V1. The content model must not preclude adding topic association
  later, but no topic/taxonomy feature is built now.

### V1.3 Content model requirements

A Note has at minimum: a title, a body, a publication status, created
and last-modified timestamps, and a revision history (see V1.5). The
exact set of statuses (e.g. whether a third state such as "Unpublished"
exists alongside Draft/Published) is an implementation-design decision
(tracked as a GitHub Issue), not fixed here.

### V1.4 Editing and saving

- The author can create a new Note and save it as a Draft at any point,
  without it being publicly visible.
- The author can edit an existing Note, published or not.
- Saving a Draft does not require the content to be complete or valid
  for publication.
- Publishing a Note makes it visible to visitors at a stable URL.
- Published content must be revertible to a non-public state.

### V1.5 Revision

- Content the author explicitly saves is retained as a distinct
  revision. Automatic/background saving, if ever added, is not required
  to create a revision on its own.
- The author must be able to view a Note's revision history.
- Whether/how a past revision can be restored is not decided here.

### V1.6 Technical baseline (supersedes Section 3 for V1 features only)

- V1 requires authentication (to restrict editing to the author) and
  persistent storage. V0's "No server-side application" constraint does
  not hold for V1 — some backend (a hosted API, serverless functions, or
  a BaaS) is required.
- V0's already-shipped static pages are unaffected: V1 adds capability,
  it does not retroactively change how the current site is built or
  deployed.
- Specific technology (which backend/BaaS, auth provider, database,
  hosting alongside GitHub Pages) is not decided here — deferred to
  implementation-design discussion, tracked as a GitHub Issue rather
  than a separate design document. See `ARCHITECTURE.md` for what was
  settled on.

### V1.7 Explicitly not required for V1

- Topics, Taxonomy, taxonomy evolution (`product.md`)
- AI-assisted authoring features (`product.md`'s AI philosophy)
- Multi-author support
- Comments, reactions, or any visitor interaction with published content

---

## Part 3: Q/A — Personal Inquiry

> Q/A is a category in `product.md`'s Core model, motivated by
> `invariants.md`'s Preservation value principle: personal inquiry — a
> question genuinely being pursued, and the answer arrived at — has
> standing to be preserved on its own, independent of whether it is
> ever composed into a Note or published. It emerged from
> implementation-design discussion (mohokoto.github.io#12) rather than
> being specified in advance here; this section documents it after the
> fact so the requirement and what was built to satisfy it
> (`ARCHITECTURE.md`) stay in sync. As with Part 2, requirements only —
> data storage format, API design, and specific technology choices are
> implementation-design decisions, tracked as GitHub Issues.

### V3.1 Purpose

Enable mohokoto to record personal inquiry (a question and its current
answer) directly, independent of whether it is ever composed into a
Note, and to preserve relationships between related pieces of inquiry
over time.

### V3.2 Scope

- Same single-author, same-authentication constraint as V1.2.
- A Q/A has no publication or visibility state of its own — it is never
  directly visible to a visitor. Only content a Note deliberately
  composes from it, and that Note publishes (per Part 2), becomes
  public.
- How a Note draws on Q/A (referencing, snapshotting) is out of scope
  for this requirement set — it's a cross-object workflow requirement,
  not a per-object one, and belongs in `FLOW.md` (planned, not yet
  created — see mohokoto.github.io#17), not in this Part.

### V3.3 Content model requirements

- A Q/A has at minimum a question and an answer, and its relationships
  to other Q/A's.
- Neither the question nor the answer is required to be complete for a
  Q/A to exist — a bare label is sufficient, so that a recalled
  interest can be captured the moment it comes to mind rather than
  requiring it be worked into a proper question first.
- A Q/A's relationships to other Q/A's must be preservable, covering
  both how one piece of inquiry gave rise to another and connections
  that aren't about how something arose.

### V3.4 Revision

Same principle as V1.5: content the author explicitly saves is retained
as a distinct revision.

### V3.5 Deletion

A Q/A must be deletable outright, as an explicit, author-initiated
action. Deleting a Q/A referenced by another Q/A's relationships must
not corrupt or block that reference — the surviving Q/A keeps its own
record of the relationship even once its target is gone.
