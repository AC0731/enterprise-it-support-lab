[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = "High")]
param(
    [switch]$FlushDns,
    [switch]$RenewDhcp,
    [switch]$ResetWinsock
)

$ErrorActionPreference = "Stop"

if (-not ($FlushDns -or $RenewDhcp -or $ResetWinsock)) {
    Write-Host "No remediation selected. Use -FlushDns, -RenewDhcp, or -ResetWinsock."
    exit 0
}

if ($FlushDns -and $PSCmdlet.ShouldProcess($env:COMPUTERNAME, "Flush DNS resolver cache")) {
    ipconfig /flushdns
}

if ($RenewDhcp -and $PSCmdlet.ShouldProcess($env:COMPUTERNAME, "Release and renew DHCP lease")) {
    ipconfig /release
    ipconfig /renew
}

if ($ResetWinsock -and $PSCmdlet.ShouldProcess($env:COMPUTERNAME, "Reset Winsock catalog; reboot may be required")) {
    netsh winsock reset
}
