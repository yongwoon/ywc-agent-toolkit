#!/usr/bin/env python3
"""Unit tests for extract-nitpick-comments.py.

Run directly: `python3 test_extract_nitpick_comments.py`
Exit 0 = pass. Stdlib `unittest` only, no `pytest`.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT_DIR = Path(__file__).resolve().parent
SCRIPT_PATH = SCRIPT_DIR / "extract-nitpick-comments.py"
FIXTURE_PATH = SCRIPT_DIR / "fixtures" / "nitpick-review-body.html"


def _load_module():
    spec = importlib.util.spec_from_file_location("extract_nitpick_comments", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


enc = _load_module()


class ExtractNitpickCommentsTests(unittest.TestCase):
    def test_ac1_well_formed_body_extracts_all_items(self) -> None:
        body = """
<details>
<summary>🧹 Nitpick comments (2)</summary><blockquote>
<details>
<summary>src/example/a.ts (2)</summary><blockquote>

`10-15`: **첫 번째 제목입니다.**

첫 번째 본문입니다.

<!-- cr-comment:v1:abc0001 -->

---

`20`: **두 번째 제목입니다.**

두 번째 본문입니다.

<!-- cr-comment:v1:abc0002 -->

</blockquote></details>
</blockquote>
</details>
"""
        items = enc.extract(body)
        self.assertEqual(len(items), 2)
        for item in items:
            self.assertEqual(item["parse_status"], "ok")
            for field in ("hash", "path", "line_start", "line_end", "title", "body"):
                self.assertNotIn(item[field], (None, ""), field)
        self.assertEqual(items[0]["line_start"], 10)
        self.assertEqual(items[0]["line_end"], 15)
        self.assertEqual(items[1]["line_start"], 20)
        self.assertEqual(items[1]["line_end"], 20)
        self.assertEqual(len(items), 2)

    def test_ac2_no_nitpick_section_returns_empty_array(self) -> None:
        body = "<p>LGTM, no issues found.</p>"
        self.assertEqual(enc.extract(body), [])

    def test_ac2_zero_count_nitpick_section_returns_empty_array(self) -> None:
        body = "<details><summary>🧹 Nitpick comments (0)</summary></details>"
        self.assertEqual(enc.extract(body), [])

    def test_ac5_malformed_block_falls_back_not_dropped(self) -> None:
        body = """
<details>
<summary>🧹 Nitpick comments (1)</summary><blockquote>
<details>
<summary>src/example/b.ts (1)</summary><blockquote>

이 블록에는 줄 범위 prefix와 cr-comment 마커가 없습니다.

</blockquote></details>
</blockquote>
</details>
"""
        items = enc.extract(body)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["parse_status"], "raw_fallback")
        self.assertIn("줄 범위", items[0]["body"])
        self.assertEqual(items[0]["line_start"], None)
        self.assertEqual(items[0]["line_end"], None)

    def test_ac5_unclosed_details_tag_falls_back_not_dropped(self) -> None:
        # Truncated input: the per-file <details> block never closes and
        # carries no cr-comment marker (AC5's explicit "unclosed tags" case).
        body = """
<details>
<summary>🧹 Nitpick comments (1)</summary><blockquote>
<details>
<summary>src/example/f.ts (1)</summary><blockquote>

`7`: **누락된 close tag를 테스트합니다.**

이 블록은 의도적으로 닫는 태그 없이 끝납니다."""
        items = enc.extract(body)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["parse_status"], "raw_fallback")
        self.assertEqual(items[0]["path"], "src/example/f.ts")
        self.assertIn("닫는 태그", items[0]["body"])

    def test_malformed_file_summary_still_captures_content(self) -> None:
        # Per-file <summary> text that doesn't match "<path> (<count>)" must
        # still open a block -- a well-formed item inside it is not dropped.
        body = """
<details>
<summary>🧹 Nitpick comments (1)</summary><blockquote>
<details>
<summary>broken summary without a count</summary><blockquote>

`1`: **A**

body a

<!-- cr-comment:v1:aaa -->

