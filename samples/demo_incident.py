#!/usr/bin/env python3
"""Generate deterministic sample evidence for the portfolio README."""
from pathlib import Path

from supportkit.models import CheckResult
from supportkit.report import build_report, write_json, write_markdown


results = [
    CheckResult(
        "system_inventory",
        "PASS",
        "Windows 11 Enterprise 23H2 on Dell Latitude 5440",
        "info",
        {"hostname": "WKSTN-042", "os": "Windows 11 Enterprise", "asset_tag": "LAB-042"},
    ),
    CheckResult(
        "disk_health",
        "PASS",
        "Disk usage is 61.8% (warning threshold 85%)",
        "info",
        {"used_percent": 61.8, "warn_percent": 85, "path": "C:\\"},
    ),
    CheckResult(
        "dns_health",
        "WARN",
        "DNS resolution for intranet.corp.example failed: temporary resolver failure",
        "medium",
        {"hostname": "intranet.corp.example", "addresses": []},
    ),
    CheckResult(
        "tcp_health",
        "WARN",
        "TCP connection to intranet.corp.example:443 failed: connection timed out",
        "medium",
        {"hostname": "intranet.corp.example", "port": 443, "timeout": 2.0},
    ),
    CheckResult(
        "service:Print Spooler",
        "WARN",
        "Print Spooler status is Stopped",
        "medium",
        {"service": "Print Spooler", "observed_status": "Stopped"},
    ),
]

report = build_report(results)
out = Path("samples")
write_json(report, str(out / "incident-demo.json"))
write_markdown(report, str(out / "incident-demo.md"))

print("Enterprise IT Support Lab — Incident Triage")
print("=" * 50)
for item in results:
    print(f"[{item.status:4}] {item.name:<24} {item.summary}")
print("-" * 50)
print(f"Priority: {report['priority']} | Risk score: {report['risk_score']}")
print("Recommended actions:")
for index, action in enumerate(report["recommended_actions"], start=1):
    print(f"  {index}. {action}")
