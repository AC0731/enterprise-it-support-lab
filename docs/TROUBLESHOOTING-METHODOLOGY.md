# Troubleshooting methodology

This lab uses a repeatable support workflow rather than ad-hoc changes.

## 1. Define impact and scope

Establish who is affected, what is unavailable, when it started, and whether the fault follows the user, endpoint, network, or service.

## 2. Capture the baseline

Collect configuration and error evidence before remediation. For endpoint incidents this usually includes system identity, IP/DNS configuration, relevant service state, storage health, event logs, timestamps, and recent changes.

## 3. Separate layers

Test in an order that narrows the failure domain:

1. Local endpoint / resource pressure
2. Adapter and IP configuration
3. Gateway / routing
4. DNS resolution
5. TCP service reachability
6. Application / authentication layer

## 4. Make the smallest reversible change

Prefer a targeted cache flush, service restart, configuration correction, or credential refresh over broad resets. Use `-WhatIf` / `ShouldProcess` where practical for administrative PowerShell.

## 5. Validate and document

Repeat the original failing test, verify related functions, capture post-change evidence, and record the exact action taken.

## 6. Escalate with evidence

When the fault is outside endpoint ownership, escalate with scope, timestamps, test results, logs, recent changes, and actions already attempted so the receiving team does not restart discovery from zero.
