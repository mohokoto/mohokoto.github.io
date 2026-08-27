# Architecture (Global)

① Regulates the elements of this system — the technical structure
currently built (repos, services, routes) and the qualifying criteria
an object must satisfy to be a valid element of this system in the
first place.
② Applies system-wide.
③ Does not cover relationships between objects (`RELATIONS.md`),
system behavior or cross-object workflow (`BEHAVIOR.md`), or
subsystem-internal content models and state transitions
(`SITE.md`/`NOTES.md`/`Q-A.md`).

If the running system and this document disagree, that's a bug in one
of the two to be resolved deliberately. Update this document when the
actual structure changes.

## What counts as a valid element

Every Note and Q/A held by this system must carry personal value
arising from the individual's own experience, judgment, taste, context,
or circumstances and activity — not merely value a generic LLM response
could already supply. Regeneratability alone is not grounds for keeping
something: general knowledge easily re-obtained by asking an LLM again
doesn't qualify on its own. This is not limited to reflective content —
reference information that only carries meaning because of the
individual's own circumstances (a project's server IP, a contract's
expiry date) qualifies too. The test is uniqueness of preservation
value, not personal relevance in general, and it applies to the
information an object holds, not necessarily the whole object as one
indivisible unit — a single Note can mix material that satisfies this
test with material that doesn't, as long as the object's reason for
being preserved rests on the part that qualifies.

The individual remains the author of their own inquiry and judgment. A
Note or Q/A may freely mix the individual's own writing with AI output
and external material — the test is not what proportion of the
sentences they typed. What must hold is that the inquiry and the
meaning-making are theirs: an AI's interpretation must not displace the
individual's own memory or judgment, and refining, summarizing, or
reorganizing content must not quietly substitute the AI's account of
what mattered for the individual's own.

## What a Note and a Q/A each are

- **Q/A** is the unit of personal inquiry: a question the user is
  actually pursuing, together with the current answer they have arrived
  at. Neither field is required to be fully formed to exist — a bare
  label is enough to create one (see `Q-A.md` for the content model).
- **Note** is the atomic unit of written content: what the user
  actually writes, across whatever range of subjects (see `NOTES.md`
  for the content model). Conceptually this category is a composed,
  publishable document — "Article" or "Document" would describe it more
  precisely. The name "Note" is kept because it's load-bearing in the
  implementation well beyond identifiers: published URLs
  (`/notes/{slug}/`), storage layout across two repositories, the
  `notes-published` repository name, and the sync workflow all assume
  it.

## System overview

