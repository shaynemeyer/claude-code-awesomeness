#!/usr/bin/env python3
"""Convert a Markdown file to a styled PDF, rendering Mermaid diagrams inline.

Pipeline:
  1. pandoc: markdown -> HTML body fragment
  2. unwrap <pre class="mermaid"><code>...</code></pre> to
     <pre class="mermaid">...</pre> (mermaid.js expects raw text, not a
     nested <code> element)
  3. wrap the body in an HTML document with print-safe CSS and mermaid.js
     loaded from a CDN
  4. headless Chrome --print-to-pdf the document

Chrome's default print header/footer ("about:blank", timestamp, page
number) is suppressed by keeping the CSS @page margin at or under 8mm
and simulating real document margins with body padding instead --
`--print-to-pdf-no-header` alone does not reliably suppress it.

Usage:
  python3 build_pdf.py --md report.md --out report.pdf [--theme default]
"""
import argparse
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile


def find_chrome():
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        shutil.which("google-chrome"),
        shutil.which("chromium"),
        shutil.which("chromium-browser"),
        shutil.which("google-chrome-stable"),
    ]
    for c in candidates:
        if c and (os.path.exists(c) or shutil.which(c)):
            return c
    return None


def find_pandoc():
    return shutil.which("pandoc")


CSS = u"""
@page { margin: 8mm; size: A4; }
html, body {
  font-family: -apple-system, "Helvetica Neue", Arial, sans-serif;
  color: #222;
  line-height: 1.55;
}
body { padding: 12mm 15mm; max-width: 780px; margin: 0 auto; }
h1 { color: #1B2A4A; border-bottom: 3px solid #2E86AB; padding-bottom: 8px; }
h2 { color: #1B2A4A; margin-top: 1.6em; }
h3 { color: #2E86AB; }
code { background: #f2f6fa; padding: 2px 5px; border-radius: 3px; font-size: 0.9em; }
pre code { background: none; padding: 0; }
pre { background: #f8f9fb; border: 1px solid #e0e4ea; border-radius: 6px; padding: 12px; overflow-x: auto; font-size: 0.85em; }
pre.mermaid { background: #ffffff; border: 1px solid #e0e4ea; text-align: center; padding: 10px; }
table { border-collapse: collapse; width: 100%; margin: 1em 0; font-size: 0.92em; }
th, td { border: 1px solid #d5dbe3; padding: 6px 10px; text-align: left; }
th { background: #1B2A4A; color: white; }
tr:nth-child(even) { background: #f2f6fa; }
blockquote { border-left: 3px solid #2E86AB; margin-left: 0; padding-left: 12px; color: #555; }
img { max-width: 100%; }
"""

HTML_TEMPLATE = u"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>{css}</style>
</head>
<body>
{body}
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>mermaid.initialize({{ startOnLoad: true, theme: '{theme}' }});</script>
</body>
</html>
"""

MERMAID_BLOCK_RE = re.compile(
    r'<pre class="mermaid"><code[^>]*>(.*?)</code></pre>',
    re.S,
)


def unwrap_mermaid_blocks(body_html):
    def _unwrap(m):
        inner = m.group(1)
        return u'<pre class="mermaid">' + inner + u'</pre>'
    return MERMAID_BLOCK_RE.sub(_unwrap, body_html)


def markdown_to_body_html(md_path, pandoc_path):
    result = subprocess.run(
        [pandoc_path, md_path, "-f", "markdown", "-t", "html", "--standalone=false"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError("pandoc failed: %s" % result.stderr)
    return result.stdout


def assemble_html(body_html, theme):
    body_html = unwrap_mermaid_blocks(body_html)
    return HTML_TEMPLATE.format(css=CSS, body=body_html, theme=theme)


def html_to_pdf(html_path, pdf_path, chrome_path, wait_ms=6000):
    cmd = [
        chrome_path, "--headless", "--disable-gpu", "--no-sandbox",
        "--print-to-pdf-no-header",
        "--virtual-time-budget=%d" % wait_ms,
        "--print-to-pdf=%s" % pdf_path,
        "file://%s" % html_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 or not os.path.exists(pdf_path):
        raise RuntimeError("chrome print-to-pdf failed: %s" % result.stderr)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--md", required=True, help="path to the source markdown file")
    parser.add_argument("--out", required=True, help="output PDF path")
    parser.add_argument("--theme", default="default", help="mermaid theme: default, dark, forest, neutral")
    parser.add_argument("--keep-html", action="store_true", help="keep the intermediate HTML file (printed to stdout)")
    args = parser.parse_args()

    pandoc_path = find_pandoc()
    if not pandoc_path:
        print("ERROR: pandoc not found on PATH. Install with: brew install pandoc", file=sys.stderr)
        sys.exit(1)

    chrome_path = find_chrome()
    if not chrome_path:
        print("ERROR: no Chrome/Chromium binary found", file=sys.stderr)
        sys.exit(1)

    body_html = markdown_to_body_html(args.md, pandoc_path)
    full_html = assemble_html(body_html, args.theme)

    tmpdir = tempfile.mkdtemp(prefix="md2pdf_")
    html_path = os.path.join(tmpdir, "doc.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    try:
        html_to_pdf(html_path, args.out, chrome_path)
    except RuntimeError as e:
        print("ERROR: %s" % e, file=sys.stderr)
        sys.exit(1)
    finally:
        if args.keep_html:
            print("intermediate HTML kept at: %s" % html_path)
        else:
            shutil.rmtree(tmpdir, ignore_errors=True)

    print("wrote %s" % args.out)


if __name__ == "__main__":
    main()
