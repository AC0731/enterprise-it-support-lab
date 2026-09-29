# Runbook — Print Spooler / queue issue

1. Confirm whether the issue affects one document, one printer, or all printers.
2. Capture queue state and printer mapping before clearing anything.
3. Check `Spooler` service state and recent PrintService/System events.
4. Remove a single stuck job first; avoid deleting the whole queue unless necessary.
5. Restart the spooler only when active jobs and user impact are understood.
6. For repeated failures, validate driver version, print server reachability, and recent driver/policy changes.

Use `Get-Service Spooler` and the diagnostic script before remediation so the incident record has pre-change evidence.
