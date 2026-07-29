# markdown-to-pdf

A user-level skill that converts a markdown file into a styled PDF, rendering any Mermaid diagrams inline.

## What it does

The pipeline is: `pandoc` converts markdown to an HTML body fragment, Claude's script wraps that in a styled HTML document with mermaid.js loaded from a CDN, and headless Chrome prints the result to PDF. Mermaid diagrams render live inside the same page Chrome prints — there's no separate "render diagram to image, then insert image" step, which keeps the pipeline simple and the diagrams crisp at any zoom level.

## When it triggers

Automatically, whenever you ask to turn a markdown doc into a PDF — "write this to a PDF," "export this as a PDF," "convert this doc to PDF." Works from an existing `.md` file or from content described directly in conversation.

## Usage

```bash
write docs/architecture-explainer.md to a PDF
convert this report to a PDF
export the migration doc as a PDF
```

Output defaults to the same directory as the source markdown, same base filename with a `.pdf` extension, unless you specify otherwise.

## The header/footer fix

Headless Chrome normally stamps every printed page with a browser-style header/footer — a timestamp, the file URL, and a page number. The `--print-to-pdf-no-header` flag does **not** reliably suppress this on its own. What actually controls it is the page's CSS `@page` margin: Chrome only adds its own header/footer once the effective margin exceeds roughly 8mm.

`scripts/build_pdf.py` works around this by setting `@page { margin: 8mm; }` — right at the threshold — and getting normal-looking document margins from `body { padding: 12mm 15mm; }` instead. This was found by testing margin values from 0mm to 10mm directly: 8mm and under stay clean, 9mm and up bring the header/footer back. If you need to adjust visual margins, change the `body` padding, not the `@page` margin.

## Requirements

- `pandoc`: `brew install pandoc`
- Headless-capable Chrome or Chromium. The script checks common install locations (macOS app bundle, `PATH` on Linux) automatically.
- Network access to `cdn.jsdelivr.net`, needed only if the source markdown contains Mermaid diagrams.
- `PyMuPDF` (`pip3 install --user pymupdf`), optional — used only to rasterize a page for visual verification after building, not required for the PDF itself.

Nothing is installed on your behalf — if `pandoc` or Chrome is missing, Claude tells you what to install.

## Styling

Fixed CSS baked into the script: navy headings (`#1B2A4A`) with a teal accent (`#2E86AB`), striped tables, monospace code blocks with light backgrounds, centered Mermaid diagram containers. To change this, edit the `CSS` constant near the top of `scripts/build_pdf.py` — it isn't exposed as a command-line option.

## Files

- `scripts/build_pdf.py` — the full pipeline: pandoc markdown→HTML, unwrap Mermaid code blocks so mermaid.js can render them, assemble the styled HTML document, headless-Chrome print-to-pdf

## Installation

Copy the `markdown-to-pdf` directory into `~/.claude/skills/`:

```bash
cp -r claude-skills/user/markdown-to-pdf ~/.claude/skills/
```
