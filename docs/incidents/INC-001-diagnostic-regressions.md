# INC-001 — Diagnostic reliability regressions

**Status:** Reproduced  
**Scope:** Disk thresholding, DNS failure handling, Windows-style service status normalization

## Symptoms

During test expansion, three reliability defects were reproduced:

1. A disk at 90% utilization could be reported as healthy with an 85% warning threshold.
2. A DNS resolver exception could terminate the complete diagnostic run instead of producing a contained warning result.
3. Service states such as `running` were flagged because the check only accepted the exact uppercase string `RUNNING`.

## Impact

These defects reduce trust in endpoint triage output. The disk defect can hide a capacity issue; the DNS defect can prevent collection of unrelated checks; the service-state defect creates false positives.

## Reproduction

Run:

```bash
python -m unittest discover -s tests -v
```

The regression suite is intentionally committed before the repair so the defect discovery is visible in repository history.
