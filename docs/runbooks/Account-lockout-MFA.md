# Runbook — Account lockout / MFA

## Objective

Restore access without weakening identity controls or creating a repeat lockout.

## Checks

- Confirm the user's identity through the approved support process.
- Determine whether the account is locked, password is expired, or MFA challenge is failing.
- Ask about old credentials stored on phones, mapped drives, services, scheduled tasks, or remote sessions.
- Review available identity/sign-in logs for repeated failures and source locations/devices.
- Reset/unlock only through authorized tooling and policy.
- Require the user to update stale saved credentials after recovery.

Never request the user's password or MFA code in a ticket/chat.
