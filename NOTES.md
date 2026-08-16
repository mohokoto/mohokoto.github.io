# Notes (Subsystem)

① Regulates the elements (content model), relationships (snapshot
mechanics with Q/A), and behavior (save/publish/unpublish/delete,
revision, publish pipeline) of the Note object.
② Applies to the Note object and its publish pipeline only.
③ Does not cover the Q/A subsystem itself, the V0 static site, or any
global-scope norm (`ARCHITECTURE.md`/`RELATIONS.md`/`BEHAVIOR.md`).
The routes exposed for Notes are inventoried in `ARCHITECTURE.md`
(Global/Elements); this document covers what using them does.

## Purpose

Enable mohokoto to write, revise, and publish Notes directly through
the site, without requiring a separate authoring tool or manual git
operations.

## Scope

- A single authenticated author (mohokoto only) can create and edit
  content through an in-browser editor on the live site.
- Visitors (unauthenticated) can only view Published content. Draft
  content and the editor itself must not be publicly accessible.
- Topics and Taxonomy are out of scope. The content model must not
  preclude adding topic association later, but no topic/taxonomy
  feature is built now.
- Not required: multi-author support; comments, reactions, or any
  visitor interaction with published content; AI-assisted authoring.

## Content model

A Note has at minimum: a title, a body, a publication status
(`draft`/`published`, a free string, deliberately not an enum), created
and last-modified timestamps, a revision history (see Revision, below),
and `sources` — snapshots of Q/A content the Note drew on (see Sources,
below).

## Sources: snapshot, not a live reference

A Note may draw on one or more Q/A's, and one Q/A may feed several
Notes — but a Note is not a view onto them. A Note's `sources` are a
snapshot of the Q/A content it drew on at the time the source was
added or last refreshed: a later change to the source Q/A does not
propagate into the Note, and is pulled in only when the user explicitly
refreshes that source. Editing a Note never edits a Q/A back.

## Editing and saving

- The author can create a new Note and save it as a Draft at any point,
  without it being publicly visible.
- The author can edit an existing Note, published or not.
- Saving a Draft does not require the content to be complete or valid
  for publication.
- Publishing a Note makes it visible to visitors at a stable URL
  (`/notes/{slug}/`).
- Published content must be revertible to a non-public state.

## Revision

- Content the author explicitly saves is retained as a distinct
  revision. Automatic/background saving, if ever added, is not required
  to create a revision on its own.
- The author must be able to view a Note's revision history.

## Publish pipeline

1. The author writes in the Editor UI. `PUT /notes/:slug` commits
   Markdown + frontmatter to `content-drafts`. Every save that actually
   changes title/body/sources is one commit — that history is the
   revision log directly, not a separate feature. The comparison
   normalizes trailing newlines on `body`, since a round trip through
   the Editor could otherwise register as a change on its own.
2. `POST /notes/:slug/publish` renders the Note's Markdown to static
   HTML, commits it to `notes-published`, then triggers
   `mohokoto.github.io`'s `sync-notes.yml` (see `ARCHITECTURE.md` for
   the underlying two-GitHub-App mechanism this pipeline uses).
3. `sync-notes.yml` syncs `notes-published` into `mohokoto.github.io`
   and regenerates the Notes index, sorted newest-first.
4. GitHub Pages rebuilds the live site from the new commit.

## State transitions

Save, Publish, Un-publish, and Delete are four independent actions, not
variations of one toggle — Publish always means "make the current draft
content the live version," regardless of what `status` already was,
which is why "published + Publish" (republish) is its own row below,
not a no-op. Delete is the odd one out structurally: every other
action's "To" is still `draft` or `published` (the Note keeps
existing), but Delete has no "To" at all — it's the only transition
that exits the state space entirely.

