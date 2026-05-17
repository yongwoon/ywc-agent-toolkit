# HTML Output Format for Claude Code Skills

> Shared reference document. Linked from any `ywc-*` skill that produces a
> human-facing review report, testsheet, or research artifact and supports the
> `--format html` flag.

## 1. Purpose

A Markdown file longer than ~100 lines is rarely read end to end — the reader
scrolls, skims, and closes it. Skill output that nobody reads cannot drive a
decision. This document defines a single, consistent HTML output mode that
`ywc-*` skills can opt into so that the human on the other end actually reads
the report and acts on it.

HTML earns this over Markdown on five axes:

- **Information density** — color, severity badges, SVG diagrams, and layout
  that Markdown cannot express.
- **Visual clarity** — tabs, collapsible sections, and a fixed summary header
  keep a long report scannable instead of a wall of text.
- **Shareability** — a self-contained `.html` file opens directly in any
  browser and can be handed to a teammate as a single attachment or an S3 link.
- **Interaction** — checkboxes, sign-off state, and copy buttons turn a static
  report into something the reader operates.
- **Markdown preservation** — the HTML file carries its own Markdown source
  inside it (see §6), so the machine surface is never lost.

### When to emit HTML

HTML mode is **opt-in** via `--format html`. The default stays `markdown`
because HTML costs 2–4× the output tokens and is opt-in precisely so the user
controls that cost. Emit HTML when the output is a **human-facing,
decision-making artifact read once** — a review report, a testsheet, a research
comparison, a postmortem.

### When not to emit HTML

Never emit HTML for **version-controlled canonical documents** — specifications
under `docs/specification/`, task directories under `tasks/`, changelogs,
ubiquitous-language glossaries, project docs. Those files are diffed, grepped,
and consumed by downstream skills; HTML would add diff noise and break tooling.
Those skills do not expose `--format` at all.

## 2. The Single-File Rule

The output must be **one self-contained `.html` file**. No external CSS, no CDN
`<link>` or `<script src>`, no separate image files. Everything — styles,
scripts, and any SVG — lives inline.

The reason is the shareability axis: a self-contained file opens offline, can be
uploaded to S3 and shared as a bare link, or attached to a message without a
broken-asset trail. A file with external dependencies breaks the moment it
leaves the machine that made it.

