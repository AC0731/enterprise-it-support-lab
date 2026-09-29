#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from supportkit.collectors import disk_health, dns_health, service_health, system_inventory, tcp_health
from supportkit.report import build_report, write_json, write_markdown


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Enterprise endpoint diagnostic and incident triage toolkit")
    parser.add_argument("--host", default="example.com", help="Hostname used for DNS/TCP validation")
    parser.add_argument("--port", type=int, default=443, help="TCP port used for connectivity validation")
    parser.add_argument("--disk-path", default="/", help="Filesystem path to inspect")
    parser.add_argument("--disk-warn", type=int, default=85, help="Disk usage warning threshold")
    parser.add_argument("--service", default="Print Spooler", help="Service label for demonstration")
    parser.add_argument("--service-status", default="RUNNING", help="Observed service state")
    parser.add_argument("--out", default="artifacts", help="Output directory")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    results = [
        system_inventory(),
        disk_health(args.disk_path, args.disk_warn),
        dns_health(args.host),
        tcp_health(args.host, args.port),
        service_health(args.service, args.service_status),
    ]
    report = build_report(results)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    write_json(report, str(out / "endpoint-health.json"))
    write_markdown(report, str(out / "endpoint-health.md"))

    print("IT Support Diagnostic Summary")
    print("=" * 30)
    for item in results:
        print(f"[{item.status:4}] {item.name:<24} {item.summary}")
    print(f"\nPriority: {report['priority']} | Risk score: {report['risk_score']}")
    print(f"Reports: {out / 'endpoint-health.json'}, {out / 'endpoint-health.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
