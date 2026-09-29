# INC-001 — Diagnostic reliability regressions

**Status:** Resolved  
**Scope:** Disk thresholding, DNS failure handling, Windows-style service status normalization

## Symptoms

While expanding the diagnostic checks, I ran into three reliability defects:

1. A disk at 90% utilization could be reported as healthy with an 85% warning threshold.
2. A DNS resolver exception could terminate the complete diagnostic run instead of producing a contained warning result.
3. Service states such as `running` were flagged because the check only accepted the exact uppercase string `RUNNING`.

## Impact

These defects reduce trust in endpoint triage output. The disk defect can hide a capacity issue; the DNS defect can prevent collection of unrelated checks; the service-state defect creates false positives.

## What I checked

Run:

```bash
python -m unittest discover -s tests -v
```

Once I isolated the behavior, I added regression coverage for it and fixed the root cause in the following changes. The commit history keeps that sequence visible.

## Root cause

- Disk check used `<` instead of `>=` when evaluating the warning threshold.
- DNS lookup was not wrapped in exception handling, so resolver failures escaped the collector boundary.
- Service status comparison used a raw, case-sensitive string.

## Resolution

- Corrected disk threshold logic and added threshold validation.
- Converted DNS resolver exceptions into structured `WARN` results so remaining checks continue.
- Normalized service state with `strip().upper()` before evaluation.
- Added port and timeout validation to harden TCP checks while touching the collector layer.

## Verification

The complete unit test suite passes after the repair.
