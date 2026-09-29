[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = "High")]
param(
    [string]$Path = $env:TEMP,
    [int]$OlderThanDays = 7,
    [switch]$Execute
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $Path)) {
    throw "Cleanup path does not exist: $Path"
}

$cutoff = (Get-Date).AddDays(-1 * $OlderThanDays)
$candidates = Get-ChildItem -LiteralPath $Path -File -Recurse -ErrorAction SilentlyContinue |
    Where-Object { $_.LastWriteTime -lt $cutoff }

$totalBytes = ($candidates | Measure-Object -Property Length -Sum).Sum
if (-not $totalBytes) { $totalBytes = 0 }

Write-Host "Cleanup scope: $Path"
Write-Host "Files older than $OlderThanDays day(s): $($candidates.Count)"
Write-Host ("Candidate size: {0:N2} MB" -f ($totalBytes / 1MB))

$candidates |
    Sort-Object Length -Descending |
    Select-Object -First 20 FullName, Length, LastWriteTime |
    Format-Table -AutoSize

if (-not $Execute) {
    Write-Host "Preview only. No files were removed. Re-run with -Execute after reviewing the candidate list."
    exit 0
}

foreach ($file in $candidates) {
    if ($PSCmdlet.ShouldProcess($file.FullName, "Remove aged temporary file")) {
        Remove-Item -LiteralPath $file.FullName -Force -ErrorAction Stop
    }
}
