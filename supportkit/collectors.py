from __future__ import annotations

import platform
import shutil
import socket
from pathlib import Path

from .models import CheckResult


def system_inventory() -> CheckResult:
    return CheckResult(
        name="system_inventory",
        status="PASS",
        summary=f"{platform.system()} {platform.release()} on {platform.machine()}",
        data={
            "hostname": socket.gethostname(),
            "os": platform.system(),
            "release": platform.release(),
            "architecture": platform.machine(),
            "python": platform.python_version(),
        },
    )


def disk_health(path: str = "/", warn_percent: int = 85) -> CheckResult:
    usage = shutil.disk_usage(Path(path))
    used_percent = round((usage.used / usage.total) * 100, 1)
    # BUG: comparison is reversed. Healthy disks can be warned while full disks pass.
    status = "WARN" if used_percent < warn_percent else "PASS"
    return CheckResult(
        name="disk_health",
        status=status,
        severity="medium" if status == "WARN" else "info",
        summary=f"Disk usage is {used_percent}% (warning threshold {warn_percent}%)",
        data={"used_percent": used_percent, "warn_percent": warn_percent, "path": path},
    )


def dns_health(hostname: str = "example.com") -> CheckResult:
    # BUG: one failed lookup raises an exception and aborts the entire diagnostic run.
    addresses = sorted({item[4][0] for item in socket.getaddrinfo(hostname, 443)})
    return CheckResult(
        name="dns_health",
        status="PASS",
        summary=f"Resolved {hostname} to {len(addresses)} address(es)",
        data={"hostname": hostname, "addresses": addresses},
    )


def tcp_health(hostname: str = "example.com", port: int = 443, timeout: float = 2.0) -> CheckResult:
    try:
        with socket.create_connection((hostname, port), timeout=timeout):
            return CheckResult(
                name="tcp_health",
                status="PASS",
                summary=f"TCP connection to {hostname}:{port} succeeded",
                data={"hostname": hostname, "port": port, "timeout": timeout},
            )
    except OSError as exc:
        return CheckResult(
            name="tcp_health",
            status="WARN",
            severity="medium",
            summary=f"TCP connection to {hostname}:{port} failed: {exc}",
            data={"hostname": hostname, "port": port, "timeout": timeout},
        )


def service_health(service_name: str, observed_status: str) -> CheckResult:
    # BUG: service state is checked case-sensitively.
    healthy = observed_status == "RUNNING"
    return CheckResult(
        name=f"service:{service_name}",
        status="PASS" if healthy else "WARN",
        severity="medium" if not healthy else "info",
        summary=f"{service_name} status is {observed_status}",
        data={"service": service_name, "observed_status": observed_status},
    )
