#!/usr/bin/env python3
"""
spec-to-html.py — Convert docs/specification/*.md into a single self-contained HTML.

Read-only export tool for non-developer sharing of specifications written by
the ywc-spec-writer skill. The canonical source of truth remains the markdown
files under docs/specification/; this script produces a derived view for
stakeholders who prefer a browser-friendly artifact (table of contents,
tabs, embedded markdown).

Design alignment with tools/claude-code/skills/references/html-output.md:
  - Single self-contained file (no external CSS/JS/image references).
  - Severity color tokens are not used (specs have no severity tiers),
    but the layout (sticky header, tabs, action bar) and Copy-as-Markdown
    surface follow the same conventions so the visual language is consistent
    across ywc-* HTML artifacts.

Markdown subset: ATX headings, paragraphs, bullet/ordered lists (one level),
GFM tables, fenced code blocks, blockquotes, inline emphasis/strong/code,
links, horizontal rules. Spec docs are constrained to this subset by
ywc-spec-writer's "no program code, business-stakeholder audience" rule.

Usage:
    python3 tools/scripts/spec-to-html.py
    python3 tools/scripts/spec-to-html.py --input docs/specification \\
        --output claudedocs/spec-export-$(date +%Y-%m-%d).html \\
        --title "MyProject Specification"

Exit codes:
    0 — HTML written successfully
    1 — input directory missing or empty
    2 — argument or filesystem error
"""

from __future__ import annotations

import argparse
import datetime as _dt
import html
import pathlib
import re
import sys
from dataclasses import dataclass
from typing import List, Tuple


# ---------------------------------------------------------------------------
# Markdown → HTML converter (stdlib-only subset)
# ---------------------------------------------------------------------------

_INLINE_CODE = re.compile(r"`([^`]+)`")
_STRONG = re.compile(r"\*\*([^\*]+)\*\*|__([^_]+)__")
_EMPH = re.compile(r"(?<![*_])\*([^*\n]+)\*(?!\*)|(?<![*_])_([^_\n]+)_(?!_)")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)(?:\s+\"([^\"]+)\")?\)")
_IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"([^\"]+)\")?\)")
_AUTOLINK = re.compile(r"&lt;((?:https?|mailto):.+?)&gt;")


def _protect_codespans(text: str) -> Tuple[str, List[str]]:
    """Stash `code` spans behind placeholders so subsequent inline regexes
    do not touch their contents."""
    spans: List[str] = []

    def _stash(m: re.Match) -> str:
        spans.append(m.group(1))
        return f"\x00CODE{len(spans) - 1}\x00"

    return _INLINE_CODE.sub(_stash, text), spans


def _restore_codespans(text: str, spans: List[str]) -> str:
    for i, span in enumerate(spans):
        text = text.replace(
            f"\x00CODE{i}\x00",
            f"<code>{html.escape(span)}</code>",
        )
    return text


def _inline(text: str) -> str:
    """Convert inline markdown to HTML. Caller has already split block-level
    structure, so only inline transforms apply here."""
    text, spans = _protect_codespans(text)
    text = html.escape(text, quote=False)
    # Images come before links because both open with `[`.
    text = _IMAGE.sub(
        lambda m: '<img src="{src}" alt="{alt}"{title}>'.format(
            src=html.escape(html.unescape(m.group(2)), quote=True),
            alt=html.escape(html.unescape(m.group(1)), quote=True),
            title=(
                f' title="{html.escape(html.unescape(m.group(3)), quote=True)}"'
                if m.group(3)
                else ""
            ),
        ),
        text,
    )
    text = _LINK.sub(
        lambda m: '<a href="{href}"{title}>{label}</a>'.format(
            href=html.escape(html.unescape(m.group(2)), quote=True),
            label=m.group(1),
            title=(
                f' title="{html.escape(html.unescape(m.group(3)), quote=True)}"'
                if m.group(3)
                else ""
            ),
        ),
        text,
    )
    text = _AUTOLINK.sub(
        lambda m: (
            lambda u: f'<a href="{html.escape(u, quote=True)}">{html.escape(u)}</a>'
        )(html.unescape(m.group(1))),
        text,
    )
    # ** must run before * so bold wins over italic.
    text = _STRONG.sub(
        lambda m: f"<strong>{m.group(1) or m.group(2)}</strong>", text
    )
    text = _EMPH.sub(lambda m: f"<em>{m.group(1) or m.group(2)}</em>", text)
    return _restore_codespans(text, spans)


