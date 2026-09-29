# Runbook — DNS resolution failure

## Trigger

User can reach an IP address or local gateway but hostnames fail, applications report name-resolution errors, or the `dns_health` check returns `WARN`.

## Triage order

1. Confirm scope: one endpoint, VLAN/site, VPN users, or all users.
2. Record `ipconfig /all`; verify DHCP-assigned DNS servers and suffix search list.
3. Test the configured resolver directly with `Resolve-DnsName <host> -Server <dns-server>`.
4. Compare internal and public names to separate split-DNS/VPN issues from general resolver failure.
5. Check VPN state and routing before changing adapter settings.
6. Flush local cache only after evidence is captured: `ipconfig /flushdns`.
7. If multiple users are affected, escalate with affected subnet, resolver IPs, timestamps, and failed query examples.

## Do not

- Hard-code a public DNS server on a managed corporate endpoint without authorization.
- Reset the full network stack before collecting the current configuration.
- Treat successful ping as proof that DNS is healthy.
