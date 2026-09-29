# Runbook — Disk pressure

## Threshold

Default lab warning threshold: **85% used**. Production thresholds should follow the organization's monitoring standard.

## Triage

1. Confirm the affected volume and current free space.
2. Identify growth by user profile, application cache, logs, update cache, temp data, or application content.
3. Check whether low space is causing Windows Update, profile, application, or paging failures.
4. Prefer approved cleanup mechanisms and retention policies over manual deletion.
5. Escalate unexpected log/data growth to the application owner before removing business data.

Document space before and after remediation and note exactly what was removed.
