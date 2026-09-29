from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .models import CheckResult
from .triage import calculate_risk, recommendations


def build_report(results: list[CheckResult]) -> dict:
    score, priority = calculate_risk(results)
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "priority": priority,
        "risk_score": score,
        "checks": [item.to_dict() for item in results],
        "recommended_actions": recommendations(results),
    }


def write_json(report: dict, output: str) -> None:
    Path(output).write_text(json.dumps(report, indent=2), encoding="utf-8")


def write_markdown(report: dict, output: str) -> None:
    lines = [
        "# Endpoint Health Report",
        "",
        f"- Generated: `{report['generated_at_utc']}`",
        f"- Incident priority: **{report['priority']}**",
        f"- Risk score: **{report['risk_score']}**",
        "",
        "## Checks",
        "",
        "| Check | Status | Severity | Summary |",
        "|---|---|---|---|",
    ]
    for item in report["checks"]:
        lines.append(f"| {item['name']} | {item['status']} | {item['severity']} | {item['summary']} |")
    lines += ["", "## Recommended actions", ""]
    lines += [f"- {action}" for action in report["recommended_actions"]]
    Path(output).write_text("\n".join(lines) + "\n", encoding="utf-8")
