#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from supportkit.scenarios import all_scenarios


def render_markdown(scenarios: list[dict]) -> str:
    lines = [
        "# Controlled Incident Evidence",
        "",
        "> Sanitized lab scenarios. These are controlled failure injections, not customer or employer incidents.",
        "",
    ]

    for scenario in scenarios:
        before = scenario["before"]
        after = scenario["after"]
        lines += [
            f"## {scenario['id']}",
            "",
            f"**Symptom:** {scenario['symptom']}",
            "",
            "| Stage | Status | Summary |",
            "|---|---|---|",
            f"| Before | {before['status']} | {before['summary']} |",
            f"| After | {after['status']} | {after['summary']} |",
            "",
            f"**Decision:** {scenario['decision']}",
            "",
            f"**Controlled remediation:** {scenario['remediation']}",
            "",
            f"**Escalation if unresolved:** {scenario['escalation']}",
            "",
        ]

    return "\n".join(lines) + "\n"


def main() -> int:
    scenarios = all_scenarios()
    out = Path("docs/evidence/incidents")
    out.mkdir(parents=True, exist_ok=True)

    (out / "controlled-incidents.json").write_text(
        json.dumps(scenarios, indent=2),
        encoding="utf-8",
    )
    (out / "controlled-incidents.md").write_text(
        render_markdown(scenarios),
        encoding="utf-8",
    )

    for scenario in scenarios:
        print(
            f"{scenario['id']}: "
            f"{scenario['before']['status']} -> {scenario['after']['status']}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