| From | Action (endpoint) | To | `content-drafts` | `notes-published` | Sync triggered |
|---|---|---|---|---|---|
| draft | Save (`PUT /notes/:slug`) | draft | commit, `savedAt` ← now — skipped entirely if title/body/sources all unchanged | untouched | no |
| published | Save (`PUT /notes/:slug`) | published | commit, `savedAt` ← now — same no-op guard as above | untouched — now diverges from the draft until republished | no |
| draft | Publish (`POST /notes/:slug/publish`) | published | commit, `status` → published, `publishedAt` ← now (first time only), `lastPublishedAt` ← now | created from current draft body | yes |
| published | Publish, i.e. republish | published | commit, `lastPublishedAt` ← now (`publishedAt` untouched) | overwritten from current draft body | yes |
| published | Un-publish (`POST /notes/:slug/unpublish`) | draft | commit, `status` → draft | deleted | yes |
| draft | Un-publish | draft | commit written unconditionally even though nothing changes — unlike Save, this handler has no no-op guard | untouched (delete is skipped: nothing was there) | no |
| draft | Delete (`DELETE /notes/:slug`) | *(gone)* | file deleted | untouched (nothing published) | no |
| published | Delete (`DELETE /notes/:slug`) | *(gone)* | file deleted | deleted | yes |

The "draft + Un-publish" row isn't reachable from the Editor UI (the
Un-publish control is hidden whenever `status` is already `draft`) but
is real behavior of the API itself.

Deleting doesn't purge `content-drafts`' git history for that path —
past commits stay in `git log` even though the file (and the Note
itself) is gone. Deliberate: `git log` is *the* revision history, so a
routine Delete rewriting it would work against that rather than with
it. Delete doesn't require Un-publish first — deleting a published Note
both takes it down and removes the draft in one deliberate act, since
there's no second, different intent it could be conflated with.

## Known gaps

- **A Note's view of its sources' live state goes stale without a page
  reload.** The Editor fetches the full Q/A list once, on load, to
  decide whether each source is up to date or its target has been
  deleted; nothing re-fetches it afterward. Editing or deleting a
  source Q/A in another tab while the Note stays open won't be
  reflected until the Note's edit page is reloaded.
- **Delete's compliance with the Change-over-time norm (`BEHAVIOR.md`)
  is conditional, not structural.** That norm excludes a user's own
  explicit, confirmed deletion from what it constrains — but nothing in
  `DELETE /notes/:slug` itself enforces "human-initiated and confirmed
  per Note." The endpoint just deletes whatever slug it's given; the
  Editor UI's `confirm()` dialog is the only thing currently making
  that true. If a future feature reuses this endpoint for bulk or
  automated deletion, that safety property would no longer hold.
- **The Publish/Un-publish/Delete pipelines aren't atomic.** All three
  are 2–3 sequential network calls with no rollback. If a later step
  throws after an earlier one succeeded, `content-drafts` and the live
  site end up disagreeing. **Delete is the worst case**: if its
  `content-drafts` delete succeeds but the `notes-published` delete
  then fails, the Note is gone from the Editor entirely with no way to
  retry through the app, while the old page stays live indefinitely.
- **`content-drafts` writes across Save/Publish/Un-publish/Delete
  aren't isolated from each other beyond the Editor's own UI lock.**
  All four act on the same file by `sha`. The Editor serializes them
  client-side (one `busy` flag disables all four buttons for the
  duration of any one), but nothing enforces this server-side: two
  browser tabs, or a direct API call racing the Editor, can still send
  overlapping writes. GitHub rejects whichever lands second against a
  stale `sha`, surfaced only as a generic failure alert.
- **`sync-notes.yml` has no retry on a concurrent-dispatch push race.**
  Reproduced live twice: a `git push` from `sync-notes.yml` rejected
  non-fast-forward when racing another dispatch, or a manual push to
  the same repo. The workflow syncs full current state
  (`rsync --delete`), so a genuine loss self-heals on whatever run
  processes state next — but a push can fail silently in the meantime,
  with no retry and no alert.