_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
_HR_RE = re.compile(r"^\s*([-*_])(?:\s*\1){2,}\s*$")
_FENCE_RE = re.compile(r"^(```+|~~~+)\s*([^\s]*)\s*$")
_BULLET_RE = re.compile(r"^(\s*)([-*+])\s+(.*)$")
_ORDERED_RE = re.compile(r"^(\s*)(\d+)\.\s+(.*)$")
_BLOCKQUOTE_RE = re.compile(r"^>\s?(.*)$")
_TABLE_SEP_RE = re.compile(r"^\s*\|?\s*(?::?-+:?\s*\|\s*)+:?-+:?\s*\|?\s*$")


def _split_table_row(line: str) -> List[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    parts: List[str] = []
    buf: List[str] = []
    escaped = False
    for ch in line:
        if escaped:
            buf.append(ch)
            escaped = False
        elif ch == "\\":
            escaped = True
        elif ch == "|":
            parts.append("".join(buf).strip())
            buf = []
        else:
            buf.append(ch)
    parts.append("".join(buf).strip())
    return parts


def _table_alignments(sep_cells: List[str]) -> List[str]:
    aligns: List[str] = []
    for cell in sep_cells:
        c = cell.strip()
        left = c.startswith(":")
        right = c.endswith(":")
        if left and right:
            aligns.append("center")
        elif right:
            aligns.append("right")
        elif left:
            aligns.append("left")
        else:
            aligns.append("")
    return aligns


def md_to_html(md_text: str) -> str:
    """Convert a markdown document to an HTML fragment (no <html>/<body>)."""
    lines = md_text.replace("\r\n", "\n").split("\n")
    out: List[str] = []
    i = 0
    n = len(lines)

    def _flush_paragraph(buf: List[str]) -> None:
        if not buf:
            return
        joined = " ".join(line.strip() for line in buf).strip()
        if joined:
            out.append(f"<p>{_inline(joined)}</p>")

    while i < n:
        line = lines[i]

        fence = _FENCE_RE.match(line)
        if fence:
            marker = fence.group(1)
            lang = fence.group(2) or ""
            i += 1
            code_buf: List[str] = []
            while i < n and not (
                lines[i].startswith(marker) and lines[i].strip() == marker
            ):
                code_buf.append(lines[i])
                i += 1
            if i < n:
                i += 1  # consume closing fence
            cls = f' class="language-{html.escape(lang)}"' if lang else ""
            out.append(
                f"<pre><code{cls}>"
                + html.escape("\n".join(code_buf))
                + "</code></pre>"
            )
            continue

        m_h = _HEADING_RE.match(line)
        if m_h:
            level = len(m_h.group(1))
            out.append(f"<h{level}>{_inline(m_h.group(2))}</h{level}>")
            i += 1
            continue

        if _HR_RE.match(line):
            out.append("<hr>")
            i += 1
            continue

        if _BLOCKQUOTE_RE.match(line):
            quote_lines: List[str] = []
            while i < n and _BLOCKQUOTE_RE.match(lines[i]):
                quote_lines.append(_BLOCKQUOTE_RE.match(lines[i]).group(1))
                i += 1
            inner = md_to_html("\n".join(quote_lines))
            out.append(f"<blockquote>{inner}</blockquote>")
            continue

        if "|" in line and i + 1 < n and _TABLE_SEP_RE.match(lines[i + 1]):
            header_cells = _split_table_row(line)
            aligns = _table_alignments(_split_table_row(lines[i + 1]))
            while len(aligns) < len(header_cells):
                aligns.append("")
            i += 2
            body_rows: List[List[str]] = []
            while i < n and lines[i].strip() and "|" in lines[i]:
                body_rows.append(_split_table_row(lines[i]))
                i += 1
            html_rows: List[str] = ["<table>", "<thead><tr>"]
            for idx, cell in enumerate(header_cells):
                style = (
                    f' style="text-align:{aligns[idx]}"'
                    if idx < len(aligns) and aligns[idx]
                    else ""
                )
                html_rows.append(f"<th{style}>{_inline(cell)}</th>")
            html_rows.append("</tr></thead>")
            html_rows.append("<tbody>")
            for row in body_rows:
                html_rows.append("<tr>")
                for idx, cell in enumerate(row):
                    style = (
                        f' style="text-align:{aligns[idx]}"'
                        if idx < len(aligns) and aligns[idx]
                        else ""
                    )
                    html_rows.append(f"<td{style}>{_inline(cell)}</td>")
                html_rows.append("</tr>")
            html_rows.append("</tbody></table>")
            out.append("".join(html_rows))
            continue

        m_b = _BULLET_RE.match(line)
        m_o = _ORDERED_RE.match(line)
        if m_b or m_o:
            tag = "ol" if m_o else "ul"
            items: List[str] = []
            while i < n:
                mb = _BULLET_RE.match(lines[i])
                mo = _ORDERED_RE.match(lines[i])
                if not (mb or mo):
                    break
                content = (mb or mo).group(3)
                i += 1
                while (
                    i < n
                    and lines[i].strip()
                    and not _BULLET_RE.match(lines[i])
                    and not _ORDERED_RE.match(lines[i])
                    and not _HEADING_RE.match(lines[i])
                ):
                    content += " " + lines[i].strip()
                    i += 1
                items.append(f"<li>{_inline(content)}</li>")
                if i < n and not lines[i].strip():
                    if i + 1 < n and not lines[i + 1].strip():
                        break
                    i += 1
            out.append(f"<{tag}>{''.join(items)}</{tag}>")
            continue

        if not line.strip():
            i += 1
            continue

        para_buf = [line]
        i += 1
        while i < n and lines[i].strip() and not (
            _HEADING_RE.match(lines[i])
            or _HR_RE.match(lines[i])
            or _FENCE_RE.match(lines[i])
            or _BLOCKQUOTE_RE.match(lines[i])
            or _BULLET_RE.match(lines[i])
            or _ORDERED_RE.match(lines[i])
            or (
                "|" in lines[i]
                and i + 1 < n
                and _TABLE_SEP_RE.match(lines[i + 1])
            )
        ):
            para_buf.append(lines[i])
            i += 1
        _flush_paragraph(para_buf)

    return "\n".join(out)


# ---------------------------------------------------------------------------
# Layout assembly
# ---------------------------------------------------------------------------

_CSS = """  :root {
    --bg: oklch(98% 0 0); --surface: oklch(100% 0 0); --text: oklch(22% 0 0);
    --muted: oklch(55% 0 0); --border: oklch(90% 0 0);
    --accent: oklch(65% 0.14 240);
  }
  @media (prefers-color-scheme: dark) {
    :root { --bg: oklch(20% 0 0); --surface: oklch(25% 0 0);
      --text: oklch(92% 0 0); --muted: oklch(65% 0 0); --border: oklch(35% 0 0); }
  }
  * { box-sizing: border-box; }
  body { margin: 0; font: 16px/1.6 -apple-system, system-ui, "Helvetica Neue",
    sans-serif; background: var(--bg); color: var(--text); }
  header { position: sticky; top: 0; background: var(--surface);
    border-bottom: 1px solid var(--border); padding: 1rem 1.5rem; z-index: 10; }
  main { max-width: 60rem; margin: 0 auto; padding: 1.5rem; }
  .tabs { display: flex; gap: .25rem; flex-wrap: wrap; margin: 1rem 0; }
  .tabs button { padding: .5rem 1rem; border: 1px solid var(--border);
    background: var(--surface); color: var(--text); border-radius: .375rem;
    cursor: pointer; font: inherit; }
  .tabs button[aria-selected="true"] { background: var(--text);
    color: var(--bg); }
  .panel[hidden] { display: none; }
  h1, h2, h3, h4 { line-height: 1.25; }
  h1 { font-size: 1.875rem; margin-top: 0; }
  h2 { font-size: 1.5rem; border-bottom: 1px solid var(--border);
    padding-bottom: .25rem; margin-top: 2rem; }
  h3 { font-size: 1.25rem; margin-top: 1.5rem; }
  p { margin: .75rem 0; }
  code { font-family: ui-monospace, SFMono-Regular, monospace;
    font-size: .875em; background: var(--border); padding: .125rem .375rem;
    border-radius: .25rem; }
  pre { background: var(--surface); border: 1px solid var(--border);
    padding: 1rem; border-radius: .375rem; overflow-x: auto; }
  pre code { background: none; padding: 0; font-size: .875em; }
  table { border-collapse: collapse; width: 100%; margin: 1rem 0; }
  th, td { border: 1px solid var(--border); padding: .5rem .75rem;
    text-align: left; vertical-align: top; }
  th { background: var(--surface); font-weight: 600; }
  blockquote { border-left: 4px solid var(--accent); padding: .25rem 1rem;
    color: var(--muted); margin: 1rem 0; background: var(--surface); }
  blockquote > :first-child { margin-top: 0; }
  blockquote > :last-child { margin-bottom: 0; }
  a { color: var(--accent); }
  hr { border: none; border-top: 1px solid var(--border); margin: 2rem 0; }
  ul, ol { padding-left: 1.5rem; }
  li { margin: .25rem 0; }
  .actionbar { margin: 2rem 0 1rem; display: flex; gap: .5rem; }
  button.copy { padding: .5rem 1rem; border: 1px solid var(--border);
    background: var(--surface); color: var(--text); border-radius: .375rem;
    cursor: pointer; font: inherit; }
  .meta { font-family: ui-monospace, monospace; color: var(--muted);
    font-size: .875rem; }
  :focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
  @media (prefers-reduced-motion: reduce) {
    * { transition: none !important; }
  }
"""


_JS = """  document.querySelectorAll('[role="tab"]').forEach((tab, i) => {
    tab.onclick = () => {
      document.querySelectorAll('[role="tab"]').forEach(t =>
        t.setAttribute('aria-selected', t === tab ? 'true' : 'false'));
      document.querySelectorAll('.panel').forEach((p, j) =>
        p.hidden = i !== j);
    };
  });
  function copyMarkdown() {
    const md = document.getElementById('md-source').textContent.trim();
    navigator.clipboard.writeText(md).then(() => {
      const b = document.querySelector('button.copy');
      const original = b.textContent;
      b.textContent = 'Copied ✓';
      setTimeout(() => b.textContent = original, 1500);
    });
  }
"""


@dataclass
class Section:
    """A single spec section, derived from one markdown file."""

    filename: str
    label: str
    markdown: str
    html: str


_INDEX_PREFIX = re.compile(r"^(\d+)[-_]?(.*)$")


def _derive_label(stem: str, markdown: str) -> str:
    """Tab label: prefer first H1 in the file; fall back to stripped filename."""
    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
        if stripped:
            break
    m = _INDEX_PREFIX.match(stem)
    if m:
        cleaned = m.group(2).replace("-", " ").replace("_", " ").strip()
        return cleaned.title() if cleaned else stem
    return stem.replace("-", " ").replace("_", " ").title()


def _is_section_file(path: pathlib.Path) -> bool:
    if path.suffix.lower() != ".md":
        return False
    if path.name.lower() in {"readme.md", "index.md"}:
        return False
    return True


def collect_sections(input_dir: pathlib.Path) -> List[Section]:
    files = sorted(p for p in input_dir.iterdir() if _is_section_file(p))
    sections: List[Section] = []
    for path in files:
        md = path.read_text(encoding="utf-8")
        sections.append(
            Section(
                filename=path.name,
                label=_derive_label(path.stem, md),
                markdown=md,
                html=md_to_html(md),
            )
        )
    return sections


def _derive_title(
    input_dir: pathlib.Path,
    sections: List[Section],
    override: str | None,
) -> str:
    if override:
        return override
    readme = input_dir / "README.md"
    if readme.is_file():
        for line in readme.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("# "):
                return stripped[2:].strip()
    if sections:
        return sections[0].label
    return input_dir.name


def render_document(
    title: str,
    sections: List[Section],
    timestamp: str,
) -> str:
    if not sections:
        raise ValueError("No section files to render.")

    tab_buttons: List[str] = []
    panels: List[str] = []
    for idx, sec in enumerate(sections):
        selected = "true" if idx == 0 else "false"
        tab_buttons.append(
            f'    <button role="tab" aria-selected="{selected}">'
            f"{html.escape(sec.label)}</button>"
        )
        hidden = "" if idx == 0 else " hidden"
        panels.append(
            f'  <section class="panel" role="tabpanel" '
            f'aria-label="{html.escape(sec.label)}"{hidden}>\n'
            f"{sec.html}\n"
            f"  </section>"
        )

    embedded_md_parts: List[str] = []
    for sec in sections:
        embedded_md_parts.append(
            f"<!-- {sec.filename} -->\n{sec.markdown.strip()}\n"
        )
    embedded_md = "\n".join(embedded_md_parts)
    # The browser would treat </script> inside our text/markdown block as the
    # end of the script tag. Defuse it; the Copy-as-Markdown button reads via
    # textContent, which will see the raw character sequence either way.
    embedded_md = embedded_md.replace("</script>", "<\\/script>")

    return (
        "<!DOCTYPE html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{html.escape(title)}</title>\n"
        f"<style>\n{_CSS}</style>\n"
        "</head>\n"
        "<body>\n"
        "<header>\n"
        f"  <strong>{html.escape(title)}</strong>\n"
        f'  <div class="meta">{html.escape(timestamp)} · '
        "generated by spec-to-html.py</div>\n"
        "</header>\n"
        "<main>\n"
        '  <nav class="tabs" role="tablist">\n'
        + "\n".join(tab_buttons)
        + "\n  </nav>\n\n"
        + "\n\n".join(panels)
        + "\n\n"
        '  <div class="actionbar">\n'
        '    <button class="copy" onclick="copyMarkdown()">'
        "Copy as Markdown</button>\n"
        "  </div>\n"
        "</main>\n\n"
        '<script type="text/markdown" id="md-source">\n'
        + embedded_md
        + "\n</script>\n"
        f"<script>\n{_JS}</script>\n"
        "</body>\n"
        "</html>\n"
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _default_output() -> pathlib.Path:
    today = _dt.date.today().isoformat()
    return pathlib.Path("claudedocs") / f"spec-export-{today}.html"


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Convert docs/specification/*.md into a single self-contained "
            "HTML for non-developer sharing."
        ),
    )
    parser.add_argument(
        "--input",
        type=pathlib.Path,
        default=pathlib.Path("docs/specification"),
        help="Input directory containing the markdown spec sections "
        "(default: docs/specification).",
    )
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=None,
        help="Output HTML path (default: claudedocs/spec-export-YYYY-MM-DD.html).",
    )
    parser.add_argument(
        "--title",
        type=str,
        default=None,
        help="Document title. Defaults to the README.md H1 or the first section's H1.",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Write to stdout instead of a file. Useful for piping or inspection.",
    )
    return parser.parse_args(argv)


def main(argv: List[str]) -> int:
    args = parse_args(argv)

    if not args.input.is_dir():
        print(f"error: input directory not found: {args.input}", file=sys.stderr)
        return 1

    sections = collect_sections(args.input)
    if not sections:
        print(
            f"error: no markdown section files found in {args.input} "
            "(README.md and index.md are excluded by design)",
            file=sys.stderr,
        )
        return 1

    title = _derive_title(args.input, sections, args.title)
    timestamp = _dt.datetime.now().strftime("%Y-%m-%d %H:%M %Z").strip()
    document = render_document(title, sections, timestamp)

    if args.stdout:
        sys.stdout.write(document)
        return 0

    output = args.output or _default_output()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(document, encoding="utf-8")
    print(
        f"✅ Spec exported: {output}\n"
        f"  Sections: {len(sections)} "
        f"({', '.join(s.filename for s in sections)})\n"
        f"  Title: {title}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