</blockquote></details>
</blockquote>
</details>
"""
        items = enc.extract(body)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["parse_status"], "ok")
        self.assertEqual(items[0]["path"], "broken summary without a count")

    def test_sanitize_for_log_strips_crlf_and_truncates(self) -> None:
        dirty = "a" * 300 + "\r\nWARNING: injected fake log line"
        safe = enc._sanitize_for_log(dirty)
        self.assertNotIn("\n", safe)
        self.assertNotIn("\r", safe)
        self.assertLessEqual(len(safe), enc.MAX_LOG_FIELD_LEN + len("...(truncated)"))

    def test_warning_lines_never_contain_raw_crlf_from_untrusted_path(self) -> None:
        body = """
<details>
<summary>🧹 Nitpick comments (1)</summary><blockquote>
<details>
<summary>evil\r\npath (1)</summary><blockquote>

no line-range prefix here at all

</blockquote></details>
</blockquote>
</details>
"""
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            items = enc.extract(body)
        self.assertEqual(len(items), 1)
        for line in stderr.getvalue().splitlines():
            self.assertTrue(line == "" or line.startswith("WARNING:"))

    def test_parser_exception_degrades_to_fallback_not_exit_1(self) -> None:
        with patch.object(enc._NitpickParser, "feed", side_effect=RuntimeError("boom")):
            items = enc.extract("<details><summary>🧹 Nitpick comments (1)</summary></details>")
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["parse_status"], "raw_fallback")

    def test_edge_case_reported_count_mismatch_warns_not_fails(self) -> None:
        body = """
<details>
<summary>🧹 Nitpick comments (5)</summary><blockquote>
<details>
<summary>src/example/e.ts (1)</summary><blockquote>

`1`: **A**

body a

<!-- cr-comment:v1:aaa -->

</blockquote></details>
</blockquote>
</details>
"""
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            items = enc.extract(body)
        self.assertEqual(len(items), 1)
        self.assertIn("summary reported 5 Nitpick item(s), parsed 1", stderr.getvalue())

    def test_edge_case_empty_stdin_returns_empty_array(self) -> None:
        self.assertEqual(enc.extract(""), [])

    def test_raw_fallback_hash_is_empty_when_no_marker(self) -> None:
        # Amendment B: raw_fallback items with no cr-comment marker must carry
        # hash: "" so they are never eligible for marker-based dedup/exclusion.
        body = """
<details>
<summary>🧹 Nitpick comments (1)</summary><blockquote>
<details>
<summary>src/example/b.ts (1)</summary><blockquote>

이 블록에는 줄 범위 prefix와 cr-comment 마커가 없습니다.

</blockquote></details>
</blockquote>
</details>
"""
        items = enc.extract(body)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["hash"], "")

    def test_marker_present_but_no_line_range_falls_back_with_hash(self) -> None:
        # A marker exists but the leading `N`/`N-M` line-range prefix is
        # missing -- raw_fallback, but the marker's hash must be preserved
        # (not emptied), distinguishing this from the no-marker-at-all case.
        body = """
<details>
<summary>🧹 Nitpick comments (1)</summary><blockquote>
<details>
<summary>src/example/g.ts (1)</summary><blockquote>

**제목만 있고 줄 범위가 없습니다.**

본문입니다.

<!-- cr-comment:v1:deadbeef -->

</blockquote></details>
</blockquote>
</details>
"""
        items = enc.extract(body)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["parse_status"], "raw_fallback")
        self.assertEqual(items[0]["hash"], "deadbeef")
        self.assertEqual(items[0]["line_start"], None)
        self.assertEqual(items[0]["line_end"], None)

    def test_marker_and_line_range_present_but_no_title_falls_back_with_hash(self) -> None:
        # Marker + line-range prefix both present, but no leading **title**
        # bold span -- raw_fallback, marker's hash must be preserved.
        body = """
<details>
<summary>🧹 Nitpick comments (1)</summary><blockquote>
<details>
<summary>src/example/h.ts (1)</summary><blockquote>

`3`: 제목이 굵게 표시되지 않았습니다.

<!-- cr-comment:v1:cafef00d -->

