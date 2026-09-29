# Endpoint Health Report

- Generated: `2026-09-29T10:44:15.823965+00:00`
- Incident priority: **P2**
- Risk score: **9**

## Checks

| Check | Status | Severity | Summary |
|---|---|---|---|
| system_inventory | PASS | info | Windows 11 Enterprise 23H2 on Dell Latitude 5440 |
| disk_health | PASS | info | Disk usage is 61.8% (warning threshold 85%) |
| dns_health | WARN | medium | DNS resolution for intranet.corp.example failed: temporary resolver failure |
| tcp_health | WARN | medium | TCP connection to intranet.corp.example:443 failed: connection timed out |
| service:Print Spooler | WARN | medium | Print Spooler status is Stopped |

## Recommended actions

- Validate DNS server assignment, flush resolver cache, and retest name resolution.
- Check local firewall/VPN path, gateway reachability, and upstream service status.
- Validate service startup type, dependencies, event logs, and recent change history.
