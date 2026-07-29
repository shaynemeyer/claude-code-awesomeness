---
name: pptx-deck
description: Converts a markdown document (slide outline, presentation doc, or any structured markdown with headers/bullets/tables/mermaid diagrams) into a PowerPoint .pptx file. Use whenever the user asks to "make this a PowerPoint," "create a deck," "turn this into slides," "export to pptx," or asks for a presentation file from existing markdown content.
allowed-tools: Read, Write, Bash, Glob
---

# PowerPoint Deck Generator

Converts markdown into a real, editable `.pptx` file — title slide, content slides with bullets/tables/images, mermaid diagrams rendered to PNG and embedded, and speaker notes populated from any "talk track" / narration text in the source.

This skill does the slide-splitting and content judgment itself (via the model), then hands a structured JSON spec to a deterministic Python script for layout. It does not use an LLM-based markdown-to-slide converter — you (the agent) read the markdown and decide the slide boundaries.

## When to use this

- User has a markdown doc (a plan, a report, a written explainer) and asks for a PowerPoint/deck/slides
- User asks to convert a specific `.md` file to `.pptx`
- User describes slide content directly and asks for a deck (no markdown source needed — build the JSON spec directly from the conversation)

## Prerequisites

Check these once per session, not per invocation:

```bash
python3 -c "import pptx" 2>&1          # pip install python-pptx
python3 -c "import PIL" 2>&1           # pip install pillow
```

For decks containing mermaid diagrams, also need headless Chrome/Chromium (checked automatically by `render_mermaid.py` — it looks in common install locations and on `PATH`; if not found it skips that diagram and continues without failing the whole deck).

If `python-pptx` or `Pillow` is missing, install with `pip3 install --user python-pptx pillow` before proceeding (ask the user first if the environment is unusual — e.g. a managed/locked-down Python).

## Procedure

1. **Read the source.** If given a markdown file path, read it in full. If given slide content directly in conversation, skip to step 2 using that content.

2. **Decide slide boundaries.** This is a judgment call, not a mechanical split:
   - Each top-level heading (`#`/`##`) is usually one slide, but split further if a section has too much content for one slide (rule of thumb: more than ~7 bullet lines, or a bullet list plus a table, means split it)
   - Any fenced ` ```mermaid ` code block becomes an **image slide** (see step 3) — do not also dump the raw mermaid text onto a bullets slide
   - Any markdown table becomes a **table slide** (`table` field in the spec) — do not flatten it into bullets
   - Prose paragraphs become bullets — break sentences into concise bullet points rather than pasting full paragraphs; a slide is a prompt for the speaker, not the transcript
   - If the source markdown already has a "talk track" / "speaker notes" / "notes" section per slide (as produced by the presentation-writing workflow used in this environment), that text goes into the slide's `notes` field verbatim — do not shorten it
   - If there is no explicit talk track, leave `notes` empty rather than inventing one

3. **Render any mermaid diagrams to PNG first**, before building the JSON spec, since the spec needs the image file paths:

   ```bash
   # for each mermaid code block, write the raw code to a temp .mmd file, then:
   python3 ~/.claude/skills/pptx-deck/scripts/render_mermaid.py \
     --code-file /tmp/diagram_1.mmd \
     --out /tmp/diagram_1.png
   ```

   - Use a fresh temp file per diagram (`/tmp/diagram_N.mmd`)
   - If this script exits non-zero (no Chrome found, or a mermaid syntax error), do not fail the whole deck — fall back to putting the raw mermaid source as a monospace-style bullet note on that slide, and tell the user at the end which diagram(s) couldn't be rendered
   - `--theme` defaults to `default`; only change it if the user asks for a dark deck

4. **Write the JSON spec** to a temp file (e.g. `/tmp/deck_spec.json`), following this schema exactly:

   ```json
   {
     "title": "Deck title",
     "subtitle": "Optional one-line subtitle for the title slide",
     "slides": [
       {
         "title": "Slide title",
         "subtitle": "Optional slide subtitle",
         "bullets": [
           {"level": 0, "text": "Top-level point"},
           {"level": 1, "text": "Sub-point, indented"}
         ],
         "notes": "Full speaker notes / talk track for this slide"
       },
       {
         "title": "A table slide",
         "table": {
           "headers": ["Col A", "Col B"],
           "rows": [["a1", "b1"], ["a2", "b2"]],
           "col_widths": [1, 2]
         }
       },
       {
         "title": "A diagram slide",
         "image": "/tmp/diagram_1.png",
         "notes": "Talk track explaining the diagram"
       }
     ]
   }
   ```

   Rules:
   - Each slide object should use **at most one** of `bullets` / `table` / `image` — the layout script doesn't attempt to combine them on one slide. If a section genuinely needs two of these, split it into two slides.
   - `bullets[].level` is `0` for top-level, `1`+ for indented — mirror the nesting in the source markdown
   - Keep bullet text concise (under ~20 words per bullet); this is a slide, not a paragraph
   - `notes` should be the full talk-track text if the source provides one — do not truncate it for the notes field, only for the on-slide bullets

5. **Build the deck**:

   ```bash
   python3 ~/.claude/skills/pptx-deck/scripts/build_deck.py \
     --spec /tmp/deck_spec.json \
     --out <output-path>.pptx
   ```

   Default the output path to the same directory as the source markdown, same base filename with `.pptx` extension, unless the user specifies otherwise.

6. **Verify structurally** (optional but recommended for anything non-trivial): read the pptx back with `python-pptx` and print each slide's shape count / table presence / picture presence, to confirm nothing silently dropped. Do not attempt pixel-level visual verification unless LibreOffice (`soffice`) or Keynote is available on the machine — check with `which soffice` first; skip this if absent rather than trying to install it.

7. **Clean up temp files** (`/tmp/diagram_*.mmd`, `/tmp/diagram_*.png` if embedded, `/tmp/deck_spec.json`) once the `.pptx` is confirmed written — but only after confirming the pptx opens/parses correctly, since the PNGs are embedded by reference at build time, not copied in afterward.

## Design defaults

The layout script (`scripts/build_deck.py`) uses a fixed, professional look — 16:9 widescreen, navy titles (`#1B2A4A`) with a teal accent underline (`#2E86AB`), striped tables. This isn't configurable via the JSON spec; if the user wants a different visual style (company brand colors, a specific template), edit the color constants at the top of `build_deck.py` directly rather than adding spec-level styling options — keep the spec schema focused on content, not presentation styling.

## Files

- `scripts/render_mermaid.py` — renders one mermaid diagram to a cropped PNG via headless Chrome + mermaid.js (CDN). Requires network access to `cdn.jsdelivr.net`.
- `scripts/build_deck.py` — assembles a `.pptx` from the JSON spec using `python-pptx`. Pure layout, no markdown parsing, no network access.

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| `render_mermaid.py` exits 1, "no Chrome/Chromium binary found" | No headless-capable browser installed | Fall back to a text bullet with the raw mermaid source; tell the user which diagram was skipped |
| Diagram image looks blank/mostly white | mermaid syntax error, diagram didn't render before screenshot | Check the `.mmd` source for syntax errors; increase `--width`/`--height` if content is very wide (e.g. long sequence diagrams) |
| `ModuleNotFoundError: pptx` or `PIL` | Missing Python deps | `pip3 install --user python-pptx pillow` |
| Table looks cramped / overflowing | Too many columns or long cell text for the slide width | Shorten cell text, or split into two slides |
| Deck opens but a slide is blank | JSON spec slide had none of `bullets`/`table`/`image` set | Check the spec — every content slide needs at least one |