</blockquote></details>
</blockquote>
</details>
"""
        items = enc.extract(body)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["parse_status"], "raw_fallback")
        self.assertEqual(items[0]["hash"], "cafef00d")

    def test_trailing_content_after_final_marker_recovered_not_dropped(self) -> None:
        # AC5: content appearing after the last cr-comment marker in a file
        # block must never be silently dropped -- it surfaces as a trailing
        # raw_fallback item.
        body = """
<details>
<summary>🧹 Nitpick comments (1)</summary><blockquote>
<details>
<summary>src/example/i.ts (1)</summary><blockquote>

`1`: **정상 항목입니다.**

본문입니다.

<!-- cr-comment:v1:aaa111 -->

마지막 마커 뒤에 남은 트레일링 콘텐츠입니다.

</blockquote></details>
</blockquote>
</details>
"""
        items = enc.extract(body)
        self.assertEqual(len(items), 2)
        ok_items = [item for item in items if item["parse_status"] == "ok"]
        fallback_items = [item for item in items if item["parse_status"] == "raw_fallback"]
        self.assertEqual(len(ok_items), 1)
        self.assertEqual(len(fallback_items), 1)
        self.assertIn("트레일링", fallback_items[0]["body"])
        self.assertEqual(fallback_items[0]["hash"], "")

    def test_edge_case_multiple_items_same_file_not_merged(self) -> None:
        body = """
<details>
<summary>🧹 Nitpick comments (2)</summary><blockquote>
<details>
<summary>src/example/c.ts (2)</summary><blockquote>

`1`: **A**

body a

<!-- cr-comment:v1:aaa -->

---

`2`: **B**

body b

<!-- cr-comment:v1:bbb -->

</blockquote></details>
</blockquote>
</details>
"""
        items = enc.extract(body)
        self.assertEqual(len(items), 2)
        hashes = {item["hash"] for item in items}
        self.assertEqual(hashes, {"aaa", "bbb"})
        line_starts = {item["line_start"] for item in items}
        self.assertEqual(line_starts, {1, 2})

    def test_edge_case_unicode_roundtrips(self) -> None:
        body = """
<details>
<summary>🧹 Nitpick comments (1)</summary><blockquote>
<details>
<summary>src/example/d.ts (1)</summary><blockquote>

`3`: **한국어 제목 테스트입니다.**

日本語のテキストも含む本文です。

<!-- cr-comment:v1:abcdef123456 -->

</blockquote></details>
</blockquote>
</details>
"""
        items = enc.extract(body)
        self.assertEqual(len(items), 1)
        self.assertIn("한국어", items[0]["title"])
        self.assertIn("日本語", items[0]["body"])
        dumped = json.dumps(items, ensure_ascii=False)
        reloaded = json.loads(dumped)
        self.assertEqual(reloaded[0]["title"], items[0]["title"])

    def test_fixture_file_parses_into_expected_shape(self) -> None:
        body = FIXTURE_PATH.read_text(encoding="utf-8")
        items = enc.extract(body)
        self.assertEqual(len(items), 4)
        paths: dict[str, int] = {}
        for item in items:
            paths[item["path"]] = paths.get(item["path"], 0) + 1
        self.assertGreaterEqual(len(paths), 2)
        self.assertTrue(any(count >= 2 for count in paths.values()))
        self.assertTrue(any(item["parse_status"] == "raw_fallback" for item in items))
        ok_items = [item for item in items if item["parse_status"] == "ok"]
        fallback_items = [item for item in items if item["parse_status"] == "raw_fallback"]
        self.assertEqual(len(ok_items), 3)
        for item in ok_items:
            for field in ("hash", "path", "line_start", "line_end", "title", "body"):
                self.assertNotIn(item[field], (None, ""), field)
        for item in fallback_items:
            self.assertEqual(item["hash"], "")

    def test_cli_empty_stdin_exits_zero_with_empty_array(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(SCRIPT_PATH)],
            input="",
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(json.loads(proc.stdout), [])

    def test_cli_fixture_via_stdin_exits_zero_with_valid_json(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(SCRIPT_PATH)],
            input=FIXTURE_PATH.read_text(encoding="utf-8"),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0)
        items = json.loads(proc.stdout)
        self.assertEqual(len(items), 4)


if __name__ == "__main__":
    unittest.main()
