#!/usr/bin/env python3
from __future__ import annotations

import html
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 4:
        raise SystemExit("usage: build_evidence_page.py INPUT OUTPUT TITLE")

    source = Path(sys.argv[1])
    destination = Path(sys.argv[2])
    title = sys.argv[3]
    content = source.read_text(encoding="utf-8", errors="replace")

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{html.escape(title)}</title>
<style>
  html,body{margin:0;background:#0d1117;color:#c9d1d9;font-family:Consolas,'Courier New',monospace}
  .bar{height:70px;background:#161b22;display:flex;align-items:center;padding:0 28px;border-bottom:1px solid #30363d}
  .dots{display:flex;gap:10px;margin-right:22px}
  .dot{width:15px;height:15px;border-radius:50%}
  .red{background:#ff5f57} .yellow{background:#febc2e} .green{background:#28c840}
  .title{font-size:20px;font-weight:600}
  pre{white-space:pre-wrap;word-break:break-word;margin:0;padding:32px;font-size:18px;line-height:1.55}
</style>
</head>
<body>
  <div class="bar"><div class="dots"><span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span></div><div class="title">{html.escape(title)}</div></div>
  <pre>{html.escape(content)}</pre>
</body>
</html>"""
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(page, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
