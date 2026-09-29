#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from playwright.sync_api import sync_playwright


def capture(page, source: str, destination: str, width: int, height: int) -> None:
    uri = Path(source).resolve().as_uri()
    page.set_viewport_size({"width": width, "height": height})
    page.goto(uri, wait_until="load")
    page.screenshot(path=destination, full_page=True)


def main() -> int:
    Path("docs/screenshots").mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        capture(
            page,
            "docs/evidence/windows-triage.html",
            "docs/screenshots/windows-triage-live.png",
            1600,
            1200,
        )
        capture(
            page,
            "docs/evidence/test-suite.html",
            "docs/screenshots/test-suite-live.png",
            1600,
            900,
        )
        browser.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
