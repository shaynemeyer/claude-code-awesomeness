# drawio

A user-level skill that generates diagrams as native draw.io (`.drawio`) files, with optional export to PNG, SVG, or PDF.

## What it does

Claude writes the diagram directly as mxGraphModel XML — no Mermaid or CSV intermediate step, so the result is a real draw.io file you can open and edit. When an export format is requested, it uses the draw.io desktop CLI with `--embed-diagram`, which keeps the full diagram XML inside the exported PNG/SVG/PDF. Those exports stay editable in draw.io.

## When it triggers

Automatically, whenever you ask for a diagram: flowchart, architecture diagram, ER diagram, sequence diagram, class diagram, network diagram, mockup, or wireframe. It also triggers on any mention of draw.io / drawio / `.drawio` files, or on a request to export a diagram to PNG, SVG, or PDF.

## Usage

```bash
create a flowchart of the login process
png flowchart for login
svg: ER diagram for the orders schema
pdf architecture overview
```

Without a format, you get a `.drawio` file. With one, you get `name.drawio.png` (or `.svg` / `.pdf`) and the intermediate `.drawio` file is removed, since the export already contains the diagram.

| Format | Embedded XML | Notes                                    |
| ------ | ------------ | ---------------------------------------- |
| `png`  | Yes          | Viewable everywhere, editable in draw.io |
| `svg`  | Yes          | Scalable, editable in draw.io            |
| `pdf`  | Yes          | Printable, editable in draw.io           |
| `jpg`  | No           | Lossy, no embedded XML support           |

## Requirements

Export needs the [draw.io desktop app](https://www.drawio.com/), which ships the CLI. The skill locates it per platform (macOS app bundle, `drawio` on PATH for Linux, the Windows executable under `/mnt/c/...` on WSL2). If it isn't found, the `.drawio` file is kept and Claude tells you so — nothing is installed on your behalf.

Edge routing is optionally cleaned up with `npx @drawio/postprocess` when available; it is skipped silently otherwise.

## Files

- `SKILL.md` — the skill itself: workflow, output formats, CLI location and flags, file naming, troubleshooting
- `draw-io-xml-reference.md` — the XML reference Claude consults while generating: shape styles, edge routing, containers, swimlanes, cross-functional tables, layers, tags, metadata and placeholders, dark mode

## Installation

Copy the `drawio` directory into `~/.claude/skills/`:

```bash
cp -r claude-skills/user/drawio ~/.claude/skills/
```
