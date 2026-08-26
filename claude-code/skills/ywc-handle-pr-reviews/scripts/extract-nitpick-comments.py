#!/usr/bin/env python3
"""
extract-nitpick-comments.py

Reads one CodeRabbit review `body` string from stdin (the raw HTML/markdown
value of `.body` from `GET /pulls/{pr}/reviews/{review_id}`). Locates the
`<details><summary>Nitpick comments (N)</summary>` section and emits a JSON
array of pseudo-comment objects to stdout -- one per per-file line-range
block terminated by a `<!-- cr-comment:v1:<hex> -->` marker.

No network calls. This is a pure parsing layer; `fetch-nitpick-comments.sh`
(sibling script) owns fetching reviews over the network and piping bodies
here.

## Output Contract

JSON array to stdout, one object per Nitpick item:

  [{"hash": "9dd61764f7e5cfad48b73fc4", "path": "apps/backend/src/foo.ts",
    "line_start": 134, "line_end": 168, "title": "...", "body": "...",
    "severity": "nitpick", "parse_status": "ok"}, ...]

`parse_status` is `"ok"` for a cleanly parsed item, or `"raw_fallback"` when
the nested structure inside a per-file block does not match the expected
pattern (hash-less block, unclosed tags) -- the verbatim unparsed text is
exposed in `body` rather than silently dropped (AC5). A `raw_fallback` item
may have `hash: ""` and `line_start`/`line_end: null` when those could not be
extracted.

The summary line's item-count hint (`(N)`) is read as a hint only -- the
actual parsed block count is what gets emitted; a mismatch is logged to
stderr as a warning, never treated as an error.

Exit codes:
  0  success (array may be [])
  2  usage error (no stdin / --help)

Usage:
  cat review-body.html | python3 extract-nitpick-comments.py
"""
from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser

NITPICK_SUMMARY_RE = re.compile(r"Nitpick comments\s*\((\d+)\)")
FILE_SUMMARY_RE = re.compile(r"^(?P<path>.+?)\s*\((?P<count>\d+)\)\s*$")
LINE_RANGE_RE = re.compile(r"^\s*`(?P<start>\d+)(?:-(?P<end>\d+))?`:\s*")
TITLE_RE = re.compile(r"^\*\*(?P<title>.+?)\*\*")
HASH_MARKER_RE = re.compile(r"<!--\s*cr-comment:v1:([0-9a-fA-F]+)\s*-->")
COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
TAG_RE = re.compile(r"<[^>]+>")
LEADING_TRAILING_NOISE_RE = re.compile(r"^[\s\-—]+|[\s\-—]+$")
# Structural wrapper markup (e.g. the per-file <blockquote>) precedes the
# first item's line-range prefix; strip it once from the left only -- never
# from the middle/end, where a nested sub-<details> block must stay verbatim.
# No `+` inside the alternatives (each arm matches one unit) to avoid the
# nested-quantifier-with-alternation shape that is normally a ReDoS red flag,
# even though this anchored .sub() usage was not exploitable as written.
LEADING_WRAPPER_RE = re.compile(r"^(?:\s|[\-—]|<[^>]+>)+")
MAX_LOG_FIELD_LEN = 200


def _fallback(path: str | None, text: str, hash_value: str = "") -> dict:
    return {
        "hash": hash_value,
        "path": path or "",
        "line_start": None,
        "line_end": None,
        "title": "",
        "body": text,
        "severity": "nitpick",
        "parse_status": "raw_fallback",
    }


def _sanitize_for_log(text: str) -> str:
    """Make untrusted text safe to interpolate into a stderr WARNING line.

    The review body is untrusted third-party (bot) content; without this,
    an attacker-controlled path/summary string could inject spoofed log
    lines (CR/LF) or flood stderr with an unbounded string.
    """
    text = text.replace("\r", "\\r").replace("\n", "\\n")
    if len(text) > MAX_LOG_FIELD_LEN:
        text = text[:MAX_LOG_FIELD_LEN] + "...(truncated)"
    return text


def _has_meaningful_text(raw: str) -> bool:
    text = COMMENT_RE.sub("", raw)
    text = TAG_RE.sub("", text)
    text = LEADING_TRAILING_NOISE_RE.sub("", text)
    return bool(text.strip())


