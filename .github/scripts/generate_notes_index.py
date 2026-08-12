#!/usr/bin/env python3
"""Regenerate notes/index.html by scanning notes/*/index.html.

Run from the repo root, after notes/ has been rsynced from
notes-published (sync-notes.yml). Sorts newest-first using each note's
<meta name="date"> (added by the Worker at publish time,
mohokoto.github.io#8); notes published before that existed fall back to
the synced file's git commit date.
"""

import html
import re
import subprocess
import sys
from pathlib import Path

NOTES_DIR = Path("notes")
# <h1>, not <title> - renderNoteHtml's <title> has a " · mohokoto" suffix
# for the browser tab, which a naive <title> extraction here would carry
# straight into the list (observed live: "테스트 2 · mohokoto" as the link
# text). <h1> is always just the bare escaped title.
TITLE_RE = re.compile(r"<h1>(.*?)</h1>", re.DOTALL)
DATE_RE = re.compile(r'<meta\s+name="date"\s+content="([^"]*)"')


def git_commit_date(path: Path) -> str:
    result = subprocess.run(
        ["git", "log", "-1", "--format=%cI", "--", str(path)],
        capture_output=True,
        text=True,
        check=False,
    )
    date = result.stdout.strip()
    return date or "1970-01-01T00:00:00Z"


def collect_notes():
    notes = []
    if not NOTES_DIR.is_dir():
        return notes
    for entry in sorted(NOTES_DIR.iterdir()):
        note_file = entry / "index.html"
        if not entry.is_dir() or not note_file.is_file():
            continue
        text = note_file.read_text(encoding="utf-8")
        title_match = TITLE_RE.search(text)
        title = html.unescape(title_match.group(1)).strip() if title_match else entry.name
        date_match = DATE_RE.search(text)
        date = date_match.group(1) if date_match else git_commit_date(note_file)
        notes.append({"slug": entry.name, "title": title, "date": date})
    notes.sort(key=lambda n: n["date"], reverse=True)
    return notes


def render(notes) -> str:
    items = "\n".join(
        f'        <li><a href="/notes/{html.escape(n["slug"])}/">{html.escape(n["title"])}</a> '
        f'<time datetime="{html.escape(n["date"])}">{html.escape(n["date"][:10])}</time></li>'
        for n in notes
    )
    if not notes:
        items = "        <li class=\"empty\">Nothing published yet.</li>"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Notes · mohokoto</title>
  <meta name="description" content="Notes from mohokoto.">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css">
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>

  <header class="site-header">
    <nav aria-label="Primary">
      <a href="/#home" class="brand">mohokoto</a>
      <ul>
        <li><a href="/#about">About</a></li>
        <li><a href="/#projects">Projects</a></li>
        <li><a href="/notes/">Notes</a></li>
        <li><a href="/#links">Links</a></li>
      </ul>
    </nav>
  </header>

  <main id="main">
    <article>
      <h1>Notes</h1>
      <ul class="link-list">
{items}
      </ul>
    </article>
  </main>

  <footer class="site-footer">
    <p>&copy; mohokoto</p>
  </footer>
</body>
</html>
"""


def main():
    notes = collect_notes()
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    (NOTES_DIR / "index.html").write_text(render(notes), encoding="utf-8")
    print(f"Wrote notes/index.html with {len(notes)} note(s).", file=sys.stderr)


if __name__ == "__main__":
    main()
