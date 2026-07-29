---
name: markdown-to-pdf
description: Converts a markdown file (or markdown content described in conversation) into a styled PDF, rendering any Mermaid diagrams inline. Use whenever the user asks to "write this to a PDF," "export this markdown as a PDF," "convert this doc to PDF," or asks for a PDF version of a report/explainer/plan that currently exists as markdown.
allowed-tools: Read, Write, Bash
---

# Markdown to PDF

Converts a markdown document into a real PDF via `pandoc` (markdown → HTML) and headless Chrome (HTML → PDF), with Mermaid diagrams rendered live by mermaid.js inside the printed page — no separate image-extraction step needed.

## When to use this

- User asks to turn an existing `.md` file into a PDF
- User asks for a PDF of a report/explainer/plan that was just written in the conversation
- User describes content directly and asks for a PDF (write the markdown to a temp file first, then run the pipeline)

## Prerequisites

Check these once per session:

```bash
which pandoc            # brew install pandoc
which "Google Chrome" 2>/dev/null || ls "/Applications/Google Chrome.app" 2>/dev/null
```

If `pandoc` is missing, ask before installing (`brew install pandoc` on macOS) — don't install silently. Headless Chrome/Chromium is required for the HTML→PDF step and for Mermaid rendering; the script checks common install locations and `PATH` automatically.

## Procedure

1. **Get the markdown source.** If given a file path, use it directly. If given content in conversation, write it to a temp `.md` file first.

2. **Run the build script**:

   ```bash
   python3 ~/.claude/skills/markdown-to-pdf/scripts/build_pdf.py \
     --md <source>.md \
     --out <output>.pdf
   ```

   Default the output path to the same directory as the source markdown, same base filename with a `.pdf` extension, unless the user specifies otherwise.

3. **If the doc contains Mermaid diagrams** (` ```mermaid ` code blocks), no extra step is needed — the script unwraps them from pandoc's HTML output and lets mermaid.js (loaded from a CDN) render them live inside the same page that gets printed to PDF. This requires network access to `cdn.jsdelivr.net`; if that's unavailable, diagrams will render as empty boxes or raw text — tell the user network access is required for diagrams.

4. **Verify the result** by rasterizing a page or two rather than assuming success:

   ```bash
   python3 -c "
   import fitz
   doc = fitz.open('<output>.pdf')
   print('pages:', doc.page_count)
   doc[0].get_pixmap(dpi=100).save('/tmp/_verify_p1.png')
   "
   ```

   Read the resulting PNG back to confirm the page rendered as expected (margins sane, no leftover browser chrome, diagrams present) before telling the user it's done. `PyMuPDF` (`import fitz`) must be installed for this (`pip3 install --user pymupdf`); skip verification if unavailable rather than blocking on it.

5. **Clean up** any temp markdown file you created in step 1. The script cleans up its own intermediate HTML automatically (unless `--keep-html` is passed for debugging).

## Why this works the way it does

Headless Chrome's `--print-to-pdf` normally adds a browser-style header/footer (timestamp, file URL, page number) to every page, and `--print-to-pdf-no-header` alone does **not** reliably suppress it. The actual trigger is the page's `@page` CSS margin: Chrome only injects its own header/footer when the effective top/bottom margin is **greater than ~8mm**. `scripts/build_pdf.py` works around this by setting `@page { margin: 8mm; }` (right at the threshold) and simulating normal document margins with `body { padding: 12mm 15mm; }` instead. This was verified empirically (8mm clean, 9mm+ brings the header/footer back) — don't "fix" this by increasing the `@page` margin thinking it looks cramped; adjust the `body` padding instead.

## Styling

`scripts/build_pdf.py` embeds a fixed CSS block (navy `#1B2A4A` headings with a teal `#2E86AB` accent, striped tables, monospace code blocks, styled Mermaid containers). This is not exposed as a command-line option — if the user wants different colors or fonts, edit the `CSS` constant near the top of the script directly.

## Files

- `scripts/build_pdf.py` — the full pipeline: pandoc markdown→HTML, unwrap Mermaid code blocks, assemble a styled HTML document with mermaid.js, headless Chrome print-to-pdf

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| `pandoc: command not found` | pandoc not installed | `brew install pandoc` (ask first) |
| `no Chrome/Chromium binary found` | No headless-capable browser installed | Install Google Chrome, or note the limitation to the user |
| Mermaid diagrams show as raw text or empty boxes | No network access to `cdn.jsdelivr.net`, or mermaid syntax error | Confirm network access; check the `.md` source's mermaid code blocks for syntax errors |
| Every page has a timestamp/URL/page-number footer | `@page` margin in the CSS exceeds ~8mm | Keep `@page` margin ≤8mm in `build_pdf.py`'s `CSS` constant; use `body` padding for visual margin instead |
| PDF renders but layout looks cramped/wide | `max-width`/`padding` in `CSS` too tight or too loose for the content | Adjust `body { max-width; padding }` in `build_pdf.py`'s `CSS` constant |
