# INC-003 — Troubleshooting cases

**Status:** Verified by regression tests  
**Scope:** DNS failure, Windows service outage, disk pressure

While extending the support workflow, I had to account for several failure states where a normal health check was not enough. I documented the evidence path, the competing causes I considered, the change I would make, and the verification step after the change.

## 1. DNS resolution failure

### Initial symptom

A required hostname does not resolve even though general IP connectivity is still available.

### What I considered

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

Observed states:

```text
Before: WARN — DNS resolution for support.lab.example failed: resolver unavailable
After:  PASS — Resolved support.lab.example to 1 address(es)
```

### Troubleshooting decision

Successful IP connectivity with failed name resolution narrowed the problem to DNS rather than a general network outage.

### Change and verification

```powershell
.\scripts\Repair-NetworkStack.ps1 -FlushDns -WhatIf
.\scripts\Repair-NetworkStack.ps1 -FlushDns
```

I kept the resolver configuration as evidence before clearing the cache, then repeated the lookup to confirm name resolution recovered.

### Escalation

If several endpoints fail against the same resolver, the handoff includes the resolver IP, failed query, timestamp, endpoint/VPN scope, and successful IP-connectivity evidence.

---

## 2. Print Spooler service outage

### Initial symptom

Print jobs cannot be processed and the Print Spooler is stopped.

### What I considered

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

Observed states:

```text
Before: WARN — Print Spooler status is Stopped
After:  PASS — Print Spooler status is Running
```

### Troubleshooting decision

I checked service state and event evidence before changing the service state so a restart did not hide the useful pre-change evidence.

### Change and verification

```powershell
.\scripts\Repair-Service.ps1 -Name Spooler
.\scripts\Repair-Service.ps1 -Name Spooler -Execute -WhatIf
.\scripts\Repair-Service.ps1 -Name Spooler -Execute
```

After the service change, I checked the service state again and compared it with the original symptom.

### Escalation

Repeated stops are escalated with PrintService/System events, driver version, print-server reachability, and exact restart/failure timestamps.

---

## 3. Disk pressure

### Initial symptom

The system volume reaches 93% utilization against an 85% warning threshold.

### What I considered

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

Observed states:

```text
Before: WARN — Disk usage is 93.0% (warning threshold 85%)
After:  PASS — Disk usage is 68.0% (warning threshold 85%)
```

### Troubleshooting decision

I identified the largest approved temporary/log consumers before deleting anything rather than doing a broad cleanup.

### Change and verification

```powershell
.\scripts\Invoke-DiskCleanup.ps1 -Path $env:TEMP -OlderThanDays 7
.\scripts\Invoke-DiskCleanup.ps1 -Path $env:TEMP -OlderThanDays 7 -Execute -WhatIf
```

The script lists the affected files and size first. After cleanup, I repeated the disk check to verify the original threshold problem was gone.

### Escalation

Unexpected application or log growth is escalated to the application owner before business/application data is removed.

## Verification source

The WARN → PASS transitions below are regression/case-harness results using the project collector functions. They are not the same evidence as the separate Windows Server 2025 health verification in the repository README and screenshots.

```bash
PYTHONPATH=. python samples/troubleshooting_cases.py
python -m unittest discover -s tests -v
```

Expected transitions:

```text
LAB-DNS-001: WARN -> PASS
LAB-SVC-001: WARN -> PASS
LAB-DISK-001: WARN -> PASS
```

No employer or customer data is included in these project records.
