# Site (Subsystem)

① Regulates the elements, relationships, and behavior of the V0 static
site — what it's built from and how it's deployed and accessed.
② Applies to the static site (`mohokoto.github.io`'s `index.html`,
`styles.css`, and related static assets) only.
③ Does not cover the Note or Q/A subsystems, or any global-scope norm
(`ARCHITECTURE.md`/`RELATIONS.md`/`BEHAVIOR.md`).

## Purpose

A personal website for `mohokoto`: a simple, durable home for personal
information, projects, interests, and links.

## Scope

- Static website
- Hosted on GitHub Pages
- Publicly accessible
- Responsive across desktop and mobile
- Easy to maintain and extend

## Technical baseline

- HTML5, CSS3
- JavaScript only when necessary
- No framework required
- No server-side application
- GitHub Pages deployment
- One curated display web font is permitted as a deliberate, documented
  exception to minimal dependencies (see Design principles), loaded with
  `display=swap` so it does not block rendering. No other external
  runtime dependencies.

## Site structure

The site supports:

- Home
- About
- Projects
- Links

The exact presentation and content of these sections is intentionally
left open.

## Design principles

- Simple, fast, readable, accessible, responsive
- Minimal dependencies (one deliberate exception: a display web font,
  see Technical baseline)
- Easy to modify

### Visual direction

The site's visual identity draws its mood, palette, and typographic
sensibility from a vintage-glamour editorial moodboard (warm cream
background, deep jewel-tone accents — wine, sage, gold — a large serif
display face, and generous editorial spacing/dividers). Only the tone is
referenced: no illustration, photography, or likeness from the source
moodboard appears on the site. A styling decision, not a structural one.

## Accessibility

The site:

- Uses semantic HTML
- Maintains a logical heading hierarchy
- Supports keyboard navigation
- Provides meaningful alternative text for images
- Maintains sufficient contrast
- Respects reduced-motion preferences where applicable

## Deployment

The production site is `https://mohokoto.github.io/`. Changes are
deployed through the Git repository and GitHub Pages.
