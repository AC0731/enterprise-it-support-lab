# Troubleshooting Case Evidence

## LAB-DNS-001

**Symptom:** Hostname lookup fails while general network reachability remains available.

| Stage | Status | Summary |
|---|---|---|
| Before | WARN | DNS resolution for support.lab.example failed: resolver unavailable |
| After | PASS | Resolved support.lab.example to 1 address(es) |

**Decision:** Treat the problem as a DNS failure domain rather than a general connectivity outage.

**Remediation:** Capture resolver configuration first; flush only the local resolver cache when cache corruption is plausible.

**Escalation if unresolved:** If multiple endpoints show the same resolver failure, escalate with resolver IP, query name, timestamps, and affected subnet/VPN scope.

## LAB-SVC-001

**Symptom:** Print queue is unavailable and the Print Spooler service is stopped.

| Stage | Status | Summary |
|---|---|---|
| Before | WARN | Print Spooler status is Stopped |
| After | PASS | Print Spooler status is Running |

**Decision:** Confirm service state and event evidence before changing service state.

**Remediation:** Preview the service start, then start only the affected service if dependencies and recent change history do not indicate a broader fault.

**Escalation if unresolved:** Escalate repeated stops with PrintService/System events, driver version, print-server reachability, and the restart timestamp.

## LAB-DISK-001

**Symptom:** System volume exceeds the 85% warning threshold.

| Stage | Status | Summary |
|---|---|---|
| Before | WARN | Disk usage is 93.0% (warning threshold 85%) |
| After | PASS | Disk usage is 68.0% (warning threshold 85%) |

**Decision:** Identify approved temporary/log growth before deleting data.

**Remediation:** Preview cleanup of aged temporary files, then remove only the approved scope and recheck the original volume.

**Escalation if unresolved:** Escalate unexpected application/log growth before deleting business or application data.
