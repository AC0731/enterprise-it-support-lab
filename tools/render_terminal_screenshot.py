#!/usr/bin/env python3
"""Render plain terminal capture text to documentation PNGs."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import sys


def load_font(size: int):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationMono-Regular.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()


def render(source: Path, destination: Path, title: str) -> None:
    lines = source.read_text(encoding="utf-8", errors="replace").splitlines()
    font = load_font(18)
    title_font = load_font(18)
    padding = 32
    line_height = 30
    width = max(1200, min(2200, max((len(line) for line in lines), default=80) * 12 + (padding * 2)))
    content_height = max(1, len(lines)) * line_height
    height = 78 + padding + content_height + padding

    image = Image.new("RGB", (width, height), "#0d1117")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, 78), fill="#161b22")
    draw.ellipse((24, 27, 42, 45), fill="#ff5f57")
    draw.ellipse((52, 27, 70, 45), fill="#febc2e")
    draw.ellipse((80, 27, 98, 45), fill="#28c840")
    draw.text((122, 23), title, fill="#c9d1d9", font=title_font)

    y = 78 + padding
    for line in lines:
        color = "#c9d1d9"
        if "FAILED" in line or "ERROR" in line:
            color = "#ff7b72"
        elif "WARN" in line or "P2" in line:
            color = "#d29922"
        elif "PASS" in line or line.strip().endswith("OK"):
            color = "#3fb950"
        draw.text((padding, y), line[:118], fill=color, font=font)
        y += line_height

    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(destination)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit("usage: render_terminal_screenshot.py SOURCE DESTINATION TITLE")
    render(Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3])
