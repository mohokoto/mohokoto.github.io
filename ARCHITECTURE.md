# Architecture

## Status

This document is a **normative description of the current system** —
what exists and how it's wired together, as of now. It is not a
design proposal, a future plan, or a record of how decisions were
reached (that's what the closed GitHub Issues referenced throughout
are for). If the running system and this document disagree, that's a
bug in one of the two to be resolved deliberately, not something this
document should silently absorb by being regenerated from whatever the
code happens to do.

It sits alongside `SPEC.md` in the doc hierarchy, one level below it:

```text
product.md        (why — long-term philosophy)
    ↓
invariants.md      (what must always hold, regardless of implementation)
    ↓
SPEC.md            (what must be built — required behavior, technology-agnostic)
    ↓
ARCHITECTURE.md    (this document — what's actually built, right now)
    ↓
implementation (4 repos, below)
```

`SPEC.md`'s V1.6 explicitly defers "specific technology... to
implementation-design discussion, tracked as a GitHub Issue" — this
document is where those since-settled decisions live once they stopped
being discussion and became the system. Rationale for *why* a given
choice was made generally isn't repeated here; each section links the
issue where it was decided.

Update this document when the actual structure changes. Don't let it
drift into describing an old shape after a redesign.

## System overview

```text
Editor UI (browser) ──── mohokoto-worker.parkseohwa.workers.dev ──── behind Cloudflare Access
        │                         │
        │ Note CRUD, publish/     │ GitHub App A: contents:write
        │ unpublish               ▼
        │                 content-drafts (private)
        │                 canonical source + revision history (git log)
        │
        │ on publish/unpublish:
        │  1. render Markdown→HTML, commit to notes-published
        │  2. GitHub App B: actions:write → trigger sync workflow
        ▼
notes-published (public)          mohokoto.github.io (public)
static HTML artifact         ◄──  sync-notes.yml pulls notes/ from
                              rsync notes-published, rebuilds notes/index.html,
                                   commits + pushes → GitHub Pages serves it
```

Four repos, one Cloudflare Worker, two GitHub Apps, one GitHub Actions
workflow. No other backend, database, or hosting exists.

## Repositories

| Repo | Visibility | Purpose |
|---|---|---|
| `mohokoto.github.io` | public | The live site (GitHub Pages). V0 static pages (`index.html`, `styles.css`) plus the synced `notes/` tree. |
| `notes-published` | public | Intermediate artifact: rendered static HTML for currently-published Notes only. Not meant to be browsed directly. |
| `content-drafts` | private | Canonical source for every Note, published or not. Its git log *is* the revision history (SPEC.md V1.5) — nothing else stores revisions. |
| `worker` | private | Cloudflare Worker source. The only backend/API in the system, and also serves the Editor UI (see below). |

## Data flow: Draft → Publish → Live

1. Author writes in the Editor UI (served by the Worker, see below).
   `PUT /notes/:slug` commits Markdown + frontmatter to `content-drafts`
   via GitHub App A. Every save that actually changes title/body is one
   commit — that history is V1.5's revision log directly, not a
   separate feature.
2. `POST /notes/:slug/publish`: Worker renders the Note's Markdown to
   static HTML (`marked`), commits it to `notes-published` (App A
   again), then calls GitHub App B to fire
   `mohokoto.github.io`'s `sync-notes.yml` via `workflow_dispatch`.
