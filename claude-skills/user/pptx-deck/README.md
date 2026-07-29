# pptx-deck

A user-level skill that converts markdown into a real, editable PowerPoint (`.pptx`) file — title slide, content slides with bullets/tables/images, Mermaid diagrams rendered to PNG and embedded, and speaker notes populated from any talk-track text in the source.

## What it does

Claude reads the source markdown and does the slide-splitting itself — deciding where a section becomes one slide vs. several, which content becomes bullets vs. a table vs. an image — then writes a structured JSON spec describing every slide. That spec is handed to a deterministic Python script for layout, so the visual result (fonts, colors, table styling, image placement) is consistent across runs rather than left to an LLM to typeset by hand.

There is no markdown-to-slide auto-converter involved. Slide boundaries and content judgment are Claude's job; layout and rendering are the scripts' job.

## When it triggers

Automatically, whenever you ask to turn something into a PowerPoint, deck, or slides — "make this a PowerPoint," "create a deck from this doc," "turn this into slides," "export to pptx." Works from an existing markdown file, or directly from content described in conversation with no source file at all.

## Usage

```bash
turn docs/migration-plan.md into a PowerPoint
make a deck out of this: <pasted content>
export this presentation doc to pptx
```

Output defaults to the same directory as the source markdown, same base filename with a `.pptx` extension, unless you specify otherwise.

## How Mermaid diagrams are handled

Any ` ```mermaid ` code block in the source becomes its own image slide:

1. The raw Mermaid source is written to a temp `.mmd` file
2. `scripts/render_mermaid.py` renders it via headless Chrome + mermaid.js (loaded from a CDN) and screenshots the result
3. The screenshot is autocropped to remove surrounding whitespace with Pillow
4. The cropped PNG is embedded into its own slide in the deck

If no Chrome/Chromium binary is found, or a diagram fails to render, that one diagram is skipped — the rest of the deck still builds, and Claude tells you which diagram(s) didn't make it in.

## Requirements

- `python-pptx` and `Pillow`: `pip3 install --user python-pptx pillow`
- Headless-capable Chrome or Chromium, only needed if the source contains Mermaid diagrams. The skill checks common install locations (macOS app bundle, `PATH` on Linux) automatically.
- Network access to `cdn.jsdelivr.net` (to load mermaid.js), only needed for Mermaid rendering.

Nothing is installed on your behalf — if a dependency is missing, Claude tells you what to install.

## Design

Fixed, professional layout: 16:9 widescreen, navy titles (`#1B2A4A`) with a teal accent underline (`#2E86AB`), striped tables. This isn't exposed as a spec option — the JSON spec is content-only (titles, bullets, tables, images, notes). To change the visual style (brand colors, a different template), edit the color constants at the top of `scripts/build_deck.py` directly.

## Files

- `SKILL.md` — the skill itself: when to use it, how to split markdown into slides, the JSON spec schema, the build procedure, troubleshooting
- `scripts/render_mermaid.py` — renders one Mermaid diagram to a cropped PNG via headless Chrome
- `scripts/build_deck.py` — assembles a `.pptx` from a JSON slide spec via `python-pptx`; no markdown parsing, no network access

## Installation

Copy the `pptx-deck` directory into `~/.claude/skills/`:

```bash
cp -r claude-skills/user/pptx-deck ~/.claude/skills/
```