SVG diagrams are inlined as `<svg>` elements. Raster screenshots (e.g. from
`ywc-ui-ux-review`'s live exploration) are embedded as `data:` URIs.

## 3. Severity Color Tokens

Review skills share a five-level severity vocabulary. HTML mode maps each tier
to one CSS custom property so that a finding tagged Critical looks identical
across `ywc-impl-review`, `ywc-security-audit`, `ywc-spec-validate`, and
`ywc-product-review`.

| Tier | Symbol | CSS token | Color (oklch) |
| --- | --- | --- | --- |
| Critical | 🚨 | `--sev-critical` | `oklch(58% 0.22 25)` — red |
| High | 🔴 | `--sev-high` | `oklch(68% 0.19 45)` — orange |
| Medium | 🟡 | `--sev-medium` | `oklch(80% 0.16 90)` — amber |
| Low | 🔵 | `--sev-low` | `oklch(65% 0.14 240)` — blue |
| Info | ℹ️ | `--sev-info` | `oklch(70% 0.02 260)` — slate |

The symbol is kept *inside* each finding card as well — the color is the scan
layer, the symbol is the plain-text fallback that survives a copy-to-Markdown.
Do not invent new tiers or colors; the five-level scale is the single source of
truth.

## 4. Document Structure

Every HTML report uses the same four-region structure so a reader who has seen
one `ywc-*` HTML report can navigate any other one:

1. **Summary header** — fixed at the top: skill name, target, timestamp, and a
   one-line verdict (gate band, completion status, or finding counts).
2. **Tab navigation** — one tab per top-level section. For review skills the
   tabs are the review axes (e.g. Spec / Security / QA); for `ywc-product-review`
   the five perspectives; for a single-section report a tab strip is optional.
3. **Finding cards** — within each tab, one card per finding, left-bordered with
   the severity color token and carrying the severity symbol, location anchor,
   description, and recommended action.
4. **Action bar** — a `Copy as Markdown` button (§6) and, where the skill
   defines them, skill-specific controls (e.g. testsheet checkboxes).

Long supporting content (prerequisites, full evidence, raw logs) goes inside
`<details>` elements so the default view stays scannable.

## 5. HTML Skeleton

Generate the file from this skeleton. It is intentionally compact and
dependency-free — fill the regions, do not restructure them. Keep the inline
`<style>` and `<script>` as written; they encode the severity tokens (§3),
accessibility rules (§7), and the copy mechanism (§6).

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><!-- SKILL — TARGET --></title>
<style>
  :root {
    --bg: oklch(98% 0 0); --surface: oklch(100% 0 0); --text: oklch(22% 0 0);
    --muted: oklch(55% 0 0); --border: oklch(90% 0 0);
    --sev-critical: oklch(58% 0.22 25); --sev-high: oklch(68% 0.19 45);
    --sev-medium: oklch(80% 0.16 90); --sev-low: oklch(65% 0.14 240);
    --sev-info: oklch(70% 0.02 260);
  }
  @media (prefers-color-scheme: dark) {
    :root { --bg: oklch(20% 0 0); --surface: oklch(25% 0 0);
      --text: oklch(92% 0 0); --muted: oklch(65% 0 0); --border: oklch(35% 0 0); }
  }
  * { box-sizing: border-box; }
  body { margin: 0; font: 16px/1.6 -apple-system, system-ui, sans-serif;
    background: var(--bg); color: var(--text); }
  header { position: sticky; top: 0; background: var(--surface);
    border-bottom: 1px solid var(--border); padding: 1rem 1.5rem; z-index: 10; }
  main { max-width: 60rem; margin: 0 auto; padding: 1.5rem; }
  .tabs { display: flex; gap: .25rem; flex-wrap: wrap; margin: 1rem 0; }
  .tabs button { padding: .5rem 1rem; border: 1px solid var(--border);
    background: var(--surface); color: var(--text); border-radius: .375rem;
    cursor: pointer; }
  .tabs button[aria-selected="true"] { background: var(--text);
    color: var(--bg); }
  .panel[hidden] { display: none; }
  .finding { background: var(--surface); border: 1px solid var(--border);
    border-left: 4px solid var(--sev-info); border-radius: .375rem;
    padding: .75rem 1rem; margin: .75rem 0; }
  .finding.critical { border-left-color: var(--sev-critical); }
  .finding.high { border-left-color: var(--sev-high); }
  .finding.medium { border-left-color: var(--sev-medium); }
  .finding.low { border-left-color: var(--sev-low); }
  .loc { font-family: ui-monospace, monospace; color: var(--muted);
    font-size: .875rem; }
  .actionbar { margin: 1.5rem 0; }
  button.copy { padding: .5rem 1rem; border: 1px solid var(--border);
    background: var(--surface); color: var(--text); border-radius: .375rem;
    cursor: pointer; }
  :focus-visible { outline: 2px solid var(--sev-low); outline-offset: 2px; }
  @media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
</style>
</head>
<body>
<header>
  <strong><!-- Skill name --></strong> — <!-- target -->
  <div class="loc"><!-- timestamp · one-line verdict --></div>
</header>
<main>
  <nav class="tabs" role="tablist"><!-- one <button role="tab"> per section --></nav>

  <section class="panel" role="tabpanel"><!-- finding cards for this section -->
    <article class="finding critical">
      <strong>🚨 Critical</strong>
      <span class="loc">path/to/file.ts:42</span>
      <p><!-- description --></p>
      <p><em>Action:</em> <!-- recommended fix --></p>
    </article>
  </section>

  <div class="actionbar">
    <button class="copy" onclick="copyMarkdown()">Copy as Markdown</button>
  </div>
</main>

<!-- Markdown surface: rendered by no browser, copied by the button. -->
<script type="text/markdown" id="md-source">
<!-- The complete Markdown report goes here verbatim. -->
</script>
<script>
  // Tab switching
  document.querySelectorAll('[role="tab"]').forEach((tab, i) => {
    tab.onclick = () => {
      document.querySelectorAll('[role="tab"]').forEach(t =>
        t.setAttribute('aria-selected', t === tab));
      document.querySelectorAll('.panel').forEach((p, j) =>
        p.hidden = i !== j);
    };
  });
  // Copy the embedded Markdown surface to the clipboard
  function copyMarkdown() {
    const md = document.getElementById('md-source').textContent.trim();
    navigator.clipboard.writeText(md).then(() => {
      const b = document.querySelector('button.copy');
      b.textContent = 'Copied ✓';
      setTimeout(() => b.textContent = 'Copy as Markdown', 1500);
    });
  }
</script>
</body>
</html>
```

## 6. Markdown Preservation

HTML is the **human view**; Markdown is the **machine surface** that downstream
skills, Git, and tooling depend on. HTML mode must never destroy the Markdown
surface — it carries it.

The skeleton embeds the complete Markdown report inside a
`<script type="text/markdown" id="md-source">` block. Browsers do not render an
unknown script type, so the Markdown is invisible on screen but present in the
file. The `Copy as Markdown` button copies that block to the clipboard verbatim.

This is why HTML mode produces **one file, not two**: the `.html` file *is* the
carrier of its own Markdown. When the user needs the Markdown — to paste into a
PR, commit a report, or feed another skill — they click the button. No separate
`.md` file is written, so there is no second artifact to keep in sync and no
diff noise.

The embedded Markdown must be the exact report the skill would have produced in
`--format markdown` mode. Generate the Markdown report first, then wrap it in
the HTML — never let the two drift.

**Exception — interactive testsheets (`ywc-gen-testcase`):** The embedded
Markdown is the original testsheet template (identical to `--format markdown`
output). The `Copy as Markdown` button assembles the *current* state on the
fly — original content with sign-off front-matter (tester name, per-scenario
Pass/Fail/Blocked, notes) drawn from `localStorage` — so the exported Markdown
reflects the reviewer's completed work, not the blank template. This is the
only case where the exported surface diverges from the embedded template.

## 7. Accessibility

The report is for a human; an inaccessible report fails its one job. The
skeleton already encodes the baseline — keep it intact:

- **Semantic structure** — `<header>`, `<main>`, `<nav>`, `<section>`,
  `<article>`. Tabs use `role="tablist"` / `role="tab"` / `role="tabpanel"`.
- **Keyboard operable** — every control is a real `<button>`; `:focus-visible`
  styling is defined.
- **Contrast** — the oklch tokens hold a legible contrast ratio in both light
  and dark mode (`prefers-color-scheme` is handled).
- **Reduced motion** — `prefers-reduced-motion` disables transitions.

## 8. File Naming and Location

Write the file to `claudedocs/<skill>-<YYYY-MM-DD>.html`, matching the existing
convention in `ywc-ui-ux-review`. If a file with that name already exists,
append `-v<N>` rather than overwriting — a prior report may already have been
shared or signed off.

For `ywc-gen-testcase`, the filename follows that skill's own input-mode naming
table (`pr-<n>-<slug>`, `task-<...>`, etc.) with an `.html` extension instead of
`.md`.

## 9. Skill Integration

A skill adopting HTML mode adds exactly two things — no per-skill HTML logic.

**One `## Arguments` row:**

```markdown
| `--format` | `--format markdown\|html` | `--format html` | Output format. Default `markdown`. With `html`, writes a self-contained HTML report to `claudedocs/`. See [html-output.md](../references/html-output.md). |
```

**One paragraph appended to the skill's existing output section:**

> **HTML mode (`--format html`)** — emits the same findings as a self-contained
> HTML report: severity color coding, tab navigation, and a `Copy as Markdown`
> button. Structure and conventions follow
> [html-output.md](../references/html-output.md). The Markdown surface is
> preserved inside the file, so downstream integration is unaffected.

Skills that already write their output to a file (`ywc-ui-ux-review`,
`ywc-gen-testcase`) change only the extension and the serializer. Skills that
print their report to the chat (`ywc-impl-review`, `ywc-security-audit`,
`ywc-product-review`, `ywc-spec-validate`, `ywc-tech-research`,
`ywc-incident-postmortem`) additionally write the file in HTML mode and report
its path to the user.

## 10. Anti-Patterns

- **External dependencies** — a CDN link, a Google Fonts `<link>`, a separate
  `.css` file. Breaks the single-file rule and the shareability axis.
- **Dropping the Markdown surface** — emitting HTML with an empty or stale
  `md-source` block. The machine surface must always be the exact Markdown
  report.
- **Inventing severity colors** — any color not in the §3 token table. Breaks
  cross-skill visual consistency.
- **HTML for canonical documents** — specs, tasks, changelogs, glossaries. They
  are diffed and grepped; HTML belongs only to human-facing decision artifacts.
- **Decorative HTML** — animations, gradients, or imagery that do not encode
  information. The report's job is to be read and acted on, not admired.
- **HTML as the default** — `--format` must default to `markdown`. HTML's
  2–4× token cost is opt-in.
