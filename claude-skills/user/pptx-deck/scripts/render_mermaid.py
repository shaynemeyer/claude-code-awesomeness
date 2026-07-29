#!/usr/bin/env python3
"""Render a single Mermaid diagram to a tightly-cropped PNG.

Uses headless Chrome + mermaid.js (via CDN) to screenshot the rendered
diagram, then autocrops whitespace with Pillow. Requires network access
to fetch mermaid.js from a CDN.
"""
import argparse
import os
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


HTML_TEMPLATE = u"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  html,body {{ margin:0; padding:0; background:#ffffff; }}
  .mermaid {{ display:inline-block; padding:24px; background:#ffffff; }}
</style>
</head>
<body>
<pre class="mermaid">{code}</pre>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
  mermaid.initialize({{ startOnLoad: true, theme: '{theme}' }});
</script>
</body></html>
"""


def render(code, out_png, theme="default", width=2000, height=3000):
    chrome = find_chrome()
    if not chrome:
        print("ERROR: no Chrome/Chromium binary found", file=sys.stderr)
        return False

    tmpdir = tempfile.mkdtemp(prefix="mmd_")
    html_path = os.path.join(tmpdir, "diagram.html")
    raw_png = os.path.join(tmpdir, "raw.png")

    html = HTML_TEMPLATE.format(code=code, theme=theme)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    cmd = [
        chrome, "--headless", "--disable-gpu", "--no-sandbox",
        "--hide-scrollbars", "--force-color-profile=srgb",
        "--virtual-time-budget=6000",
        "--window-size=%d,%d" % (width, height),
        "--screenshot=%s" % raw_png,
        "file://%s" % html_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 or not os.path.exists(raw_png):
        print("ERROR: chrome render failed: %s" % result.stderr, file=sys.stderr)
        shutil.rmtree(tmpdir, ignore_errors=True)
        return False

    try:
        from PIL import Image, ImageChops
    except ImportError as e:
        print("ERROR: missing python dependency: %s" % e, file=sys.stderr)
        shutil.rmtree(tmpdir, ignore_errors=True)
        return False

    img = Image.open(raw_png).convert("RGB")
    bg = Image.new("RGB", img.size, (255, 255, 255))
    diff = ImageChops.difference(img, bg)
    bbox = diff.getbbox()
    if bbox:
        pad = 12
        left = max(0, bbox[0] - pad)
        top = max(0, bbox[1] - pad)
        right = min(img.width, bbox[2] + pad)
        bottom = min(img.height, bbox[3] + pad)
        img = img.crop((left, top, right, bottom))

    img.save(out_png)
    shutil.rmtree(tmpdir, ignore_errors=True)
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--code-file", required=True, help="path to a file containing the mermaid source")
    parser.add_argument("--out", required=True, help="output PNG path")
    parser.add_argument("--theme", default="default")
    parser.add_argument("--width", type=int, default=2000)
    parser.add_argument("--height", type=int, default=3000)
    args = parser.parse_args()

    with open(args.code_file, "r", encoding="utf-8") as f:
        code = f.read()

    ok = render(code, args.out, theme=args.theme, width=args.width, height=args.height)
    sys.exit(0 if ok else 1)