class _NitpickParser(HTMLParser):
    """Walks <details>/<summary> nesting to find the Nitpick section and
    per-file blocks, then buffers each per-file block's raw inner markup
    (including any nested sub-<details>, e.g. "Prompt for AI Agents") for
    regex-based item splitting on the leaf text -- never on tag structure.
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.items: list[dict] = []
        self.warnings: list[str] = []
        self.reported_count: int | None = None
        self._depth = 0
        self._in_nitpick = False
        self._nitpick_depth: int | None = None
        self._in_summary = False
        self._pending_summary: list[str] | None = None
        self._file_path: str | None = None
        self._file_depth: int | None = None
        self._buffer: list[str] = []

    # -- HTMLParser callbacks --

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag == "details":
            self._depth += 1
            if self._file_depth is not None:
                self._buffer.append(self.get_starttag_text() or f"<{tag}>")
            return
        if self._file_depth is not None:
            self._buffer.append(self.get_starttag_text() or f"<{tag}>")
            return
        if tag == "summary":
            self._in_summary = True
            self._pending_summary = []

    def handle_startendtag(self, tag: str, attrs) -> None:
        if self._file_depth is not None:
            self._buffer.append(self.get_starttag_text() or f"<{tag}/>")

    def handle_endtag(self, tag: str) -> None:
        if tag == "summary" and self._in_summary:
            self._in_summary = False
            text = "".join(self._pending_summary or []).strip()
            self._pending_summary = None
            self._on_summary(text)
            return
        if tag == "details":
            if self._file_depth is not None and self._depth > self._file_depth:
                self._buffer.append("</details>")
                self._depth -= 1
                return
            if self._file_depth is not None and self._depth == self._file_depth:
                self._close_file_block()
                self._depth -= 1
                return
            if self._in_nitpick and self._depth == self._nitpick_depth:
                self._in_nitpick = False
                self._nitpick_depth = None
            self._depth -= 1
            return
        if self._file_depth is not None:
            self._buffer.append(f"</{tag}>")

    def handle_data(self, data: str) -> None:
        if self._in_summary:
            self._pending_summary.append(data)
            return
        if self._file_depth is not None:
            self._buffer.append(data)

    def handle_comment(self, data: str) -> None:
        if self._file_depth is not None:
            self._buffer.append(f"<!--{data}-->")

    # -- structural helpers --

    def _on_summary(self, text: str) -> None:
        if not self._in_nitpick and self._file_depth is None:
            match = NITPICK_SUMMARY_RE.search(text)
            if match:
                self._in_nitpick = True
                self._nitpick_depth = self._depth
                self.reported_count = int(match.group(1))
            return
        if (
            self._in_nitpick
            and self._file_depth is None
            and self._depth == self._nitpick_depth + 1
        ):
            match = FILE_SUMMARY_RE.match(text)
            # A per-file <summary> that doesn't match "<path> (<count>)" still
            # opens a block (using the raw summary text as a best-effort path)
            # rather than silently skipping its content -- AC5 / Reliability
            # NFR require every Nitpick section to resolve to an item or a
            # raw_fallback, never to be dropped.
            self._file_path = match.group("path") if match else text
            self._file_depth = self._depth
            self._buffer = []

    def _close_file_block(self) -> None:
        raw = "".join(self._buffer)
        self._split_items(self._file_path, raw)
        self._file_path = None
        self._file_depth = None
        self._buffer = []

    def flush_unclosed(self) -> None:
        """Recover content from a per-file <details> block still open at EOF.

        Malformed/truncated input (Amendment 5's "untrusted third-party
        content" + AC5's explicit "unclosed tags" example) must never lose
        an already-buffered item -- flush whatever was captured as a
        raw_fallback instead of discarding it silently.
        """
        if self._file_depth is None:
            return
        raw = "".join(self._buffer)
        if _has_meaningful_text(raw):
            self.warnings.append(f"unclosed file block '{_sanitize_for_log(self._file_path or '')}'")
            self.items.append(_fallback(self._file_path, raw.strip()))
        self._file_path = None
        self._file_depth = None
        self._buffer = []

    # -- item splitting (regex on leaf text only, never on tag structure) --

    def _split_items(self, path: str | None, raw: str) -> None:
        safe_path = _sanitize_for_log(path or "")
        markers = list(HASH_MARKER_RE.finditer(raw))
        if not markers:
            if _has_meaningful_text(raw):
                self.warnings.append(f"no cr-comment marker found in file block '{safe_path}'")
                self.items.append(_fallback(path, raw.strip()))
            return
        start = 0
        for marker in markers:
            segment = raw[start:marker.start()]
            self._parse_segment(path, segment, marker.group(1))
            start = marker.end()
        trailing = raw[start:]
        if _has_meaningful_text(trailing):
            self.warnings.append(f"unterminated trailing content in file block '{safe_path}'")
            self.items.append(_fallback(path, trailing.strip()))

    def _parse_segment(self, path: str | None, segment: str, hash_value: str) -> None:
        safe_path = _sanitize_for_log(path or "")
        text = LEADING_WRAPPER_RE.sub("", segment)
        line_match = LINE_RANGE_RE.match(text)
        if not line_match:
            self.warnings.append(
                f"no line-range prefix found for Nitpick item '{hash_value}' in '{safe_path}'"
            )
            self.items.append(_fallback(path, segment.strip(), hash_value))
            return
        rest = text[line_match.end():].strip()
        title_match = TITLE_RE.match(rest)
        if not title_match:
            self.warnings.append(
                f"no bolded title found for Nitpick item '{hash_value}' in '{safe_path}'"
            )
            self.items.append(_fallback(path, segment.strip(), hash_value))
            return
        line_start = int(line_match.group("start"))
        line_end = int(line_match.group("end")) if line_match.group("end") else line_start
        title = title_match.group("title").strip()
        body = rest[title_match.end():].strip()
        self.items.append({
            "hash": hash_value,
            "path": path or "",
            "line_start": line_start,
            "line_end": line_end,
            "title": title,
            "body": body,
            "severity": "nitpick",
            "parse_status": "ok",
        })


def extract(body: str) -> list[dict]:
    parser = _NitpickParser()
    try:
        parser.feed(body)
        parser.close()
        parser.flush_unclosed()
    except Exception as exc:  # noqa: BLE001 -- untrusted input must never exit 1
        print(f"WARNING: parser raised on malformed input: {exc}", file=sys.stderr)
        return [_fallback(None, body)]
    for warning in parser.warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    if parser.reported_count is not None and parser.reported_count != len(parser.items):
        print(
            f"WARNING: summary reported {parser.reported_count} Nitpick item(s), "
            f"parsed {len(parser.items)}",
            file=sys.stderr,
        )
    return parser.items


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print(__doc__, file=sys.stderr)
        return 2
    if sys.stdin.isatty():
        print("usage: extract-nitpick-comments.py < review-body.html", file=sys.stderr)
        return 2
    data = sys.stdin.read()
    items = extract(data)
    print(json.dumps(items, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