```text
Editor UI (browser) ──── mohokoto-worker.mohokoto.workers.dev ──── behind Cloudflare Access
        │                         │
        │ Note/Q-A CRUD,          │ GitHub App A: contents:write
        │ publish/unpublish       ▼
        │                 content-drafts (private)
        │                 canonical source + revision history (git log)
        │
        │ on publish/unpublish/delete:
        │  1. (publish only) render Markdown→HTML, commit to notes-published
        │  2. remove/write notes-published as needed, then
        │     GitHub App B: actions:write → trigger sync workflow
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
| `content-drafts` | private | Canonical source for every Note (published or not) and every Q/A — neither has a publish state of its own here. Its git log *is* the revision history — nothing else stores revisions. |
| `worker` | private | Cloudflare Worker source. The only backend/API in the system, and also serves the Editor UI. |

## Cloudflare Worker (`mohokoto-worker`)

Single Hono app, one deployment target
(`mohokoto-worker.mohokoto.workers.dev`, no custom domain). Serves
three kinds of things from one origin — a deliberate choice to avoid
the multi-origin Access/CORS surface a separate editor host would add:

- **JSON API** — `GET/POST /notes`, `GET/PUT/DELETE /notes/:slug`,
  `POST /notes/:slug/publish|unpublish`, `GET /notes/:slug/revisions`;
  `GET/POST /qa`, `GET/PUT/DELETE /qa/:id`, `GET /qa/:id/revisions`.
  What each route does is `NOTES.md`/`Q-A.md`'s concern, not this
  document's.
- **Editor UI** — `GET /` and `GET /q` (both serve the Q/A list — Q/A is
  the main screen, not Notes; see `BEHAVIOR.md`'s Q selection → Note
  creation workflow) and `GET /q/edit/:id` (Q/A editor); `GET /n` (Note
  list) and `GET /edit/:slug` (Note editor). A persistent nav in the
  shared page header links every page to both lists, regardless of
  which one is home. Both rendered server-side as plain HTML/CSS/JS
  strings (`src/ui.ts`). No build step, no framework — templates are
  TypeScript template literals. EasyMDE and its dependency (Font
  Awesome, loaded by EasyMDE itself) come from jsDelivr at runtime, not
  bundled.
- **Static assets** — `manifest.json` and PWA icons, served via
  Workers static assets (`[assets]` in `wrangler.toml`, files in
  `public/`) rather than a Hono route. First and only binary content
  this project serves.

`requireAccess()` middleware (`src/access.ts`) runs on every request
except the static assets: verifies the `Cf-Access-Jwt-Assertion` header
against Cloudflare Access's JWKS endpoint. This is deliberate
defense-in-depth on top of Access's own edge-level enforcement, not a
substitute for it.

KV namespace `TOKEN_CACHE` holds GitHub App installation tokens
(55-minute TTL, under GitHub's 1-hour expiry) so a token isn't minted
on every request, and the resolved `<html lang>` V0 currently declares
(`site-lang.ts`, 1-hour TTL) — see Language, below.

## Two GitHub Apps, not one

A single GitHub App's permissions are uniform across every repo it's
installed on — there's no way to grant `contents:write` on one repo and
only `actions:write` on another within one App. So there are two:

| App | Permission | Installed on |
|---|---|---|
| `mohokoto-content-sync` (App A) | `contents:write` | `content-drafts`, `notes-published` |
| `mohokoto-publish-trigger` (App B) | `actions:write` only | `mohokoto.github.io` |

App B can *only* dispatch workflow runs — it has no path to write file
content anywhere, including in `mohokoto.github.io`. This is the
blast-radius boundary: even a fully compromised Worker can trigger
syncs but can't rewrite the live site's source or touch Note/Q-A drafts
directly through App B. (The constraint this creates for any new
`workflow_dispatch`-triggerable workflow is a `BEHAVIOR.md` norm.)

## Access control

**Cloudflare Access** gates the entire `mohokoto-worker.mohokoto.workers.dev`
domain at Cloudflare's edge (before the Worker or static assets ever
run) — one Access Application (`mohokoto-worker`), one policy: allow
`parkseohwa@gmail.com` only.

**One exception**: a second Access Application
(`mohokoto-worker public PWA assets`) with a `bypass` policy, scoped
exactly to `/manifest.json` and `/icons/*`. Added because the Web App
Manifest spec fetches the manifest and its referenced icons in a way
that doesn't reliably carry Access's session cookie even with
`crossorigin="use-credentials"` set — installability silently failed
until these paths were made public. The files themselves are
non-sensitive (name, icon, theme color). Verified live that the bypass
doesn't leak beyond those two prefixes.

## PWA

`manifest.json` + three icons (192px, 512px, 512px maskable — all
derived from V0's existing wine-background cream-"m" mark) satisfy
Chromium's installability requirements: `name`/`short_name`, the two
icon sizes, `start_url`, `display: standalone`,
`prefer_related_applications: false`. No service worker — confirmed
against Chromium's actual criteria that one isn't required for
installability, and none of Phase 2+ (offline shell caching, local
draft storage, sync-on-reconnect) has been built.

## Language follows V0

Editor UI chrome (button labels, messages — not Note/Q-A content, which
is whatever language the author writes) is in English or Korean,
whichever `mohokoto.github.io`'s own `<html lang>` currently declares.
The Worker fetches `https://mohokoto.github.io/` server-side and caches
the resolved language in KV for an hour. Not the visitor's browser
language, and not hardcoded.

## Commit authorship

Every commit App A makes (`content-drafts`, `notes-published`) sets
`author`/`committer` to `mohokoto <178871570+mohokoto@users.noreply.github.com>`
— GitHub's ID-based noreply address, not a real email. `notes-published`
is public; an earlier version of this used a real address there before
being caught in review and the exposed history rewritten. This is a
description of current behavior, not a forward-binding constraint on
any future commit-writing mechanism — App A is currently the only one.

## Known gaps

- No automated tests anywhere in the Worker or the sync workflow.
  Everything so far has been verified by live smoke-testing against the
  real deployed system, not by a test suite.
