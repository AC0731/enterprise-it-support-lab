[CmdletBinding()]
param(
    [int]$Hours = 8,
    [int]$MaxEvents = 100,
    [string]$OutputPath = ".\artifacts\event-log-snapshot.csv"
)

$startTime = (Get-Date).AddHours(-1 * $Hours)
$events = Get-WinEvent -FilterHashtable @{
    LogName   = @("System", "Application")
    StartTime = $startTime
    Level     = @(1, 2, 3)
} -ErrorAction SilentlyContinue |
    Sort-Object TimeCreated -Descending |
    Select-Object -First $MaxEvents TimeCreated, LogName, LevelDisplayName, ProviderName, Id, Message

$directory = Split-Path -Parent $OutputPath
if ($directory) { New-Item -ItemType Directory -Path $directory -Force | Out-Null }
$events | Export-Csv -Path $OutputPath -NoTypeInformation -Encoding UTF8
Write-Host "Exported $($events.Count) event(s) to $OutputPath"
