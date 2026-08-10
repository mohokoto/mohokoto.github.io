# Personal Website Specification

> This document specifies the current, initial implementation phase: a
> static personal homepage. It does not describe the full long-term
> product direction. See [`product.md`](product.md) for the product
> philosophy this site is the first environment for, and
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
- No server-side application
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
