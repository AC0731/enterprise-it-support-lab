# Runbook — VPN connectivity degradation

## Initial checks

- Verify the user has normal internet access before testing VPN.
- Capture client timestamp, public IP, VPN gateway, client version, and exact error.
- Check local time synchronization; certificate and SSO failures can be time-sensitive.
- Review DNS suffixes and routes after tunnel establishment.
- Test a known internal hostname and a known internal IP separately.

## Decision points

**IP works, hostname fails:** prioritize DNS/split-tunnel resolver configuration.  
**Neither works, tunnel says connected:** inspect routes, endpoint firewall, and assigned VPN address.  
**Authentication fails:** verify identity/MFA status and avoid repeated lockout attempts.  
**Many users affected:** stop endpoint-level changes and escalate as a service incident.

## Escalation package

Include client logs, timestamps with timezone, gateway/region, source network type, affected destinations, DNS results, route table summary, and whether another user/network reproduces the issue.
