# INC-003 — Controlled troubleshooting scenarios

**Status:** Verified by automated scenario tests  
**Scope:** DNS failure, Windows service outage, disk pressure

The purpose of these scenarios is to demonstrate troubleshooting decisions when something is actually wrong. The data is sanitized and intentionally controlled.

## 1. DNS resolution failure

### Initial symptom

A user can reach the network but a required hostname does not resolve.

### Competing hypotheses

- general network outage
- incorrect DNS assignment
- local resolver cache issue
- VPN/split-DNS issue
- upstream resolver outage

### Evidence sequence

```powershell
ipconfig /all
Resolve-DnsName support.lab.example
Test-NetConnection 1.1.1.1 -Port 443
```

The controlled collector state is:

```text
Before: WARN — DNS resolution for support.lab.example failed: resolver unavailable
After:  PASS — Resolved support.lab.example to 1 address(es)
```

### Decision

Successful IP connectivity with failed name resolution narrows the failure domain to DNS instead of treating it as a general network outage.

### Reversible change

```powershell
.\scripts\Repair-NetworkStack.ps1 -FlushDns -WhatIf
.\scripts\Repair-NetworkStack.ps1 -FlushDns
```

A cache flush is only appropriate after resolver configuration is captured. The runbook explicitly avoids hard-coding a public resolver on a managed endpoint.

### Escalation

If multiple endpoints fail against the same configured resolver, hand off with resolver IP, query, timestamp, endpoint/VPN scope, and successful IP-connectivity evidence.

---

## 2. Print Spooler service outage

### Initial symptom

Print jobs cannot be processed and the Print Spooler is stopped.

### Competing hypotheses

- service manually stopped
- driver crash
- dependent-service failure
- print-server/network issue
- repeated spooler fault after a recent change

### Evidence sequence

```powershell
Get-Service Spooler
Get-WinEvent -LogName System -MaxEvents 50
Get-WinEvent -LogName Microsoft-Windows-PrintService/Operational -MaxEvents 50
```

Controlled state:

```text
Before: WARN — Print Spooler status is Stopped
After:  PASS — Print Spooler status is Running
```

### Reversible change

The helper is preview-only unless `-Execute` is supplied:

```powershell
.\scripts\Repair-Service.ps1 -Name Spooler
.\scripts\Repair-Service.ps1 -Name Spooler -Execute -WhatIf
.\scripts\Repair-Service.ps1 -Name Spooler -Execute
```

The decision to start the service comes after checking event evidence and dependencies.

### Escalation

Repeated stops are escalated with PrintService/System events, driver version, print-server reachability, and exact restart/failure timestamps.

---

## 3. Disk pressure

### Initial symptom

The system volume is 93% utilized against an 85% warning threshold.

### Competing hypotheses

- user profile growth
- temporary-file accumulation
- application/log runaway
- update/cache growth
- legitimate business data growth

### Evidence sequence

```powershell
Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3"
Get-ChildItem $env:TEMP -File -Recurse -ErrorAction SilentlyContinue |
  Sort-Object Length -Descending |
  Select-Object -First 20 FullName,Length,LastWriteTime
```

Controlled state:

```text
Before: WARN — Disk usage is 93.0% (warning threshold 85%)
After:  PASS — Disk usage is 68.0% (warning threshold 85%)
```

### Reversible/targeted action

```powershell
.\scripts\Invoke-DiskCleanup.ps1 -Path $env:TEMP -OlderThanDays 7
.\scripts\Invoke-DiskCleanup.ps1 -Path $env:TEMP -OlderThanDays 7 -Execute -WhatIf
```

The script defaults to preview only and prints the candidate count, total size, and largest files. It only deletes when `-Execute` is explicitly provided.

### Escalation

Unexpected application or log growth is escalated to the application owner before business/application data is removed.

## Verification

```bash
PYTHONPATH=. python samples/controlled_incidents.py
python -m unittest discover -s tests -v
```

Expected scenario transitions:

```text
LAB-DNS-001: WARN -> PASS
LAB-SVC-001: WARN -> PASS
LAB-DISK-001: WARN -> PASS
```

## Limits

These are controlled lab failures and sanitized evidence. They demonstrate diagnostic reasoning, safe-change discipline, and verification logic; they are not presented as customer incidents or proof of production fleet ownership.
