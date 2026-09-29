[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = "Medium")]
param(
    [Parameter(Mandatory = $true)]
    [string]$Name,

    [switch]$Execute
)

$ErrorActionPreference = "Stop"
$service = Get-Service -Name $Name -ErrorAction Stop

Write-Host "Service: $($service.Name)"
Write-Host "Current status: $($service.Status)"

if ($service.Status -eq "Running") {
    Write-Host "No change required."
    exit 0
}

if (-not $Execute) {
    Write-Host "Preview only. Re-run with -Execute after reviewing dependencies and event evidence."
    exit 0
}

if ($PSCmdlet.ShouldProcess($service.Name, "Start service")) {
    Start-Service -Name $service.Name -ErrorAction Stop
    $service.Refresh()
    Write-Host "Updated status: $($service.Status)"
}