3. `sync-notes.yml` (runs in `mohokoto.github.io`): checks out both
   `notes-published` and itself, `rsync -a --delete`s `notes/` from
   the former into the latter, regenerates `notes/index.html`
   (`.github/scripts/generate_notes_index.py`, sorted newest-first
   using each page's `<meta name="date">`), commits and pushes if
   anything changed. Also runs on a `schedule` (`*/5 * * * *`) — not
   primarily as a recovery path for a failed dispatch push (see
   [Known gaps](#known-gaps): the one observed race was actually
   resolved by a later dispatch, not the schedule, which found nothing
   to sync), but as a backup for the case where a dispatch was never
   sent at all. In practice almost every commit here comes from a
   dispatch.
4. GitHub Pages rebuilds `mohokoto.github.io` from the new commit.
   Typical publish-to-live latency: dispatch is near-instant, Pages
   rebuild adds roughly 30–60s.

Un-publish is the same path in reverse: delete from `notes-published`,
same App B trigger, same sync.

## Cloudflare Worker (`mohokoto-worker`)

Single Hono app, one deployment target
(`mohokoto-worker.parkseohwa.workers.dev`, no custom domain). Serves
three kinds of things from one origin — a deliberate choice
(mohokoto.github.io#2) to avoid the multi-origin Access/CORS surface a
separate editor host would add:

- **JSON API** — `GET/POST /notes`, `GET/PUT /notes/:slug`,
  `POST /notes/:slug/publish|unpublish`, `GET /notes/:slug/revisions`.
- **Editor UI** — `GET /` (Note list) and `GET /edit/:slug` (EasyMDE
  editor), rendered server-side as plain HTML/CSS/JS strings (`src/ui.ts`).
  No build step, no framework — templates are TypeScript template
  literals. EasyMDE and its dependency (Font Awesome, loaded by EasyMDE
  itself) come from jsDelivr at runtime, not bundled.
- **Static assets** — `manifest.json` and PWA icons, served via
  Workers static assets (`[assets]` in `wrangler.toml`, files in
  `public/`) rather than a Hono route. First and only binary content
  this project serves.

`requireAccess()` middleware (`src/access.ts`) runs on every request
except the static assets: verifies the `Cf-Access-Jwt-Assertion` header
against Cloudflare Access's JWKS endpoint. This is deliberate
defense-in-depth on top of Access's own edge-level enforcement, not a
substitute for it (mohokoto.github.io#1).

KV namespace `TOKEN_CACHE` holds GitHub App installation tokens
(55-minute TTL, under GitHub's 1-hour expiry) so a token isn't minted
on every request, and the resolved `<html lang>` V0 currently declares
(`site-lang.ts`, 1-hour TTL) — see [Language](#language-follows-v0)
below.

## Two GitHub Apps, not one

A single GitHub App's permissions are uniform across every repo it's
installed on — there's no way to grant `contents:write` on one repo
and only `actions:write` on another within one App
(discovered the hard way: mohokoto.github.io#3). So there are two:

| App | Permission | Installed on |
|---|---|---|
| `mohokoto-content-sync` (App A) | `contents:write` | `content-drafts`, `notes-published` |
| `mohokoto-publish-trigger` (App B) | `actions:write` only | `mohokoto.github.io` |

App B can *only* dispatch workflow runs — it has no path to write
file content anywhere, including in `mohokoto.github.io`. This is the
blast-radius boundary: even a fully compromised Worker can trigger
syncs but can't rewrite the live site's source or touch Note drafts
directly through App B.

Constraint this creates: any new workflow in `mohokoto.github.io`
that's triggerable via `workflow_dispatch` must declare a minimal
`permissions:` block itself, since App B's `actions:write` doesn't
distinguish which workflow it's dispatching.

## Access control

**Cloudflare Access** gates the entire `mohokoto-worker.parkseohwa.workers.dev`
domain at Cloudflare's edge (before the Worker or static assets ever
run) — one Access Application (`mohokoto-worker`), one policy: allow
`parkseohwa@gmail.com` only.

**One exception**: a second Access Application
(`mohokoto-worker public PWA assets`) with a `bypass` policy, scoped
exactly to `/manifest.json` and `/icons/*`. Added because the Web App
Manifest spec fetches the manifest and its referenced icons in a way
that doesn't reliably carry Access's session cookie even with
`crossorigin="use-credentials"` set (mohokoto.github.io#8) — installability
silently failed until these paths were made public. The files
themselves are non-sensitive (name, icon, theme color). Verified live
that the bypass doesn't leak beyond those two prefixes — adjacent paths
(`/icons` without a file, `/notes`, `/edit/:slug`) still 302 to the
Access login.

## PWA

`manifest.json` + three icons (192px, 512px, 512px maskable — all
derived from V0's existing wine-background cream-"m" mark) satisfy
Chromium's installability requirements: `name`/`short_name`, the two
icon sizes, `start_url`, `display: standalone`,
`prefer_related_applications: false`. No service worker — confirmed
against Chromium's actual criteria that one isn't required for
installability, and none of Phase 2+ (offline shell caching, local
draft storage, sync-on-reconnect) has been built. If that's ever
picked up, it's new work, not something implied by what's here.

## Language follows V0

Editor UI chrome (button labels, messages — not Note content, which is
whatever language the author writes) is in English or Korean,
whichever `mohokoto.github.io`'s own `<html lang>` currently declares.
The Worker fetches `https://mohokoto.github.io/` server-side (no CORS
concern — that's a browser-only restriction) and caches the resolved
language in KV for an hour. Not the visitor's browser language, and
not hardcoded — if V0's declared language changes, the editor follows
without a code change (mohokoto.github.io#7).

## Commit authorship

Every commit App A makes (`content-drafts`, `notes-published`) sets
`author`/`committer` to `mohokoto <178871570+mohokoto@users.noreply.github.com>`
— GitHub's ID-based noreply address, not a real email. `notes-published`
is public; an earlier version of this used a real address there before
being caught in review and the exposed history rewritten
(mohokoto.github.io#7).

## Known gaps

- Individual published Note pages (`renderNoteHtml` in `src/index.ts`)
  are an unstyled placeholder — no V0 visual language applied yet,
  unlike the Notes index page. Tracked in #9.
- No automated tests anywhere in the Worker or the sync workflow.
  Everything so far has been verified by live smoke-testing against
  the real deployed system, not by a test suite.
- **`sync-notes.yml` has no retry on a concurrent-dispatch push race.**
  Reproduced live: two `workflow_dispatch` runs 6s apart
  (2026-08-12T05:06:06Z started first, T05:06:12Z started second). The
  first finished its commit+push before the second reached its own
  push, so the second's `git push` was rejected non-fast-forward (exact
  error confirmed in the job log) — by the time it failed, the first
  run had already pushed the same target state (both synced from the
  same `notes-published` content, 6s apart with nothing published in
  between). Nothing was actually missing: the next scheduled run
  10 minutes later logged "No changes to sync." — confirming the state
  was already correct, not that it healed something. Because the
  workflow always syncs *full current state* via `rsync --delete`
  rather than an incremental diff, a genuine loss (two dispatches
  racing over materially *different* content) would self-heal on
  whatever run — dispatch or schedule — processes state next; this
  incident just didn't require that, since the failed run was
  redundant from the moment it lost the race. The real gap is
  narrower than "content gets lost": a push can fail silently, with
  no retry and no alert, and nothing in this repo would surface that
  it happened.

  **Second occurrence, different racer**: reproduced again on
  2026-08-12T10:35Z, this time not two dispatches racing each other but
  a dispatch racing a *manual* `git push` (active development on this
  repo's own files - styles.css, the sync script - happening
  concurrently with live publish/unpublish testing that triggers the
  same workflow). Rejected non-fast-forward, same as before; unlike the
  first incident, this one *did* leave the live site stale (a Note's
  updated byline didn't appear) until manually re-triggered, since
  nothing else re-synced state on its own before that. Confirms the
  race isn't limited to dispatch-vs-dispatch - anything that pushes to
  this repo's main is a participant, including a human editing docs
  here at the same time someone's using the Editor.
