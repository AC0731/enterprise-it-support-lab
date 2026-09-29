from __future__ import annotations

from collections import namedtuple
from unittest.mock import patch

from supportkit.collectors import disk_health, dns_health, service_health

Usage = namedtuple("Usage", "total used free")


def dns_failure_scenario() -> dict:
    with patch(
        "supportkit.collectors.socket.getaddrinfo",
        side_effect=OSError("resolver unavailable"),
    ):
        before = dns_health("support.lab.example")

    with patch(
        "supportkit.collectors.socket.getaddrinfo",
        return_value=[
            (2, 1, 6, "", ("93.184.216.34", 443)),
        ],
    ):
        after = dns_health("support.lab.example")

    return {
        "id": "LAB-DNS-001",
        "symptom": "Hostname lookup fails while general network reachability remains available.",
        "before": before.to_dict(),
        "after": after.to_dict(),
        "decision": "Treat as a DNS failure domain rather than a general connectivity outage.",
        "remediation": "Capture resolver configuration first; flush only the local resolver cache when cache corruption is plausible.",
        "escalation": "If multiple endpoints reproduce the same resolver failure, escalate with resolver IP, query name, timestamps, and affected subnet/VPN scope.",
    }


def service_outage_scenario() -> dict:
    before = service_health("Print Spooler", "Stopped")
    after = service_health("Print Spooler", "Running")

    return {
        "id": "LAB-SVC-001",
        "symptom": "Print queue is unavailable and the Print Spooler service is stopped.",
        "before": before.to_dict(),
        "after": after.to_dict(),
        "decision": "Confirm service state and event evidence before changing service state.",
        "remediation": "Preview the service start, then start only the affected service if dependencies and recent change history do not indicate a broader fault.",
        "escalation": "Escalate repeated stops with PrintService/System events, driver version, print-server reachability, and the restart timestamp.",
    }


def disk_pressure_scenario() -> dict:
    with patch(
        "supportkit.collectors.shutil.disk_usage",
        return_value=Usage(total=100, used=93, free=7),
    ):
        before = disk_health("C:\\", warn_percent=85)

    with patch(
        "supportkit.collectors.shutil.disk_usage",
        return_value=Usage(total=100, used=68, free=32),
    ):
        after = disk_health("C:\\", warn_percent=85)

    return {
        "id": "LAB-DISK-001",
        "symptom": "System volume exceeds the 85% warning threshold.",
        "before": before.to_dict(),
        "after": after.to_dict(),
        "decision": "Identify approved temporary/log growth before deleting data.",
        "remediation": "Preview cleanup of aged temporary files, then remove only the approved scope and recheck the original volume.",
        "escalation": "Escalate unexpected application/log growth before deleting business or application data.",
    }


def all_scenarios() -> list[dict]:
    return [
        dns_failure_scenario(),
        service_outage_scenario(),
        disk_pressure_scenario(),
    ]
