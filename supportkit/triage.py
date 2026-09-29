from __future__ import annotations

from .models import CheckResult

SEVERITY_WEIGHT = {"info": 0, "low": 1, "medium": 3, "high": 6, "critical": 10}


def calculate_risk(results: list[CheckResult]) -> tuple[int, str]:
    score = sum(SEVERITY_WEIGHT.get(item.severity, 0) for item in results if item.status != "PASS")
    if score >= 10:
        return score, "P1"
    if score >= 6:
        return score, "P2"
    if score >= 3:
        return score, "P3"
    return score, "P4"


def recommendations(results: list[CheckResult]) -> list[str]:
    actions: list[str] = []
    names = {item.name for item in results if item.status != "PASS"}
    if "dns_health" in names:
        actions.append("Validate DNS server assignment, flush resolver cache, and retest name resolution.")
    if "tcp_health" in names:
        actions.append("Check local firewall/VPN path, gateway reachability, and upstream service status.")
    if "disk_health" in names:
        actions.append("Review disk consumption, temporary files, profile growth, and endpoint cleanup policy.")
    if any(name.startswith("service:") for name in names):
        actions.append("Validate service startup type, dependencies, event logs, and recent change history.")
    return actions or ["No remediation required. Record baseline and close the health check."]
